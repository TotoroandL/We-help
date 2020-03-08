from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import Truncator
import math
from datetime import datetime


# Login （个人信息模块）的models #

class MasterType(models.Model):
    type = (
        ('delivery', "快递"),
        ('procurement', "代购"),
        ('print', "打印"),
        ('umbrella', "共享伞"),
        ('others', "其他"),
    )
    master_type_id = models.AutoField(primary_key=True, verbose_name='商品类型')
    master_type_name = models.CharField(max_length=20, choices=type, default='delivery', null=True, blank=True, verbose_name='接单类型')


class User(AbstractUser):
    """
    用户资料
    """
    gender_choice = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    login = (
        ('0', u'离线'),
        ('1', u'在线'),
    )
    username = models.CharField(max_length=64, verbose_name='用户名', unique=True)
    name = models.CharField(max_length=64, blank=True, verbose_name='姓名')
    gender = models.CharField(max_length=2, choices=gender_choice)
    college = models.CharField(max_length=64, blank=True, verbose_name='学院')
    major = models.CharField(max_length=64, blank=True, verbose_name='专业')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    qq_num = models.CharField(max_length=64, blank=True, verbose_name='QQ号')
    avatar = models.ImageField(upload_to='avatar', verbose_name='头像')

    final_remark = models.FloatField(max_length=10, null=True, blank=True, verbose_name='总评分')
    task_take_num = models.IntegerField(default=0, blank=True, verbose_name='接单总次数')
    alike = models.IntegerField(default=0, blank=True, verbose_name='点赞总次数')
    attention = models.IntegerField(default=0, blank=True, verbose_name='关注总次数')

    is_login = models.CharField(max_length=128, choices=login, default='0', verbose_name='')

    master_type = models.ForeignKey(MasterType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='达人类型')

    become_master_datetime = models.DateTimeField(auto_now_add=True, verbose_name='成为达人时间')
    master_take_delivery_times = models.IntegerField(default=0, blank=True, verbose_name='接快递总次数')
    master_take_buy_times = models.IntegerField(default=0, blank=True, verbose_name='接代购总次数')
    master_take_print_times = models.IntegerField(default=0, blank=True, verbose_name='接打印总次数')
    master_take_umbrella_times = models.IntegerField(default=0, blank=True, verbose_name='接共享伞总次数')
    master_take_others_times = models.IntegerField(default=0, blank=True, verbose_name='接其他单次数')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# Login （个人信息模块）的models #


# Send （发单模块）和Take（接单模块） 的models #

class TaskSend(models.Model):
    """
    发单信息
    """
    state = (
        ('0', "未接单"),
        ('1', "已接单"),
    )
    type = (
        ('delivery', "快递"),
        ('buy', "代购"),
        ('print', "打印"),
        ('umbrella', "共享伞"),
        ('others', "其他"),
    )
    task_id = models.AutoField(primary_key=True, verbose_name='订单ID')
    task_category = models.CharField(max_length=128, choices=type, default='delivery', null=True, blank=True, verbose_name='分类')
    task_time = models.DateTimeField(max_length=128, verbose_name='任务时间', null=True)
    task_place = models.CharField(max_length=128, verbose_name='任务地点')
    task_reward = models.IntegerField(blank=True, verbose_name='报酬')
    task_details = models.CharField(max_length=128, blank=True, verbose_name='详情')
    task_send_time = models.DateTimeField(auto_now_add=True, verbose_name='订单发出时间')
    task_img = models.ImageField(upload_to='task_img', null=True, default='avatar/default.png', verbose_name='发单图片')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发出者')
    task_state = models.CharField(max_length=128, choices=state, default='0', null=True, blank=True, verbose_name='是否被接')
    send_collection_times = models.IntegerField(default=0, blank=True, verbose_name='被收藏次数')

    class Meta:
        ordering = ["task_send_time"]
        verbose_name = "发单表"
        verbose_name_plural = "发单表"


class MasterLike(models.Model):
    """
    对达人点赞
    """
    master = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='被赞者', related_name='be_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞用户', related_name='like')
    like_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        ordering = ["like_time"]
        verbose_name = "点赞"
        verbose_name_plural = "点赞"


