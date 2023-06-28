from django.shortcuts import render, redirect
from django import forms
import markdown2
import random

from . import util

class SearchForm(forms.Form):
    Search = forms.CharField(label='', widget=forms.TextInput(attrs={'name':'SearchForm', 'placeholder':'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'name':'title', 'rows':'1', 'margin':'auto', 'style':'display: flexbox; text-align: left; width: 30%; margin-right: 70%; margin-bottom: 10px'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'name':'content', 'placeholder':'Enter markdown content here.', 'style':'display: flexbox; text-align: left; margin-right: 50%'}))

def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries(),
        'form': SearchForm()
    })

def new_entry(request):
    if request.method == 'POST':
        entryForm = NewEntryForm(request.POST)
        if entryForm.is_valid():
            title = entryForm.cleaned_data['title']
            content = entryForm.cleaned_data['content']
            if title in util.list_entries():
                return Error(request, 'This page already exists!')
            else:
                util.save_entry(title, content)
                return Entry(request, title)
        else:
            return Error(request, 'The form was not filled out correctly.')
    else:
        return render(request, 'encyclopedia/new_entry.html', {
            'newEntryForm': NewEntryForm(),
            'form': SearchForm()
        })

def Entry(request, title):
    query = util.get_entry(title)
    
    if not query:
        error = 'Error, the requested page could not be found.'
        return render(request, 'encyclopedia/error.html', {
            'error': error,
            'form': SearchForm()
        })
    else:
        mkdown = util.get_entry(title)
        content = markdown2.markdown(mkdown)
        return render(request, 'encyclopedia/entry.html', {
            'title':title, 
            'content':content,
            'form': SearchForm()
        })


def search(request):
    error = "Error, No pages found matching your search."
    possible_entries = []
    if request.method == 'GET':
        search = SearchForm(request.GET)
        if search.is_valid():
            query = search.cleaned_data['Search']
            for entry in util.list_entries():
                if query.casefold() == entry.casefold():
                    return Entry(request, query)
                elif query.casefold() in entry.casefold():
                    possible_entries.append(entry)
            if len(possible_entries) > 0:
                return render(request, 'encyclopedia/search.html', {
                    'form': SearchForm(),
                    'possible_entries': possible_entries
                })
            else:
                return Error(request, error)
        else:
            return Error(request, error)

def Edit(request, title):
    if request.method == 'GET':
        content = util.get_entry(title)
        return render(request, 'encyclopedia/Edit.html', {
            'form': SearchForm(),
            'editForm': NewEntryForm({"title": title, "content": content})
        })
    else:
        editedForm = NewEntryForm(request.POST)
        if editedForm.is_valid():
            title = editedForm.cleaned_data['title']
            content = editedForm.cleaned_data['content']
            util.save_entry(title, content)
            return Entry(request, title)
            
        


def Error(request, error_message):
    return render(request, 'encyclopedia/error.html', {
        'error': error_message,
        'form': SearchForm()
        
    })

def random_page(request):
    list_of_entries = util.list_entries()
    random_num = random.randint(0, len(list_of_entries) - 1)
    chosen_entry = list_of_entries[random_num]
    return Entry(request, chosen_entry)
    