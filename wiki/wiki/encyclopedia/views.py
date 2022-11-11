from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from . import util

# display list of entries
def index(request): 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# view entry, display error if no entry
def view(request, title):
    entry = util.get_entry(f"{title}")
    entry_link = f"wiki/{title}"
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

# search entries
def search(request):
    if request.method == "POST":
        results = []
        entries = util.list_entries()
        q = request.POST['q']

        for entry in entries:

            #redirect to page if perfect match
            if entry.lower() == q.lower():
                return render(request, "encyclopedia/entry.html", {
                    "title": q,
                    "entry": util.get_entry(f"{q}")
                })
            
            #redirect to list of results containing a substring
            if q.lower() in entry.lower():
                results.append(entry)
                return render(request, "encyclopedia/results.html", {
                    "results": results
                })

        #not found, return error page
        
        return render(request, "encyclopedia/error.html", {
                "title": q
            })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        
        # check if title used
        entries = util.list_entries()
        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/error_new_page.html", {
                "title": title
            })
            
        # save to file
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)

        # redirect to new entry
        return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": util.get_entry(f"{title}")
                })

    else:
        return render(request, "encyclopedia/new_page.html")

def edit_page(request):
    if request.method == "POST":
        title = request.POST['title']
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": util.get_entry(f"{title}")
        })

    else:
        return render(request, "encyclopedia/edit_page.html")