class MasterFavorite(models.Model):
    """
    关注达人
    """
    master = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='被关注者', related_name='be_fav')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='粉丝', related_name='fav')
    fav_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        ordering = ["fav_time"]
        verbose_name = "关注"
        verbose_name_plural = "关注"


class GoodType(models.Model):
    """
    商品类型
    """
    type = (
        ('food', "食物"),
        ('cloth', "衣服"),
        ('furniture', "家具"),
        ('book', "书籍"),
        ('stationary', "文具"),
        ('others', '其他'),
    )
    good_type_id = models.AutoField(primary_key=True, verbose_name='商品类型')
    good_type_name = models.CharField(max_length=20, choices=type, default='食物', null=True, blank=True, verbose_name='商品类型')

    class Meta:
        ordering = ["good_type_id"]
        verbose_name = "商品类型"


class Good(models.Model):
    """
    商品
    """
    good_id = models.AutoField(primary_key=True, verbose_name='商品ID')
    good_sender_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='卖家')
    good_portrait = models.ImageField(upload_to='good_img', default='avatar/default.png', verbose_name='商品图片')
    good_name = models.CharField(max_length=20, default="", verbose_name='商品名称')
    good_prize = models.FloatField(max_length=128, verbose_name='价格')
    good_description = models.CharField(max_length=256, blank=True, verbose_name='描述')
    good_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='发出时间')
    good_category = models.ForeignKey(GoodType, on_delete=models.CASCADE, verbose_name='商品分类')
    fav = models.IntegerField(default=0, blank=True, verbose_name='收藏总次数')
    car = models.IntegerField(default=0, blank=True, verbose_name='加入购物车总次数')

    def __str__(self):
        return self.good_name


class GoodCar(models.Model):
    """
    购物车
    """
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='购物车的商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='加入者')
    add_car_time = models.DateTimeField(auto_now_add=True, verbose_name='加入购物车时间')

    class Meta:
        ordering = ["add_car_time"]
        verbose_name = "Pie"
        verbose_name_plural = "加入购物车"


class GoodFavorite(models.Model):
    """
    收藏商品
    """
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='收藏的商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='收藏者')
    favorite_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        ordering = ["favorite_time"]
        verbose_name = "收藏"
        verbose_name_plural = "收藏"


class TaskTake(models.Model):
    """
    订单信息
    """
    state = (
        ('0', "已完成"),
        ('1', "未完成"),
    )
    task_take_id = models.AutoField(primary_key=True, verbose_name='订单ID')
    task_taker_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接单ID')
    task_send_id = models.OneToOneField(TaskSend, on_delete=models.CASCADE, verbose_name='发单表')
    task_take_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='接单时间')
    task_take_state = models.CharField(max_length=32, choices=state, default="1", blank=True, null=True, verbose_name='订单状态')
    task_take_mark = models.FloatField(max_length=128,  blank=True, null=True, verbose_name='订单评分')

    def __str__(self):
        return str(self.task_taker_id)


class Collection(models.Model):
    """
    收藏的发单
    """
    collection_id = models.AutoField(primary_key=True, verbose_name='收藏ID')
    collection_collector_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='收藏者')
    collection_thing_id = models.ForeignKey(TaskSend, on_delete=models.CASCADE, verbose_name='收藏的商品')
    collection_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    def __str__(self):
        return str(self.collection_id)


class Competition(models.Model):
    """
    大赛
    """
    competition_id = models.AutoField(primary_key=True)
    competition_sender_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    competition_poster = models.ImageField(upload_to='competition_img', verbose_name='大赛海报')
    competition_title = models.CharField(max_length=50, default="", verbose_name='大赛主题')
    competition_description = models.CharField(max_length=200, verbose_name='大赛简介')
    competition_time = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='发布时间')
    competition_colletion_times = models.IntegerField(default=0, blank=True, verbose_name='收藏次数')


class CollectionCompetition(models.Model):
    """
    收藏的比赛
    """
    collectioncompetition_id = models.AutoField(primary_key=True, verbose_name='收藏比赛ID')
    collectioncompetition_thing_id = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='收藏的比赛')
    collectioncompetition_collector_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='收藏者')
    collectioncompetition_time = models.DateTimeField(auto_now_add=True, verbose_name='比赛收藏时间')


