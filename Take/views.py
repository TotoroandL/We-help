from django.shortcuts import render, redirect
from Login.models import Collection, User, TaskSend,  GoodType, Good, Competition, TaskTake, CollectionCompetition
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#接单首页
def task_take(request):
    return render(request, 'task_take.html')

#接单的首页。将未被接的任务的前30个任务放到前端展示。
def task_take_division_all(request):
     tasksone = TaskSend.objects.filter(task_state='0').order_by('-task_send_time')[0:50]
     p = Paginator(tasksone, 10)  # 分页，10篇文章一页
     if p.num_pages <= 1:  # 如果文章不足一页
         tasks = tasksone  # 直接返回所有文章
         data = ''  # 不需要分页按钮
     else:
         page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
         tasks = p.page(page)  # 返回指定页码的页面
         left = []  # 当前页左边连续的页码号，初始值为空
         right = []  # 当前页右边连续的页码号，初始值为空
         left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
         right_has_more = False  # 标示最后一页页码前是否需要显示省略号
         first = False  # 标示是否需要显示第 1 页的页码号。
         # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
         # 其它情况下第一页的页码是始终需要显示的。
         # 初始值为 False
         last = False  # 标示是否需要显示最后一页的页码号。
         total_pages = p.num_pages
         page_range = p.page_range
         if page == 1:  # 如果请求第1页
             right = page_range[page:page + 2]  # 获取右边连续号码页
             if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                 # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                 right_has_more = True
             if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                 # 所以需要显示最后一页的页码号，通过 last 来指示
                 last = True
         elif page == total_pages:  # 如果请求最后一页
             left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
             if left[0] > 2:
                 left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
             if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                 first = True
         else:  # 如果请求的页码既不是第一页也不是最后一页
             left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
             right = page_range[page:page + 2]  # 获取右边连续号码页
             if left[0] > 2:
                 left_has_more = True
             if left[0] > 1:
                 first = True
             if right[-1] < total_pages - 1:
                 right_has_more = True
             if right[-1] < total_pages:
                 last = True
         data = {  # 将数据包含在data字典中
             'left': left,
             'right': right,
             'left_has_more': left_has_more,
             'right_has_more': right_has_more,
             'first': first,
             'last': last,
             'total_pages': total_pages,
             'page': page
         }
     return render(request,  'task_take_division_all.html', context={'tasks': tasks, 'data': data})

def task_take_division_hot(request):
    tasksone = TaskSend.objects.filter(task_state='0').order_by('-send_collection_times')[0:50]
    p = Paginator(tasksone, 10)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        tasks = tasksone  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        tasks = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request, 'task_take_division_hot.html', context={'tasks': tasks, 'data': data})

#任务的分类。前端点击链接后，将传回的字符串作为筛选条件。将相应类别的任务及该类别的热门任务返回前端。
def task_take_division(request,task_category):
    taskstwo = TaskSend.objects.filter(task_category=task_category, task_state='0')
    taskone = TaskSend.objects.filter(task_category=task_category, task_state='0').first()
    p = Paginator(taskstwo, 10)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        tasks = taskstwo  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        tasks = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request, 'task_take_division.html',  context={'tasks': tasks, 'data': data, 'taskone': taskone})

#任务的详情。从前端传值，将任务的id传到后端。从数据库筛选出相应的任务并将结果渲染到前端。
def task_take_division_details(request,task_id):
    user_id = request.session.get('user_id')
    task = TaskSend.objects.get(task_id=task_id)
    collection = Collection.objects.filter(collection_thing_id=task_id, collection_collector_id=user_id)
    return render(request, 'task_take_division_details.html', locals())

def task_sender_details(request,sender_id,task_id):
    sender = User.objects.get(pk=sender_id)
    task_id = task_id
    return render(request, 'task_sender_details.html', locals())
#以下三个函数用于实现任务的收藏
#错误信息的返回
def error_response(message):
    data = {}
    data['collection_state'] = 'fail'
    data['message'] = message
    return JsonResponse(data)
#成功信息的返回
def success_response(message):
    data = {}
    data['collection_state'] = 'ok'
    data['message'] = message
    return JsonResponse(data)
def cerror_response(message):
    data = {}
    data['collection_state'] = 'ok-fail'
    data['message'] = message
    return JsonResponse(data)

def task_take_collection(request):
    if not request.session.get('is_login') == True:
        return error_response('未登录!')
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    collection_thing_id = request.GET.get('task_id')
    collection_thing = TaskSend.objects.get(task_id=collection_thing_id)
    is_collection = request.GET.get('is_collection')
    if is_collection == 'true':
        an_collection = Collection.objects.filter(collection_thing_id=collection_thing, collection_collector_id=user)
        if not an_collection:
            Collection.objects.create(collection_thing_id=collection_thing, collection_collector_id=user)
            task = TaskSend.objects.get(task_id=collection_thing_id)
            task.send_collection_times += 1
            task.save()
            return success_response('收藏成功')
        else:
            return error_response('已收藏过')
    else:
        if Collection.objects.filter(collection_thing_id=collection_thing, collection_collector_id=user).exists():
            Collection.objects.filter(collection_thing_id=collection_thing, collection_collector_id=user).delete()
            task = TaskSend.objects.get(task_id=collection_thing_id)
            times = task.send_collection_times
            if times == 0:
                return error_response('数据不存在，不能取消收藏')
            else:
                task.send_collection_times -= 1
                task.save()
            return cerror_response('已取消收藏')
        else:
            return error_response('数据不存在')

