from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse


# Create your views here.
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have succesfully logged out')
    return redirect(reverse('index'))