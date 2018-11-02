from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
import datetime

from . import models
from . import forms
from django.conf import settings
# Create your views here.

def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确!"
            except:
                message = "用户不存在!"
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则!
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容!"
        if register_form.is_valid():   # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user: # 用户名唯一
                    message = '用户已经存在，请重新选择用户名!'
                    return render(request,'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:   # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱!'
                    return render(request, 'login/register.html', locals())

                # 当一切OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)   # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                
                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往注册邮箱，进行确认!'
                return render(request, 'login/confirm.html', locals())  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就没登录，就没有登出一说
        return redirect('/index/')
    request.session.flush()         # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
    

def hash_code(s, salt='mysites'):   # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())   # update方法只接收bytes类型
    return h.hexdigest()
    

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email(email,  code):
    from django.core.mail import EmailMultiAlternatives
    subject = '你好，王善文'
    text_content = '''你好，王善文！'''
    html_content = '''Hello,
    欢迎注册Wrangler.com.cn学习网. http://192.168.30.188:9988/register/ '''.format(code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求"
        return render(request, 'login/confirm.html', locals())


    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期，请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录'
        return render(request, 'login/confirm.html', locals())
