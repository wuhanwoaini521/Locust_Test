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


def compare_json(expected: Any, actual: Any) -> List[str]:
    """递归比较两段数据结构，返回差异明细。

    每条差异为人类可读的字符串，带字段路径，方便直接贴进压测报告：

        ["data.code: 期望 0，实际 500"]

    返回空列表表示两者完全一致。
    """
    diffs: List[str] = []

    def _type_name(value: Any) -> str:
        return type(value).__name__

    def _join(path: str, key: Any) -> str:
        return f"{path}.{key}" if path else str(key)

    def _cmp(cur_expected: Any, cur_actual: Any, path: str) -> None:
        label = path or "root"
        if isinstance(cur_expected, dict):
            if not isinstance(cur_actual, dict):
                diffs.append(
                    f"{label}: 类型不一致，期望 dict，实际 {_type_name(cur_actual)}"
                )
                return
            for key, value in cur_expected.items():
                if key in cur_actual:
                    _cmp(value, cur_actual[key], _join(path, key))
                else:
                    diffs.append(f"{_join(path, key)}: 期望存在该字段，实际缺失")
            for key in cur_actual:
                if key not in cur_expected:
                    diffs.append(f"{_join(path, key)}: 实际多出的字段")
        elif isinstance(cur_expected, list):
            if not isinstance(cur_actual, list):
                diffs.append(
                    f"{label}: 类型不一致，期望 list，实际 {_type_name(cur_actual)}"
                )
                return
            if len(cur_expected) != len(cur_actual):
                diffs.append(
                    f"{label}: 长度不一致，期望 {len(cur_expected)}，"
                    f"实际 {len(cur_actual)}"
                )
                return
            for index, (item_e, item_a) in enumerate(zip(cur_expected, cur_actual)):
                _cmp(item_e, item_a, f"{path}[{index}]")
        else:
            # 标量统一按字符串比较，兼容 "200" 与 200 这类宽松场景
            if str(cur_expected) != str(cur_actual):
                diffs.append(f"{label}: 期望 {cur_expected!r}，实际 {cur_actual!r}")

    _cmp(expected, actual, "")
    return diffs


def read_json(file_path: str) -> Any:
    """读取 JSON 文件并返回解析后的对象。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


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
    """通过 `.conf` 配置启动 locust（参数以列表传递，避免 shell 注入）。"""
    subprocess.run(["locust", f"--config={file_stem}.conf"], check=False)


def run_locust_native(test_file: str, host: str, run_time: str) -> None:
    """直接以命令行参数方式启动 locust。"""
    subprocess.run(
        [
            "locust", "-f", test_file,
            f"--host={host}", "--headless",
            "-u", "100", "-r", "100",
            "--run-time", run_time,
        ],
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
