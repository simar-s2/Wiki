from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
import difflib
import random
from django.contrib import messages
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def get_entry(request, title):
    html_content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "entry": html_content,
    })
    
def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        if not query: return HttpResponseRedirect("/")
        elif util.get_entry(query) != None: return HttpResponseRedirect(f"/wiki/{query}")
        else:
            results = []
            entries = util.list_entries()
            for entry in entries:
                similarity = difflib.SequenceMatcher(None, query, entry).ratio()
                if similarity > 0.5: results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not content or not title: return HttpResponseRedirect('/create_page')
        elif util.get_entry(title) != None:
            messages.error(request, 'Title already exists!')
            return HttpResponseRedirect('/create_page')
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')
    else:
        return render(request, "encyclopedia/create_page.html")

def random_selector(request): 
    return HttpResponseRedirect(f'wiki/{random.choice(util.list_entries())}')

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        print(content)
        if not content:
            messages.error(request, 'Page content cannot be empty!')
            return HttpResponseRedirect(f'/edit/{title}')
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f'/wiki/{title}')

    return render(request, "encyclopedia/edit_page.html", {
        "title":title,
        "content":util.get_entry(title)
    })
