import requests
from requests_html import HTMLSession
import bs4 
import os
import re

#THIS FUNCTION GET THE TEXT FROM A WEBSITE ADDRESSED BY AN INPUT LINK

def fetchcodex(link):
    linko = requests.get(link)
    print(linko.text)
    return linko

# THIS FUNCTION GOES TROUGH ALL NODES WITH A DEFINED ID IN A DEFINED WEBSITE, ACCESSES THE LINKS CONTAINED THEREIN AND PRINTS THE TEXT INTO A TXT DOCUMENT, PARSED OF ANY HTML SYNTAX 

def go33(link, n_class="", n_id=""):
    sauce = requests.get(link) #.text?
    soup = bs4.BeautifulSoup(sauce.content, 'html.parser') #'lxml'? apparently same output
    codices = soup.find_all('a') 
    asession = HTMLSession()
    r = asession.get(link)
    r.html.render()
    
    #website = get_website(link)
    print(r.html.absolute_links)
    about = r.html.find('#codices', first=True)
    a = about.find('a')
    print(a)
    #print(about.text)
    #print(about.absolute_links)
    print(codices)
    # continue to navigate to the next "a"
    #for dynamic webistes as this one one needs Selenium or requests-html
    for h in codices:
        href = [h.get('href')]
        if re.match(r'.*kodexek/.*$', str(href)):
        #if re.match(r'.*\.txt$', str(href)):
            #session = HTMLSession()
            #q = session.get(href)
            #print(q)
            text = fetchcodex(href)
            print(text)
     
 # SE SI TRATTA DI UN SITO WEB DINAMICO, SI POTREBBE CREARE UN LOOP PER ACCEDERE IL LINK, COMPOSTO DA UNA PARTE GENERALE E DALLA PARTE SPECIFICA (GLI ELEMENTI SPECIFICI DI CIASCUN LINK SARANNO SALVATI IN UNA LISTA)