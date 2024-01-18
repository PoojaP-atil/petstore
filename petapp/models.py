from django.db import models

# Create your models here.
class CustomManager(models.Manager):
    def get_pet_age(self):
        #return super().get_queryset().filter(Age = 1)
        return super().get_queryset().filter(Species="chow chow")
        #return super().get_queryset().order_by('Age')


class pet(models.Model):
    gender = (('Male','Male'),('Female','Female'))
    Image = models.ImageField(upload_to='media')
    Name = models.CharField(max_length=200)
    Species = models.CharField(max_length=200)
    Breed = models.CharField(max_length=200)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=200, choices = gender)
    Weight = models.FloatField(default=0)
    Height = models.FloatField(default=0)
    Description = models.CharField(max_length=500)
    Price = models.FloatField()
    slug = models.SlugField(default='',null=False)
    pets = CustomManager()

    class Meta:
        db_table = 'pet'

class register(models.Model):
    gender = (('Male','Male'),('Female','Female')) 
    Name = models.CharField(max_length=200)
    Gender = models.CharField(max_length=200, choices = gender)
    Age = models.IntegerField()
    Address = models.CharField(max_length=500)
    State = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNo = models.BigIntegerField()  
    Email = models.EmailField()
    Password = models.CharField(max_length=200)

    class Meta:
        db_table = 'register'

class cart(models.Model):
    productid = models.ForeignKey(pet,on_delete = models.CASCADE)
    customerid = models.ForeignKey(register,on_delete= models.CASCADE)
    quantity = models.IntegerField()
    totalamount = models.FloatField()

    class Meta:
        db_table = "cart"

class order(models.Model):
    Name = models.CharField(max_length=200)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    Pincode = models.IntegerField()
    PhoneNo = models.BigIntegerField()
    totalbillamount = models.FloatField() 
    ordernumber = models.CharField(max_length=200 , default = 0)


    class Meta:
        db_table = "order1"

class payment(models.Model):
    customerid = models.ForeignKey(register,on_delete = models.CASCADE)
    orderid = models.ForeignKey(order,on_delete = models.CASCADE)
    paymentstatus = models.CharField(max_length = 100,default = 'pending')
    transactionid = models.CharField(max_length = 200)
    paymentmode = models.CharField(max_length = 100,default='paypal')

    class Meta:
        db_table = "payment"

class orderdetails(models.Model):
    paymentid = models.ForeignKey(payment,on_delete = models.CASCADE, null = True)
    customerid = models.ForeignKey(register,on_delete = models.CASCADE)
    productid = models.ForeignKey(pet, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    totalprice = models.FloatField()
    ordernumber = models.CharField(max_length=200 , default = 0)

    
    class Meta:
        db_table = "oderdetails"

