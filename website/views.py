# coding=utf-8
from itertools import chain
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from website.form import RegisterForm, LoginForm, EditInfoForm, QuestionForm, AnswerForm, CommentForm
from website.models import UserInfo, Question, Answer, Comment, Event, Follow
import datetime


def navbar(request):
    """''return navbar user name''"""
    template_var = dict()
    if request.user.is_authenticated():
        template_var["user_name"] = _(u"%s") % request.user.first_name
        template_var["user_avatar"] = UserInfo.objects.get(account=request.user).avatar
    else:
        HttpResponseRedirect(reverse('login'))
    return template_var


def index(request):
    """首页视图"""
    template_var = dict()
    follow = Follow.objects.filter(follower=request.user).values('follow_by')
    event = Event.objects.filter(account__in=follow).order_by('-time')
    template_var['eventlist'] = event
    return render_to_response("index.html", template_var,
                              context_instance=RequestContext(request))


def user_home(request):
    template_var = dict()
    if request.user.is_authenticated():
        try:
            userinfo = UserInfo.objects.get(account=request.user)
            event = Event.objects.filter(account=request.user).order_by('-time')
            # template_var.update(user_var(user))
            template_var['userinfo'] = userinfo
            template_var['eventlist'] = event
        except UserInfo.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
            # user = User.objects.get(id=userid)
    return render_to_response('user_home.html', template_var,
                              context_instance=RequestContext(request))


def user_home_(request, user_id):
    template_var = dict()
    try:
        user = User.objects.get(id=user_id)
        otheruserinfo = UserInfo.objects.get(account=User.objects.get(id=user_id))
        event = Event.objects.filter(account=user).order_by('-time')
        template_var['eventlist'] = event
        template_var['userinfo'] = otheruserinfo
    except UserInfo.DoesNotExist or User.DoesNotExist:
        return HttpResponseRedirect(reverse('login'))
        # user = User.objects.get(id=userid)
    template_var['other'] = True
    template_var['is_followed'] = False
    try:
        follow = Follow.objects.filter(follower=request.user).get(follow_by=user)
        template_var['is_followed'] = True
    except Follow.DoesNotExist:
        template_var['is_followed'] = False
    except Follow.MultipleObjectsReturned:
        template_var['is_followed'] = True
    if request.method == 'POST':
        if request.POST['btn'] == 'cancel_follow':
            Follow.objects.filter(follower=request.user, follow_by=user).delete()
        else:
            ff = Follow.objects.create(follower=request.user, follow_by=user)
            ff.save()
        return HttpResponseRedirect(reverse(user_home_, args=user_id))
    return render_to_response('user_home.html', template_var,
                              context_instance=RequestContext(request))


def user_detail_info(request):
    template_var = dict()
    if request.user.is_authenticated():
        try:
            userinfo = UserInfo.objects.get(account=request.user)
            template_var['userinfo'] = userinfo
        except UserInfo.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
    return render_to_response('user_info_detail.html', template_var,
                              context_instance=RequestContext(request))


def user_detail_other(request, user_id):
    template_var = dict()
    try:
        otheruserinfo = UserInfo.objects.get(account=User.objects.get(id=user_id))
        template_var['userinfo'] = otheruserinfo
        template_var['other'] = True
    except UserInfo.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    return render_to_response('user_info_detail.html', template_var,
                              context_instance=RequestContext(request))


# todo upload image wrong
def user_info_edit(request):
    template_var = dict()
    form = EditInfoForm()
    if request.user.is_authenticated():
        try:
            user = UserInfo.objects.get(account=request.user)
        except UserInfo.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        form = EditInfoForm(initial={'city': user.city, 'introduce': user.introduce,
                                     'industry': user.industry, 'phone_number': user.phone_number,
                                     'short_introduce': user.short_introduce}, )
        if request.method == 'POST':
            form = EditInfoForm(request.POST, request.FILES)
            # user.avatar = request.FILES['avatar']
            # newpic = EditInfoForm(avatar=request.FILES['avatar'])
            # newpic.save()
            user.city = request.POST['city']
            user.industry = request.POST['industry']
            user.short_introduce = request.POST['short_introduce']
            user.introduce = request.POST['introduce']
            user.phone_number = request.POST['phone_number']
            user.sex = request.POST['sex']
            user.save()
            return HttpResponseRedirect(reverse('userdetail'))
    template_var['form'] = form
    template_var['user'] = user
    return render_to_response('user_info_edit.html', template_var,
                              context_instance=RequestContext(request))


