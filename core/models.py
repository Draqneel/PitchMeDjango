from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    title = models.CharField(max_length=256, blank=True, verbose_name='Название')
    dt_start = models.DateTimeField(null=False, blank=True, verbose_name='Время начала')
    dt_end = models.DateTimeField(null=False, blank=True, verbose_name='Время окончания')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    themes = models.ManyToManyField('Theme')

    def __str__(self):
        return f'{self.title}'


class City(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Имя')

    def __str__(self):
        return f'{self.name}'


class Theme(models.Model):
    title = models.CharField(max_length=256, blank=True, verbose_name='Название темы')

    def __str__(self):
        return f'{self.title}'


class UserFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    dt_start = models.DateTimeField(blank=True, verbose_name='Время с')
    dt_end = models.DateTimeField(blank=True, verbose_name='Время до')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    themes = models.ManyToManyField('Theme')

    def __str__(self):
        return f'Фильтр для {self.user.username} [{self.pk}]'


class Notification(models.Model):
    to_user = models.ForeignKey(User, related_name='notifications',
                                on_delete=models.CASCADE, verbose_name='Сообщение для')
    is_read = models.BooleanField(default=False)
    filter = models.ForeignKey(UserFilter, on_delete=models.CASCADE, verbose_name='Фильтр')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


@receiver(post_save, sender=Event, dispatch_uid="send_notifications")
def send_notifications(sender, instance, **kwargs):
    filters = UserFilter.objects.filter(
        Q(city__pk=instance.city.pk) &
        Q(dt_start__lte=instance.dt_start) &
        Q(dt_end__gte=instance.dt_start)
        # & Q(themes__in=instance.themes.all())
    ).distinct()
    notified = set()
    for f in filters:
        if f.user not in notified:
            notification = Notification.objects.create(
                to_user=f.user,
                filter=f,
                event=instance,
            )
            notification.save()
            notified.add(f.user)
