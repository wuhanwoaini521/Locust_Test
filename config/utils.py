import json
import os
import sys
from config.load_config import Config_Operation
from config.log_config import Logger

logger = Logger()

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

# 判断两段json是否相等
flag_list = []


def cmp(src_data, dst_data):
    flag = True
    if isinstance(src_data, dict):
        """若为dict格式"""
        for key in dst_data:
            if key not in src_data:
                # print("src不存在这个key%s" % key)
                # flag = False
                flag_list.append(False)
        for key in src_data:
            if key in dst_data:
                """递归"""
                cmp(src_data[key], dst_data[key])
            else:
                # print("dst不存在这个key %s" % key)
                # flag = False
                flag_list.append(False)
    elif isinstance(src_data, list):
        """若为list格式"""
        if len(src_data) != len(dst_data):
            print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
        # for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
        for src_list, dst_list in zip(src_data, dst_data):
            """递归"""
            cmp(src_list, dst_list)
    else:
        if str(src_data) != str(dst_data):
            # print("该值不相等：% s" % src_data)
            flag_list.append(False)

    return flag_list


# 读取json文件
def read_json(file):
    return json.load(open(file, 'r', encoding="utf-8"))


# 创建配置文件 master
def create_master(filename, section_name):
    logger.info("=====检查master配置文件=====")
    file_path = root_path + os.path.sep + filename
    master_is_exists = os.path.exists(file_path)

    if not master_is_exists:
        logger.info("=====master配置文件不存在，创建master配置文件=====")
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(f"[{section_name}]")

    conf = Config_Operation(filename)
    section_list = conf.get_section()
    if section_name not in section_list:
        conf.add_section(section_name)


# 创建配置文件 slave
def create_slave(section_name, kwargs, slave_num=4):
    """
    根据slave_num创建slave数量
    :param slave_num:  想要创建的slave数量
    :return:
    """
    logger.info("=====创建slaver配置文件=====")
    slave_config_module = "locust_slave%s.conf"
    slave_name = []
    for i in range(1, slave_num + 1):
        with open(slave_config_module % i, "w", encoding='utf-8') as f:
            con = Config_Operation(slave_config_module % i)
            con.add_config(section_name, kwargs)
        slave_name.append(slave_config_module % i)
    return slave_name


# 修改配置文件
def update_master(filename, section_name, master_kwargs):
    logger.info("=====检查配置文件是否变更开始=====")
    conf = Config_Operation(filename)
    conf.judge_config(section_name, master_kwargs)


# cmd 运行 locust命令
def run_cmd_locust_config(file_name):
    os.system(f"locust --config={file_name}.conf")


def run_cmd_locust_native(test_file, host, run_time):
    os.system(f"locust -f {test_file} --host={host} --headless -u 100 -r 100 --run-time {run_time}")


# 判断配置文件是否存在，（创建操作）
def init_confg(filename, section_name, master_kwargs, slave_kwargs, need_master=True, slave_num=4):
    """
    初始化配置文件
    :param need_master:  是否需要创建 master和slave分布式测试环境
    :param filename:
    :param section_name:
    :param master_kwargs:
    :param slave_kwargs:
    :param slave_num:
    :return:
    """
    slave_name = None
    create_master(filename, section_name)
    if need_master:
        slave_name = create_slave(section_name, slave_kwargs, slave_num)
    update_master(filename, section_name, master_kwargs)
    return slave_name


def del_slave_config(file_name):
    """
    删除slave配置
    :param file_name:
    :return:
    """
    slave_names = os.listdir(root_path)
    # print(slave_names)
    for slave in slave_names:
        if slave.startswith(file_name):
            os.remove(root_path + os.path.sep + slave)


def del_master_config(file_name):
    """
    删除master配置
    :param file_name:
    :return:
    """
    master_names = os.listdir(root_path)
    # print(slave_names)
    for master in master_names:
        if master.startswith(file_name):
            os.remove(root_path + os.path.sep + master)


if __name__ == '__main__':
    # conf_dict = {"a": "1"}
    # create_slave("system", conf_dict)

    # create_master("locust_master.conf", "system")
    del_slave_config()
