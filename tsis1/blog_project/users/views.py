from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Follow, Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'user': user})


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)

    # Get or create the profile for the user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile_view', username=user.username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/profile_edit.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile_view', username=user_to_follow.username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow_instance = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    follow_instance.delete()
    return redirect('profile_view', username=user_to_unfollow.username)
