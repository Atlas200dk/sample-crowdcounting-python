#!/bin/bash

script_path="$( cd "$(dirname "$0")" ; pwd -P )"

remote_host=$1

. ${script_path}/func_deploy.sh
. ${script_path}/func_util.sh

app_path="${script_path}/.."

function modify_graph()
{
    echo "Modify presenter server information in graph.config..."
    touch ${app_path}/crowdcountingapp/graph.py 
    presenter_ip=`grep presenter_server_ip ${app_path}/presenterserver/crowd_counting/config/config.conf | awk -F '=' '{print $2}' | sed 's/[^0-9.]//g'`
    if [[ $? -ne 0 ]];then
        echo "ERROR: get presenter server ip failed, please check ${app_path}/presenterserver/crowd_counting/config/config.conf."
        return 1
    fi
    
    presenter_port=`grep presenter_server_port ${app_path}/presenterserver/crowd_counting/config/config.conf | awk -F '=' '{print $2}' | sed 's/[^0-9]//g'`
    if [[ $? -ne 0 ]];then
        echo "ERROR: get presenter server port failed, please check ${app_path}/presenterserver/crowd_counting/config/config.conf."
        return 1
    fi
    `> ${app_path}/crowdcountingapp/graph.py`
    echo "presenter_ip = '${presenter_ip}'" >> ${app_path}//crowdcountingapp/graph.py
    echo "presenter_port = ${presenter_port}" >> ${app_path}//crowdcountingapp/graph.py
    return 0
}

function main()
{
    echo "Modify presenter server configuration..."
    check_ip_addr ${remote_host}
    if [[ $? -ne 0 ]];then
        echo "ERROR: invalid host ip, please check your command format: ./prepare_graph.sh host_ip ."
        exit 1
    fi
    bash ${script_path}/prepare_presenter_server.sh ${remote_host}
    if [[ $? -ne 0 ]];then
        exit 1
    fi
    
    modify_graph
    if [[ $? -ne 0 ]];then
        exit 1
    fi
    
    echo "Finish to prepare facedetectionapp graph."
    exit 0
}

main
