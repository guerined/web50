from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django import forms
from . import util
import random
from django.urls import reverse

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title_display(request,TITLE):
    if util.get_entry(TITLE) is None:
        return render(request, "encyclopedia/404.html", {"title": TITLE})
    else:
        content = markdown2.markdown(util.get_entry(TITLE))
        return render(request,"encyclopedia/display.html", { "title": TITLE, "content": content})

def search(request):
    if request.method == "POST" :
        query = request.POST['q']
        all_entries = util.list_entries()
        entries = []
        for entry in all_entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse('title_display', args=(entry,)))
            if query.lower() in entry.lower():
                entries.append(entry)
        return render(request,"encyclopedia/search_results.html", {"query": query, "entries": entries})
    else:
        return render(request, "encyclopedia/404_Search.html")

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            path = "/entries/" + title + ".md"
            content = form.cleaned_data["content"]
            try:
                f = open("entries/" + title + ".md", "x")
            except FileExistsError:
                return render(request, "encyclopedia/404_Already_Exist.html")
            else:
                f.write("# "+ title)
                f.write("\n")
                f.write("\n")
                f.write(content)
                f.close()
                return HttpResponseRedirect(reverse('title_display', args=(title,)))
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })

def randomwiki(request):
    titles = util.list_entries()
    TITLE = random.choice(titles)
    content = markdown2.markdown(util.get_entry(TITLE))
    return render(request,"encyclopedia/display.html", { "title": TITLE, "content": content})

def editentry(request, TITLE):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            path = "/entries/" + title + ".md"
            content = form.cleaned_data["content"]
            try:
                f = open("entries/" + title + ".md", "w")
            except FileNotFoundError:
                return render(request, "encyclopedia/404.html", {"title": TITLE})
            else:
                f.write("# "+ title)
                f.write("\n")
                f.write("\n")
                f.write(content)
                f.close()
                return HttpResponseRedirect(reverse('title_display', args=(title,)))
    if util.get_entry(TITLE) is None:
        return render(request, "encyclopedia/404.html", {"title": TITLE})
    else:
        precontent = (util.get_entry(TITLE))
        content = precontent.split("\n",2)[2]
        data = {'title':TITLE, 'content':content}
        form = NewEntryForm(initial=data)
        return render(request, "encyclopedia/edit.html", {
        "form": form, "title":TITLE
    })

        