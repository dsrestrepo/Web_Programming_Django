from django.shortcuts import render
from django import forms

from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

#to convert markdown:
from markdown2 import markdown

import random

#forms:
#search bar
class NewForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'id' : 'id_search', 'placeholder': 'Search Encyclopedia'}))
#new page
class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title",widget=forms.TextInput(attrs={'id' : 'id_pageTitle', 'placeholder': 'Title Of The New Page'}))
    pageBody = forms.CharField(label="Description",widget=forms.Textarea(attrs={'id' : 'id_pageBody', 'placeholder': 'Body Of The New Page'}))
#Edit page
class EditPageForm(forms.Form):
    editBody = forms.CharField(label="Edit",widget=forms.Textarea(attrs={'id' : 'id_editBody', 'placeholder': 'Edit the Body'}))


#index and search bar:
def index(request):
    #search bar:
    if request.method == 'GET':
        form = NewForm(request.GET)
        # Check if form data is valid (server-side)
        if form.is_valid():
            value = form.cleaned_data["search"]
            substrings=[]
            for search in util.list_entries():
                #if is the same displays entry
                if value.lower() == search.lower():
                    return HttpResponseRedirect(reverse('entry', args=[search]))
                #else, compare substring and saves the true results
                elif value.lower() in search.lower():
                    substrings.append(search)
            #display the options with substing       
            return render(request,"encyclopedia/options.html",{
                "form": NewForm,
                "value": value,
                "substrings":substrings
            })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewForm    
            })
    #index:
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm    
    })


#display entry or error file doesn't found
def entry(request, search):
    searchBody=util.get_entry(search)
    if (searchBody != None):
        bodyText= markdown(searchBody)
    else:
        bodyText=None
    return render(request, "encyclopedia/entry.html",{
        "search":search,
        "searchBody":searchBody,
        "bodyText":bodyText,
        "form": NewForm    
    })

#create a New Page   
def newPage(request):
    message=False
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            title = form.cleaned_data["pageTitle"]
            body = form.cleaned_data["pageBody"]
            for search in util.list_entries():
                #if is the same displays entry
                if title.lower() == search.lower():
                    message=True
                    return render(request,"encyclopedia/newPage.html",{
                    'form': NewForm,
                    'newform':form,
                    'message':message
                    })
            #The title doesn't exist we can save the new page:
            util.save_entry(title,body)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request,"encyclopedia/newPage.html",{
            'form': NewForm,
            'newform':form,
            'message':message
            })
    return render(request,"encyclopedia/newPage.html",{
        'form': NewForm,
        'newform':NewPageForm,
        'message':message
    })


#edit
def edit(request, title):
    searchBody=util.get_entry(title)
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            body = form.cleaned_data["editBody"]
            #print(body)
            util.save_entry(title,body)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request, "encyclopedia/edit.html",{
            "title":title,        
            "editform":form,
            "form":NewForm    
            })
                    
    return render(request, "encyclopedia/edit.html",{
        "title":title,        
        "editform":EditPageForm(initial={'editBody':searchBody}),
        "form":NewForm    
    })

#random
def randomf(request):
    entries=util.list_entries()
    rand = random.randint(0, len(entries) - 1)
    title=entries[rand]
    searchBody=util.get_entry(title)
    bodyText= markdown(searchBody)
    return render(request, "encyclopedia/entry.html",{
        "search":title,
        "searchBody":searchBody,
        "bodyText":bodyText,
        "form": NewForm    
    })    
