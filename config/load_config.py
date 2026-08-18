# coding=utf-8
"""配置文件读写操作 📂.

基于 configparser 操作 `.conf` 格式配置文件。
"""

import configparser
import os
from pathlib import Path
from typing import Any, Dict, List

from config.log_config import ROOT_PATH, Logger

logger = Logger()


class ConfigOperation:
    """对 configparser 的封装，提供配置文件的增删改查。"""

    def __init__(self, filename: str):
        self.file = filename if Path(filename).is_absolute() else ROOT_PATH / filename
        # 确保文件存在
        if not Path(self.file).exists():
            Path(self.file).touch()
        self.cf = configparser.ConfigParser()
        self.cf.read(str(self.file), encoding="utf-8")

    def _save(self) -> None:
        with open(self.file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def get_config(self, section_name: str) -> Dict[str, str]:
        """获取指定 section 下的所有键值对。"""
        if section_name not in self.cf.sections():
            return {}
        return dict(self.cf.items(section_name))

    def get_section(self) -> List[str]:
        """获取全部 section 名。"""
        return self.cf.sections()

    def add_section(self, section_name: str) -> None:
        """新增 section。"""
        if section_name not in self.cf.sections():
            self.cf.add_section(section_name)
            self._save()

    def add_config(self, section_name: str, kwargs: Dict[str, Any]) -> None:
        """新增 section 并写入键值对。"""
        self.cf.add_section(section_name)
        for k, v in kwargs.items():
            self.cf[section_name][k] = str(v)
        self._save()

    def add_config_single(self, section_name: str, kwargs: Dict[str, Any]) -> None:
        """在已有 section 下新增单个键值。"""
        if section_name not in self.cf.sections():
            self.cf.add_section(section_name)
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                self.cf[section_name][k] = str(v)
        self._save()

    def update_config(self, section_name: str, kwargs: Dict[str, Any]) -> None:
        """修改已有键的值。"""
        if section_name not in self.cf.sections():
            self.cf.add_section(section_name)
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                self.cf.set(section_name, k, str(v))
        self._save()

    def judge_config(self, section_name: str, kwargs: Dict[str, Any]) -> None:
        """对比传入配置与现有配置，自动新增或更新差异项。"""
        old_config = self.get_config(section_name)
        for k, v in kwargs.items():
            if k not in old_config:
                logger.info(f">>>>查询到新增参数 {k}，开始插入数据")
                self.add_config_single(section_name, {k: v})
            elif old_config[k] != kwargs[k]:
                logger.info(f">>>>查询到配置文件变更 {k}: {v}，开始修改")
                self.update_config(section_name, {k: v})


if __name__ == "__main__":
    file_name = "../locust_master.conf"
    config = ConfigOperation(file_name)
    config.add_section("system")
    print(config.get_section())
