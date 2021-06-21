#Objective: to collect data for the RWJ and Institute of Medicine's Future of Nursing 2020 Initiative re: interprofessional collaboration among nurses. 
#Scrape all the articles published in NEJM in 2020 to get the articles' and authors' metadata. 
#Use resulting output to estimate a count of how many articles were (co)-authored by nurses (any authors who have RN, BSN, DNP, NP, etc. following their name)


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import time


nejm2020 = requests.get('https://www.nejm.org/medical-archives/2020')

json_data = []

base_url = 'https://www.nejm.org'

#Get all issue links.
soup1=BeautifulSoup(nejm2020.text, 'lxml')

links = [a.get('href') for a in soup1.find_all('a', href=re.compile('^/toc/nejm/382/'))]
for i in links:
    issuelink = base_url + i
    openissue = requests.get(issuelink)
    soup2=BeautifulSoup(openissue.text, 'lxml')
    print(issuelink)

#Get all article links. 
    for a in soup2: 
        doi = [a.get('href') for a in soup2.find_all('a', {"class":"m-teaser-item__link"})]

  
#Metadata for each article. 
    for each in doi:
        nejmdict={"articletype":"NaN", "title":"NaN", "date":"NaN", "author":"NaN", "url":"NaN"}
        articleurl=base_url + each
        time.sleep(5)
        openarticle=requests.get(articleurl)
        soup3=BeautifulSoup(openarticle.text, 'lxml')
        
        articletype = soup3.find('p', {"class":re.compile("^m-article-header__type")})     
        title = soup3.find("span",{"class":"title_default"})
        date = soup3.find("a", {"href":re.compile("^/toc/nejm/382/")})
        author  = soup3.find("ul",{"class":"m-article-header__authors f-ui"})
        url = articleurl

        print(title)
   
        if articletype is not None:
            nejmdict['articletype']=articletype.text.strip()
                
        if title is not None:
            nejmdict['title']=title.text.strip()
        
        if date is not None:
            nejmdict['date']=date.text.strip()
                
        if author is not None:
            nejmdict['author']=author.text.strip()
                
        if url is not None:
            nejmdict['url']=url 
                            
        json_data.append(nejmdict)
    
    print(date)

df=pd.DataFrame(json_data)
df.to_csv('nejm_jan_june_2020.csv')

print("Saved")
