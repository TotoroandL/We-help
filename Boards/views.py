
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm, PostForm, ReportForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Login.models import Board, Post, Topic, User
from . import models


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/luntan.html'  # 现在是CBV视图，可以实现分页了 具体要用FBV


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'boards/topics.html', {'board': board, 'topics': topics})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST'and request.FILES.get('img'):
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  #request可以将发布主题的用户设置为当前登录的用户
            topic.img = request.FILES.get('img')
            #topic.img = img
            #user_id = request.session['user_id']
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
                post_img=topic.img
            )

        #if request.FILES.get('img'):
            #img = request.FILES.get('img')
            #topic.img = img
            #topic.save()
        return redirect('new_topic2')
            #return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST'and request.FILES.get('post_img'):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.post_img = request.FILES.get('post_img')
            post.save()
            topic.last_updated = timezone.now() # 最近更新人
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic,'form': form})

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'boards/new_post.html', {'form': form})

@method_decorator(login_required, name='dispatch') #不能用@login_required直接装饰类
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name ='boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name ='post'

    def get_queryset(self):
        queryset = super().get_queryset() #super可以重用父类
        return queryset.filter(created_by=self.request.user) #解决其他用户也可以编辑帖子的问题

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('edit_post2')
        #return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):

        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True  #用session可以不让同一用户的访问统计为多次访问
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def complain(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    template_name = 'boards/complain.html',
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.report_topic = topic
            report.report_created_by = request.user
            report.save()

            return redirect('/luntan/')
    else:
        form = ReportForm()
    return render(request, 'boards/complain.html', locals())

@login_required
def contact_us(request):
    template_name = 'boards/contact_us.html',
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.Contacted_by = request.user
            contact.save()

            return redirect('/luntan/')
    else:
        form = ContactForm()
    return render(request, 'boards/contact_us.html',locals())



def search_subject(request):
    username = request.POST.get('user','')
    search_subject = request.GET.get("subject")
    topic_list=Topic.objects.filter(subject__contains=search_subject)
    return render(request, 'boards/searchresult.html', {"user":username, "topic_list":topic_list})


def edit_post2(request ):
    return render(request,'boards/edit_post2.html')

def new_topic2(request):
    return render(request,'boards/new_topic2.html')

def delete2(request):
    return render(request,'boards/delete2.html')

def complain2(request):
    return render(request,'boards/complain2.html')

def contact_way(request):
    return render(request,'boards/contact_way.html')

def cooperation(request):
    return render(request,'boards/cooperation.html')

def joinus(request):
    return render(request,'boards/joinus.html')

def luntanuser(request,pk,topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request,'boards/luntanuser.html', { 'topic':topic,})

def top(request,pk):
    board = get_object_or_404(Board, pk=pk)
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/top.html'
    topics = board.topics.order_by('-views')[0:5]
    #hotdoc = board.topics.order_by("-views")[0:5]
    return render(request, 'boards/top.html', {'board': board, 'topics': topics})



