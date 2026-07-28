"""Regression tests for /api/schools SQL 注入面修复。

不依赖具体数据行,只断言:
1. 常规参数与注入尝试均返回 200(SQL 结构未被破坏);
2. 响应为 JSON 数组;
3. 数组元素(若有)恰好包含 views.py 中字典字面量定义的 38 个 key。
"""
from django.test import TestCase, Client


EXPECTED_KEYS = frozenset({
    'U_Name_CN', 'U_Name_EN', 'U_Name_Local', 'U_City', 'U_URL',
    'U_Abbr', 'U_Other_Name', 'Description_CN', 'Description_EN',
    'Unit_CN', 'Unit_EN', 'U_Lon', 'U_Lat', 'U_id',
    'C_Name_CN', 'C_Name_EN', 'Country', 'C_Lat', 'C_Lon',
    'C_Name_Other', 'C_id', 'C_Country_EN',
    'Co_Name_CN', 'Co_Name_EN', 'Co_Continent_EN',
    'P_Name_CN', 'P_Name_EN', 'P_URL',
    'P_Physical_Geography', 'P_Human_Geography', 'P_Urban_Planning',
    'P_GIS', 'P_RS', 'P_GNSS', 'P_Transportation',
    'P_Research_Interests', 'P_people_id', 'P_Research_Interests_CN',
})


class SchoolListRegressionTests(TestCase):
    """覆盖 spec §需求与验收 中列出的 6 组请求。"""

    url = '/api/schools'

    def setUp(self):
        self.client = Client()

    def _assert_shape(self, response):
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIsInstance(payload, list)
        if payload:
            for item in payload:
                self.assertEqual(set(item.keys()), EXPECTED_KEYS)

    def test_no_params(self):
        self._assert_shape(self.client.get(self.url))

    def test_tag_single(self):
        self._assert_shape(self.client.get(self.url, {'tag': 'Urban_Planning'}))

    def test_tag_multi(self):
        self._assert_shape(
            self.client.get(self.url, {'tag': 'Urban_Planning,Transportation'})
        )

    def test_tag_non_existent(self):
        """白名单外的 tag 应被丢弃,SQL 仍能执行不 500。"""
        self._assert_shape(self.client.get(self.url, {'tag': 'NON_EXISTENT'}))

    def test_tag_injection_attempts(self):
        """注入串必须被白名单过滤,不破坏 SQL 结构。"""
        for payload in ('DROP_TABLE', '1=1', 'Urban_Planning;--'):
            with self.subTest(tag=payload):
                self._assert_shape(self.client.get(self.url, {'tag': payload}))

    def test_continent(self):
        self._assert_shape(self.client.get(self.url, {'continent': 'Asia'}))

    def test_continent_injection(self):
        """continent 走参数化占位符,注入串仅作为字面量匹配,SQL 不 500。"""
        self._assert_shape(self.client.get(self.url, {'continent': "' OR 1=1 --"}))
