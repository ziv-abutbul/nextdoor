from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_image', default='profile_image/def.jpg')
    latitude = models.FloatField(blank=True, null=True,default=31.253104)
    longitude = models.FloatField(blank=True, null=True,default=34.7892974)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


# Request model - title, description, user
class RequestModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    close = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class MessageModel(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(get_user_model(), related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class RemoveBan(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

# Comment Model - user, comment
class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


# Support ticket model - includes optional RequestModel, CommentModel, MessageModel
class SupportTicketModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    request_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status closed = "closed", open = "open", resolved = "resolved"
    status = models.CharField(max_length=10, default="open")

    def __str__(self):
        return self.description

class UserTicketModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    request_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status closed = "closed", open = "open", resolved = "resolved"
    status = models.CharField(max_length=10, default="open")

    def __str__(self):
        return self.description
