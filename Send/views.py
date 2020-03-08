from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import MasterType, User, TaskSend, GoodType, Good
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

master_list = []


def success_response(alike):
    data = { }
    data['status'] = 'SUCCESS'
    data['alike'] = alike
    data['message'] = '操作成功'
    return JsonResponse(data)


def fsuccess_response(message):
    data = {}
    data['status'] = 'SUCCESS'
    data['message'] = message
    return JsonResponse(data)


def error_response(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)


def is_login(request):
    if not request.session.get('is_login') == True:
        return error_response('请先登录')


def send_category(request):
    pass
    return render(request, 'Send/send_category.html')


def add_order(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        # 如果表单中要传文件、图片，则需要传两个参数
        task_category = request.POST.get('task_category')
        task_time = request.POST.get('task_time')
        task_place = request.POST.get('task_place')
        task_details = request.POST.get('task_details')
        task_reward = request.POST.get('task_reward')
        user_id = request.session['user_id']

        new_send = models.TaskSend()
        new_send.task_category = task_category
        new_send.task_time = task_time
        new_send.task_place = task_place
        new_send.task_details = task_details
        new_send.task_reward = task_reward
        new_send.sender_id = user_id
        new_send.save()

        send = new_send
        if request.FILES.get('task_img'):
            task_img = request.FILES.get('task_img')
            send.task_img = task_img
            send.save()
        message = '操作成功'
        return fsuccess_response(message)
    return render(request, 'Send/add_order.html', locals())


def reset(request, task_id):
    user_id = request.session.get('user_id')
    send = TaskSend.objects.get(task_id=task_id)
    user = User.objects.get(id=user_id)
    return render(request, 'Send/reset.html', {'send': send, 'user_id': user_id, 'user': user})


def filling_suc(request):
    user_id = request.session['user_id']
    task_list = TaskSend.objects.filter(sender_id=user_id).order_by('-task_send_time')[0:1]
    tasksend_list = TaskSend.objects.filter(sender_id=user_id).order_by('-task_send_time')[1:10]
    return render(request, 'Send/filling_suc.html', {'task_list': task_list, 'tasksend_list': tasksend_list})


def del_send_suc(request, task_id):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能进行关注操作')
    models.TaskSend.objects.filter(task_id=task_id).delete()
    return render(request, 'Send/suc.html')


def send_details(request, task_id):
    tasksend = models.TaskSend.objects.get(task_id=task_id)
    return render(request, 'Send/send_details.html', {'tasksend': tasksend,
                                                        })


def recommend_master(request):
    user_list = User.objects.filter(final_remark__gte=7.5).order_by('final_remark').order_by('-alike').order_by('-attention').order_by('-task_take_num')[0:20]
    delivery = MasterType.objects.get(master_type_id='1')
    buy = MasterType.objects.get(master_type_id='2')
    print = MasterType.objects.get(master_type_id='3')
    umbrella = MasterType.objects.get(master_type_id='4')
    others = MasterType.objects.get(master_type_id='5')

    return render(request, 'Send/recommend_master.html', {'user_list': user_list,
                                                          'delivery': delivery,
                                                          'buy': buy,
                                                          'print': print,
                                                          'umbrella': umbrella,
                                                          'others': others,
                                                          })


def popular_master(request):
    deliverys = User.objects.all().filter(master_type_id='1').order_by('master_take_delivery_times')[0:5]
    buys = User.objects.all().filter(master_type_id='2').order_by('master_take_buy_times')[0:5]
    prints = User.objects.all().filter(master_type_id='3').order_by('master_take_print_times')[0:5]
    umbrellas = User.objects.all().filter(master_type_id='4').order_by('master_take_umbrella_times')[0:5]
    otherss = User.objects.all().filter(master_type_id='5').order_by('master_take_others_times')[0:5]
    delivery = MasterType.objects.get(master_type_id='1')
    buy = MasterType.objects.get(master_type_id='2')
    print = MasterType.objects.get(master_type_id='3')
    umbrella = MasterType.objects.get(master_type_id='4')
    others = MasterType.objects.get(master_type_id='5')
    return render(request, 'Send/popular_master.html', {'deliverys': deliverys, 'delivery': delivery,
                                                        'buys': buys, 'buy': buy,
                                                        'prints': prints, 'print': print,
                                                        'umbrellas': umbrellas, 'umbrella': umbrella,
                                                        'otherss': otherss,  'others': others,
                                                        })


def masters(request):
    delivery = MasterType.objects.get(master_type_id='1')
    buy = MasterType.objects.get(master_type_id='2')
    print = MasterType.objects.get(master_type_id='3')
    umbrella = MasterType.objects.get(master_type_id='4')
    others = MasterType.objects.get(master_type_id='5')
    masters = User.objects.all().order_by('-date_joined')  #导入的Article模型
    p = Paginator(masters, 5)   #分页，10篇文章一页
    if p.num_pages <= 1:  #如果文章不足一页
        master_list = masters  #直接返回所有文章
        data = ''  #不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  #获取请求的文章页码，默认为第一页
        master_list = p.page(page) #返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {    #将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(request, 'Send/masters.html', context={'user_list':master_list, 'data': data,
                                                         'delivery': delivery,
                                                         'buy': buy,
                                                         'print': print,
                                                         'umbrella': umbrella,
                                                         'others': others,
                                                         })


