from django.db import models


class BotUser(models.Model):
    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural = 'Bot Users'

    user_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    first_name = models.CharField(max_length=127, verbose_name='First Name')
    last_name = models.CharField(max_length=127, verbose_name='Last Name', blank=True, null=True)
    username = models.CharField(max_length=64, verbose_name='Username', blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='Join Date')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - @{self.username}'
