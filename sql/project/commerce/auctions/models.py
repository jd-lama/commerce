from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from datetime import timezone
class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length= 10)

    def __str__(self) -> str:
        return f"{self.category}"

class Listing(models.Model):
    title  = models.CharField(max_length=60)
    flAction = models.BooleanField(default = True)
    creatd_date = models.DateTimeField(default= timezone.now)
    description = models.CharField(null = True, max_length=100)
    startingBid = models.FloatField()
    currentBid = models.FloatField(blank= True, null = True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="similar_listing")
    creator = models.ForeignKey(User,on_delete=models.PROTECT,related_name="all_creater_listing")
    watchers = models.ManyToManyField(User,blank=True,related_name="watched_lisings")
    buyer = models.ForeignKey(User,null=True,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.title} - {self.startingBid}"
    
class Bid(models.Model):
    action = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateTimeField(auto_new=True)

class Comment(models.Model):
    comment = models.CharField(max_length= 100)
    createdDate = models.DateTimeField(default= timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="get_comment")

    def get_creation_data(self):
        return self.createdDate.strftime('%H %d %Y')

class Picture(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="get_pictures")
    picture = models.ImageField(upload_to="images/")
    alt_text = models.CharField(max_length=100)

