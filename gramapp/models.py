from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics",blank=True)
    bio = models.TextField(blank=True)


class Post(models.Model):
    image = models.ImageField(upload_to='gram_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    user_id= models.ForeignKey(Profile,on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id= models.ForeignKey(User,on_delete=models.CASCADE)
    post_id= models.ForeignKey(Post,on_delete=models.CASCADE)

class Likes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id= models.ForeignKey(User,on_delete=models.CASCADE)
    post_id= models.ForeignKey(Post,on_delete=models.CASCADE)

class Follows(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    follower_id= models.OneToOneField(Profile,on_delete=models.CASCADE)
    followee_id= models.OneToOneField(User,on_delete=models.CASCADE)


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class PhotoTags(models.Model):
    post_id= models.ForeignKey(Post,on_delete=models.CASCADE)
    tag_id= models.ForeignKey(Tag,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
  




