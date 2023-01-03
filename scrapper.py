from bs4 import BeautifulSoup
import requests
import urllib
import csv
import pandas as pd


HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})

urls = ['https://www.amazon.in/s?k=laptop&i=computers&rh=n%3A1375424031%2Cp_n_feature_twenty-three_browse-bin%3A27387161031%7C27387168031%2Cp_72%3A1318476031&dc&crid=21X0ZDNORCOI&qid=1668161253&rnid=1318475031&sprefix=laptop%2Caps%2C232&ref=sr_pg_1',
'https://www.amazon.in/s?k=laptop&i=computers&rh=n%3A1375424031%2Cp_n_feature_twenty-three_browse-bin%3A27387161031%7C27387168031%2Cp_72%3A1318476031&dc&page=2&crid=21X0ZDNORCOI&qid=1668164365&rnid=1318475031&sprefix=laptop%2Caps%2C232&ref=sr_pg_2',
'https://www.amazon.in/s?k=laptop&i=computers&rh=n%3A1375424031%2Cp_n_feature_twenty-three_browse-bin%3A27387161031%7C27387168031%2Cp_72%3A1318476031&dc&page=3&crid=21X0ZDNORCOI&qid=1668164370&rnid=1318475031&sprefix=laptop%2Caps%2C232&ref=sr_pg_3',
'https://www.amazon.in/s?k=laptop&i=computers&rh=n%3A1375424031%2Cp_n_feature_twenty-three_browse-bin%3A27387161031%7C27387168031%2Cp_72%3A1318476031&dc&page=4&crid=21X0ZDNORCOI&qid=1668164800&rnid=1318475031&sprefix=laptop%2Caps%2C232&ref=sr_pg_4']

base_url = 'https://www.amazon.in'

db = open('./data.csv','w')
writer = csv.writer(db)

dict = {'Title':pd.NA,'Brand':pd.NA,'Standing screen display size':pd.NA,'Resolution':pd.NA,'Processor Brand':pd.NA,'Processor Type':pd.NA,'Processor Count':pd.NA,'RAM Size':pd.NA,'Memory Technology':pd.NA,'Price':pd.NA}

writer.writerow(list(dict.keys())+['Customer Review','Link'])


for url in urls:

    resp = requests.get(url,headers=HEADERS)
 

    search_soup = BeautifulSoup(resp.text,features='lxml')

    # get all the a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal links
    links = search_soup.find_all('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    ctr = 0
    print('Total: ',len(links))

    for link in links:
        ctr+=1
        print('Current:',ctr)
        laptop = base_url+link['href']
        resp = requests.get(laptop,headers=HEADERS)
        laptop_soup = BeautifulSoup(resp.text,features='lxml')
        dict['Title']=laptop_soup.find('span',class_ = 'a-size-large product-title-word-break').text.strip()
        dict['Price']=laptop_soup.find('span',class_='a-price-whole')

        if(dict['Price']==None):
            print(laptop)
            continue
        else:
            dict['Price']=dict['Price'].text
        
        rating = laptop_soup.find('span',class_='a-icon-alt')

        if(rating!=None):
            rating = rating.text
        else:
            rating = pd.NA
        
        ths = laptop_soup.find_all('th',class_ = "a-color-secondary a-size-base prodDetSectionEntry")
        tds = laptop_soup.find_all('td',class_="a-size-base prodDetAttrValue")

        for i in range(len(ths)):
            if(ths[i].text.strip() in dict.keys()):
                dict[ths[i].text.strip()]=tds[i].text.strip()[1:]


        print(dict['Brand'])
        writer.writerow(list(dict.values())+[rating,laptop])

        for k in dict.keys():
            dict[k]=pd.NA


