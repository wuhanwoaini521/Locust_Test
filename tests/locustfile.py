# coding=utf-8
from locust import HttpUser, TaskSet, task
from config.utils import cmp, read_json
import json
import os
import sys

from data.result_data import req1, req2, req3, req4, req5, req6, req7, req8, req9, req10


current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)


class MyBlogs(TaskSet):
	@task(1)
	def post_Process_data1(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data1.json")  # 读取json文件
	
		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True, name="data1_test") as res:
			c = cmp(req1, res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data2(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data2.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True, name="data2_test") as res:
			c = cmp(req2, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data3(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data3.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data3_test") as res:
			c = cmp(req3, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data4(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data4.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data4_test") as res:
			c = cmp(req4, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data5(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data5.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data5_test") as res:
			c = cmp(req5, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data6(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data6.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data6_test") as res:
			c = cmp(req6, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data7(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data7.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data7_test") as res:
			c = cmp(req7, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data8(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data8.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data8_test") as res:
			c = cmp(req8, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data9(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data9.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data9_test") as res:
			c = cmp(req9, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")

	@task(1)
	def post_Process_data10(self):
		# 定义请求头
		header = {"Content-Type": "application/json"}
		json_file = read_json("./data/data10.json")  # 读取json文件

		with self.client.post("/Process", json=json_file, headers=header, verify=False, catch_response=True,
							  name="data10_test") as res:
			c = cmp(req10, res.json())
			# print(res.json())
			if len(c) == 0:
				# print("scuuess")
				res.success()
			else:
				res.failure("失败")


class websitUser(HttpUser):
	tasks = [MyBlogs]
	min_wait = 3000  # 单位为毫秒
	max_wait = 6000  # 单位为毫秒


if __name__ == "__main__":
	import os
	os.system("locust -f locustfile.py --host=http://192.168.1.200:8000")