# todo upload content should have a base format like \n or \t
def ask_question(request):
    template_var = dict()
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST.copy())
        title = request.POST['title']
        content = request.POST['content']
        topic = request.POST['topic']
        account = request.user
        question = Question.objects.create(title=title, content=content, account=account, topic=topic)
        question.save()
        event = Event.objects.create(account=account, question=question)
        event.save()
        userinfo = UserInfo.objects.get(account=account)
        userinfo.question_number += 1
        userinfo.save()
        return HttpResponseRedirect(reverse('question', args=[question.id]))
    template_var['form'] = form
    return render_to_response('ask_question.html', template_var, context_instance=RequestContext(request))


def question(request, qid):
    template_var = dict()
    form = AnswerForm()
    thequestion = Question.objects.get(id=qid)
    theanswer = Answer.objects.filter(question=thequestion)
    template_var['title'] = thequestion.title
    template_var['content'] = thequestion.content
    template_var['topic'] = thequestion.topic
    template_var['answer'] = theanswer
    template_var['form'] = form
    if request.method == 'POST':
        content = request.POST['content']
        account = request.user
        answer = Answer.objects.create(author=account, content=content, question=thequestion)
        answer.save()
        event = Event.objects.create(account=request.user, answer=answer)
        event.save()
    return render_to_response('question.html', template_var, context_instance=RequestContext(request))


def comment(request, answer):
    template_var = dict()
    form = CommentForm()
    template_var['form'] = form
    ans = Answer.objects.get(id=answer)
    template_var['answer'] = ans
    template_var['comment'] = Comment.objects.filter(answer=answer)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment.objects.create(author=request.user, content=content, answer=ans)
        comment.save()
    return render_to_response('comment.html', template_var, context_instance=RequestContext(request))


def topic_detail(request, tp_name):
    template_var = dict()
    template_var['question'] = Question.objects.filter(topic=tp_name)
    template_var['tp_name'] = tp_name
    return render_to_response('topic_detail.html', template_var, context_instance=RequestContext(request))


def topic_list(request):
    template_var = dict()
    template_var['questionset'] = Question.objects.values_list('topic', flat=True).distinct()
    return render_to_response('topic_list.html', template_var, context_instance=RequestContext(request))


def register(request):
    """注册视图"""
    template_var = {}
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST.copy())
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email, email, password, first_name=username)
            userinfo = UserInfo.objects.create(
                account=user,
                register_time=datetime.datetime.now(),
                like_number=0,
                question_number=0,
                mark_number=0,
                phone_number=0,
                avatar='image/defimage.jpg'
            )
            userinfo.save()
            user.save()
            _login(request, email, password)  # 注册完毕 直接登陆
            return HttpResponseRedirect(reverse("index"))
    template_var["form"] = form
    return render_to_response("register.html", template_var, context_instance=RequestContext(request))


def _login(request, username, password):
    """登陆核心方法"""
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth_login(request, user)
            request.session['user'] = username
            ret = True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户不存在'))
    return ret


def login(request):
    template_var = {}
    form = LoginForm()
    template_var['user'] = request.user
    if request.method == "POST":
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            _login(request, email, password)
            return HttpResponseRedirect(reverse("index"))
    template_var["form"] = form
    return render_to_response("login.html", template_var, context_instance=RequestContext(request))


def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        return view(request, *args, **kwargs)

    return new_view


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


def temp(request):
    return render_to_response('temp.html')


def articles(request, year):
    return HttpResponse(year)