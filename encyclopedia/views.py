from django.shortcuts import render, redirect
import markdown2
from . import util
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    content = util.get_entry(entry_name)  # Get raw Markdown content
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Error 404: Page not found."
        })
    
    html_content = markdown2.markdown(content)  # Convert Markdown to HTML
    
    return render(request, "encyclopedia/entry.html", {
        "title": entry_name,  # Pass the entry title
        "entry": html_content  # Pass the converted HTML content
    })

def search(request):
    query = request.GET.get("q", "").strip()  # Get query from the search box
    entries = util.list_entries()  # Get all entries

    for entry in entries:
        if query.lower() == entry.lower():  # Case-insensitive comparison
            return redirect("encyclopedia:entry", entry_name=entry)  # Redirect using the original entry name
    
    # If no exact match, show a results page with partial matches
    matches = []  # Start with an empty list
    for entry in entries:  # Loop through each encyclopedia entry
        if query.lower() in entry.lower():  # Check if query is inside the entry (ignoring case)
            matches.append(entry)  # If yes, add it to the list of matches

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "matches": matches
    })

def new_entry(request):
    """Display the form for creating a new entry OR process form submission."""
    if request.method == "POST":
        title = request.POST.get("entry_title").strip()
        content = request.POST.get("entry_body").strip()

        if util.get_entry(title):  
            return render(request, "encyclopedia/new.html", {
                "error": "An entry with this title already exists!",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)

        return redirect("encyclopedia:entry", entry_name=title)  # Redirect to new entry page
    
    return render(request, "encyclopedia/new.html")


def edit_entry(request, entry_name):
    """Allow users to edit an existing entry."""
    
    if request.method == "POST":
        content = request.POST.get("entry_body", "").strip()
        
        if not content:
            return render(request, "encyclopedia/edit.html", {
                "title": entry_name,
                "content": util.get_entry(entry_name),
                "error": "Content cannot be empty."
            })

        util.save_entry(entry_name, content)  # Save edited content
        return redirect("encyclopedia:entry", entry_name=entry_name)  # Redirect to entry page

    # Load existing content when accessing the edit page
    content = util.get_entry(entry_name)


    return render(request, "encyclopedia/edit.html", {
        "title": entry_name,
        "content": content
    })

def random_entry(request):
    
    entries = util.list_entries()  # Get all entries
    random = randint(0, len(entries)-1) # Generate a random integer

    return redirect("encyclopedia:entry", entry_name=entries[random])  # Redirect using the random number
