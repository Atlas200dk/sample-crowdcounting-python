# encoding=utf-8
import cv2
import crowd_counting
from presenter_types import *
import time
import sys
import re
import client
import threading
from ChannelManager import ChannelManager
import ConfigParser

def show_message(msg):
    print("%s", msg)

if __name__ == "__main__":

    lenofUrl = len(sys.argv)
    if lenofUrl <= 1:
        show_message("[ERROR] Please input mp4/Rtsp URL")
        exit()
    elif lenofUrl >= 3:
        show_message("[ERROR] param input Error")
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
    conf = ConfigParser.ConfigParser()
    a = conf.read("presenter.ini")
    presenter_ip = conf.get("presenter", "presenter_ip")
    presenter_port = int(conf.get("presenter", "presenter_port"))
    crowd_counting_app = crowd_counting.CrowdCountingInference()
    crowd_counting_app.clientsocket = client.PresenterSocketClient((presenter_ip, presenter_port), 5, None)
    thread_app = threading.Thread(target=crowd_counting_app.clientsocket.start_connect)
    thread_app.setDaemon(True)
    thread_app.start()

    time.sleep(0.1)

    if crowd_counting_app.graph is None:
        print("creat graph fail")
        exit(1)

    channel_manager = ChannelManager()
    if crowd_counting_app.clientsocket is None:
        print('detection_app.clientsocket is None')
        exit()

    data = channel_manager.OpenChannelAndReturnSendData()

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






