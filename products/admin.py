from django.contrib import admin
from .models import ItemMain, ItemsImages, ItemsSpecifications, ItemFaq, ItemRating, ItemsCat

# Register your models here.

admin.site.register(ItemMain)
admin.site.register(ItemsImages)
admin.site.register(ItemsSpecifications)
admin.site.register(ItemFaq)
admin.site.register(ItemRating)
admin.site.register(ItemsCat)

