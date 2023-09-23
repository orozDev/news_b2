from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from core.models import News, Category, Tag, Comment


def workspace(request):
    if request.user.is_authenticated:
        news = News.objects.filter(author=request.user).order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 6)
        paginator = Paginator(news, limit)
        news = paginator.get_page(offset)
        return render(request, 'workspace/index.html', {'news_list': news})
    return redirect('/')


def list_of_categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.all().order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 30)
        paginator = Paginator(categories, limit)
        categories = paginator.get_page(offset)
        return render(request, 'workspace/categories.html', {'categories': categories})
    return redirect('/')


def detail_news(request, id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=id, author=request.user)
        comments = Comment.objects.filter(news=news)
        return render(request, 'detail_news.html', {'news': news, 'comments': comments})
    return redirect('/')


def create_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/create_category.html', {'message': 'Name is required'})
            category = Category.objects.create(name=name)
            return redirect('/workspace/categories/')

        return render(request, 'workspace/create_category.html')
    return redirect('/')


def update_category(request, id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=id)
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/update_category.html', {
                    'message': 'Name is required',
                    'category': category,
                })

            category.name = name
            category.save()
            return redirect('/workspace/categories/')

        return render(request, 'workspace/update_category.html', {'category': category})
    return redirect('/')


def delete_category(request, id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=id)
        category.delete()
        return redirect('/workspace/categories/')
    return redirect('/')


def create_news(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            content = request.POST.get('content')
            image = request.FILES.get('image')
            tags = Tag.objects.filter(id__in=list(map(int, request.POST.getlist('tags'))))
            category = Category.objects.get(id=int(request.POST.get('category')))
            is_published = request.POST.get('is_published')
            date = timezone.now()
            author = request.user

            print(is_published, name, image, request.POST.getlist('tags'))

            newsImageSystem = FileSystemStorage('media/news_images/')
            newsImageSystem.save(image.name, image)

            news = News.objects.create(
                name=name,
                description=description,
                content=content,
                category=category,
                date=date,
                author=author,
                image=image,
                is_published=is_published == 'on',
            )

            for tag in tags:
                news.tags.add(tag)

            return redirect('/workspace/')

        tags = Tag.objects.all()
        categories = Category.objects.all()
        return render(request, 'workspace/create_news.html', {
            'tags': tags,
            'categories': categories
        })

    return redirect('/')


def update_news(request, id):
    news = get_object_or_404(News, id=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            news.name = request.POST.get('name')
            news.description = request.POST.get('description')
            news.content = request.POST.get('content')
            news.category = Category.objects.get(id=int(request.POST.get('category')))
            news.is_published = request.POST.get('is_published') == 'on'

            image = request.FILES.get('image')
            tags = Tag.objects.filter(id__in=list(map(int, request.POST.getlist('tags'))))

            for tag in news.tags.all():
                news.tags.remove(tag)

            for tag in tags:
                news.tags.add(tag)

            if image:
                newsImageSystem = FileSystemStorage('media/news_images/')
                newsImageSystem.delete(news.image)
                newsImageSystem.save(image.name, image)
                news.image = image

            news.save()
            return redirect(f'/workspace/news/{news.id}/')

        tags = Tag.objects.all()
        categories = Category.objects.all()
        return render(request, 'workspace/update_news.html', {
            'news': news,
            'tags': tags,
            'categories': categories
        })

    return redirect('/')

# Create your views here.
