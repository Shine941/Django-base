from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from book.models import BookInfo


def index(request):
    # 在这里实现增删改查
    books = BookInfo.objects.all()
    print(books)
    return HttpResponse('index')
# mysql数据存储在硬盘
# redis的数据存储在内存

# 我把硬盘的数据保存在内存也成为缓存

# ##################增加数据##################

# 方式一 对象实例化
book = BookInfo(
    name='Django',
    pub_date='2000-1-1',
    readcount=10
)
# 必须要调用save方法才能将数据保存到数据库中
book.save()
# 方式二
# objects--相当于一个代理，实现增删改查
BookInfo.objects.create(
    name='测试开发',
    pub_date='2020-1-1',
    readcount=100
)
# ##################修改数据##################
# 方式一
# select * from bookinfo where id = 6
book = BookInfo.objects.get(id=6)
book.name = '运维开发入门'
# 想要保存数据也要使用save()方法
book.save()
# 方式二
# filter 过滤
BookInfo.objects.filter(id=6).update(name='爬虫入门', commentcount=666)
BookInfo.objects.get(id=5).update(name='5555', commentcount=999)  # 不能用

# ##################删除数据###################
# 方法一
book = BookInfo.objects.get(id=8)
# 删除分两种，物理删除（这条记录的数据  删除）和 逻辑删除 （修改标记位 例如 is_delete=False)
book.delete()  # 物理删除
# 方式2
BookInfo.objects.get(id=6).delete()
BookInfo.objects.filter(id=5).delete()

# ##################查询数据##################
# get查询单一结果，如果不存在会抛出模型类.DoesNotExist异常。
try:
    book = BookInfo.objects.get(id=1)
except BookInfo.DoesNotExist:  # 自己设置异常输出，查询结果不存在则输出
    print('查询结果不存在')
# all查询多个结果。
books = BookInfo.objects.all()
from book.models import PeopleInfo

PeopleInfo.objects.all()
# count查询结果数量。
BookInfo.objects.all().count()

# ##################过滤查询##################
# 实现SQL中的where功能，包括
# filter过滤出多个结果
# exclude排除掉符合条件剩下的结果
# get过滤单一结果
# 对于过滤条件的使用，上述三个方法相同，故仅以filter进行讲解。
# 模型类名.objects.filter(属性名__运算符=值)  # 获取n个结果 n=0,1,2,3,4......
# 模型类名.objects.exclude(属性名__运算符=值)  # 获取n个结果 n=0,1,2,3,4......
# 模型类名.objects.get(属性名__运算符=值)  # 获取1个结果  或者 异常


# 查询编号为1的图书
book = BookInfo.objects.get(id=1)  # 简写（属性名=值）
BookInfo.objects.get(id__exact=1)  # 完整形式 两个下划线
BookInfo.objects.get(pk=1)  # pk primary key 主键
BookInfo.objects.filter(id=1)  # 简写（属性名=值）
# 查询书名包含'湖'的图书
BookInfo.objects.filter(name__contains='湖')
# 查询书名以'部'结尾的图书
BookInfo.objects.filter(name__endswith='部')
# 查询书名为空的图书
BookInfo.objects.filter(name__isnull=True)
# 查询编号为1或3或5的图书
BookInfo.objects.filter(id__in=[1, 3, 5])
# 查询编号大于3的图书
# 大于 gt greate 大
# 大于等于 gte e equal
# 小于 lt little
# 小于等于 lte
BookInfo.objects.filter(id__gt=3)
# 查询编号不等于3的书籍
BookInfo.objects.exclude(id=3)
# 查询1980年发表的图书
BookInfo.objects.filter(pub_date__year=1980)
# 查询1990年1月1日后发表的图书
BookInfo.objects.filter(pub_date__gt='1990-1-1')
# 错误的
# BookInfo.objects.filter(pub_date__gt='199011')

# ##################F##################
from django.db.models import F

# 使用：两个属性的比较 （属性一 运算符 属性二）
# 语法形式：以filter为例，模型类名.objects.filter(属性名__运算符=F('第二个属性名'))
# 查询阅读量大于等于评论量的图书
BookInfo.objects.filter(readcount__gte=F('commentcount'))

# ##################并且##################
# 查询阅读里昂大于20,并编号小于3的图书
BookInfo.objects.filter(readcount__gt=20).filter(id__lt=3)
# 或者
BookInfo.objects.filter(readcount__gt=20, id__lt=3)
# ##################Q##################
from django.db.models import Q

# 或者语法：模型类名.objects.filter(Q(属性名__运算符=值)|Q()|...)
# 并且语法：模型类名.objects.filter(Q(属性名__运算符=值)&Q()&...)
# not非语法：模型类名.objects.filter(～Q(属性名__运算符=值))
# 查询阅读里昂大于20,并编号小于3的图书
BookInfo.objects.filter(Q(readcount__gt=20) | Q(id__lt=3))
# # 查询编号不是3的图书
BookInfo.objects.filter(~Q(id=3))
# ##################聚合函数##################
from django.db.models import Sum, Max, Min, Avg, Count
# 模型类名.objects.aggregate(Xxx('字段名'))
BookInfo.objects.aggregate(Sum('readcount'))
# ##################排序##################
BookInfo.objects.all().order_by('readcount')  # 升序  -readcount是降序

# ##################两个表的级联操作##################
# 查询书籍为1的所有人物信息
# 获取了id为1的书籍
book=BookInfo.objects.get(id=1)
book.peopleinfo_set.all()
# 查询人物为1的书籍信息
person = PeopleInfo.objects.get(id=1)
person.book.name
person.book.readcount
# ##################关联过滤查询##################
# 语法形式
# 查询1的数据，条件为n
# 模型类名.objects.(关联模型类名小写__字段名__运算符=值)
# 查询图书，要求图书人物为‘郭靖'
BookInfo.objects.filter(peopleinfo__name__exact='郭靖')
BookInfo.objects.filter(peopleinfo__name='郭靖')
# 查询图书，要求图书人物的描述包含'八'
BookInfo.objects.filter(peopleinfo__description__contains='八')
# 查询书名为‘天龙八部’的所有人物
PeopleInfo.objects.filter(book__name='天龙八部')
PeopleInfo.objects.filter(book__name__exact='天龙八部')
# 查询阅读量大于30的所有人物
PeopleInfo.objects.filter(book__readcount__gt=30)
