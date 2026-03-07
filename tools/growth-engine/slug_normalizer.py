import re

def normalize(slug):
    slug = slug.lower()
    slug = slug.replace("_","-")
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+','-',slug)
    return slug.strip("-")
