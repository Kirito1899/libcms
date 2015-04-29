# coding=utf-8

from django.db import models
from participants.models import Library


class Banner(models.Model):
    libraries = models.ManyToManyField(Library, blank=True)
    image = models.ImageField(upload_to=u'participant_banners/%Y/%m/%d')
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    url = models.CharField(max_length=500, verbose_name=u'Ссылка для клика по банеру', blank=True)
    target_blank = models.BooleanField(default=False, verbose_name=u'Открывать ссылку в новой вкладке')
    show_period = models.IntegerField(default=5, help_text=u'Период показа в секундах')
    global_banner = models.BooleanField(
        default=False,
        db_index=True,
        help_text=u'Будет отображен на всех сайтах без исключения'
    )
    owned = models.BooleanField(
        default=True,
        verbose_name=u'Банером может управлять организация',
        help_text=u'Возможность отсутствует, если банер был создан вышестоящим администратором'
    )
    active = models.BooleanField(default=True, db_index=True)
    start_date = models.DateTimeField(verbose_name=u'Дата начала показа', db_index=True)
    end_date = models.DateTimeField(verbose_name=u'Дата окончания показа', db_index=True)

