from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from core.models import News, Category, Comment


def main(request):
    search = request.GET.get('search', None)
    if search:
        news = News.objects.filter(name__icontains=search, is_published=True).order_by('-id')
    else:
        news = News.objects.filter(is_published=True).order_by('-id')
    tag = request.GET.get('tag', None)
    if tag:
        news = news.filter(tags__id=tag).order_by('-id')

    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 12)

    paginator = Paginator(news, limit)
    news = paginator.get_page(offset)

    return render(request, 'index.html', {'news_list': news})


def detail_news(request, id):
    news = get_object_or_404(News, id=id, is_published=True)
    comments = Comment.objects.filter(news=news)
    return render(request, 'detail_news.html', {'news': news, 'comments': comments})


def about(request):
    return render(request, 'about.html')


def news_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    news = News.objects.filter(category=category).order_by('-id')
    return render(request, 'index.html', {'news_list': news})


def create_comment_ajax(request):
    news_id = int(request.POST.get('news'))
    name = request.POST.get('name')
    text = request.POST.get('text')
    news = get_object_or_404(News, id=news_id)

    new_comment = Comment.objects.create(
        news=news,
        name=text,
        text=text,
    )
    return JsonResponse({
        'news': new_comment.news.id,
        'name': new_comment.name,
        'text': new_comment.text,
        'date': new_comment.date.strftime('%d %B %Y')
    })


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return render(request, 'auth/login.html', {'message': 'Enter required fields'})
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'auth/login.html', {'message': 'The user is not found or invalid password'})
    return render(request, 'auth/login.html')


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'auth/profile.html')
    return redirect('/')


def change_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            userChecking = User.objects.filter(username=username)

            if userChecking.exists() and request.user.username != username:
                return render(request, 'auth/change_profile.html', {
                    'message': f'User with this username {username} is already exists'})

            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            return redirect('/profile/')

        return render(request, 'auth/change_profile.html')
    return redirect('/')


def change_password(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = request.user

            if not user.check_password(password):
                return render(request, 'auth/change_password.html', {'message': 'Please enter valid password'})
            if new_password != confirm_password:
                return render(request, 'auth/change_password.html', {'message': 'The passwords don\'t match'})
            if len(new_password) < 8:
                return render(request, 'auth/change_password.html', {
                    'message': 'You password must contain more than 8 charchers'})

            user.set_password(new_password)
            user.save()
            login(request, user)
            return redirect('/profile/')

        return render(request, 'auth/change_password.html')
    return redirect('/')


# Create your views here.
