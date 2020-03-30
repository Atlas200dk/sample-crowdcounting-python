English|[中文](Readme_cn.md)

# Dense Crowd Counting \(Python\)<a name="EN-US_TOPIC_0232652767"></a>

Developers can deploy this application on the Atlas 200 DK or the AI acceleration cloud server to decode local MP4 files or RTSP video streams, predict the number of people in the crowd images, and send the result to the Presenter Server for storage and display.

The current application adapts to  [DDK&RunTime](https://ascend.huawei.com/resources)  of 1.3.0.0 as well as 1.32.0.0 and later versions.

## Prerequisites<a name="en-us_topic_0228752403_en-us_topic_0219905762_section137245294533"></a>

Before deploying this sample, ensure that:

-   Mind Studio  has been installed.

-   The Atlas 200 DK developer board has been connected to  Mind Studio, the SD card has been created, and the build environment has been configured.
-   The developer board is connected to the Internet over the USB port by default. The IP address of the developer board is  **192.168.1.2**.

## Sample Deployment<a name="en-us_topic_0228752403_section412811285117"></a>

You can use either of the following methods:

1.  Quick deployment: visit  [https://github.com/Atlas200dk/faster-deploy](https://github.com/Atlas200dk/faster-deploy).

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   The quick deployment script can be used to deploy multiple samples rapidly. Select  **sample-crowdcounting-python**.  
    >-   The quick deployment script automatically completes code download, model conversion, and environment variable configuration. To learn about the detailed deployment process, go to  [2. Common deployment](#en-us_topic_0228752403_li3208251440).  

2.  <a name="en-us_topic_0228752403_li3208251440"></a>Common deployment: visit  [https://github.com/Atlas200dk/sample-README/tree/master/sample-crowdcounting-python](https://github.com/Atlas200dk/sample-READEME/tree/master/sample-crowdcounting-python).

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   In this deployment mode, you need to manually download code, convert models, and configure environment variables.  


## Environment Settings<a name="en-us_topic_0228752403_section681934411710"></a>

Note: If the HiAI library, OpenCV library, and related dependencies have been installed on the developer board, skip this step.

1.  Configure the network connection of the developer board.

    Configure the network connection of the Atlas DK developer board by referring to  [https://github.com/Atlas200dk/sample-README/tree/master/DK\_NetworkConnect](https://github.com/Atlas200dk/sample-README/tree/master/DK_NetworkConnect).

2.  Install the environment dependencies.

    Configure the environment dependency by referring to  [https://github.com/Atlas200dk/sample-README/tree/master/DK\_Environment](https://github.com/Atlas200dk/sample-README/tree/master/DK_Environment).


## Deployment<a name="en-us_topic_0228752403_en-us_topic_0219905762_section1872516528910"></a>

1.  Go to the root directory where the crowdcounting-python application code is located as the  Mind Studio  installation user, for example,  **$HOME/sample-crowdcounting-python**.
2.  <a name="en-us_topic_0228752403_en-us_topic_0228757087_li9634105881418"></a>Run the deployment script to prepare the project environment, including configuring Presenter Server. Presenter Server is used to receive the data sent by the application and display the result through the browser.

    **bash deploy.sh** _host\_ip_

    -   _host\_ip_: indicates the IP address of the Atlas 200 DK developer board.

    Command example:

    **bash deploy.sh 192.168.1.2**

    When the message  **Please choose one to show the presenter in browser\(default: 127.0.0.1\):**  is displayed, enter the IP address used for accessing the Presenter Server service in the browser. Generally, the IP address is that configured for the virtual NIC.

    Select the IP address used by the browser to access the Presenter Server service in  **Current environment valid ip list**.

3.  Start Presenter Server.

    Run the following command to start the Presenter Server program of the crowd counting application in the background:

    **bash start\_presenterserver.sh**

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   Running this script will kill other Presenter Server processes on the server. If no process is running on the background, the message "presenter server not in process" is displayed. If a process is running in the background, the message "presenter server stop success" is displayed.  
    >-   After the application is stopped, you can run the  **bash stop\_presenterserver.sh**  command to stop Presenter Server.  

    If the information shown in  [Figure 1](#en-us_topic_0228752403_en-us_topic_0228757087_fig69531305324)  is displayed, the Presenter Server service has been started successfully.

    **Figure  1**  Starting the Presenter Server process<a name="en-us_topic_0228752403_en-us_topic_0228757087_fig69531305324"></a>  
    ![](figures/starting-the-presenter-server-process.png "starting-the-presenter-server-process")

    Use the URL shown in the preceding figure to log in to Presenter Server. The IP address is that typed in  [Step 2](#en-us_topic_0228752403_en-us_topic_0228757087_li9634105881418)  and the default port number is  **7007**. The following figure indicates that Presenter Server has been started successfully.

    **Figure  2**  Home page<a name="en-us_topic_0228752403_en-us_topic_0228757087_fig64391558352"></a>  
    ![](figures/home-page.png "home-page")

    The following figure shows the IP address used by Presenter Server and  Mind Studio  to communicate with the Atlas 200 DK.

    **Figure  3**  IP address example<a name="en-us_topic_0228752403_en-us_topic_0228757087_fig1881532172010"></a>  
    ![](figures/ip-address-example.png "ip-address-example")

    In the preceding figure:

    -   The IP address of the Atlas 200 DK developer board is  **192.168.1.2**  \(connected in USB mode\).
    -   The IP address used by Presenter Server to communicate with the Atlas 200 DK is in the same network segment as the IP address of the Atlas 200 DK on the UI Host server, for example,  **192.168.1.223**.
    -   The following describes how to access the IP address \(such as  **10.10.0.1**\) of Presenter Server using a browser. Because Presenter Server and  Mind Studio  are deployed on the same server, you can access  Mind Studio  through the browser using the same IP address.

4.  Parse local videos and RTSP video streams using the crowd counting \(Python\) application.
    -   To parse a local video, upload the video file to the host.

        For example, upload the video file  **crowd.mp4**  to the  **/home/HwHiAiUser/sample**  directory on the host.

        >![](public_sys-resources/icon-note.gif) **NOTE:**   
        >H.264 and H.265 MP4 files are supported. If an MP4 file needs to be edited, you are advised to use FFmpeg. If a video file is edited by other tools, FFmpeg may fail to parse the file.  

    -   If only RTSP video streams need to be parsed, skip this step.


## Run<a name="en-us_topic_0228752403_en-us_topic_0219905762_section6245151616426"></a>

1.  Log in to the host side as the  **HwHiAiUser**  user in SSH mode on Ubuntu Server where  Mind Studio  is located.

    **ssh HwHiAiUser@192.168.1.2**

2.  Go to the directory where the application code is stored as the  **HwHiAiUser**  user.

    **cd \~/HIAI\_PROJECTS/sample-crowdcounting-python**

3.  Run the application.

    **python main.py** _channel_

    -   _channel_: input video file name or RTSP stream address

    The following is a command example for running video files:

    **python main.py /home/HwHiAiUser/sample/crowd.mp4**

    The following is a command example for running RTSP video streams:

    **python main.py rtsp://192.168.2.37:554/cam/realmonitor?channel=1&subtype=0**

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >You can press  **Ctrl**+**C**  to stop the application.  

4.  Use the URL displayed upon the start of the Presenter Server service to log in to Presenter Server.

    Wait for Presenter Agent to transmit data to the server. Click  **Refresh**. When there is data, the icon in the  **Status**  column for the corresponding channel changes to green, as shown in  [Figure 4](#en-us_topic_0228752403_en-us_topic_0228757087_fig113691556202312).

    **Figure  4**  Presenter Server page<a name="en-us_topic_0228752403_en-us_topic_0228757087_fig113691556202312"></a>  
    ![](figures/presenter-server-page.png "presenter-server-page")

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   The Presenter Server supports a maximum of 10 channels at the same time \(each  _presenter\_view\_app\_name_  parameter corresponds to a channel\).  
    >-   Due to hardware limitations, each channel supports a maximum frame rate of 20 fps. A lower frame rate is automatically used when the network bandwidth is low.  

5.  Click a link in the  **View Name**  column, for example,  **video**  in the preceding figure, and view the result.

