from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=300)
    slug = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=300)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media/slider')
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media/advertisement')
    rank = models.IntegerField()
    url = models.URLField(max_length=1000)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media/brand')
    rank = models.IntegerField()
    slug = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/customer')
    post = models.CharField(max_length=300)
    star = models.IntegerField(default=5)
    comment = models.TextField()
    def __str__(self):
        return self.name
LABELS = (('new','new'),('hot','hot'),('sale','sale'))
STOCK = (('In stock','In stock'),('Out of Stock','Out of Stock'))
class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    discounted_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    slug = models.TextField(unique=True)
    image = models.ImageField(upload_to='media/product')
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)
    labels = models.CharField(choices=LABELS,max_length=50)
    stock = models.CharField(choices=STOCK,max_length=50)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    subject = models.TextField()
    message = models.TextField()
    def __str__(self):
        return self.name

class ProductReview(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=300)
    review = models.CharField(max_length=100)
    slug = models.TextField()
    star = models.IntegerField(default=5)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    username = models.CharField(max_length=300)
    slug = models.TextField()
    quantity = models.IntegerField(default=1)
    items = models.ForeignKey(Product,on_delete=models. CASCADE)
    total = models.FloatField()
    checkout = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    
