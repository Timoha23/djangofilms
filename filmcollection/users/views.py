from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from .forms import CreationForm
from .models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('films:index')
    template_name = 'users/signup.html'


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, template_name='users/user_profile.html', context=context)
