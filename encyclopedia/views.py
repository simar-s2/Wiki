from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
import difflib
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def get_entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title)
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

def random_selector(request): 
    return HttpResponseRedirect(f'wiki/{random.choice(util.list_entries())}')
