from django.urls import path
from book.views import index
# 这个是固定写法urlpatterns = []
urlpatterns = [
    # path(路由, 视图函数名)
    path('index/', index)
]