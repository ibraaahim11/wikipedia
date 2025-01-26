from django.shortcuts import render

from . import util

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

# index of the page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def wikiEntry(request, title):
    return render(request, "encyclopedia/wikiEntry.html",{
        "title": title,
        "entry_found": util.get_entry(title) != None,
        "info": (util.convert_markdown(util.get_entry(title)))
    })

    
def search(request):
    # if search is submitted
    if request.method == "POST":
        # get the title
        title = request.POST.get('q')
        exact_entry_found = util.get_entry(title) != None
        # if entry found we redirect and we replace the placeholder of the title in the paths urls.
        if exact_entry_found:
            return HttpResponseRedirect(reverse("wikiEntry",args=[title]))
        # exact entry not found so we render search results with the similar entries found
        else:
        
            similar_entries = util.find_similar_entries(title)
            return render(request, "encyclopedia/search-results.html",{
                              "entries": similar_entries,
                              "num_entries": len(similar_entries)
                          })
        

def newPage(request):
    # render page if opening using get method
    if request.method == "GET":
        return render(request, "encyclopedia/new-page.html")
    # if the method is post 
    elif request.method == "POST":
        title = request.POST.get('title')
        entry_exists = util.get_entry(title) != None
        # if entry exists we will reload the new-page with a warning message while maintaining the entered data.
        if entry_exists:
            written_content = request.POST.get('content')
            return render(request, "encyclopedia/new-page.html",{
                "title":title,
                "written_content": written_content,
                "entry_exists": entry_exists
                
            })
        # if it doesnt exist we will create it then go to it
        else:
            content = request.POST.get('content')
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("wikiEntry",args=[title]))
            
            
        
def editEntry(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        
        return render(request, "encyclopedia/edit-entry.html",{
            "title": title,
            "content":content
        })
    elif request.method == "POST":
        
        content = request.POST.get("content")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wikiEntry",args=[title]))
    
    
    
def randomPage(request):
    title = util.random_entry_title()    
    return HttpResponseRedirect(reverse("wikiEntry",args=[title]))
    
        
        

    

