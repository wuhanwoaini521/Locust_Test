# coding=utf-8
"""校验型性能测试示例 🧪.

通过将请求返回结果与期望结果做 JSON 对比，实现"接口返回校验 + 性能压测"
一体的负载脚本。
"""

from locust import HttpUser, between, task

from config.utils import compare_json


class ProcessTask(HttpUser):
    """对 /Process 接口做带返回校验的性能测试。"""

    # 每个任务之间随机等待 3~6 秒（Locust 2.x 标准写法）
    wait_time = between(3, 6)

    @task
    def post_process(self) -> None:
        """提交 JSON 数据并校验返回是否符合预期。"""
        headers = {"Content-Type": "application/json"}
        payload = {
            # TODO: 按实际接口补充请求参数
            "example": "data"
        }
        expected = {
            # TODO: 按实际接口补充期望返回
            "code": 0
        }
        with self.client.post(
            "/Process", json=payload, headers=headers,
            catch_response=True, name="data1_test",
        ) as resp:
            # 校验：对实际返回与期望做 JSON 对比，diff 为差异明细列表
            diff = compare_json(expected, resp.json())
            if not diff:
                resp.success()
            else:
                resp.failure(f"返回数据与期望不一致: {'; '.join(diff)}")


if __name__ == "__main__":
    import subprocess

    subprocess.run(
        ["locust", "-f", "locustfile.py", "--host=http://192.168.1.200:8000"],
        check=False,
    )
