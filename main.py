# coding=utf-8
"""Locust 压测主程序 🚀.

流程：
1. 配置 locust 的 `.conf` 配置文件
2. 启动 locust（支持 master / worker 分布式）

用法：
    python main.py
"""

import threading
from datetime import datetime
from pathlib import Path

from config.log_config import Logger
from config.utils import (
    del_master_config,
    del_worker_config,
    init_confg,
    run_locust_with_config,
)

ROOT_PATH = Path(__file__).resolve().parent

# 配置文件前缀名
PRE_MASTER_NAME = "locust_master"
PRE_WORKER_NAME = "locust_worker"
SECTION_NAME = "system"

# 基于时间的报告 / 日志文件名
timestr = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
report_path = ROOT_PATH / "report" / f"locust_{timestr}_report.html"
locust_log_path = ROOT_PATH / "logs" / f"locust_{timestr}.log"
test_file = ROOT_PATH / "tests" / "locustfile.py"  # 负载测试脚本

# 实例化日志与配置工具
logger = Logger()

# 默认配置
conf_dict = {
    "locustfile": str(test_file),
    "headless": "true",
    "host": "http://192.168.1.200:8000",
    "users": "100",
    "spawn-rate": "100",
    "run-time": "10s",
    "html": str(report_path),
    "print-stats": "false",
    "logfile": str(locust_log_path),
}

# 是否需要 master / worker 分布式组合
need_worker = False

# worker 配置
worker_dict = {
    "locustfile": str(test_file),
    "headless": "true",
    "worker": "true",
}


def main() -> None:
    """执行完整的 locust 压测流程。"""
    # 确保 report / logs 目录存在
    (ROOT_PATH / "report").mkdir(exist_ok=True)
    (ROOT_PATH / "logs").mkdir(exist_ok=True)

    logger.info("=====清理 worker 配置文件=====")
    del_worker_config()
    logger.info("=====清理 master 配置文件=====")
    del_master_config()

    logger.info("=====初始化配置文件=====")
    worker_names = init_confg(
        f"{PRE_MASTER_NAME}.conf",
        SECTION_NAME,
        conf_dict,
        worker_dict,
        need_worker=need_worker,
        worker_num=3,
    )

    logger.info("=====开始执行 locust 测试=====")
    logger.info(" >>>>> 创建 master 线程")

    # 启动 master 主线程
    master_thread = threading.Thread(
        target=run_locust_with_config, args=(PRE_MASTER_NAME,)
    )
    master_thread.start()

    if worker_names:
        logger.info(" >>>>> 创建 worker 线程")
        worker_threads = [
            threading.Thread(target=run_locust_with_config, args=(name[:-5],))
            for name in worker_names
        ]
        for t in worker_threads:
            t.start()
        for t in worker_threads:
            t.join()

    master_thread.join()
    logger.info(
        f"=====locust 执行结束=====\n"
        f" >>>>>报告地址：{report_path}\n"
        f" >>>>>log 地址：{locust_log_path}"
    )


if __name__ == "__main__":
    main()
