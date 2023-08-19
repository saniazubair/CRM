from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )

    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True)

    def __str__(self):
        return self.customer.name
