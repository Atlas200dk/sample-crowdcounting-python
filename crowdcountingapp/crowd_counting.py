# encoding=utf-8
from  ConstManager import *
import ModelManager
import hiai
from hiai.nn_tensor_lib import DataType
import numpy as np
import ChannelManager
from presenter_types import *
import cv2
import time
import sys

class CrowdCountingInference(object):
    def __init__(self):
        # 实例化模型管理类
        self.model = ModelManager.ModelManager()
        self.width = 1024
        self.height = 768
        self.clientsocket = None
        self.channel_manager = ChannelManager.ChannelManager()
        self.graph = None
        self._getgraph()

    def dispose(self):
        hiai.hiai._global_default_graph_stack.get_default_graph().destroy()

    def __del__(self):
        self.dispose()

    def _getgraph(self):
        # 描述推理模型
        DescriptionInferenceModel = hiai.AIModelDescription('crowd_counting', crowd_counting_model_path)
        # 初始化Graph
        self.graph = self.model.CreateGraph(DescriptionInferenceModel)
        if self.graph is None:
            print ("Init Graph failed")

    '''
    1.定义输入Tensor的格式
    2.调用推理接口
    '''
    def Inference(self,input_image):
        inputImageTensor = hiai.NNTensor(input_image, self.height, self.width, 3, 'testImage', DataType.UINT8_T,
                                        self.height * self.width * 3)
        nntensorList = hiai.NNTensorList(inputImageTensor)
        resultList = self.model.Inference(self.graph, nntensorList)
        if not resultList:
            print("Inference fail")
            return None
        #返回推理结果
        return resultList

    def GetDetectionInfo(self, resultList):
        if not resultList:
            return None
        detection_result = []
        sum = 0.0
        sum = np.sum(resultList)
        point_lt_x = None
        point_lt_y = None
        point_rb_x = None
        point_rb_y = None
        detection_result.append([point_lt_x, point_lt_y, point_rb_x, point_rb_y, "number", sum])
        return detection_result

    def GetImageFrameData(self, deteInfo, input_image):
        dr = DetectionResult()
        image_frame = ImageFrame()
        image_frame.format = 0
        image_frame.width = input_image.shape[1]
        image_frame.height = input_image.shape[0]
        image_frame.data = cv2.imencode(".jpg", input_image)[1].tobytes()
        image_frame.size = 0
        sum = deteInfo[0][5]
        sum = int(sum)
        dr.result_text = "Predict_Num : " + str(sum)
        dr.lt.x = 2
        dr.lt.y = 2
        dr.rb.x = 3
        dr.rb.y = 3
        image_frame.detection_results.append(dr)
        resultData = self.channel_manager.PackRequestData(image_frame)
        return resultData

def dowork(src_image, crowd_counting_app):
    input_image = cv2.resize(src_image, (crowd_counting_app.width, crowd_counting_app.height))
    resultList = crowd_counting_app.Inference(input_image)
    if resultList == None:
        exit(1)
    resultinfo = crowd_counting_app.GetDetectionInfo(resultList)
    all_data = crowd_counting_app.GetImageFrameData(resultinfo, input_image)
    if all_data:
        crowd_counting_app.clientsocket.send_data(all_data)

def sqEngine(rtsp_queue,crowd_counting_app):
    while True:
        frame = rtsp_queue.get()
        if frame is None:
            time.sleep(0.1)
            continue
        dowork(frame,crowd_counting_app)
