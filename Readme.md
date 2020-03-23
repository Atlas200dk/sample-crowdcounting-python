中文|[English](Readme_EN.md)

# 密集人群人数统计（Python）<a name="ZH-CN_TOPIC_0228752403"></a>

开发者将本应用部署至Atlas 200 DK或者AI加速云服务器上实现对本地mp4文件或者RTSP视频流进行解码，对视频帧中的人群图像进行人头数量的预测，并将预测的结果信息发送至Presenter Server端进行展示。

当前分支中的应用适配**1.3.0.0**与**1.32.0.0及以上**版本的[DDK&RunTime](https://ascend.huawei.com/resources)。

## 前提条件<a name="zh-cn_topic_0219905762_section137245294533"></a>

部署此Sample前，需要准备好以下环境：

-   已完成Mind Studio的安装。

-   已完成Atlas 200 DK开发者板与Mind Studio的连接，SD卡的制作、编译环境的配置等。
-   由于需要配置开发板联网，默认设置为USB连接，开发板地址为192.168.1.2

## 样例部署<a name="section412811285117"></a>

可以选择如下快速部署或者常规方法部署，二选一即可：

1.  快速部署，请参考：  [https://gitee.com/Atlas200DK/faster-deploy](https://gitee.com/Atlas200DK/faster-deploy)  。

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   该快速部署脚本可以快速部署多个案例，请选择sample-crowdcounting-python案例部署即可。  
    >-   该快速部署脚本自动完成了代码下载、模型转换、环境变量配置等流程，如果需要了解详细的部署过程请选择常规部署方式。转: **[2. 常规部署](#li3208251440)**  

2.  <a name="li3208251440"></a>常规部署，请参考：  [https://gitee.com/Atlas200DK/sample-README/tree/master/sample-crowdcounting-python](https://gitee.com/Atlas200DK/sample-README/tree/master/sample-crowdcounting-python)  。

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   该部署方式，需要手动完成代码下载、模型转换、环境变量配置等过程。完成后，会对其中的过程更加了解。  


## 环境配置<a name="section681934411710"></a>

**注：开发板上hiai库、opencv库、相关依赖已安装可跳过此步骤。**

1.  配置开发板联网。

    请参考[https://gitee.com/Atlas200DK/sample-README/tree/master/DK\_NetworkConnect](https://gitee.com/Atlas200DK/sample-README/tree/master/DK_NetworkConnect)  ，进行开发板网络连接配置。

2.  安装环境依赖。

    请参考[https://gitee.com/Atlas200DK/sample-README/tree/master/DK\_Environment](https://gitee.com/Atlas200DK/sample-README/tree/master/DK_Environment)  ，进行环境依赖配置。


## 部署<a name="zh-cn_topic_0219905762_section1872516528910"></a>

1.  以Mind Studio安装用户进入crowdcounting-python应用代码所在根目录，如：$HOME/sample-crowdcounting-python。
2.  <a name="zh-cn_topic_0228757087_li9634105881418"></a>执行部署脚本，进行工程环境准备，Presenter Server服务器的配置等操作，其中Presenter Server用于接收Application发送过来的数据并通过浏览器进行结果展示。

    **bash deploy.sh** _host\_ip_

    -   _host\_ip_：Atlas 200 DK开发者板的IP地址。

    命令示例：

    **bash deploy.sh 192.168.1.2**

    当提示“Please choose one to show the presenter in browser\(default: 127.0.0.1\):“时，请输入在浏览器中访问Presenter Server服务所使用的IP地址（一般为虚拟网卡的IP地址。）

    请在“Current environment valid ip list“中选择通过浏览器访问Presenter Server服务使用的IP地址。

3.  启动Presenter Server。

    执行如下命令在后台启动密集人群人数统计应用的Presenter Server主程序。

    **bash start\_presenterserver.sh**

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >执行此脚本会先杀死后台的其他Presenter Server进程。后台无正在执行的进程会提示presenter server not in process；后台有正在执行的进程会提示presenter server stop success。  

    如[图 Presenter Server进程启动](#zh-cn_topic_0228757087_fig69531305324)所示，表示presenter\_server的服务启动成功。

    **图 1**  Presenter Server进程启动<a name="zh-cn_topic_0228757087_fig69531305324"></a>  
    ![](figures/Presenter-Server进程启动-55.png "Presenter-Server进程启动-55")

    使用上图提示的URL登录Presenter Server，仅支持Chrome浏览器。IP地址为[步骤2](#zh-cn_topic_0228757087_li9634105881418)中输入的IP地址，端口号默为7007，如下图所示，表示Presenter Server启动成功。

    **图 2**  主页显示<a name="zh-cn_topic_0228757087_fig64391558352"></a>  
    ![](figures/主页显示-56.png "主页显示-56")

    Presenter Server、Mind Studio与Atlas 200 DK之间通信使用的IP地址示例如下图所示：

    **图 3**  IP地址示例<a name="zh-cn_topic_0228757087_fig1881532172010"></a>  
    ![](figures/IP地址示例-57.png "IP地址示例-57")

    其中：

    -   Atlas 200 DK开发者板使用的IP地址为192.168.1.2（USB方式连接）。
    -   Presenter Server与Atlas 200 DK通信的IP地址为UI Host服务器中与Atlas 200 DK在同一网段的IP地址，例如：192.168.1.223。
    -   通过浏览器访问Presenter Server的IP地址本示例为：10.10.0.1，由于Presenter Server与Mind Studio部署在同一服务器，此IP地址也为通过浏览器访问Mind Studio的IP。

4.  crowdcounting-python应用支持解析本地视频和RTSP视频流。
    -   如果需要解析本地视频，需要将视频文件传到Host侧。

        例如将视频文件crowd.mp4上传到Host侧的“/home/HwHiAiUser/sample“目录下。

        >![](public_sys-resources/icon-note.gif) **说明：**   
        >支持H264与H265格式的MP4文件，如果MP4文件需要剪辑，建议使用开源工具ffmpeg，使用其他工具剪辑的视频文件ffmpeg工具可能不支持解析。  

    -   如果仅解析RTSP视频流，本步骤可跳过。


## 运行<a name="zh-cn_topic_0219905762_section6245151616426"></a>

1.  在Mind Studio所在Ubuntu服务器中，以HwHiAiUser用户SSH登录到Host侧。

    **ssh HwHiAiUser@192.168.1.2**

2.  在HwHiAiUser用户下进入应用代码所在目录。

    **cd \~/HIAI\_PROJECTS/sample-crowdcounting-python**

3.  执行应用程序。

    **python main.py** _channel_

    -   _channel:_ 输入的视频文件名或者RTSP流地址

    视频文件运行的命令示例如下所示：

    **python main.py /home/HwHiAiUser/sample/crowd.mp4**

    RTSP视频流的命令示例如下所示：

    **python main.py rtsp://192.168.2.37:554/cam/realmonitor?channel=1&subtype=0**

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >可使用ctrl+c停止程序  

4.  使用启动Presenter Server服务时提示的URL登录 Presenter Server 网站。

    等待Presenter Agent传输数据给服务端，单击“Refresh“刷新，当有数据时相应的Channel 的Status变成绿色，如[图 Presenter Server界面](#zh-cn_topic_0228757087_fig113691556202312)所示。

    **图 4**  Presenter Server界面<a name="zh-cn_topic_0228757087_fig113691556202312"></a>  
    ![](figures/Presenter-Server界面-54.png "Presenter-Server界面-54")

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   Presenter Server最多支持10路Channel同时显示，每个  _presenter\_view\_app\_name_  对应一路Channel。  
    >-   由于硬件的限制，每一路支持的最大帧率是20fps，受限于网络带宽的影响，帧率会自动适配为较低的帧率进行展示。  

5.  单击右侧对应的View Name链接，比如上图的“video”，查看结果。

