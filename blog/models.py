from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128,blank=True)
    description = models.TextField(max_length=2048,blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to="images")
    time_created = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    content_type = models.CharField(max_length=128,default="TICKET")
    review = models.ForeignKey("Review",on_delete=models.SET_NULL, null = True, related_name="+")
    

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE,related_name="+")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=128,default="REVIEW")


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="following")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="followed_by")
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
