from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    CATEGORY_CHOICES = (('tanks', 'Танки'),
                ('healers', 'Хилы'),
                ('damage_dealers', 'ДД'),
                ('dealers', 'Торговцы'),
                ('gildmasters', 'Гилдмастеры'),
                ('quest_givers', 'Квестгиверы'),
                ('blacksmiths', 'Кузнецы'),
                ('tanners', 'Кожевники'),
                ('potion_makers', 'Зельевары'),
                ('spell_masters', 'Мастера заклинаний'))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    date = models.DateTimeField(auto_now_add=True)
    text = RichTextUploadingField(verbose_name='Контент')


class Response(models.Model):
    STATUSES = [
        ('C', 'Создан'),
        ('A', 'Принят'),
        ('D', 'Отклонен'),
    ]
    text = models.TextField('Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='C')