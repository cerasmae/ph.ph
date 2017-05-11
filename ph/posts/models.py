# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


#########################################################
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class ExampleModel(models.Model):
    content = RichTextUploadingField()


class ExampleNonUploadModel(models.Model):
    content = RichTextField()
###########################################################

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(default="media/no-img.jpg")

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

# Create your models here.
class BlogPost(models.Model):
	# bpId = models.AutoField(primary_key = True)
	owner = models.ForeignKey(User, related_name="blog_post")
	title = models.CharField(max_length = 80)
	slug = models.CharField(max_length = 80)
	content = models.TextField()
	location = models.CharField(max_length = 30)
	likes = models.IntegerField(default = 0)
	flags = models.IntegerField(default = 0)
	create_date = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.title

class Image(models.Model):
	blogpost = models.ForeignKey(BlogPost)
	image = models.ImageField()

class Comment(models.Model):
	# commentId = models.AutoField(primary_key = True)
	bpId = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
	ownerId = models.ForeignKey(User, related_name="comments")
	content = models.TextField(max_length = 150)
	create_date = models.DateTimeField(auto_now = True)

	def __str__(self):
		user = User.objects.filter(pk=self.ownerId.pk).first()

		return self.content + " by " + user.first_name + " " + user.last_name