# Send （发单模块）和Take（接单模块） 的models #


# Communication（联系模块） 的models #

class Message(models.Model):
    """
    站内私信
    """
    state = (
        ('0', "未读"),
        ('1', "已读"),
    )

    state_x = (
        ('0', "未被发件者标记"),
        ('1', "已被发件人标记"),
    )
    state_y = (
        ('0', "未被收件者标记"),
        ('1', "已被收件者标记"),
    )
    message_id = models.IntegerField(primary_key=True)
    txtmessage = models.CharField(max_length=100, null=False, verbose_name='留言内容名字')
    message_sender = models.CharField(max_length=100, null=False, verbose_name='留言发出者名字')
    message_receiver = models.CharField(max_length=100,null=False,verbose_name='留言接收者名字')
    message_receiver_ID = models.CharField(max_length=100,null=False,verbose_name='留言接收者ID')
    message_sender_ID = models.CharField(max_length=100,null=False,verbose_name='留言发出者ID')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    title = models.CharField(max_length=100,null=True,verbose_name='留言标题')
    is_new = models.CharField(max_length=100,choices=state,default='0',blank=True,null=True,verbose_name='是都已阅')
    is_marked_bysender = models.CharField(max_length=100,choices=state_x,default='0',blank=True,null=True,verbose_name='是否被发件者标注')
    is_marked_byreceiver= models.CharField(max_length=100,choices=state_y,default='0',blank=True,null=True,verbose_name='是否被收件人标记')


class Notice(models.Model):
    """
    系统通知
    """
    state = (
        ('0', "未读"),
        ('1', "已读"),
    )
    Notice_ID = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name='系统通知标题')
    message_fromsystem = models.CharField(max_length=100, null=False, verbose_name='系统通知')
    message_receiver = models.CharField(max_length=100, null=False, verbose_name='接收系统通知者名字')
    is_new = models.CharField(max_length=100,choices=state,default='0',blank=True,null=True,verbose_name='是否已读')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='通知发出时间')


class suggestion(models.Model):
    """
    用户反馈建议
    """
    title = models.CharField(max_length=100,null=True,blank=True,verbose_name='用户反馈标题')
    suggestion = models.CharField(max_length=100,null=False,verbose_name='用户反馈')
    sender = models.CharField(max_length=100,null=True,verbose_name='反馈者名字')

# Communication（联系模块） 的models #


# Boards（论坛模块）的models #

class Board(models.Model):
    """
    模块信息
    """
    name = models.CharField(max_length=30, unique=True, blank=True, verbose_name='板块名称')
    description = models.CharField(max_length=100, blank=True, verbose_name='板块描述')

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    """
    话题
    """
    subject = models.CharField(max_length=255, blank=True, verbose_name='主题名称')  #题目
    last_updated = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='最近更新')  #字段在实例第一次保存的时候会保存当前时间
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE, verbose_name='所属板块名称')
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE, verbose_name='发帖人')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览数')
    img = models.ImageField(upload_to='img', null=True, verbose_name='图片')

    def __str__(self):
        return self.subject

    # 解决分页过多，提供更多导航
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 4
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)


class Post(models.Model):
    """
    话题内容
    """
    message = models.TextField(max_length=4000, verbose_name='帖子内容')
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE, verbose_name='帖子主题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发帖时间')
    updated_at = models.DateTimeField(null=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name='发帖人')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE, verbose_name='帖子更新人')
    post_img = models.ImageField(upload_to='post_img', null=True, verbose_name='图片')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)


class Report(models.Model):
    """
    举报信息
    """
    report_created_by = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE, verbose_name='举报人')
    message = models.TextField(max_length=4000, verbose_name='举报内容')
    report_topic = models.ForeignKey(Topic, related_name='reports', on_delete=models.CASCADE, verbose_name='举报帖子')


class Contact(models.Model):
    Contacted_by =  models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE, verbose_name='联系人')
    message = models.TextField(max_length=400, verbose_name='联系内容')
    description = models.CharField(max_length=50, blank=True, verbose_name='联系描述')
    contacted_at = models.DateTimeField(auto_now_add=True, verbose_name='联系时间')



class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证码类型", choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')), max_length=30)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email   # 这里很重要，否则在后台就显示不出Meta信息
