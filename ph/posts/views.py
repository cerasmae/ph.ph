# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import User
from .models import BlogPost
from .models import Comment
from .models import Profile

from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


#############

from django.core.urlresolvers import reverse
from django.views import generic

from . import forms

def createBlogPost_view(request):
	form_class = forms.CkEditorForm

	if request.user.is_authenticated():
		if request.method == "POST":
			title = request.POST['title'].strip()
			content = forms.CkEditorForm()
			location = request.POST['location'].strip()

			bpost = BlogPost.objects.create(title=title, content=content, location=location, owner=request.user)
			bpost.save()
			return redirect('post-detail')

	return render(request, 'form.html' )


class CkEditorFormView(generic.FormView):
    form_class = forms.CkEditorForm
    template_name = 'form.html'

    def form_valid(self, form):
    	print "PLS WORK"

    def get_success_url(self):
        # return reverse('ckeditor-form')
        # return HttpResponse(self.request)
        


ckeditor_form_view = CkEditorFormView.as_view()

###############


# Create your views here.
def index(request):
	blogposts = BlogPost.objects.all().order_by("-create_date")
	return render(request, 'index.html', {"blogposts" : blogposts})

def signup(request):
	return render(request, 'signup.html')

def user_profile(request, user_id, user_username):
	# user = User.objects.filter(pk = user_id)
	return render(request, 'profile.html')

def post_detail(request, post_id, slug):
	blogpost = get_object_or_404(BlogPost, pk=post_id)
	comments = Comment.objects.filter(bpId = blogpost).order_by('-create_date')

	if request.method == "POST":
		comment = request.POST['comment'].strip()

		if request.user.is_authenticated():
			new_comment = Comment.objects.create(content=comment, bpId=blogpost, ownerId=request.user)
			new_comment.save()

		print comment

	return render(request, 'post.html', {"blogpost" : blogpost, "comments" : comments})

def signup_view(request):
	if request.user.is_authenticated():
		return redirect('index')

	context = {}

	if request.method == "POST":
		username = request.POST['username'].strip()
		password1 = request.POST['password1'].strip()
		password2 = request.POST['password2'].strip()
		first_name = request.POST['first_name'].strip()
		last_name = request.POST['last_name'].strip()
		email = request.POST['email'].strip()

		# print username, password1, password2, first_name, last_name, email

		username_valid = User.objects.filter(username=username)
		email_valid = User.objects.filter(email=email)
		context["first_name"] = first_name
		context["last_name"] = last_name

		if email_valid.exists():
			context["error_message"] = "Email is already registered."
		elif username_valid.exists():
			context["error_message"] = "Username is already taken."
		elif password1 != password2:
			context["error_message"] = "Passwords did not match."
		else:
			context = {}
			new_user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
			new_user.set_password(password1)
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			profile.save()
			auth_user = authenticate(username=username, password=password1)
			if auth_user is not None:
				login(request, auth_user)
				print "USER IS AUTHENTICATED"
				return redirect('index')
			# print "USER IS OKAY"

	return render(request, 'signup.html', context=context)



def login_view(request):
	if request.user.is_authenticated():
		return redirect('index')

	context = {}

	if request.method == "POST":
		username = request.POST['username'].strip()
		password = request.POST['password'].strip()

		user = authenticate(username=username, password=password)

		if user is not None:
			print "username and password are correct"
			login(request, user)
			return redirect('index')

		else:
			context["error_message"] = "Wrong username or password"
			context["username"] = username

	return render(request, 'registration/login.html', context=context)

def logout_view(request):
	logout(request)
	return redirect('index')

def profile_view(request):
	profile = get_object_or_404(Profile, user=request.user)

	if request.method == "POST":
		form = ImageUploadForm(request.POST, request.FILES)

		if form.is_valid():
			profile.photo = form.cleaned_data['photo']
			profile.save()

	return render(request, 'profile.html', {"profile":profile, "user":request.user})
