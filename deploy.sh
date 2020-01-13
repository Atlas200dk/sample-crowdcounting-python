#!/bin/bash

script_path="$( cd "$(dirname "$0")" ; pwd -P )"

remote_host=$1

app_name="crowdcountingapp"
model_dir="model"

. ${script_path}/script/func_deploy.sh
. ${script_path}/script/func_util.sh

function deploy_app()
{
    #set remote_port
    parse_remote_port

    if [ -d ${script_path}/${app_name} ];then
        echo "[Step] Deploy app and model..."
        deploy_app_lib_path ${app_name} ${script_path} ${remote_host} ${model_dir}
        if [[ $? -ne 0 ]];then
            return 1
        fi
    fi
    return 0
}

main()
{
    check_ip_addr ${remote_host}
    if [[ $? -ne 0 ]];then
        echo "ERROR: invalid host ip, please check your command format: ./deploy.sh host_ip."
        exit 1
    fi
    
    echo "[Step] Prepare presenter server information and graph.py..."
    bash ${script_path}/script/prepare_graph.sh ${remote_host}

    deploy_app
    if [[ $? -ne 0 ]];then
        exit 1
    fi

    echo "Finish to deploy crowdcountingapp."
    exit 0
}

main
