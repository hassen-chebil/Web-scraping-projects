# -*- coding: utf-8 -*-
"""Coronasvirus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uvAi9zaxbltSoMAqiWGzaL0iFHSiDfMb
"""

#installation of packages
!pip install deep-translator

# Requests module is used for making HTTP requests
import requests
# re module is used for working with regular expressions
import re
import urllib.request
# bs4 module is used for parsing and navigating html and xml documents
from bs4 import BeautifulSoup
# deep_translator module is used for translation tasks, specifically using GoogleTranslator
from deep_translator import GoogleTranslator
# json module is used for handling json data 
import json
# Pandas module is used for data manipulation and data analysis
import pandas as pd
# datetime module is used for working with date and time
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

#Getting available countries list for help
countrieslinks = []
links = []
aTags = BeautifulSoup(requests.get("https://www.worldometers.info/coronavirus/#countries").content, 'html.parser').find('table', {'id': 'main_table_countries_today'}).find('tbody').findAll('a', {'class': 'mt_a'})
for a in aTags:
  links.append(a['href'][a['href'].index('/')+1:-1])
  countrieslinks.append(f"Insert ==> {a['href'][a['href'].index('/')+1:-1]} <== for: {a.text}")

#Getting the equivalent argument for each country to use in the GET request
link_DataCountry = {}
for counter, link in enumerate(links):
  try:
    tgt = BeautifulSoup(requests.get("https://www.worldometers.info/coronavirus/country/"+link+"/").content, 'html.parser').find('a', {'class': 'load-more__btn'})
    link_DataCountry[link] = tgt['data-country']
    print(f"({counter}/{len(links)}) ** {link} Done! moving to next...")
  except:
    print(f"({counter}/{len(links)}) ** {link} Not found! moving to next...")



#Inputing the desired country and getting its latest cases
paysTarget = input('Enter country name: ').lower()
try:
    soup = BeautifulSoup(requests.get(f"https://www.worldometers.info/coronavirus/news-block/news_main_updates.php?fd=lm_{today}&country={link_DataCountry[paysTarget]}&days_count=14").content, 'html.parser').findAll('button', {'class': 'btn btn-light date-btn'})
    dates_En = []
    cases_En = []
    for date in soup:
        c = date.find_next_sibling('div', {'class': 'newsdate_div'}).findChild('li', {'class': 'news_li'})
        cases_En.append(c.text[:c.text.index('in')].strip())
        dates_En.append(date.text.strip())    

    new_cases_En = []
    new_deaths_En = []

    for e in cases_En:
        if "new cases" in e and "new deaths" in e:
            new_cases_En.append(e.split('and')[0].strip())
            new_deaths_En.append(e.split('and')[1].strip())
        elif "new cases" in e:
            new_cases_En.append(e)
            new_deaths_En.append("No new deaths")
        elif "new deaths" in e:
            new_cases_En.append("No new cases")
            new_deaths_En.append(e)
        else:
            new_cases_En.append("No new cases")
            new_deaths_En.append("No new deaths")

    new_cases_Fr = [GoogleTranslator(source='en', target='fr').translate(e) for e in new_cases_En]
    new_deaths_Fr = [GoogleTranslator(source='en', target='fr').translate(e) for e in new_deaths_En]
    dates_Fr = [GoogleTranslator(source='en', target='fr').translate(e) for e in dates_En]

    coronaDict_En = {
        "date": dates_En,
        "new_cases": new_cases_En,
        "new_deaths": new_deaths_En
    }
    df_En = pd.DataFrame(coronaDict_En)
    print("Anglais:\n", df_En)

    coronaDict_Fr = {
        "date": dates_Fr,
        "nouveaux_cas": new_cases_Fr,
        "nouveaux_deces": new_deaths_Fr
    }
    df_Fr = pd.DataFrame(coronaDict_Fr)
    print("Francais:\n", df_Fr)

except Exception as e:
    print(e, '\nCountry not in list!\nTo know what to put check ==> countrieslinks <== variable!')






