from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import TweeterUser, Tweet, Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, CreateNewUserForm, NewTweetForm
import re
# def welcome(request, *args, **kwargs):
#     return render(request, 'welcome.html')


@login_required(login_url="/login")
def home_page(request, *args, **kwargs):
    following_users = request.user.tweeteruser.following.all()
    logged_in_tweets = Tweet.objects.filter(author=request.user.tweeteruser)
    tweets = Tweet.objects.filter(author__in=following_users)

    all_tweets = logged_in_tweets | tweets
    all_tweets = all_tweets.order_by('-created_date')
    return render(request, 'home.html', {'tweets': all_tweets})


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
            the_tweet = Tweet.objects.create(body=data['new_tweet'], author=request.user.tweeteruser)

            tweet_body = data['new_tweet']
            matches = re.findall(r'@(\w+)', tweet_body)

            for match in matches:
                matched_user = TweeterUser.objects.get(user__username=match)
                Notification.objects.create(notified=matched_user, not_tweet=the_tweet)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = NewTweetForm()

    return render(request, 'generic_form.html', {'form': form})


def logout_view(request, *args, **kwargs):
    logout(request)
    return render(request, 'logout.html')


def notification_view(request):
    if request.user.is_authenticated:
        notif = Notification.objects.filter(notified=request.user.tweeteruser)

        for notify in notif:
            notify.delete()

    return render(request, 'notification.html', {'notif': notif})
