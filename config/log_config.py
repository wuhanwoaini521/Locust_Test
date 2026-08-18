# coding=utf-8
"""日志控制器 📝.

统一封装 Python 标准库 logging，支持同时输出到控制台与文件。
"""

import datetime
import logging
import os
from pathlib import Path

# 项目根目录
ROOT_PATH = Path(__file__).resolve().parent.parent


class Logger:
    """轻量日志控制器 💬."""

    def __init__(self, log_level: int = logging.DEBUG):
        self.log_level = log_level
        self.formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        )
        self.log_path = ROOT_PATH / "logs"
        self.log_path.mkdir(exist_ok=True)

        log_date = datetime.datetime.now().strftime("%Y_%m_%d")
        log_filename = ROOT_PATH / "logs" / f"log_{log_date}.log"

        # 避免重复添加 handler
        self.logger = logging.getLogger("locust_test")
        self.logger.setLevel(self.log_level)
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_filename, encoding="utf-8")
            console_handler = logging.StreamHandler()
            file_handler.setFormatter(self.formatter)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


if __name__ == "__main__":
    logger = Logger()
    logger.info("this is info test")
    logger.error("this is error test")
    logger.debug("this is debug test")
    logger.critical("this is critical test")
