# Create your views here.

from django.shortcuts import render_to_response 
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib import auth
import django.contrib.auth.forms as auth_forms
import django.contrib.auth.views as auth_views

import forms
import models

from django.db.models import Max

from web import settings

def home(request):
    notices = models.Notice.objects.all().order_by("-timestamp")[:3]

    form = None
    if not request.user.is_authenticated():
        form = auth_forms.AuthenticationForm()
        
    return render_to_response("home.html", {
        'form':form,
        'notices':notices
        },
        context_instance = RequestContext(request))

def ping(request):
    return HttpResponse("OK")

def login(request):
    if request.POST:
        data = request.POST
        form = auth_forms.AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    auth.login( request, user )
                    messages.info(request, "Login successful")

                    if request.GET.has_key("next"):
                        return HttpResponseRedirect(request.GET["next"])
                else:
                    messages.error(request, "That account has been disabled.")
        else:
            messages.error(request, "Username or password incorrect")

    return HttpResponseRedirect("%s/home/"%(settings.SITE_URL,))

def logout(request):
    return auth_views.logout(request, "%s/home/"%(settings.SITE_URL,))

def change_password(request):
    return auth_views.password_change(request, post_change_redirect="%s/home/"%(settings.SITE_URL,))

def forgot_password(request):
    return auth_views.password_reset(request, post_reset_redirect="%s/home/"%(settings.SITE_URL,))

def register(request):
    if request.POST:
        data = request.POST
        form = forms.UserCreationForm(data = data)

        if form.is_valid():
            form.save()
            messages.info(request, "Registration Successful")
            return HttpResponseRedirect("%s/home/"%(settings.SITE_URL,))
    else:
        form = forms.UserCreationForm()

    return render_to_response("register.html", 
            {'form':form},
            context_instance = RequestContext(request))

def help(request):
    return render_to_response("help.html", 
            context_instance = RequestContext(request))

