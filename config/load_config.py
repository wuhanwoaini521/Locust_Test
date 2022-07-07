# coding=utf-8
import configparser
import os
import sys
from datetime import datetime
from config.log_config import Logger

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)


logger = Logger()


class Config_Operation:

    def __init__(self, file):
        self.cf = configparser.ConfigParser()
        self.cf.read(file, encoding='utf-8')
        self.file = file

    def get_config(self, section_name):
        """
        获取默认配置
        :return:
        """
        option_dict = {}
        # 读取所有的sections
        sections = self.cf.sections()
        # 获取指定sections下的所有options名
        options = self.cf.options(section_name)
        # print("配置文件中system下的配置：%" % options)
        # 获取指定sections下所有options的键值对
        options_dict = self.cf.items(section_name)
        for option in options_dict:
            k, v = option
            # print("%s: %s" % (k, v))
            option_dict[k] = v
        return option_dict

    def get_section(self):
        """
        获取sections列表
        :return:
        """
        section_list = self.cf.sections()
        return section_list

    def add_section(self, section_name):
        """
        增加配置文件的section_name
        :param section_name:
        :return:
        """
        self.cf.add_section(section_name)
        self.cf.write(open(self.file, mode="w", encoding='utf-8'))

    def add_config(self, section_name, kwargs):
        """
        增加配置文件整体内容
        :param file:
        :return:
        """
        # 根据section_name 增加1
        self.cf.add_section(section_name)
        self.cf[section_name] = kwargs

        self.cf.write(open(self.file, mode="w"))

    def add_config_single(self, section_name, kwargs):
        """
        增加配置文件中某个sections下的options
        :param section_name:
        :param kwargs:
        :return:
        """
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                self.cf[section_name][k] = v

        self.cf.write(open(self.file, mode="w", encoding='utf-8'))

    def update_config(self, section_name, kwargs):
        """
        修改配置文件中的内容
        :param section_name:
        :param kwargs:
        :return:
        """
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                self.cf.set(section_name, k, v)

        self.cf.write(open(self.file, mode="w", encoding='utf-8'))

    def judge_config(self, section_name, kwargs):
        """
        判断用户传入的配置文件是否进行了变更
        1. 如果没有发生变更，则不动
        2. 如果发生变更，则调用 update_config方法
        :param section_name:
        :param kwargs:
        :return:
        """
        # 获取配置文件的内容
        old_config = self.get_config(section_name)
        update_dict = {}
        add_dict = {}
        # 判断传入的数据是否与配置文件中一致
        for k, v in kwargs.items():
            if k not in old_config.keys():
                add_dict[k] = kwargs[k]
                logger.info(">>>>查询到新增参数，开始插入数据")
                self.add_config_single(section_name, add_dict)
                add_dict = {}
            else:
                if old_config[k] == kwargs[k]:
                    pass
                else:
                    logger.info(">>>>查询到配置文件变更，开始修改配置文件")
                    logger.info(">>>>修改的配置： %s:%s" % (k, v))
                    update_dict[k] = kwargs[k]

        self.update_config(section_name, update_dict)


if __name__ == '__main__':

    file_name = "../locust_master.conf"
    config = Config_Operation(file_name)
    config.add_section("system")
    get_section = config.get_section()
    print(get_section)

