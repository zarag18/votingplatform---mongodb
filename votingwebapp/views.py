from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm 
from django import forms 
from .models import Category, CategoryItem, votes_collection, users_collection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from email_validator import validate_email 
from django.core.exceptions import ValidationError 
import requests



# Create your views here.
#creating the templates for the different webpages 
def index (request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request, "index.html", context)

@login_required(login_url="signin") #to make sure user is logged in before they can vote 
def detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category=category)
    
    msg = None
    
    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            msg = "voted"
            
    if request.method == 'POST':
        selected_id = request.POST.get("category_item")
        item = CategoryItem.objects.get(id=selected_id)
        item.total_vote += 1
        
        item_category = item.category 
        item_category.total_vote += 1
        
        item.voters.add(request.user)
        item_category.voters.add(request.user)
        
        item.save()
        item_category.save()
        # Insert vote information into MongoDB collection
        vote_info = {
            'ID of Category Item': str(item.id),
            'Total Votes of Item': item.total_vote,
            'Item Name': item.title,
            'Voter Username': request.user.username,
        }
        votes_collection.insert_one(vote_info)
        
        return redirect("result", slug=category.slug)
    
    context = {"category": category, "categories": categories, "msg": msg}
    return render(request, "detail.html", context)

         

def result (request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)
    context = {"category":category, "items":items}
    return render(request, "result.html", context)



def signin(request):
    msg = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                else:
                    return redirect("index")
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Invalid Credentials"

    form = AuthenticationForm()
    context = {"form": form, "msg": msg}
    return render(request, "signin.html", context)


def signup(request):
    class SignUpForm(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User #by importing user 
            fields = ['username', 'email', 'password1', 'password2']

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Perform additional email validation
            email = form.cleaned_data['email']
            try:
                validate_email(email) #uses the validation library from django to verify email
            except ValidationError:
                form.add_error('email', 'Invalid email address')
            else:
                form.save()
                # Additional processing
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                users = {
                    "Username": username,
                    "Email Address": email
                }
                users_collection.insert_one(users)  # users are inserted into the database
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("index")

    context = {"form": form}
    return render(request, "signup.html", context)

def signout(request):
    logout(request)
    return redirect("index")

def poll_results(request):
    # Fetch all category items with their associated votes
    category_items = CategoryItem.objects.all()
    category = Category.objects.all()
    context = { 'category':category, 'category_items': category_items}
    return render(request, 'pollresults.html', context)

