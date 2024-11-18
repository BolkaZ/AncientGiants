from django.db import models
from django.contrib.auth.models import User

class Period(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название периода")
    detail_text = models.TextField(verbose_name="Описание периода")
    start = models.CharField(max_length=50, verbose_name="Начало периода")
    end = models.CharField(max_length=50, verbose_name="Окончание периода")
    #found_quantity = models.PositiveIntegerField(verbose_name="Количество найденных окаменелостей")
    image = models.URLField(max_length=500, verbose_name="Изображение периода")
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    animals = models.ManyToManyField("Animal", verbose_name="Животные")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'

class Animal(models.Model):
    #period = models.ForeignKey(Period, related_name='animals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название')
    group = models.CharField(max_length=255, verbose_name='Группа')
    quantity_found = models.IntegerField(verbose_name='Количество найденных окаменелостей особи')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'


class Bid(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
     verbose_name='Пользователь')  # Разрешить null
    period = models.ManyToManyField(Period, verbose_name='Период')
    #animals = models.ManyToManyField(Animal)
    session_id = models.CharField(max_length=255,blank=True, null=True,
     verbose_name='Сессия пользователя')

    STATUS_CHOICES = (
        ('DRAFT', 'Черновик'),
        ('ON_DELETE', 'Удален'),
        ('APPROVED', 'Сформирована'),
        ('FINISHED', 'Завершен'),
        ('REJECTED', 'Отклонён'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name='Статус', default='DRAFT')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Bid for {self.period.name} by {self.user.username if self.user else 'No User'}"


    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'