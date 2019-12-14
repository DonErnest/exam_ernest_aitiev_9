from django.contrib.auth.models import User
from django.db import models

class Photo(models.Model):
    photo = models.ImageField(null=False, blank=False, upload_to='photos', verbose_name='Фотография')
    description = models.CharField(max_length=150, null=False, blank=False, verbose_name='Подпись')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE, blank=False,verbose_name='Автор')

    def __str__(self):
        return "Фото {} пользователя {}".format(self.description[:10], self.author.username)

class Comment(models.Model):
    text = models.TextField(max_length=300, null=False, blank=False, verbose_name='Комментарий')
    photo = models.ForeignKey('webapp.Photo', null=False, related_name='comments', on_delete=models.CASCADE, blank=False, verbose_name='Фотография')
    author = models.ForeignKey(User, null=False,blank=False, related_name='comments', on_delete=models.CASCADE, verbose_name='Автор комментария')
    added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    def __str__(self):
        return "Комментарий пользователя {} о фотографии {}".format(self.author.username, self.photo.description[:10])

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes_added', on_delete=models.CASCADE, verbose_name='Автор лайка')
    photo = models.ForeignKey('webapp.Photo', related_name='likes_received', null=False, blank=False, on_delete=models.CASCADE, verbose_name='Понравившаяся фотография')