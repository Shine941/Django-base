from django.http import HttpResponse
from django.shortcuts import render, redirect
from book.models import BookInfo

# Create your views here.
def create_book(request):
    book = BookInfo.objects.create(
        name='abc',
        pub_date='2000-1-1',
        readcount=10
    )
    return HttpResponse('create')


def shop(request, city_id, mobile):
    # import re
    # if not re.match('\d{5}', shop_id):
    #     return HttpResponse('没有此商品')
    print(city_id, mobile)
    query_params = request.GET
    print(query_params)
    # <QueryDict: {'order': ['readcount']}> 具有字典的特性还具有一键多值
    # <QueryDict: {'order': ['readcount', 'readcomment'], 'page': ['1']}>
    # order = query_params.get('order')  # readcount 当order只有一个时候可以用get
    # order = query_params['order']  # readcount
    order = query_params.getlist('order')  # 多个值：['readcount', 'readcomment']
    print(order)
    return HttpResponse('饭店')


def register(request):
    data = request.POST
    print(data)
    return HttpResponse('ok')


def json(request):
    # request.POST  # json 不能通过request.POST获取数据
    body = request.body
    print(body)  # b'{\n    "name":"itcast",\n    "age":10\n}'  byte类型
    body_str = body.decode()  # byte类型转码
    print(body_str)  # str类型
    # {
    #     "name":"itcast",
    #     "age":10
    # }
    # json类型字符串可以转换为python的字典
    import json
    body_dict = json.loads(body_str)
    print(body_dict)  # {'name': 'itcast', 'age': 10}
    # #########请求头###########
    # print(request.META)
    print(request.META['SERVER_PORT'])
    return HttpResponse('json')


def method(request):
    print(request.method)
    return HttpResponse('method')


from django.http import HttpResponse, JsonResponse


def response(request):
    # response = HttpResponse('res', status=200)
    # # 设置响应头
    # response['name']='itcast'
    # return response
    # json-->dict
    # dict-->json
    # 定义一个字典
    info = {
        'name': 'itcast',
        'address': 'shunyi'

    }
    girl_friends = [
        {
            'name': 'rose',
            'address': 'shunyi'
        },
        {
            'name': 'jack',
            'address': 'changping'
        }
    ]
    # data 返回的响应数据，一般是字典类型
    # safe=True表示我们的data是字典数据
    # JsonResponse 可以把字典转换为json
    # 现在给了一个非字典数据，出了问题自己负责
    # response = JsonResponse(data=girl_friends, safe=False)
    # return response
    return redirect('http://www.itcast.cn')
    # import json
    # data = json.dumps(girl_friends)
    # response = HttpResponse(data)
    # return response
    # 1xx
    # 2xx
    # 3xx
    # 4xx   请求有问题 例如：404 找不到页面，路由有问题；403 禁止访问，权限有问题
    # 5xx


# ############################
"""

查询字符串
http://ip:port/path/?key=value&key1=value1..
url 以？为分割 分为两部分
？前面为 请求路径
？ 后面为 查询字符串 查询字符串类似为字典 key=value 多个数据采用&拼接
"""
# #############cookie###############
"""
第一次请求,携带查询字符串
http://127.0.0.1:8000/set_cookie/?usernmae=itcast&password=123
服务器接收到请求之后，获取username,服务器设置cookie信息,cookie信息包括username
浏览器接收到服务器的相应之后，应该把cookie保存起来
第二次访问及其之后的请求，我们访问http://127.0.0.1:8000，都会携带cookie信息。服务器就可以读取cookie信息，来判断用户身份
"""


def set_cookie(request):
    # 1.获取查询字符串数据
    username = request.GET.get("username")
    password = request.GET.get("password")
    # 2.服务器设置cookie信息
    # 通过响应对象.set_cookie 方法
    response = HttpResponse('set_cookie')
    # key,value=''
    # max_age是一个秒数，从响应开始计数的一个秒数
    response.set_cookie('name', username, max_age=60*60)
    response.set_cookie('pwd', password)
    response.delete_cookie('name')  # 删除cookie
    return response

def get_cookie(request):
    # 获取cookie
    # print(request.COOKIES)  # 字典数据：{'name': 'itcast'}
    name = request.COOKIES.get('name')
    return HttpResponse(name)

# #################################
# session是保存在服务器端，数据相对安全
# session需要依赖于cookie
"""
第一次请求http://127.0.0.1:8000/set_session/?username=itheima，我们在服务器端设置session信息
服务器同时会生成一个sessionid的cookie信息
浏览器接收到这个信息后，会把cookie数据保存起来
第二次及其之后的请求，都会携带这个sessionid，服务器会验证这个sessionid，验证没有问题会读取相关数据，实现业务逻辑
"""


def set_session(request):
    # 1.模拟获取用户信息
    username = request.GET.get('username')
    # 2.设置session信息
    # 假如我们通过模型查询 查询到了 用户的信息
    user_id = 1
    request.session['user_id'] = user_id
    request.session['username'] = username
    return HttpResponse('set_session')


def get_session(request):
    # user_id = request.session['user_id']  # 如果没有数据，显示异常
    # username = request.session['username']
    user_id = request.session.get('user_id')  # 如果没有数据，显示null不会出现异常
    username = request.session.get('username')
    # '%s' %username
    content = '{},{}'.format(user_id, username)
    return HttpResponse(content)
