# encoding=utf-8
from  ConstManager import *
import ModelManager
import hiai
from hiai.nn_tensor_lib import DataType
import os
import threading
import numpy as np
import ChannelManager
from presenter_types import *
import cv2
import time
import re
import client
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
        hiai.hiai._global_default_graph_stack.get_default_graph().destroy()

    def _getgraph(self):
        # 描述推理模型
        inferenceModel = hiai.AIModelDescription('crowd_counting', crowd_counting_model_path)
        # 初始化Graph
        self.graph = self.model.CreateGraph(inferenceModel)
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
            sys.exit(1)
        sum = 0.0
        for i in range(len(resultList[0][0])):
            for j in range(len(resultList[0][0][0])):
                sum = sum + resultList[0][0][i][j][0]
        print('predict num = ', sum)

        dr = DetectionResult()
        image_frame = ImageFrame()
        image_frame.format = 0
        image_frame.width = input_image.shape[1]
        image_frame.height = input_image.shape[0]
        image_frame.data = cv2.imencode(".jpg", input_image)[1].tobytes()
        image_frame.size = 0

        dr.result_text = "Predict_Num : " + str(sum)
	dr.lt.x = 0
	dr.lt.y = 0
	dr.rb.x = 1
	dr.rb.y = 1
        image_frame.detection_results.append(dr)
        resultData = self.channel_manager.PackRequestData(image_frame)
        #返回推理结果
        return resultData
def mergeUV(u, v):
    if u.shape == v.shape:
        uv = np.zeros(shape=(u.shape[0], u.shape[1]*2))
        for i in range(0, u.shape[0]):
            for j in range(0, u.shape[1]):
                uv[i, 2*j] = u[i, j]
                uv[i, 2*j+1] = v[i, j]
        return uv
    else:
        print("size of Channel U is different with Channel V")


def rgb2nv12(image):
    if image.ndim == 3:
        b = image[:, :, 0]
        g = image[:, :, 1]
        r = image[:, :, 2]
        y = (0.299*r+0.587*g+0.114*b)
        u = (-0.169*r-0.331*g+0.5*b+128)[::2, ::2]
        v = (0.5*r-0.419*g-0.081*b+128)[::2, ::2]
        uv = mergeUV(u, v)
        yuv = np.vstack((y, uv))
        return yuv.astype(np.uint8)
    else:
        print("image is not BGR format")

def dowork(src_image, crowd_counting_app):
    input_image = cv2.resize(src_image, (crowd_counting_app.width, crowd_counting_app.height))
    yuv = rgb2nv12(input_image)
    resultList = crowd_counting_app.Inference(yuv)
    if resultList:
        crowd_counting_app.clientsocket.send_data(resultList)

def sqEngine(rtsp_queue,crowd_counting_app):
    while True:
        frame = rtsp_queue.get()
        if frame is None:
            time.sleep(0.1)
            continue
        dowork(frame,crowd_counting_app)
