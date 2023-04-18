from django.db import models


class User(models.Model):
    User_ID = models.AutoField(primary_key=True)
    User_FName = models.CharField(default="-", max_length=255)
    User_MName = models.CharField(default="-", max_length=255)
    User_LName = models.CharField(default="-", max_length=255)
    User_Login = models.CharField(unique=True, null=False, max_length=255)
    User_Password = models.CharField(null=False, max_length=255)
    Wallet = models.FloatField(default=0.0)


class Category(models.Model):
    PAYMENT_TYPES = [
        ('in', 'доход'),
        ('out', 'расход')
    ]
    Category_ID = models.AutoField(primary_key=True)
    Category_Name = models.CharField(null=False, max_length=255)
    Payment_Type = models.CharField(null=False, choices=PAYMENT_TYPES, max_length=255)

    class Meta:
        verbose_name_plural = "categories"


class Payment(models.Model):
    METHOD_TYPES = [
        ('RUB', 'руб'),
        ('EUR', 'евро'),
        ('USD', 'доллар')
    ]
    Payment_ID = models.AutoField(primary_key=True)
    Payment_Time = models.DateTimeField(auto_now_add=True)
    Amount = models.FloatField(null=False)
    Method = models.CharField(null=False, choices=METHOD_TYPES, max_length=255)
    Comment = models.TextField(default="-")
    Owner = models.ForeignKey('User', on_delete=models.PROTECT)
    Category = models.ForeignKey('Category', on_delete=models.PROTECT)
