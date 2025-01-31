from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ClothingItem, Outfit
from .forms import ClothingItemForm, OutfitForm
from .color_matcher import ColorMatcher

def home(request):
    return render(request, 'wardrobe/home.html')

@login_required
def add_clothes(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('view_wardrobe')
    else:
        form = ClothingItemForm()
    return render(request, 'wardrobe/add_clothes.html', {'form': form})

@login_required
def view_wardrobe(request):
    items = ClothingItem.objects.filter(user=request.user)
    return render(request, 'wardrobe/view_wardrobe.html', {'items': items})

@login_required
def create_outfit(request):
    if request.method == 'POST':
        form = OutfitForm(request.POST)
        if form.is_valid():
            outfit = form.save(commit=False)
            outfit.user = request.user
            outfit.save()
            form.save_m2m()
            return redirect('view_wardrobe')
    else:
        form = OutfitForm()
    return render(request, 'wardrobe/create_outfit.html', {'form': form})

@login_required
def view_wardrobe(request):
    items = ClothingItem.objects.filter(user=request.user)
    return render(request, 'wardrobe/view_wardrobe.html', {'items': items})

@login_required
def item_detail(request, item_id):
    item = ClothingItem.objects.get(id=item_id, user=request.user)
    
    # Get matching items using different color harmonies
    matching_items = {
        'complementary': item.get_matching_}
    


    # wardrobe/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'wardrobe/signup.html', {'form': form})

def admin_home_view(request):
    return render(request, 'wardrobe/admin_home.html')

def list_users_view(request):
    users = User.objects.all()
    return render(request, 'wardrobe/list_users.html', {'users': users})

def change_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('list_users')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'wardrobe/change_password.html', {'form': form, 'user': user})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                  return redirect('admin_home') 
            else:
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'wardrobe/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def home(request):
    return render(request, 'wardrobe/home.html')



@login_required
def outfit_generator(request):
    # Fetch all clothing items of the logged-in user
    items = ClothingItem.objects.filter(user=request.user)

    # Organize items by category
    tops = items.filter(category='TOP')
    bottoms = items.filter(category='BOTTOM')
    dresses = items.filter(category='DRESS')
    shoes = items.filter(category='SHOE')
    accessories = items.filter(category='ACCESSORY')

    outfits = []

    # Generate outfits by combining tops, bottoms, dresses, shoes, and accessories
    for top in tops:
        for bottom in bottoms:
            for shoe in shoes:
                for accessory in accessories:
                    # Optionally, add color matching logic here
                    outfits.append({
                        'top': top,
                        'bottom': bottom,
                        'shoe': shoe,
                        'accessory': accessory
                    })

    # If dresses are available, include them in outfits
    for dress in dresses:
        for shoe in shoes:
            for accessory in accessories:
                outfits.append({
                    'dress': dress,
                    'shoe': shoe,
                    'accessory': accessory
                })

    return render(request, 'wardrobe/outfit_generator.html', {'outfits': outfits})