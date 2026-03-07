import os

count=0

for root,dirs,files in os.walk("."):

    for f in files:

        if f.endswith(".html"):

            count+=1

print("Total HTML pages:",count)
