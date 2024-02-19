from django.db import models
from django.contrib.auth.models import User
from .mongoDB import database

# Create your models here.

votes_collection = database['votes'] #name of collection 
users_collection = database['users']

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.title
    

class CategoryItem(models.Model):
    title = models.CharField(max_length=200)
    total_vote = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    voters = models.ManyToManyField(User, blank=True)

    @property
    def percentage_vote(self): #self variable allows you to differenciate between instance variables (belongs to a particular user)
        category_votes = self.category.total_vote #to get the amount of votes made for each individual item
        items_votes = self.total_vote #how much votes that person made

        if category_votes == 0:
            vote_in_percentage = 0 #show 0 if no votes were made

        else: 
            vote_in_percentage = (items_votes/category_votes) * 100 #operation to get the percentage votes 
        return vote_in_percentage 

    def __str__(self):
        return self.title
    

