# coding=utf-8
"""工具函数库 🛠️.

提供 JSON 对比、配置文件创建、locust 命令启动等辅助能力。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.load_config import ConfigOperation
from config.log_config import ROOT_PATH, Logger

logger = Logger()


def compare_json(src: Any, dst: Any) -> List[bool]:
    """递归比较两段数据结构是否完全一致。

    返回不相等位置的结果列表，空列表表示完全相等。
    """
    flag_list: List[bool] = []

    def _cmp(cur_src: Any, cur_dst: Any) -> None:
        if isinstance(cur_src, dict):
            if not isinstance(cur_dst, dict):
                flag_list.append(False)
                return
            for key in cur_dst:
                if key not in cur_src:
                    flag_list.append(False)
            for key in cur_src:
                if key in cur_dst:
                    _cmp(cur_src[key], cur_dst[key])
                else:
                    flag_list.append(False)
        elif isinstance(cur_src, list):
            if not isinstance(cur_dst, list) or len(cur_src) != len(cur_dst):
                flag_list.append(False)
                return
            for src_item, dst_item in zip(cur_src, cur_dst):
                _cmp(src_item, dst_item)
        else:
            if str(cur_src) != str(cur_dst):
                flag_list.append(False)

    _cmp(src, dst)
    return flag_list


def read_json(file_path: str) -> Any:
    """读取 JSON 文件并返回解析后的对象。"""
    return json.load(open(file_path, "r", encoding="utf-8"))


def create_master_config(filename: str, section_name: str) -> None:
    """创建 master 配置文件（若不存在）。"""
    logger.info("=====检查 master 配置文件=====")
    file_path = ROOT_PATH / filename
    if not file_path.exists():
        logger.info("=====master 配置文件不存在，创建 master 配置文件=====")
        file_path.touch()
    conf = ConfigOperation(filename)
    if section_name not in conf.get_section():
        conf.add_section(section_name)


def create_worker_config(
    kwargs: Dict[str, Any], worker_num: int = 4
) -> List[str]:
    """根据 worker_num 生成指定数量的 worker 配置文件。

    返回生成的配置文件路径列表。
    """
    logger.info("=====创建 worker 配置文件=====")
    worker_config_name = "locust_worker{}.conf"
    worker_names = []
    for i in range(1, worker_num + 1):
        fname = worker_config_name.format(i)
        conf = ConfigOperation(fname)
        conf.add_config("system", kwargs)
        worker_names.append(fname)
    return worker_names


def update_master_config(
    filename: str, section_name: str, master_kwargs: Dict[str, Any]
) -> None:
    """更新 master 配置文件中传入的键值对。"""
    logger.info("=====检查配置文件是否变更开始=====")
    conf = ConfigOperation(filename)
    conf.judge_config(section_name, master_kwargs)


def run_locust_with_config(file_stem: str) -> None:
    """通过 `.conf` 配置启动 locust。"""
    subprocess.run(f"locust --config={file_stem}.conf", check=False)


def run_locust_native(test_file: str, host: str, run_time: str) -> None:
    """直接以命令行参数方式启动 locust。"""
    subprocess.run(
        f"locust -f {test_file} --host={host} --headless -u 100 -r 100 --run-time {run_time}",
        check=False,
    )


def init_confg(
    filename: str,
    section_name: str,
    master_kwargs: Dict[str, Any],
    worker_kwargs: Dict[str, Any],
    need_worker: bool = True,
    worker_num: int = 4,
) -> Optional[List[str]]:
    """初始化配置文件。

    :param need_worker: 是否需要创建 master / worker 分布式测试环境
    :param worker_num: worker 节点数量
    :return: worker 配置文件路径列表（若 need_worker 为 False 返回 None）
    """
    create_master_config(filename, section_name)
    worker_names = None
    if need_worker:
        worker_names = create_worker_config(worker_kwargs, worker_num)
    update_master_config(filename, section_name, master_kwargs)
    return worker_names


def _delete_configs(prefix: str) -> None:
    """删除指定前缀的配置文件。"""
    for item in os.listdir(ROOT_PATH):
        if item.startswith(prefix) and item.endswith(".conf"):
            (ROOT_PATH / item).unlink()
            logger.info(f"删除配置文件: {item}")


def del_worker_config() -> None:
    """删除所有 worker 配置文件。"""
    _delete_configs("locust_worker")


def del_master_config() -> None:
    """删除所有 master 配置文件。"""
    _delete_configs("locust_master")


if __name__ == "__main__":
    del_worker_config()
    del_master_config()
