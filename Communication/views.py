from django.shortcuts import render,redirect
from Login.models import User,Message,suggestion,Notice,TaskSend
from django.core.paginator import Paginator

def about_platform(request):

    return render(request,'about_platform.html')

def system_message(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username = request.session['username']
    user = User.objects.get(username=username)
    system_message = Notice.objects.filter(message_receiver=username,is_new=0).order_by('-c_time')
    return render(request,'communication/index.html',{
                  'system_message':system_message,
    })

def notice_details(request,message_id):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username = request.session['username']
    user = User.objects.get(username=username)
    system_message = Notice.objects.get(Notice_ID=message_id)
    system_message.is_new = 1
    system_message.save()
    return render(request,'communication/notice_details.html',{
                  'system_message':system_message,
                  'username':username,
                  'user':user,
    })

def message_details(request,message_id):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username = request.session['username']
    user = User.objects.get(username=username)
    message = Message.objects.get(message_id=message_id)
    if message.message_receiver == username:
        message.is_new = 1
        message.save()
    return render(request,'communication/message_details.html',{
                  'message':message,
                  'username':username,
                  'user':user,
    })

def person_message(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    user_id = request.session['user_id']
    message = Message.objects.filter(message_receiver_ID=user_id,is_new=0,is_marked_byreceiver=0).order_by('-c_time')
    p = Paginator(message, 10)   #分页，10篇文章一页
    if p.num_pages <= 1:  #如果文章不足一页
        good_list = message  #直接返回所有文章
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
    return render(request,'communication/person_message.html', context={'good_list': good_list, 'data': data, 'type': type})

def write_message(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username= request.session['username']
    user_id = request.session['user_id']
    user = User.objects.get(username=username)
    if request.method == 'POST':
        message_receiver=request.POST.get('username')
        try:
           message_receiver_obj=User.objects.get(username=message_receiver)
           title=request.POST.get('title')
           message=request.POST.get('message')
           message=Message.objects.create(txtmessage=message,
                               message_sender=user.username,
                               message_receiver=message_receiver,
                               message_receiver_ID=message_receiver_obj.id,
                               message_sender_ID=user_id,
                               title=title,
                               )

           return render(request, 'communication/write_message_success.html', {
            'message':message,
            'username': username,
            'user': user,
            'message_receiver':message_receiver_obj,
        })
        except:
            error_message='没有该用户'
            return render(request,'communication/write_message.html',{
                'error_message':error_message,
            })
    return render(request, 'communication/write_message.html')

def contact_us(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username=request.session['username']
    user=User.objects.get(username=username)
    if request.method == 'POST':
       username=user.username
       title = request.POST.get('title')
       txtsuggestion=request.POST.get('message')
       suggestion.objects.create(suggestion=txtsuggestion,sender=username,title=title)
       return render(request,'Communication/contact_us_success.html',{
              'user':user,
              'username': username,
          })
    return render(request,'Communication/contact_us.html',{
        'user':user,
        'username': username,
    })

def chat(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username = request.session['username']
    return render(request,'communication/chat.html',{
                  'username':username,
    })

def mark_by_receiver(request,message_id):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username = request.session['username']
    user = User.objects.get(username=username)
    message = Message.objects.get(message_id=message_id)
    message.is_marked_byreceiver = 1
    message.save()
    return render(request,'communication/mark_success.html',{
                  'message':message,
                  'username':username,
                  'user':user,
    })

def marked_message(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    user_id=request.session['user_id']
    username = request.session['username']
    user = User.objects.get(username=username)
    messagex = Message.objects.filter(is_marked_byreceiver=1,message_receiver_ID=user_id).order_by('-c_time')
    messagey = Message.objects.filter(is_marked_bysender=1, message_sender_ID=user_id).order_by('-c_time')
    return render(request,'communication/marked_message.html',{
                  'messagex':messagex,
                  'messagey':messagey,
                  'username':username,
                  'user':user,
    })

def message_by_me(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    user_id=request.session['user_id']
    message = Message.objects.filter(message_sender_ID=user_id).order_by('-c_time')
    p = Paginator(message, 10)   #分页，10篇文章一页
    if p.num_pages <= 1:  #如果文章不足一页
        good_list = message  #直接返回所有文章
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
    return render(request,'communication/message_by_me.html', context={'good_list': good_list, 'data': data, 'type': type}
    )

def message_read(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    user_id=request.session['user_id']
    username = request.session['username']
    message = Message.objects.filter(message_receiver_ID=user_id,is_new=1).order_by('-c_time')
    notice = Notice.objects.filter(message_receiver=username,is_new=1).order_by('-c_time')
    return render(request,'communication/message_read.html',{
                  'message':message,
                  'notice':notice,
    })

def search_message(request):
    if not request.session.get('is_login') == True:
        return redirect('/login/')
    username=request.session['username']
    if request.method == 'POST':
        title=request.POST.get('title')
        message=Message.objects.filter(title__contains=title,message_receiver=username)
        notice=Notice.objects.filter(title__contains=title,message_receiver=username)
        return render(request, 'communication/message_read.html', {
            'message': message,
            'notice':notice,
        })
