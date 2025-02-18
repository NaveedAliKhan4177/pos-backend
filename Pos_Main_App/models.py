from django.db import models
from django.utils import timezone
from datetime import datetime, time

# Create your models here.




#this model is for storing the making process of dish


class Dishes_model(models.Model):

    Dishes_Food_Type=[
        ('Chicken','Chicken'),
        ('Mutton','Mutton'),
        ('Veg','Veg'),
    ]

    Dishes_Type=[
        ('Main Course','Main Course'),
        ('Starter','Starter'),
        ('Sweet','Sweet'),
        ('Cold Drink','Cold Drink'),
        ('Roti','Roti')
    
    ]


    Dishes_Quantity=[
        ('Full','Full'),
        ('Half','Half')
    ]


    Dish_Image= models.ImageField(upload_to='Dish_Images/')
    Dish_Name=models.CharField(max_length=100)
    Dish_Quantity= models.CharField(max_length=4,default='Full',  choices=Dishes_Quantity)
    Dish_Price= models.PositiveIntegerField()
    Dish_Food_Type= models.CharField(max_length=7, choices=Dishes_Food_Type)
    Dish_Type= models.CharField(max_length=11, choices=Dishes_Type)
    Dish_Information= models.CharField(max_length=100000)




    def __str__ (self):
        return self.Dish_Name
    


class Table_model(models.Model):
    Table_Number = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.Table_Number}"  #  Convert integer to string




class Employe_model(models.Model):

    Employes_Position=[
        ('waiter','waiter'),
        ('cook','cook'),
        ('Other','Other')
    ]
    Employe_Name= models.CharField(max_length=100, blank=False,null=False)
    Employe_Number= models.CharField(max_length=10, unique=True, null=False, blank=False)
    Employe_Address= models.CharField(max_length=1000, null=False, blank=False)
    Employe_Position= models.CharField(max_length=6, null=False, blank=False, choices=Employes_Position)



    def __str__(self):
        return self.Employe_Name



class OrderedDish_model(models.Model):
    bill = models.ForeignKey('Bill_model', on_delete=models.CASCADE, related_name='ordered_dishes')
    dish = models.ForeignKey('Dishes_model', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dish.Dish_Name} x {self.quantity} (Bill {self.bill.bill_number})"





class Bill_model(models.Model):
    bill_number = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('Employe_model', on_delete=models.SET_NULL, null=True, blank=False, related_name='bills_served')
    table = models.ForeignKey('Table_model', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    dishes = models.ManyToManyField('Dishes_model', through='OrderedDish_model', related_name='bills')


    def __str__(self):
        return f"Bill {self.bill_number} - {self.created_at}"

    def save(self, *args, **kwargs):
        # Generate bill number only if the bill is being created (not updated)
        if not self.pk:
            # Get the current date and time
            now = timezone.now()
            # Check if it's after 12 PM
            if now.time() >= time(12, 0):
                # Reset bill number after 12 PM
                last_bill = Bill_model.objects.filter(created_at__date=now.date()).order_by('-bill_number').first()
            else:
                # Use the previous day's bills to determine the next bill number
                last_bill = Bill_model.objects.filter(created_at__date=now.date()).order_by('-bill_number').first()
            
            # Set the bill number
            if last_bill:
                self.bill_number = last_bill.bill_number + 1
            else:
                self.bill_number = 1  # Start from 1 if no bills exist for the day

        super().save(*args, **kwargs)



