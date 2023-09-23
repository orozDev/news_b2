from django.db import models


class Category(models.Model):
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    name = models.CharField(max_length=250, verbose_name='название', unique=True)
    
    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField(max_length=255, verbose_name='название')

    def __str__(self):
        return f'{self.name}'


class News(models.Model):
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    name = models.CharField(max_length=100, verbose_name='название')
    image = models.ImageField(upload_to='news_images/', verbose_name='обложка')
    description = models.CharField(max_length=250, verbose_name='Краткое описание')
    content = models.TextField(verbose_name='контент')
    category = models.ForeignKey(
        Category, verbose_name='категория', on_delete=models.CASCADE, related_name='news')
    tags = models.ManyToManyField(Tag, verbose_name='теги', related_name='news')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')
    is_published = models.BooleanField(default=True, verbose_name='публичность')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='автор', null=True)
    
    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Comment(models.Model):

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарий'

    name = models.CharField(max_length=100, verbose_name='Имя и фамилия')
    text = models.TextField(verbose_name='текст')
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             verbose_name='новость', related_name='comments')
    date = models.DateField(verbose_name='дата добавление', auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.news.name}'

# Create your models here.