#实现接单成功
def task_take_success(request,task_id):
    if not request.session.get('is_login')== True:
        return HttpResponseRedirect('/login/')
    else:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        task = TaskSend.objects.get(task_id=task_id)
        an_collection = TaskTake.objects.filter(task_send_id=task, task_taker_id=user)
        if not an_collection:
            TaskTake.objects.create(task_send_id=task, task_taker_id=user)
            #更新相应类别任务的接单总次数
            if task.task_category == 'delivery':
                user.master_take_delivery_times += 1
                user.save()
            else:
                if task.task_category == 'buy':
                    user.master_take_buy_times += 1
                    user.save()
                else:
                    if task.task_category == 'print':
                        user.master_take_print_times += 1
                        user.save()
                    else:
                        if task.task_category == 'umbrella':
                            user.master_take_umbrella_times += 1
                            user.save()
                        else:
                            user.master_take_others_times += 1
                            user.save()
             #更新接单总次数
            user.task_take_num += 1
            user.save()
             # 接单后，发单表中任务状态变为“已接单”
            task.task_state = 1
            task.save()
            task_take = TaskTake.objects.filter(task_taker_id=user).order_by('-task_take_time').first()
            tasktakes = TaskTake.objects.filter(task_taker_id=user).order_by('-task_take_time')[1:10]
        else:
            return render(request, 'task_take.html')
    return render(request, 'task_take_success.html', locals())

#系统根据用户历史记录来推荐
#定义一个将变量名转换为字符串的函数
#def namestr(namespace,obj):
    #return [name for name in namespace if namespace[name] is obj]

def task_take_recommend(request):
    if not request.session.get('is_login') == True:
        return HttpResponseRedirect('/login/')
    else:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        #根据用户所接的数量最多的任务的类别，给用户推荐这个类别的任务。
        delivery = user.master_take_delivery_times
        buy = user.master_take_buy_times
        print = user.master_take_print_times
        umbrella = user.master_take_umbrella_times
        others = user.master_take_others_times
        #将接每一类别的任务的次数存为一个数组，并进行排序
        a = [delivery, buy, print, umbrella, others]
        for j in range(len(a)-1):
            for i in range(len(a)-1-j):
                if a[i] < a[i+1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
        num = []
        if a[0] == delivery:
            num.append('delivery')
        else:
            if a[0] == buy:
                num.append('buy')
            else:
                if a[0] == print:
                    num.append('print')
                else:
                    if a[0] == umbrella:
                        num.append('umbrella')
                    else:
                        num.append('others')
        num_first = num[0]
        tasks = TaskSend.objects.filter(task_category=num_first, task_state='0').order_by('-task_send_time')
        p = Paginator(tasks, 10)  # 分页，10篇文章一页
        if p.num_pages <= 1:  # 如果文章不足一页
            tasks_list = tasks  # 直接返回所有文章
            data = ''  # 不需要分页按钮
        else:
            page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
            tasks_list = p.page(page)  # 返回指定页码的页面
            left = []  # 当前页左边连续的页码号，初始值为空
            right = []  # 当前页右边连续的页码号，初始值为空
            left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
            right_has_more = False  # 标示最后一页页码前是否需要显示省略号
            first = False  # 标示是否需要显示第 1 页的页码号。
            # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
            # 其它情况下第一页的页码是始终需要显示的。
            # 初始值为 False
            last = False  # 标示是否需要显示最后一页的页码号。
            total_pages = p.num_pages
            page_range = p.page_range
            if page == 1:  # 如果请求第1页
                right = page_range[page:page + 2]  # 获取右边连续号码页
                if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                    # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                    right_has_more = True
                if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                    # 所以需要显示最后一页的页码号，通过 last 来指示
                    last = True
            elif page == total_pages:  # 如果请求最后一页
                left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
                if left[0] > 2:
                    left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                    first = True
            else:  # 如果请求的页码既不是第一页也不是最后一页
                left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
                right = page_range[page:page + 2]  # 获取右边连续号码页
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True
            data = {  # 将数据包含在data字典中
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
                'total_pages': total_pages,
                'page': page
            }
        return render(request, 'task_take_recommend.html', context={'current_page': tasks_list, 'data': data})


#上传商品
def task_take_goods(request):
    if not request.session.get('is_login')==True:
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
       good_category = request.POST.get('good_category', None)
       good_prize = request.POST.get('good_prize', None)
       good_description = request.POST.get('good_description', None)
       good_name = request.POST.get('good_name', None)
       user_id = request.session.get('user_id')
       user = User.objects.get(pk=user_id)
       type = GoodType.objects.get(good_type_name=good_category)
       good_type_id = type.good_type_id
       new_good = Good()
       new_good.good_sender_id = user
       new_good.good_name = good_name
       new_good.good_category_id = good_type_id
       new_good.good_prize = good_prize
       new_good.good_description = good_description
       new_good.save()
       good = new_good
       if request.FILES.get('good_portrait'):
           good_portrait = request.FILES.get('good_portrait')
           good.good_portrait = good_portrait
           good.save()
       return redirect('/Take/task_take_goods_success/')
    return render(request, 'task_take_goods.html', locals())





#上传商品成功
def task_take_goods_success(request):
    if not request.session.get('is_login') == True:
        return HttpResponseRedirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    goodone = Good.objects.filter(good_sender_id=user).order_by('-good_time').first()
    goods = Good.objects.filter(good_sender_id=user).order_by('-good_time')[0:10]
    return render(request, 'task_take_good_success.html', locals())

#删除商品
def task_take_delete(request,good_id):
    if not request.session.get('is_login') == True:
        return error_response('未登录，不能进行关注操作')
    try:
        good = Good.objects.get(good_id=good_id)
        if good:
            Good.objects.get(good_id=good_id).delete()
            goods = Good.objects.all().order_by('-good_time')[0:10]
            return render(request, 'task_take_delete_good.html', { 'goods': goods})
        else:
            redirect('/Take/task_take/')
    except:
        message = '您已经删除了该商品！不能重复删除！'
        goods = Good.objects.all().order_by('-good_time')[0:10]
    return render(request, 'task_take_delete_good.html', {'message':message, 'goods':goods})

#任务说明
def task_take_tips(request):
    return render(request, 'task_take_tips.html')

#大赛
def task_take_competition(request):
    competitionsone = Competition.objects.order_by('-competition_time')[0:50]
    p = Paginator(competitionsone, 10)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        competitions = competitionsone  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        competitions = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request, 'task_take_competition.html', context={'competitions': competitions, 'data': data})

