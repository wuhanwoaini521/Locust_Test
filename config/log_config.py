import datetime
import logging
import os
import sys
import time

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

class Logger:
    """
    日志控制器
    """
    def __init__(self):
        self.log_level = logging.DEBUG
        self.log_datetime = datetime.datetime.now().strftime("%Y_%m_%d")
        self.log_filename = "log_" + self.log_datetime + ".log"
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        # self.log_path = os.path.abspath(os.getcwd()) + '/logs/'
        self.log_path = root_path + '/logs/'
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        self.log_path_filename = os.path.join(self.log_path + self.log_filename)

        self.fileHandler = logging.FileHandler(self.log_path_filename)
        self.consoleHandler = logging.StreamHandler()

        # 控制器连接格式器
        self.fileHandler.setFormatter(self.formatter)
        self.consoleHandler.setFormatter(self.formatter)

        # 创建记录器并配置
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)

        if not self.logger.handlers:  # 判断是否有未关闭的FileHandler或者StreamHandler， 如果有就不新建，没有就新建
            # 记录器连接控制器
            self.logger.addHandler(self.fileHandler)
            self.logger.addHandler(self.consoleHandler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':

    print(current_directory, " --- " , root_path)

    c = Logger()
    c.info("this is info test")
    c.error("this is error test")
    c.debug("this is error test")
    c.critical("this is critical test")


