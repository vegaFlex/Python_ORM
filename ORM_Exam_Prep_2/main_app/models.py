from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Count


class TimeStampedModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(order_count=Count('order')).filter(order_count__gt=2).order_by('-order_count')


class Profile(TimeStampedModel):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(TimeStampedModel):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.profile.full_name}"
