# coding=utf-8
from datetime import datetime
from config.load_config import Config_Operation, Logger
import os
import sys
from config.utils import create_slave, run_cmd_locust_config, init_confg, create_master, del_slave_config, del_master_config
import threading

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(
    current_directory) + os.path.sep + ".")
sys.path.append(root_path)

"""
1. 先配置locust的配置文件
2. 启动locust
"""

# locust配置文件
pre_master_name = "locust_master"
pre_slave_name = "locust_slave"
section_name = "system"

# 生成report和log的文件名（根据时间）
now = datetime.now()
timestr = now.strftime("%Y_%m_%d_%H_%M_%S")

# report和log地址
report_path = f".\\report\\locust_{timestr}_report.html"
locust_log_path = f".\\logs\\locust_{timestr}.log"
file_name = ".\\tests\\locustfile.py"
master_config_name = f"{pre_master_name}.conf"

# 实例化 - 日志功能
logger = Logger()

# 实例化 - locust.conf配置文件功能
c_operation = Config_Operation(pre_master_name)

# 配置文件(默认)
conf_dict = {
    "locustfile": file_name,
    "headless": "true",
    "host": "http://192.168.1.200:8000",
    "users": "100",
    "spawn-rate": "100",
    "run-time": "10s",
    "html": report_path,
    "print-stats": "false",
    "logfile": locust_log_path
}

# 是否需要master 和slave 组合
master_config = {
    "master": "true"
}

# slave 配置
slave_dict = {
    "locustfile": file_name,
    "headless": "true",
    "worker": "true",
}

need_master = False
if need_master:
    conf_dict.update(master_config)


if __name__ == '__main__':

    logger.info("=====清空slaver配置文件=====")
    del_slave_config(pre_slave_name)
    logger.info("=====清空master配置文件=====")
    del_master_config(pre_master_name)

    logger.info("=====初始化配置文件=====")

    # 判断是否需要创建master文件
    slave_name = init_confg(master_config_name, section_name,
                            conf_dict, slave_dict, need_master=need_master, slave_num=3)
    # print(slave_name)
    logger.info("=====开始执行locust测试=====")
    logger.info(" >>>>> 创建master线程")
    slave_list = []

    # 启动master主线程
    t1 = threading.Thread(target=run_cmd_locust_config,
                          args=(pre_master_name,))
    t1.start()

    if slave_name is not None:
        logger.info(" >>>>> 创建slave线程")
        # 启动slave线程
        for i in slave_name:
            s_name = i[:-5]
            t = threading.Thread(target=run_cmd_locust_config, args=(s_name,))
            slave_list.append(t)
        for t in slave_list:
            t.start()
        for t in slave_list:
            t.join()

    t1.join()
    logger.info(
        f"=====locust执行结束=====\n >>>>>报告地址：{report_path} \n >>>>>log地址：{locust_log_path}")
