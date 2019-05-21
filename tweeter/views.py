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
    tweets = Tweet.objects.all()
    return render(request, 'home.html', {'tweets': tweets})


def login_view(request, *args, **kwargs):
    form = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(
                username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_page(request, name):
    user = TweeterUser.objects.get(name=name)
    tweets = Tweet.objects.filter(author=user)
    context = {'user': user, 'tweets': tweets}

    if request.user.is_authenticated:
        logged_in_u = request.user.tweeteruser

    if request.method == 'POST':
        if request.POST.get('follow'):
            logged_in_u.following.add(user)
        elif request.POST.get('unfollow'):
            logged_in_u.following.remove(user)

    return render(request, 'user.html', context)


def create_user(request, *args, **kwargs):
    form = None

    if request.method == 'POST':
        form = CreateNewUserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            new_user = User.objects.create(
                username=data['username'])

            new_user.set_password(data['password'])
            new_user.save()

            TweeterUser.objects.create(
                user=new_user, name=data['name'])

            if new_user is not None:
                login(request, new_user)
                return HttpResponseRedirect(reverse('home'))

    else:
        form = CreateNewUserForm()

    return render(request, 'generic_form.html', {'form': form})


def tweet_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)

    return render(request, 'tweet.html', {'tweet': tweet})


def new_tweet(request, *args, **kwargs):
    form = None

    if request.method == 'POST':
        form = NewTweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Tweet.objects.create(body=data['new_tweet'], author=request.user.tweeteruser)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = NewTweetForm()

    return render(request, 'generic_form.html', {'form': form})


def logout_view(request, *args, **kwargs):
    logout(request)
    return render(request, 'logout.html')
