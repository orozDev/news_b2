from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden

from core.models import News, Category, Tag, Comment


def workspace(request):
    if request.user.is_authenticated:
        news = News.objects.filter(author=request.user).order_by('-id')
        search = request.GET.get('search1', None)
        message = None
        if search:
            news = News.objects.filter(name__icontains=search).order_by('name')
            message = f'found news by title {search}'
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 6)
        paginator = Paginator(news, limit)
        news = paginator.get_page(offset)
        categories = Category.objects.all().order_by('name')
        tags = Tag.objects.all().order_by('name')
        return render(request, 'workspace/index.html', {'news_list': news, 'categories': categories, 'tags': tags, 'message': message,})
    return redirect('/')


def filter_news_by_cat(request, id):
    category = get_object_or_404(Category, id=id)
    categories = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    if category:
        news = News.objects.filter(category=category).order_by('-id')
        return render(request, 'workspace/index.html', {'news_list': news, 'categories': categories, 'tags': tags})
    return redirect('/')


def filter_news_by_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    categories = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    if tag:
        news = News.objects.filter(tags__id=tag.id).order_by('-id')
        return render(request, 'workspace/index.html', {'news_list': news, 'categories': categories, 'tags': tags})
    return redirect('/')
    
    


def list_of_categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.all().order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 5)
        paginator = Paginator(categories, limit)
        categories = paginator.get_page(offset)
        return render(request, 'workspace/categories.html', {'categories': categories})
    return redirect('/')


def detail_news(request, id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=id, author=request.user)
        comments = Comment.objects.filter(news=news)
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(comments, limit)
        comments = paginator.get_page(offset)
        return render(request, 'workspace/detail_news.html', {'news': news, 'comments': comments})
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
                newsImageSystem.delete(news.image.name)
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

def list_of_tags(request):
    if request.user.is_authenticated:
        tags = Tag.objects.all().order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 20)
        paginator = Paginator(tags, limit)
        tags = paginator.get_page(offset)
        return render(request, 'workspace/tags.html', {'tags': tags})
    return redirect('/')


def create_tag(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/create_tag.html', {'message': 'Name is required'})
            tag = Tag.objects.create(name=name)
            return redirect('/workspace/tags/')

        return render(request, 'workspace/create_tag.html')
    return redirect('/')


def update_tag(request, id):
    if request.user.is_authenticated:
        tag = get_object_or_404(Tag, id=id)
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/update_tag.html', {
                    'message': 'Name is required',
                    'tag': tag,
                })

            tag.name = name
            tag.save()
            return redirect('/workspace/tags/')

        return render(request, 'workspace/update_tag.html', {'tag': tag})
    return redirect('/')


def delete_tag(request, id):
    if request.user.is_authenticated:
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return redirect('/workspace/tags/')
    return redirect('/')


def delete_news(request, id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=id)
        news.delete()
        return redirect('/workspace/')
    return redirect('/')


def delete_comment(request, id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return JsonResponse({'isDeleted': True})
    return HttpResponseForbidden()

