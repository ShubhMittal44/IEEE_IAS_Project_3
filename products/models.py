from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.utils.text import slugify
import uuid


class ItemsCat(models.Model):
    catName = models.CharField(max_length=20, default="")

    def __str__(self) -> str:
        return self.catName

class ItemMain(models.Model):
    title = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=25)
    description = models.TextField()
    category = models.ForeignKey(ItemsCat, on_delete=models.CASCADE)
    availablity = models.BooleanField(default=False)
    shippingCharges = models.IntegerField(default=0)   
    offers = models.IntegerField(default=0)
    plantingAndCare = models.TextField()
    slug = models.SlugField(max_length=50,unique=True, default="", editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ItemsImages(models.Model):
    title = models.ForeignKey(ItemMain, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'images')

    def __str__(self) -> str:
        return str(self.title)


class ItemsSpecifications(models.Model):
    title = models.ForeignKey(ItemMain, on_delete=models.CASCADE)
    commonName = models.TextField(default="", max_length=50)
    plantSpread = models.TextField(default="", max_length=50)
    maxHeight = models.TextField(default="", max_length=50)
    sunlight = models.TextField(default="", max_length=50)
    watering = models.TextField(default="", max_length=50)
    soil = models.TextField(default="", max_length=50)
    temp = models.TextField(default="", max_length=50)
    ferti = models.TextField(default="", max_length=50)
    bloomTime = models.TextField(default="", max_length=50)

    def __str__(self) -> str:
        return str(self.title)


class ItemFaq(models.Model):
    title = models.ForeignKey(ItemMain, on_delete=models.CASCADE)
    question = models.CharField(max_length=50)
    answer = models.TextField()

    def __str__(self) -> str:
        return str(self.title)


class ItemRating(models.Model):
    title = models.ForeignKey(ItemMain, on_delete=models.CASCADE)
    ratingCount = models.IntegerField()
    rating = models.IntegerField()
    ratingValue = models.DecimalField(decimal_places=2, max_digits=10, editable=False)
    feedback = models.TextField(default="")

    def save(self, *args, **kwargs):
        self.ratingValue = self.rating / self.ratingCount
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)