def master_details(request, master_id):
    user_id = request.session.get('user_id')
    master = models.User.objects.get(id=master_id)
    master_fav = models.MasterFavorite.objects.filter(master_id=master_id, user_id=user_id)
    master_lik = models.MasterLike.objects.filter(master_id=master_id, user_id=user_id)
    return render(request, 'Send/master_details.html', {'master': master,
                                                        'master_fav': master_fav,
                                                        'master_lik': master_lik,
                                                        'user_id': user_id})


def master_like(request):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能进行点赞操作')
    user_id = request.session['user_id']
    master_id = request.GET.get('master_id')
    is_like = request.GET.get('is_like')

    # 创建一个点赞记录
    if is_like == 'true':
        # 进行点赞，即实例化一个点赞记录
        master_lik = models.MasterLike.objects.filter(master_id=master_id, user_id=user_id)
        # 通过created来判断点赞记录是否存在，如果存在则不进行点赞，如果不存在则进行点赞数量加一
        if not master_lik:
            # 不存在点赞记录并且已经创建点赞记录，需要将点赞数量加一
            models.MasterLike.objects.create(master_id=master_id, user_id=user_id)
            user = models.User.objects.get(id=master_id)
            user.alike += 1
            user.save()
            return success_response(user.alike)
    else:
        # 取消点赞
        # 先查询数据是否存在，存在则进行取消点赞
        if models.MasterLike.objects.filter(master_id=master_id, user_id=user_id).exists():
            # 数据存在，取消点赞
            # 删除点赞记录
            models.MasterLike.objects.filter(master_id=master_id, user_id=user_id).delete()
            # 判断对应的点赞数量数据是否存在，如果存在则对点赞数量进行减一
            user = models.User.objects.get(id=master_id)
            alike = user.alike
            if alike == 0:
                # 数据不存在，返回错误信息
                return error_response('数据不存在，不能取消点赞')
            else:
                # 数据存在，对数量进行减一
                user.alike -= 1
                user.save()
                return success_response(user.alike)
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能点赞')


def master_favorite(request):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能进行关注操作')
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    master_id = request.GET.get('master_id')
    master = models.User.objects.get(id=master_id)
    is_fav = request.GET.get('is_fav')

    if is_fav == 'true':
        master_fav = models.MasterFavorite.objects.filter(master=master, user=user)
        if not master_fav:
            models.MasterFavorite.objects.create(master=master, user=user)
            user = models.User.objects.get(id=master_id)
            user.attention += 1
            user.save()
            return fsuccess_response("关注成功")
        else:
            # 已经关注
            models.MasterFavorite.objects.get(master=master, user=user).delete()
            return error_response('已经关注过')
    else:
        if models.MasterFavorite.objects.filter(master=master, user=user).exists():
            models.MasterFavorite.objects.get(master=master, user=user).delete()
            user = models.User.objects.get(id=master_id)
            user.attention -= 1
            user.save()
            return fsuccess_response("取消关注成功")
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消关注')


def add_order_of_master(request, master_id):
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    master = models.User.objects.get(id=master_id)
    if request.method == "POST" and request.FILES['task_img']:
        # 如果表单中要传文件、图片，则需要传两个参数
        task_category = request.POST.get('task_category')
        task_time = request.POST.get('task_time')
        task_place = request.POST.get('task_place')
        task_details = request.POST.get('task_details')
        task_reward = request.POST.get('task_reward')
        task_img = request.FILES.get('task_img')
        user_id = request.session['user_id']
        user = models.User.objects.get(id=user_id)
        # 这些都好了，创建新的发单的表单

        new_send = models.TaskSend()
        new_send.task_category = task_category
        new_send.task_time = task_time
        new_send.task_place = task_place
        new_send.task_details = task_details
        new_send.task_reward = task_reward
        new_send.task_img = task_img
        new_send.sender_id = user_id
        new_send.save()

        new_take = models.TaskTake()
        new_take.task_send_id_id = new_send.task_id
        new_take.task_taker_id_id = master_id
        new_take.save()
        message = '操作成功'
        return fsuccess_response(message)

    return render(request, 'Send/add_order_of_master.html', {'master': master, 'user': user, 'user_id': user_id})


