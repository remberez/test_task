from django.views.generic import ListView
from django.views import View
from . import models
from django.shortcuts import render


class MenuView(ListView):
    model = models.Menu
    template_name = 'menu/menu_list.html'
    context_object_name = 'menus'


class MenuDetailView(View):
    model = models.Menu

    def get(self, request, menu_slug):
        menu = self.model.objects.get(
            slug=menu_slug,
        )
        return render(
            request,
            'menu/menu_detail.html',
            {
                'menu': menu,
            }
        )


class ItemDetailView(View):
    model = models.MenuItem

    def get(self, request, item_path):
        item = self.model.objects.filter(path=item_path).first()
        return render(
            request,
            'menu/item_detail.html',
            {
                'item': item,
            }
        )
