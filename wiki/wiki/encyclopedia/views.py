from django.shortcuts import render
from django.http import HttpResponse

from . import util

# display list of entries
def index(request):
    if request.method == "POST":
        return render(request, "encyclopedia/results.html")
    
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
    results = []
    entries = util.list_entries()
    q = request.GET.get("q")

    #for entry in entries:
        #if entry.lower() == q.lower()


