from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, LoginForm, ProfilesForm, MessageForm, CommentForm

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from . models import Profiles, Message, Comment, Likes
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('profile', kwargs={'user': user}))
            else:
                return HttpResponse("Profil mavjud emas")
        else:
            return HttpResponse("Siz noto'g'ri malumot kiritdingiz yoki " +
                                    "ro'yhatdan o'tmagansiz. Ro'yhatdan o'tish uchun " +
                                    "iltimos havolani bosing")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@csrf_protect
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = User.objects.get(username=cd['username'])
            Profiles.objects.create(owner=user)
            return redirect(reverse('login'))
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
@csrf_exempt
def user_profile(request, user):
    form = ProfilesForm()
    if request.method == 'POST':
        data = ProfilesForm(request.POST, request.FILES)
        if data.is_valid():
            cd = data.cleaned_data
            aaa = Profiles.objects.get(owner__username=user)
            if cd['nickname']:
                aaa.nickname = cd['nickname']
            if cd['image']:
                aaa.image = cd['image']
            aaa.save()

    if request.method == 'POST':
        msg_form = MessageForm(request.POST)
        if msg_form.is_valid():
            cd = msg_form.cleaned_data
            owner = Profiles.objects.get(owner__username=user)
            Message.objects.create(user=owner, message=cd['message'])
    msg_form = MessageForm()

    msg = Message.objects.all().order_by('created_at')
    details = Profiles.objects.get(owner__username=user)
    friends = Profiles.objects.all()
    return render(request, 'account/profile.html', {'details': details,
                                                    'form': form,
                                                    'friends': friends,
                                                    'msg_form': msg_form,
                                                    'msg': msg})


@csrf_exempt
def comments(request, comment_to, commenter):
    owner_comments = Profiles.objects.get(pk=comment_to)
    owner_profile = Profiles.objects.get(pk=commenter)

    post = get_object_or_404(Profiles, pk=comment_to)
    posted = get_object_or_404(Profiles, pk=commenter)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment(post=post, posted=posted, body=cd['body'])
            new_comment.save()

        like = request.POST.get('like')
        if like == 'True':
            p = Likes(like_to=post, liked_from=posted, liked=True)
            p.save()

    comment_form = CommentForm()

    try:
        user_comments = Comment.objects.exclude(posted=post)
    except ObjectDoesNotExist:
        user_comments = ''

    like_up = Likes.objects.filter(like_to__id=comment_to)
    like_owner = Likes.objects.filter(like_to__id=comment_to, liked_from__id=commenter)

    return render(request, 'account/comments.html', {'owner_comments': owner_comments,
                                                     'owner_profile': owner_profile,
                                                     'comment_form': comment_form,
                                                     'user_comments': user_comments,
                                                     'like_up': like_up,
                                                     'like_owner': like_owner})


def likes(request, comment_owner):
    profile_owner = Profiles.objects.get(pk=comment_owner)
    profile_comments = Comment.objects.filter(post__id=comment_owner)
    profile_likes = Likes.objects.filter(like_to__id=comment_owner)

    return render(request, 'account/likes.html', {'profile_owner': profile_owner,
                                                  'profile_comments': profile_comments,
                                                  'profile_likes': profile_likes})
