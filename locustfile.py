# coding=utf-8
"""Locust 性能测试主入口文件 🐝.

简单的 GET/POST 负载示例，可直接运行：
    locust -f locustfile.py --host=http://your-host
"""

from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    """Simulated user behavior 模拟用户行为。"""

    # 每个任务之间随机等待 3~6 秒（Locust 2.x 标准写法）
    wait_time = between(3, 6)

    @task(2)
    def get_index(self) -> None:
        """高频任务：访问首页。"""
        self.client.get("/")

    @task(1)
    def post_process(self) -> None:
        """低频任务：提交数据到 /Process。"""
        payload = {"hello": "playwright", "from": "locust"}
        headers = {"Content-Type": "application/json"}
        with self.client.post(
            "/Process", json=payload, headers=headers, catch_response=True
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"请求失败，状态码: {resp.status_code}")
            else:
                resp.success()


if __name__ == "__main__":
    import subprocess

    subprocess.run(
        ["locust", "-f", "locustfile.py", "--host=http://localhost:8000"],
        check=False,
    )
