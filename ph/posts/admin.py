# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from posts.models import BlogPost
from posts.models import Comment

from posts.models import ExampleModel
from posts.models import ExampleNonUploadModel

from posts.models import Profile

class BlogPostAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("title",)}

# Register your models here.
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment)

admin.site.register(ExampleModel)
admin.site.register(ExampleNonUploadModel)
admin.site.register(Profile)
