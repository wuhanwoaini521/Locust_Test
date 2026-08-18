# 🐝 Locust Test

> 基于 **Python Locust** 的**性能测试 / 压测**示例项目 🚀
> 支持 master / worker **分布式压测**，自带`配置文件自动生成`与`日志系统`。

---

## ✨ 项目特色

- ✅ **Distributed 分布式压测**：一键创建 master + 多个 worker 节点
- 📄 **自动配置**：`.conf` 配置文件自动生成 / 比对 / 更新
- 📝 **内置日志**：控制台 + 文件双输出，按天归档
- 📊 **结果报告**：自动生成 HTML 报告
- 🧪 **校验型压测**：接口返回与期望结果自动比对

## 🛠️ 技术栈

| 技术 | 说明 |
|------|------|
| 🐍 Python | 3.8+ |
| 🐝 Locust | 2.x |
| 📦 configparser | 标准库配置读写 |

## 📦 安装

```bash
git clone https://github.com/wuhanwoaini521/Locust_Test.git
cd Locust_Test

pip install locust
```

## 🚀 使用

### 单节点压测（快速开始）

直接运行顶层的负载脚本：

```bash
locust -f locustfile.py --host=http://your-host
```

然后浏览器打开 `http://localhost:8089`，填写并发数开始压测。

### 使用配置文件（推荐）

```bash
python main.py
```

会执行以下流程：
1. 🧹 清理历史配置文件
2. ⚙️ 自动生成 `locust_master.conf`（如需分布式再生成 worker 配置）
3. 🚀 以 headless 模式启动 locust
4. 📊 生成带时间戳的 HTML 报告到 `report/`

### 分布式压测（master / worker）

1. 打开 `main.py`，将 `need_worker` 改为 `True`
2. 修改 `worker_num` 控制 worker 数量
3. 运行 `python main.py`

## 📁 项目结构

```
Locust_Test/
├── config/
│   ├── __init__.py
│   ├── load_config.py      # configparser 配置读写封装
│   ├── log_config.py       # 日志系统
│   └── utils.py            # 工具函数（JSON 对比、配置生成、locust 启动）
├── tests/
│   └── locustfile.py       # 校验型压测脚本（接口返回比对）
├── report/                 # 生成 HTML 报告（已 gitignore）
├── logs/                   # 运行日志（已 gitignore）
├── locustfile.py           # 压测主脚本（入口）
└── main.py                 # 压测主程序
```

## ⚙️ 关键配置说明

`main.py` 里的默认配置：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `host` | `http://192.168.1.200:8000` | 被测系统地址 |
| `users` | `100` | 并发用户数 |
| `spawn-rate` | `100` | 每秒启动用户数 |
| `run-time` | `10s` | 压测持续时间 |
| `headless` | `true` | 无界面模式 |
| `need_worker` | `False` | 是否启用分布式 |

> 💡 请根据实际被测环境修改 `host` 和目标接口。

## 🧪 校验型压测怎么用

在 `tests/locustfile.py` 中：

```python
payload   = {"example": "data"}   # 请求参数
expected  = {"code": 0}           # 期望返回
```

Locust 会根据 `compare_json` 的比对结果，把不一致的请求标记为 `failure`。

## 📄 License

MIT License © 2024 [wuhanwoaini521](https://github.com/wuhanwoaini521)
