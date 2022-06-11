import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages, auth
from django.contrib.auth import login as auth_login, logout, get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from .forms import *


# Create your views here.


def indexHandler(request):
    course = Course.objects.all()
    shi = Shi.objects.all()

    Per = Course.objects.filter(is_main=1)[:1]
    new = Shi.objects.all().order_by('-time')[:6]
    small = Course.objects.all().order_by('-view')[:2]
    Bol = Course.objects.filter(is_main=1).filter(rubric=7)[:1]
    sma = Course.objects.all().order_by('-show_count').filter(rubric=7)[:2]

    return render(request, 'index.html', {
        'course': course,
        'shi': shi,
        'Per': Per,
        'new': new,
        'small': small,
        'Bol': Bol,
        'sma': sma,
    })


def It(request):
    contact_list = Shi.objects.all()
    paginator = Paginator(contact_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'It.html', {
        'page_obj': page_obj,
    })


def Video(request):
    contact_list = Course.objects.all()
    paginator = Paginator(contact_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Video.html', {
        'page_obj': page_obj,
    })


def courseHandler(request, course_int):
    first = 0
    last = 0
    page = 1
    items = Course.objects.all().order_by("-id")[:1]
    if items:
        last = items[0].id
    items = Course.objects.all().order_by("id")[:1]
    if items:
        first = items[0].id

    try:
        item = Course.objects.get(id=course_int)
        item.page = course_int - items[0].id + page
        if item.view <= 1:
            item.rus = 'просмотр'
        elif item.view < 5:
            item.rus = 'просмотра'
        else:
            item.rus = 'просмотров'

    except Course.DoesNotExist:
        item = None
    item.view = item.view + 1
    item.save()

    prev = 0
    next = 0
    if course_int > first:
        prev = course_int - 1
    if course_int < last:
        next = course_int + 1

    return render(request, 'course_item.html', {
        'item': item,
        'prev': prev,
        'next': next
    })


def shiHandler(request, shi_int):
    first = 0
    last = 0

    shis = Shi.objects.all().order_by("-id")[:1]
    if shis:
        last = shis[0].id
    shis = Shi.objects.all().order_by("id")[:1]
    if shis:
        first = shis[0].id

    try:
        stat = Shi.objects.get(id=shi_int)
        stat.view = stat.view + 1
        stat.save()
        stat.page = shi_int - shis[0].id + 1
        if stat.view == 1:
            stat.rus = 'просмотр'
        elif stat.view < 5:
            stat.rus = 'просмотра'
        else:
            stat.rus = 'просмотров'

    except Shi.DoesNotExist:
        stat = None

    prev = 0
    next = 0
    if shi_int > first:
        prev = shi_int - 1
    if shi_int < last:
        next = shi_int + 1

    return render(request, 'shi_stat.html', {
        'stat': stat,
        'prev': prev,
        'next': next,
    })


def vidHandler(request, vid_int):
    try:
        vidik = Course.objects.filter(rubric=vid_int)
    except Course.DoesNotExist:
        vidik: None

    paginator = Paginator(vidik, 2)
    page_number = request.GET.get('page')
    vidik = paginator.get_page(page_number)

    return render(request, 'Video.html', {
        'vidik': vidik,

    })


def Search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        contact_list = Shi.objects.filter(
            Q(title__icontains=search_query) | Q(short_description__icontains=search_query)) or Course.objects.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        contact_list = Course.objects.all()

    return render(request, 'Search.html', {
        'page_obj': contact_list,
    })


class add(CreateView):
    form_class = ShiForm
    template_name = 'Add.html'


class CourseAdd(CreateView):
    form_class = CourseForm
    template_name = 'CourseAdd.html'


def Register(request):
    small = Course.objects.all().order_by('?')[:2]
    shi = Shi.objects.all().order_by('?')[:1]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            pass
        messages.error(request, 'Ошибка! Проверьте правильно ли все заполнено!')
    else:
        form = RegisterForm()

    return render(request, 'Registration.html', {
        'form': form,
        'small': small,
        'shi': shi,
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            pass
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
    })


def user_logout(request):
    logout(request)
    return redirect('home')


def Reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email_template_name = "password/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        fromaddr = "sapar_000000@mail.ru"
                        toaddr = ''
                        mypass = "8dKrSFeqNZnG6rn9N8WF"

                        msg = MIMEMultipart()
                        msg['From'] = fromaddr
                        msg['To'] = toaddr
                        msg['Subject'] = "Сброс пароля"

                        body = email
                        msg.attach(MIMEText(body, 'plain'))

                        server = smtplib.SMTP('smtp.mail.ru', 2525)
                        server.starttls()
                        server.login(fromaddr, mypass)
                        text = msg.as_string()
                        server.sendmail(fromaddr, [user.email], text)
                        server.quit()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request, "password/password_reset.html", {
        "password_reset_form": password_reset_form
    })


def profile(request):
    p_user = ProfileUser()

    return render(request, 'Profile.html', {
        'p_user': p_user
    })


def edit(request):
    if request.method == 'POST':
        form = UserProf(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UserProf(instance=request.user)
    return render(request, 'Edit.html', {
        'form': form,
    })


def adduser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                form.save()
                return redirect('home')
        else:
            pass
        messages.error(request, 'Ошибка! Проверьте правильно ли все заполнено!')
    else:
        form = RegisterForm()

    return render(request, 'AddUser.html', {
        'form': form,
    })


def users(request):
    usera = User.objects.all()
    paginator = Paginator(usera, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Users.html', {
        'page_obj': page_obj,
    })


def userHandler(request, user_int):
    return render(request, 'Users.html', {})


def groups(request, user_int=None):
    action = request.POST.get('action', '')
    if action == 'edit_groups':
        group_id = request.POST.get('group_id')
        usera = User.objects.get(id=user_int)
        usera.groups.add(Group.objects.get(id=group_id))
        usera.save()
    users = User.objects.get(id=user_int)
    groups_list = Group.objects.all()
    return render(request, 'Groups.html', locals())


def change(request, user_int=None):
    action = request.POST.get('action', '')
    if action == 'edit_groups':
        pass
    groups_list = User.objects.get(id=1)

    permissions = set()

    # tmp_superuser = get_user_model()(is_active=True, is_superuser=True)

    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(groups_list))

    sorted_list_of_permissions = sorted(list(permissions))

    a = {
        group.name: [perm.name for perm in group.permissions.all()]
        for group in Group.objects.prefetch_related('permissions')
    }

    print(a)

    return render(request, 'Change.html', locals())
