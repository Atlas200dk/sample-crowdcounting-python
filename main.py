# encoding=utf-8
import cv2
import numpy as np
import crowd_counting
from presenter_types import *
import time
import os
import sys
import re
import client
import threading
import ChannelManager

#判断输入是否正确（通过rtsp://和.MP4后缀判断）
lenofUrl = len(sys.argv)
if lenofUrl <= 1:
    print("[ERROR] Please input mp4/Rtsp URL")
    exit()
elif lenofUrl >= 3:
    print("[ERROR] param input Error")
    exit()
URL = sys.argv[1]
URL1 = re.match('rtsp://', URL)
URL2 = re.search('.mp4', URL)
if URL1 is None:
    if URL2 is None:
        print("[ERROR] should input correct URL")
        exit()
    else:
        mp4_url = True
else:
    mp4_url = False

crowd_counting_app = crowd_counting.CrowdCountingInference()
crowd_counting_app.clientsocket = client.PresenterSocketClient(("192.168.1.122", 7006), 5, None)
thread_1 = threading.Thread(target=crowd_counting_app.clientsocket.start_connect)
thread_1.setDaemon(True)
thread_1.start()

time.sleep(0.1)

if crowd_counting_app.graph is None:
    print("creat graph fail")
    sys.exit(1)

channel_manager = ChannelManager.ChannelManager()
data = channel_manager.OpenChannel()
if crowd_counting_app.clientsocket is None:
    print('detection_app.clientsocket is None')
    exit()

crowd_counting_app.clientsocket.send_data(data)


cap = cv2.VideoCapture(URL)
ret, frame = cap.read()

if mp4_url:
    try:
        while ret:
            crowd_counting.dowork(frame, crowd_counting_app)
            ret, frame = cap.read()
    except Exception as e:
        print("ERROR",e)
    finally:
        crowd_counting_app.dispose()
else:
    rtsp_queue = client.Queue()
    sub_thread = threading.Thread(target=crowd_counting.sqEngine,args=(rtsp_queue,crowd_counting_app))
    sub_thread.setDaemon(True)
    sub_thread.start()
    try:
        while ret:
            rtsp_queue.put(frame)
            ret, frame = cap.read()
    except Exception as e:
        print("ERROR",e)
    finally:
        cv2.destroyAllWindows()
        cap.release()
        crowd_counting_app.dispose()