def popular_good(request):
    foods = Good.objects.all().filter(good_category_id='1').order_by('fav').order_by('car')[0:10]
    cloths = Good.objects.all().filter(good_category_id='2').order_by('fav').order_by('car')[0:10]
    furnitures = Good.objects.all().filter(good_category_id='3').order_by('fav').order_by('car')[0:10]
    books = Good.objects.all().filter(good_category_id='4').order_by('fav').order_by('car')[0:10]
    stationarys = Good.objects.all().filter(good_category_id='5').order_by('fav').order_by('car')[0:10]
    otherss = Good.objects.all().filter(good_category_id='6').order_by('fav').order_by('car')[0:10]
    food = GoodType.objects.get(good_type_id='1')
    cloth = GoodType.objects.get(good_type_id='2')
    furniture = GoodType.objects.get(good_type_id='3')
    book = GoodType.objects.get(good_type_id='4')
    stationary = GoodType.objects.get(good_type_id='5')
    others = GoodType.objects.get(good_type_id='6')
    type = GoodType.objects.all().order_by('good_type_id')
    return render(request, 'Send/popular_good.html', {'foods': foods, 'food': food,
                                                      'cloths': cloths, 'cloth': cloth,
                                                      'furnitures': furnitures, 'furniture': furniture,
                                                      'books': books, 'book': book,
                                                      'stationarys': stationarys, 'stationary': stationary,
                                                      'otherss': otherss, 'others': others,
                                                      'type': type,
                                                      })


def goods(request):
    type = GoodType.objects.all().order_by('good_type_id')
    goods = Good.objects.all().order_by('-good_time')  #导入的Article模型
    p = Paginator(goods, 5)   #分页，10篇文章一页
    if p.num_pages <= 1:  #如果文章不足一页
        good_list = goods  #直接返回所有文章
        data = ''  #不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  #获取请求的文章页码，默认为第一页
        good_list = p.page(page) #返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {    #将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(request, 'Send/goods.html', context={'good_list': good_list, 'data': data, 'type': type})


def recommend_good(request):
    good_list = Good.objects.all().order_by('fav').order_by('car')[0:20]
    type = GoodType.objects.all().order_by('good_type_id')
    return render(request, 'Send/recommend_good.html', {'good_list': good_list, 'type': type})


def good_details(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    user_id = request.session.get('user_id')
    good_fav = models.GoodFavorite.objects.filter(good=good, user_id=user_id)
    good_car = models.GoodCar.objects.filter(good=good, user_id=user_id)

    return render(request, 'Send/good_details.html', {'good': good, 'good_fav': good_fav, 'good_car': good_car})


def add_car(request):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能加入购物车')
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    good_id = request.GET.get('good_id')
    good = models.Good.objects.get(good_id=good_id)
    is_add = request.GET.get('is_add')

    if is_add == 'true':
        good_car = models.GoodCar.objects.filter(good=good, user=user)
        if not good_car:
            models.GoodCar.objects.create(good=good, user=user)
            good.car += 1
            good.save()
            return fsuccess_response("加入购物车成功")
        else:
            # 已经关注
            return error_response('已经加入购物车')
    else:
        if models.GoodCar.objects.filter(good=good, user=user).exists():
            models.GoodCar.objects.get(good=good, user=user).delete()
            good.car -= 1
            good.save()
            return fsuccess_response('删除成功')
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能从购物车中清除')


def good_favorite(request):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能收藏商品')
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    good_id = request.GET.get('good_id')
    good = models.Good.objects.get(good_id=good_id)
    is_fav = request.GET.get('is_fav')
    if is_fav == 'true':
        good_fav = models.GoodFavorite.objects.filter(good=good, user=user)
        if not good_fav:
            models.GoodFavorite.objects.create(good=good, user=user)
            good.fav += 1
            good.save()
            return fsuccess_response("成功收藏")
        else:
            # 已经关注
            return error_response('已经收藏')
    else:
        if models.GoodFavorite.objects.filter(good=good, user=user).exists():
            models.GoodFavorite.objects.get(good=good, user=user).delete()
            good.fav -= 1
            good.save()
            return fsuccess_response("取消收藏成功")
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消收藏')


def good_category(request, good_type_id):
    good_type = models.GoodType.objects.get(good_type_id=good_type_id)
    good_list = models.Good.objects.all().filter(good_category=good_type)
    return render(request, 'Send/good_category.html', {'good_list': good_list, 'good_type': good_type})


def master_category(request, master_type_id):
    master_type = models.MasterType.objects.get(master_type_id=master_type_id)
    user_list = models.User.objects.all().filter(master_type=master_type)
    delivery = MasterType.objects.get(master_type_id='1')
    buy = MasterType.objects.get(master_type_id='2')
    print = MasterType.objects.get(master_type_id='3')
    umbrella = MasterType.objects.get(master_type_id='4')
    others = MasterType.objects.get(master_type_id='5')

    return render(request, 'Send/master_category.html', {'user_list': user_list,
                                                         'delivery': delivery,
                                                         'buy': buy,
                                                         'print': print,
                                                         'umbrella': umbrella,
                                                         'others': others,
                                                         'type': master_type_id,
                                                         })


def add_competition(request):
    user_id = request.session.get('user_id')
    if request.method == "POST" and request.FILES['competition_poster']:
        # 如果表单中要传文件、图片，则需要传两个参数
        new_com = models.Competition()
        new_com.competition_sender_id_id = user_id
        new_com.competition_poster = request.FILES.get('competition_poster')
        new_com.competition_title = request.POST.get('competition_title')
        new_com.competition_description = request.POST.get('competition_description')
        new_com.save()
        return fsuccess_response("成功")
    return render(request, 'Send/add_competition.html', {'user_id': user_id})


def suc(request):
    pass
    return render(request, 'Send/suc.html')


