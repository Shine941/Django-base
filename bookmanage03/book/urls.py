from django.urls import path, converters
from book.views import create_book, shop, register, \
    json, method, response, set_cookie, get_cookie, set_session
from django.urls.converters import register_converter
from book.views import get_session


# 1.定义转换器
class MobileConverter:
    # 验证数据的关键是正则表达式
    regex = "1[3-9]\d{9}"

    # 验证没有问题的数据，给视图函数
    def to_python(self, value):
        return value

    # def to_url(self, value):
    #     # 将匹配结果用于反向解析传值时使用（了解）
    #     return value


# 2.注册转换器，才能在第三步中使用
# converter 转换器类
# type_name 转换器名字
register_converter(MobileConverter, 'phone')
urlpatterns = [
    path('create/', create_book),
    # <转换器名字:变量名>
    # 转换器会对变量数据进行正则的验证
    path('<int:city_id>/<phone:mobile>/', shop),  # 不能满足全部需求
    path('register/', register),
    path('json/', json),
    path('method/', method),
    path('res/', response),
    path('set_cookie/', set_cookie),
    path('get_cookie/', get_cookie),
    path('set_session/', set_session),
    path('get_session/', get_session),
]
"""
class IntConverter:
    regex = "[0-9]+"
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return str(value)
"""
