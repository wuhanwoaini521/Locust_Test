# coding=utf-8
import requests
from locust import HttpUser, TaskSet, task


data_list = [
]


class MyBlogs(TaskSet):
  
    @task(1)
    def post_Process_data1(self):
        # 定义请求头
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        
		
        req = self.client.post("/Process", data=data_list[0],
                               headers=header, verify=False)
							   
		print(req)
		
		if req.status_code == 200:
            print("success")
        else:
            print("fails")
	
	
			


class websitUser(HttpUser):
    tasks = [MyBlogs]
    min_wait = 3000  # 单位为毫秒
    max_wait = 6000  # 单位为毫秒


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://xxxxxxxx")
