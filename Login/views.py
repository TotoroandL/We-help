

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MasterType, GoodFavorite
from .models import TaskSend, TaskTake, User,Notice
from .forms import RegisterForm, LoginForm, ResetPWForm, TagForm,ResetPWForm, ModifyPwdForm, ForgetForm
from .models import Collection,CollectionCompetition
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import EmailVerifyRecord
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email


User = get_user_model()


class RegisterView(View):
    """
    注册视图
    """
    def get(self, request):
        logout(request)
        return render(request, 'accounts/register.html')

    def post(self, request):
        logout(request)
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User(**form.cleaned_data)
            # hash密码
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            username=new_user.username
            Notice.objects.create(title='欢迎使用WeHelp!',
                                  message_fromsystem='欢迎使用WeHelp!',
                                  message_receiver= username
                                  )
            login(request, new_user)
            return redirect('/login/')

        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """
    登录视图
    """
    def get(self, request):
        logout(request)
        return render(request, 'accounts/login.html')

    def post(self, request):
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            # 验证密码
            if user.check_password(password):
                login(request, user)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                user.is_login = 1
                user.save()
                return redirect('/')
        error_message='请输入正确的用户名和密码'
        return render(request, 'accounts/login.html', {'error_message':error_message,})


@login_required(login_url='/login/')
def logout_view(request):
    """
    注销登录视图
    """
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    user.is_login = 0
    user.save()
    logout(request)
    return redirect('/')


def success_response(message):
    data = {}
    data['status'] = 'SUCCESS'
    data['message'] = message
    return JsonResponse(data)


@login_required(login_url='/login/')
def index(request):
    """
    主页视图
    """
    user = request.user
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.college = request.POST.get('college')
        user.major = request.POST.get('major')
        user.birthday = request.POST.get('birthday')
        user.email = request.POST.get('email')
        user.qq_num = request.POST.get('qq_num')
        user.save()

    return render(request, 'accounts/index.html', {'user': request.user})


@login_required(login_url='/login/')
def reset_pw(request):
    """
    修改密码视图
    """
    form = ResetPWForm(request.POST)
    if form.is_valid():
        user = User.objects.filter(id=request.user.id).first()
        if user and user.check_password(form.cleaned_data['password1']):
            user.set_password(form.cleaned_data['password2'])
            user.save()
            return render(request, 'accounts/reset_pw.html', {'message': '修改密码成功!'})

    return render(request, 'accounts/reset_pw.html')


@login_required(login_url='/login/')
def get_orders(request):
    """
    已发订单视图
    """
    user_id = request.session['user_id']
    orders = TaskSend.objects.all().filter(sender__id=user_id)
    p = Paginator(orders, 14)  # 分页，10篇文章一页
    if p.num_pages <= 1:  # 如果文章不足一页
        order_list = orders  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
        order_list = p.page(page)  # 返回指定页码的页面
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
    return render(request, 'accounts/send.html', context={'orders': order_list, 'data': data})


@login_required(login_url='/login/')
def get_tasks(request):
    """
    已接订单视图
    """
    user_id = request.session['user_id']
    tasks = TaskTake.objects.all().filter(task_taker_id__id=user_id)
    return render(request, 'accounts/task.html', {'tasks': tasks})


@login_required(login_url='/login/')
def tags(request):
    """
    标签视图
    """
    tags = MasterType.objects.all().order_by('master_type_name')
    return render(request, 'accounts/tags.html', {'tags': tags})


@login_required(login_url='/login/')
def new_tags(request):
    """
    添加标签视图
    """
    if request.method == "POST":
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        master_type_id = request.POST.get('master_type_id')
        user.master_type_id = master_type_id
        user.save()
        type = user.master_type
        return render(request, 'accounts/new_tags.html', {'type': type})
    return render(request, 'accounts/new_tags.html')


@login_required(login_url='/login/')
def new_avatar(request):
    """
    用户头像
    """
    if request.method == 'POST' and request.FILES['avatar']:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('/index')
    return redirect('/index')



@login_required(login_url='/login/')
def get_collection(request):
    """
    我的收藏视图
    """
    user_id = request.session['user_id']
    collection = Collection.objects.all().filter(collection_collector_id__id=user_id)
    return render(request, 'accounts/collection.html', {'collections': collection})


@login_required(login_url='/login/')
def good_favorite(request):
    """
    我的收藏商品视图
    """
    user_id = request.session['user_id']
    goodfavorite = GoodFavorite.objects.all().filter(user__id=user_id)
    return render(request, 'accounts/goodfavorite.html', {'goodfavorite': goodfavorite})


def wehelp(request):
    pass
    return render(request, 'wehelp.html')


def about_platform(request):
    pass
    return render(request, 'about_platform.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'login/forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码的邮件
            send_register_email(email, 'forget')
            return render(request, 'login/send_success.html')
        else:
            return render(request, "login/forgetpwd.html", {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        # 用于查询邮箱验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的用户
                return render(request, "login/password_reset.html", {"email": email})   # 告诉页面是哪个用户在重置密码
        else:
            return render(request, "login/active_fail.html")
        # 激活成功跳转到登录页面
        return render(request, "accounts/login.html")

    # 用于实现用户修改密码的函数
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            # 如果前后两次密码不相等，那么回填信息并返回错误提示
            if pwd1 != pwd2:
                return render(request, "login/password_reset.html", {"email": email, "msg": "对不起，前后密码不一致"})
            # 如果前后两次密码相等，那么进入我们的密码修改保存
            # 取出用户信息
            user = User.objects.get(email=email)
            # 随意取出一个密码并将其进行加密
            user.password = make_password(pwd1)
            # 将更新后的用户信息保存到数据库里面
            user.save()
            # 密码重置成功以后，跳转到登录页面
            return render(request, "accounts/login.html", {"msg": "恭喜您，您的密码修改成功，请登录"})
        else:
            email = request.POST.get("email", '')
            return render(request, "login/password_reset.html", {"email": email, "modify_form": modify_form})


@login_required(login_url='/login/')
def collection_c(request):
    """
    我的收藏比赛视图
    """
    user_id = request.session['user_id']
    collection_c = CollectionCompetition.objects.all().filter(collectioncompetition_collector_id__id=user_id)
    return render(request, 'accounts/collection_c.html', locals())


def disclaimer(request):
    """
    免责声明视图
    """
    return render(request, 'disclamier.html',)


def map(request):
    """
    地图视图
    """
    return render(request, 'accounts/map.html', {'map': map})

def bar(request):
    """
    柱状图视图
    """
    return render(request, 'accounts/bar.html')

def doughnut(request):
    """
    圈饼图视图
    """
    return render(request, 'accounts/doughnut.html')

def line(request):
    """
    折线图视图
    """
    return render(request, 'accounts/line.html')

def linecus(request):
    """
    自定义提示折线图视图
    """
    return render(request, 'accounts/line-customTooltips.html')

def pie(request):
    """
    饼图视图
    """
    return render(request, 'accounts/pie.html')

def piecus(request):
    """
    自定义提示饼图视图
    """
    return render(request, 'accounts/pie-customTooltips.html')

def polar(request):
    """
    极面图视图
    """
    return render(request, 'accounts/polar-area.html')

def radar(request):
    """
    雷达区域图视图
    """
    return render(request, 'accounts/radar.html')