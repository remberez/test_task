from django.db import models
from .utils import translit_to_latin
from django.utils.text import slugify
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения', auto_now_add=True
    )
    slug = models.SlugField(
        unique=True, blank=True
    )

    class Meta:
        abstract =True


class Menu(BaseModel):
    name = models.CharField(
        verbose_name='Название меню', max_length=25,
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ('-updated_at', '-created_at')

    def get_absolute_url(self):
        return reverse('menu:menu_detail', args=[self.slug])

    def __str__(self):
        return f'Меню {self.name}'

    def save(self, *args, **kwargs):
        # Без сторонних библиотек, поэтому своя функция для трансформации кириллицы
        if not self.slug:
            transliterated_title = translit_to_latin(self.name)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)


class MenuItem(BaseModel):
    # Можно было сделать с помощью contenttypes из коробки Django,
    # или просто использовать только одну модель, но такой код
    # становится менее понятен, сложен для расширяемости и менее удобен
    # при работе с ORM.

    parent_item = models.ForeignKey(
        'self', verbose_name='Родительский пункт',
        related_name='child_menu_items', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    menu = models.ForeignKey(
        'Menu', verbose_name='Меню',
        related_name='menu_items', on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название пункта',
        max_length=25,
    )
    content = models.TextField()
    path = models.CharField(
        verbose_name='Путь', max_length=64,
        unique=True, blank=True,
    )

    class Meta:
        verbose_name = 'Пункт'
        verbose_name_plural = 'Пункты'
        ordering = ('-updated_at', '-created_at')

    def get_absolute_url(self):
        return reverse('menu:item_detail', args=[self.path])

    def __str__(self):
        return f'Пункт {self.title}'

    def generate_slug(self):
        transliterated_title = translit_to_latin(self.title)
        return slugify(transliterated_title)

    def generate_path(self):
        parent = self.parent_item
        path = self.slug
        if parent:
            path = '/'.join([parent.path, path])
        else:
            path = '/'.join([self.menu.slug, path])
        return path

    def save(self, *args, **kwargs):
        # Без сторонних библиотек, поэтому своя функция для трансформации кириллицы
        if not self.slug:
            self.slug = self.generate_slug()
        if not self.path:
            self.path = self.generate_path()
        super().save(*args, **kwargs)

    def get_children(self):
        return self.child_menu_items.all()
