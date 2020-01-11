# encoding=utf-8
import hiai

#pass 一个留白占位符
class ModelManager(object):
    def __init__(self):
        pass

    '''
    初始化成功返回Graph实例,初始化失败返回None
    '''
    def CreateGraph(self, model):
        # 获取Graph实例
        myGraph = hiai.hiai._global_default_graph_stack.get_default_graph()
        if myGraph is None:
            print ('get defaule graph failed')
            return None
        # 初始化Engine,配置推理算子(加载模型)
        # API固定调用流程
        nntensorList = hiai.NNTensorList()
        if (None == hiai.inference(nntensorList, model, None)):
            print ('Init Engine failed !!!!')
            return None
        else:
            print ('Init Engine ok!')

        # 创建推理接口
        if (hiai.HiaiPythonStatust.HIAI_PYTHON_OK == myGraph.create_graph()):
            print ('create graph ok !!!!')
            return myGraph
        else:
            print ('create graph failed!')
            return None

    '''
    传参失败或是推理失败,皆返回None
    '''

    def Inference(self, graphHandle, inputTensorList):
        if not isinstance(graphHandle, hiai.Graph):
            print ("graphHandle is not Graph object")
            return None
        # 模型输入tensorlist
        resultList = graphHandle.proc(inputTensorList)
        if resultList is None:
            print ('Inference error!')
        return resultList
