"""config.utils 单元测试 🧪.

全部离线运行，不依赖任何外部服务：

    pytest unit_tests
"""

from pathlib import Path

import pytest

from config.load_config import ConfigOperation
from config.utils import compare_json, init_confg


# ---------------------------------------------------------------------------
# compare_json
# ---------------------------------------------------------------------------

class TestCompareJson:
    """compare_json：递归 JSON 对比。"""

    def test_identical_dicts(self):
        """完全一致返回空列表。"""
        data = {"code": 0, "data": {"name": "locust", "tags": ["a", "b"]}}
        assert compare_json(data, {"code": 0, "data": {"name": "locust", "tags": ["a", "b"]}}) == []

    def test_scalar_diff_reports_path(self):
        """标量不一致时报出字段路径与期望/实际值。"""
        diffs = compare_json({"code": 0}, {"code": 500})
        assert len(diffs) == 1
        assert "code" in diffs[0]
        assert "0" in diffs[0] and "500" in diffs[0]

    def test_missing_and_extra_keys(self):
        """期望缺失 / 实际多出的字段都能被发现。"""
        expected = {"a": 1, "b": 2}
        actual = {"a": 1, "c": 3}
        diffs = compare_json(expected, actual)
        assert any("b" in d and "缺失" in d for d in diffs)
        assert any("c" in d and "多出" in d for d in diffs)

    def test_nested_dict_type_mismatch(self):
        """dict 遇上非 dict 要报类型不一致。"""
        diffs = compare_json({"a": {}}, {"a": 123})
        assert len(diffs) == 1
        assert "类型不一致" in diffs[0]

    def test_list_length_mismatch(self):
        """列表长度不同要报长度差异。"""
        diffs = compare_json([1, 2, 3], [1, 2])
        assert len(diffs) == 1
        assert "长度不一致" in diffs[0]

    def test_list_item_diff_has_index(self):
        """列表元素差异带下标路径。"""
        diffs = compare_json([{"k": 1}], [{"k": 9}])
        assert diffs == ["[0].k: 期望 1，实际 9"]

    def test_scalar_string_compare_is_lenient(self):
        """标量按字符串宽松比较，\"200\" 与 200 视为一致。"""
        assert compare_json(200, "200") == []


# ---------------------------------------------------------------------------
# ConfigOperation
# ---------------------------------------------------------------------------

class TestConfigOperation:
    """ConfigOperation：.conf 配置文件增删改查（使用 tmp_path，不碰仓库文件）。"""

    @pytest.fixture()
    def conf(self, tmp_path):
        return ConfigOperation(str(tmp_path / "locust_test.conf"))

    def test_add_and_get_config(self, conf):
        conf.add_config("system", {"host": "http://localhost:8000", "users": 10})
        got = conf.get_config("system")
        assert got["host"] == "http://localhost:8000"
        assert got["users"] == "10"  # configparser 读出来都是字符串

    def test_get_config_missing_section(self, conf):
        assert conf.get_config("not_exist") == {}

    def test_judge_config_inserts_new_key(self, conf):
        conf.add_config("system", {"users": "10"})
        conf.judge_config("system", {"spawn-rate": "5"})
        assert conf.get_config("system")["spawn-rate"] == "5"

    def test_judge_config_updates_changed_value(self, conf):
        conf.add_config("system", {"users": "10"})
        conf.judge_config("system", {"users": "20"})
        assert conf.get_config("system")["users"] == "20"

    def test_persistence_across_instances(self, tmp_path):
        path = str(tmp_path / "persist.conf")
        ConfigOperation(path).add_config("system", {"users": "7"})
        assert ConfigOperation(path).get_config("system")["users"] == "7"


# ---------------------------------------------------------------------------
# init_confg
# ---------------------------------------------------------------------------

class TestInitConfig:
    """init_confg：master / worker 配置初始化。"""

    def test_no_worker_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr("config.load_config.ROOT_PATH", Path(tmp_path))
        monkeypatch.setattr("config.utils.ROOT_PATH", tmp_path)
        result = init_confg(
            "m.conf", "system",
            {"users": "10"}, {"worker": "true"},
            need_worker=False,
        )
        assert result is None
        assert (tmp_path / "m.conf").exists()

    def test_worker_configs_created(self, tmp_path, monkeypatch):
        monkeypatch.setattr("config.load_config.ROOT_PATH", Path(tmp_path))
        monkeypatch.setattr("config.utils.ROOT_PATH", tmp_path)
        worker_names = init_confg(
            "m.conf", "system",
            {"users": "10"}, {"worker": "true"},
            need_worker=True, worker_num=2,
        )
        assert worker_names == ["locust_worker1.conf", "locust_worker2.conf"]
        for name in worker_names:
            assert (tmp_path / name).exists()
