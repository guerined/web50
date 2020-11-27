from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title_display(request,TITLE):
    if util.get_entry(TITLE) is None:
        #return HttpResponse("404 Error")
        return render(request, "encyclopedia/404.html", {"title": TITLE})
    else:
        content = markdown2.markdown(util.get_entry(TITLE))
        #return HttpResponse(content)
        return render(request,"encyclopedia/display.html", { "title": TITLE, "content": content})
