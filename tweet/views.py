from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Tweet, Profile, Team, TweetImage, Message
from .forms import TweetForm, UserRegistration, ProfileForm
from django.contrib.auth.models import User
from django.db.models import Q


# 🏠 Home Page — shows all tweets
@login_required
def index(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TweetForm(request.POST)
            files = request.FILES.getlist('images')  # 🔹 multiple images
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()

                for f in files:
                    TweetImage.objects.create(tweet=tweet, image=f)

                messages.success(request, "Your thought has been shared ☕")
                return redirect('index')
        else:
            form = TweetForm()

    return render(request, 'index.html', {'tweets': tweets, 'form': form})


# 📝 List all tweets (separate page if needed)
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-updated_at')
    return render(request, 'index.html', {'tweets': tweets})


# ➕ Create a new tweet
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet posted successfully ☕")
            return redirect('index')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


# ✏️ Edit an existing tweet
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        new_images = request.FILES.getlist('images')  # 🔹 multiple new images

        if form.is_valid():
            form.save()

            # 🔹 Add new images
            for img in new_images:
                TweetImage.objects.create(tweet=tweet, image=img)

            # 🔹 Optionally delete selected images
            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                TweetImage.objects.filter(id__in=delete_image_ids, tweet=tweet).delete()

            messages.success(request, "Tweet updated successfully ✅")
            return redirect('index')
    else:
        form = TweetForm(instance=tweet)

    existing_images = tweet.images.all()  # 🔹 fetch all images
    return render(request, 'tweet_form.html', {'form': form, 'tweet': tweet, 'existing_images': existing_images})


# ❌ Delete a tweet
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, "Tweet deleted successfully 🗑️")
        return redirect('index')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


# 👤 Register a new user
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Welcome to ChaiBreak ☕! Your account has been created.")
            return redirect('index')
    else:
        form = UserRegistration()
    return render(request, 'registration/register.html', {'form': form})


# 👤 View & Edit Profile
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully 🌟")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'teams/profile.html', {'form': form, 'profile': profile})


# 👥 Teams Page — view all teams and their members
@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/teams_page.html', {'teams': teams})


# <---------chat view---------->

@login_required

def chat_room(request, room_name):
    search_query = request.GET.get('search', '')
    users = User.objects.exclude(id=request.user.id)

    # ✅ Step 1: Check if room_name matches current logged-in user
    is_self_chat = room_name.lower() == request.user.username.lower()

    # ✅ Step 2: Default values
    chats = []
    active_chat_user = None
    welcome_message = None

    if is_self_chat:
        # ✅ Show a welcome message instead of chats
        welcome_message = f"Welcome {request.user.username}! 👋 Select a user from the list to start chatting."
    else:
        # ✅ Normal chat between current user and 'room_name'
        try:
            active_chat_user = User.objects.get(username__iexact=room_name)
        except User.DoesNotExist:
            welcome_message = f"No user found with username '{room_name}'."
            active_chat_user = None

        if active_chat_user:
            chats = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=active_chat_user)) |
                (Q(receiver=request.user) & Q(sender=active_chat_user))
            )

            if search_query:
                chats = chats.filter(content__icontains=search_query)

            chats = chats.order_by('timestamp')

    # ✅ Step 3: Get recent chats for all users
    user_last_messages = []
    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()
        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # ✅ Step 4: Render
    return render(request, "chat.html", {
        "room_name": room_name,
        "chats": chats,
        "active_chat_user": active_chat_user,
        "user_last_messages": user_last_messages,
        "search_query": search_query,
        "welcome_message": welcome_message,
    })