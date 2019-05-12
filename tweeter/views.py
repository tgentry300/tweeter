from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import TweeterUser, Tweet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LoginForm, CreateNewUserForm, NewTweetForm


# def welcome(request, *args, **kwargs):
#     return render(request, 'welcome.html')


@login_required(login_url="/login")
def home_page(request, *args, **kwargs):
    return render(request, 'home.html')


def login_view(request, *args, **kwargs):
    form = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = LoginForm()

    return render(request, 'generic_form.html', {'form': form})


@login_required
def user_page(request, *args, **kwargs):
    pass


def create_user(request, *args, **kwargs):
    pass


def tweet_view(request, *args, **kwargs):
    pass


def new_tweet(request, *args, **kwargs):
    pass
