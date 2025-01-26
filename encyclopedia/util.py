import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2
# Imports that reads the names of files in a certain directory
from os import listdir
from os.path import isfile, join
import random



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def convert_markdown(markdown_info):
    """
    Converts markdown into html. If markdown is 'None' then 'None' is returned.
    """
    if markdown_info != None:
        return markdown2.markdown(markdown_info)
    else:
        return None


def find_similar_entries(search_query):
    """
    Returns names of similar entries to the search query
    """
    
    # Get names of all entries 
    all_entries = [f.replace(".md","") for f in listdir("entries") if isfile(join("entries", f))]
    
    # Get similar files
    
    similar_entries = [f for f in all_entries if search_query.lower() in f.lower()]
    
    return similar_entries

def random_entry_title():
    """
    Rerturns the title for a random existing entry.
    """
    return (random.choice(list_entries())).replace(".md","")