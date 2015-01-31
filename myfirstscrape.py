# this is what makes the magic happen (i.e. parses the HTML)
from bs4 import BeautifulSoup
# doing our civic duty and being kind to the server
import time
# the HTTP library for Python we use to pull URLs
import requests
# pulling in python's csv module
import csv

# luckily, every URL begins this way with one parameter (key, which in this case is the council file no)
baseurl = 'http://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber='

# first, we create a new list comprehension that we're about to fill
urllist = []

# i have a list of file numbers i need, which we'll use to add on to the base URL
# first we want to map that info (file nos) into a dict using DictReader
with open('rewardsfilenos.csv') as csvfile:
    reader = csv.DictReader(csvfile)

# then, we'll want to add the base URL to every file number to get all the council file URLs
    for row in reader:
        url = baseurl + (row['Council File No.'])
        urllist.append(url)
    
# then, we want to write a text file with the complete URLs separated by new lines
# just so we have it
with open('urls.txt', 'w') as outfile:
    urls = '\n'.join(urllist)
    outfile.write(urls)
    outfile.close()

# now, we want to write a new csv where we'll put our scraped data
with open('names.csv', 'w') as finalcsvfile:
    writer = csv.writer(finalcsvfile)
    # the first row is our header row
    writer.writerow(['title', 
    	'intro_date', 
    	'last_changed_date', 
    	'exp_date', 
    	'ref_numbers', 
    	'direct_to_council', 
    	'dist', 
    	'mover', 
    	'second', 
    	'amount', 
    	'duration', 
    	'publish_date', 
    	'expire_date'])

    # now we'll go back to that urllist we made and write a loop to go through for every URL
    for url in urllist:
    	# Requests grabs each URL. Here we create a response object called R.
        r = requests.get(url)
        # then we run the HTML text that Requests has pulled through BeautifulSoup 
        soup = BeautifulSoup(r.text)
        
        # because fields show up on some files and not others, we'll want to test for the field before grabbing it
        # so we don't run into errors. If the field doesn't exist, we'll reassign that variable to a blank space. 
        try:
            title = soup.find("div", class_="reclabel", text="Title").next_sibling.next_sibling.string.strip()
        except AttributeError:
            title = ''
            
        try:
            intro_date = soup.find("div", class_="reclabel", text="Date Received / Introduced").next_sibling.next_sibling.string.strip()
        except AttributeError:
            intro_date = ''
                
        try:
            last_changed_date = soup.find("div", class_="reclabel", text="Last Changed Date").next_sibling.next_sibling.string.strip()
        except AttributeError:
            last_changed_date = ''
                
        try:
            exp_date = soup.find("div", class_="reclabel", text="Expiration Date").next_sibling.next_sibling.string.strip()
        except AttributeError:
            exp_date = ''
                
        try:
            ref_numbers = soup.find("div", class_="reclabel", text="Reference Numbers").next_sibling.next_sibling.string.strip()
        except AttributeError:
            ref_numbers = ''
                
        try:
            direct_to_council = soup.find("div", class_="reclabel", text="Direct to Council").next_sibling.next_sibling.string.strip()
        except AttributeError:
            direct_to_council = ''
                
        try:
            dist = soup.find("div", class_="reclabel", text="Council District").next_sibling.next_sibling.string.strip()
        except AttributeError:
            dist = ''
            
        try:
            mover = soup.find("div", class_="reclabel", text="Mover").next_sibling.next_sibling.text.strip()
        except AttributeError:
            mover = ''
                
        try:
            second = soup.find("div", class_="reclabel", text="Second").next_sibling.next_sibling.text.strip()
        except AttributeError:
            second = '' 
                
        try:
            amount = soup.find("div", class_="reclabel", text="Reward Amount").next_sibling.next_sibling.text.strip()
        except AttributeError:
            amount = ''
                
        try:
            duration = soup.find("div", class_="reclabel", text="Reward Duration").next_sibling.next_sibling.text.strip()
        except AttributeError:
            duration = ''
                
        try:
            publish_date = soup.find("div", class_="reclabel", text="Reward Publish Date").next_sibling.next_sibling.text.strip()
        except AttributeError:
            publish_date = ''
                    
        try:
            expire_date = soup.find("div", class_="reclabel", text="Reward Expire Date").next_sibling.next_sibling.text.strip()
        except AttributeError:
            expire_date = ''
        
        # so we can keep track of where the scraper is at, we tell it to print the title of the file it's working on
        print "Scraping: '" + title + "'"
        
        # lastly, we write a row with all those variables
        writer.writerow([title,
                        intro_date, 
                        last_changed_date, 
                        exp_date, 
                        ref_numbers, 
                        direct_to_council, 
                        dist, 
                        mover, 
                        second, 
                        amount, 
                        duration, 
                        publish_date, 
                        expire_date])

    	# before returning to the beginning of the loop, give the server a rest
        time.sleep(5)

        # rejoice
        print "Voila!"