#热门大赛
def task_take_competition_hot(request):
    competitionHotsone = Competition.objects.order_by('-competition_colletion_times')[0:50]
    p = Paginator(competitionHotsone, 10)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        competitionHots = competitionHotsone  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        competitionHots = p.page(page)  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  # 如果请求第1页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  # 如果请求最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {  # 将数据包含在data字典中
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page
        }
    return render(request, 'task_take_competition_hot.html',  context={'competitionHots': competitionHots, 'data': data})

#大赛细节
def task_take_competition_details(request,competition_id):
    if not request.session.get('is_login') == True:
        return HttpResponseRedirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    competition_one = Competition.objects.get(competition_id=competition_id)
    collectioncompetition = CollectionCompetition.objects.filter(collectioncompetition_thing_id=competition_id, collectioncompetition_collector_id=user)
    return render(request, 'task_take_competition_details.html', locals())

#大赛收藏
def task_take_competition_collection(request):
    if not request.session.get('is_login')==True:
        return HttpResponseRedirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    collectioncompetition_thing_id = request.GET.get('competition_id')
    collectioncompetition_thing = Competition.objects.get(competition_id=collectioncompetition_thing_id)
    is_collection = request.GET.get('is_collection')
    if is_collection == 'true':
        an_collection = CollectionCompetition.objects.filter(collectioncompetition_thing_id=collectioncompetition_thing, collectioncompetition_collector_id=user)
        if not an_collection:
            CollectionCompetition.objects.create(collectioncompetition_thing_id=collectioncompetition_thing, collectioncompetition_collector_id=user)
            competition = Competition.objects.get(competition_id=collectioncompetition_thing_id)
            competition.competition_colletion_times += 1
            competition.save()
            return success_response('收藏成功')
        else:
            return error_response('已收藏过')
    else:
        if CollectionCompetition.objects.filter(collectioncompetition_thing_id=collectioncompetition_thing, collectioncompetition_collector_id=user).exists():
            CollectionCompetition.objects.filter(collectioncompetition_thing_id=collectioncompetition_thing, collectioncompetition_collector_id=user).delete()
            competition = Competition.objects.get(competition_id=collectioncompetition_thing_id)
            times = competition.competition_colletion_times
            if times == 0:
                return cerror_response('数据不存在，不能取消点赞')
            else:
                competition = Competition.objects.get(competition_id=collectioncompetition_thing_id)
                competition.competition_colletion_times -= 1
                competition.save()
            return cerror_response('已取消收藏')
        else:
            return error_response('数据不存在')


#成功案例
def task_take_example(request):
    orders = TaskTake.objects.all()
    return render(request, 'task_take_example.html', locals())

def about_us(request):
    return render(request, 'about_us.html')