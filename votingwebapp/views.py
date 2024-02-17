from django.shortcuts import render, redirect
from .models import Category, CategoryItem, votes_collection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
import requests



# Create your views here.
#creating the templates for the different webpages 
def index (request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request, "index.html", context)

@login_required(login_url="signin") #to make sure user is logged in before they can vote 
def detail (request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category =category)

    msg = None 

    if request.user.is_authenticated:
        if category.voters.filter(id =request.user.id).exists():
            msg = "voted" #once the user is authenicated and has casted and vote, a msg will display saying voted 

    if request.method == 'POST':
        selected_id  = request.POST.get("category_item")
        print(selected_id)
        item = CategoryItem.objects.get(id = selected_id)
        
        item_category = item.category 
        item_category.total_vote += 1

        #Insert into MongoDB with the total vote for the category item
        votes_collection.insert_one(
            {'category_item': selected_id},
            {'$inc': {'total_vote': 1}}
        )
        print("added to database")

        # Update MongoDB with the total vote for the category
        votes_collection.insert_one(
            {'category_item': item.category.id},
            {'$inc': {'total_vote': 1}}
        )

        item.voters.add(request.user)
        item.category.voters.add(request.user)

        item.save()
        item_category.save()

        return redirect("result", slug = category.slug)
    

    context = {"category":category, "categories":categories, "msg" : msg}
    return render(request, "detail.html", context)

         

def result (request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)
    context = {"category":category, "items":items}
    return render(request, "result.html", context)

def signin(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            
            else:
            
                return redirect("index")
        else:
            msg = "Invalid Credentials"
            
    context = {"msg":msg}
    return render(request, "signin.html", context)

def signup(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            # login starts here
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            
            
    context = {"form":form}
    return render(request, "signup.html", context)
def signout(request):
    logout(request)
    return redirect("index")

