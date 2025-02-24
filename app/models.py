from django.db import models
from django.contrib.auth.models import AbstractUser 
 

class CustomUser(AbstractUser): 
    image = models.ImageField(upload_to='avatars', null=True, blank=True) 

class GoldCost(models.Model):
    product_proba = models.IntegerField()
    product_cost = models.IntegerField()

    def __str__(self):
        return str(self.product_proba)
    
    class Meta:
        verbose_name_plural = 'Gold Cost'
        ordering = ['product_proba']

class BailTicket(models.Model):
    number = models.IntegerField()
    data_created = models.DateField()
    data_gone = models.DateTimeField()
    ticket_img = models.ImageField(upload_to='ticket_images', null=True, blank=True)
    ticket_file = models.FileField(upload_to='user_tickets', blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return str(self.number)
    
    class Meta:
        verbose_name = 'BailTicket'
        verbose_name_plural = 'Bail Tickets'
        ordering = ['data_created']

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['data_created']
