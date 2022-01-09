#!/usr/bin/env python
# coding: utf-8

# In[1]:


try:
    developmentMode = True
    callAPI = True
    Local_API_Laravel = 'http://127.0.0.1:8000/api/news/store'
    Live_API_Laravel = 'https://pakteki.com/api/news/store'
    Live_API_Node = 'http://3.142.50.232:5000/api/news/all'
    API = Live_API_Laravel
    Dawn = True
    Geo = True
    Ary = True
    Ptv = True
    Express = True
    Sama = True
    Duniya = True
    Bol = True
    Abbtak = True
    Ninetytwonews = True
    Abbtak = True
    Twentyfournews = False
    Gnnnews = True
    Dailypakistan = False
    Newsone = True
    Mashion = True
    Mangobaaz = True
    Sunday = True
    Urdunews = True
    Urdupoint = True
    Tribune = True
    Hellopakistanmag = True
    Zaiqa = False
    Islamicinfoenglish = False
    Islamicinfourdu = False
    Royal = True
    Neonews = False
    City42 = False
    Jang = True

    # libraries
    from bs4 import BeautifulSoup,Comment
    import requests
    import csv
    from datetime import date
    import pandas as pd
    import time

    # Array stucture for storing data
    columns = ['title','category', 'channel', 'permalink', 'image_src', 'date_time', 'description', 'fetching_date', 'language']
    rows, cols = (0, 9)
    data = [[0]*cols]*rows
except:
    print('exception in importing libraries ..')


# In[2]:


try:
    sources = [
                ["https://www.dawn.com/trends/coronavirus", "Covid", "Dawn"],
               ["https://www.dawn.com/sport", "Sports", "Dawn"], 
               ["https://www.dawn.com/world", "International", "Dawn"],
               ["https://images.dawn.com/art-culture", "LifeStyle-Culture", "Dawn"],
               ["https://www.dawn.com/tech", "IT-Science", "Dawn"]
               ]
    if Dawn:
        counter = 0
        print('Getting Dawn News...')
        i = 1
        permalinkDawnNews = []
        for source in sources:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article', class_='box'):
                if i <= 6:
                    try:
                        permalink = article.find('a', class_='story__link')['href']
                        permalinkDawnNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkDawnNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')

            for div in soup.find_all('div',class_='w-full max-w-screen-md xl:pr-4'):
                try:
                    detail_title = div.find('div',class_='template__header').h2.a.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='template__header').find('div',class_='slideshow').find('div',class_='slideshow__slide').figure.div.picture.img['src']
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='template__main').find('div',class_='story__content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1

                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink':detail_page_source[0] ,
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter)) 
except:
    print('exception in ' + source[2])


# In[3]:


try:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    sources2 = [
                ["https://arynews.tv/category/international-2", "International", "ARY"],
                ["https://arynews.tv/category/sci-techno/", "IT-Science", "ARY"], 
                ["https://arynews.tv/category/health-2/", "Health", "ARY"],
                ["https://arynews.tv/category/business/","Business","ARY"],
                ["https://arynews.tv/category/pakistan/","National-local","ARY"],
               ]
    if Ary == True:
        print('Getting ARY News...')
        i = 1
        counter = 0
        permalinkArrayARY = []
        for source in sources2:
            sourceHTML = requests.get(source[0],headers=headers).text
            soup = BeautifulSoup(sourceHTML,'lxml')
            for div in soup.find_all('div', class_='td-module-container'):
                if i <= 6:
                    try:
                        permalink = div.find('div',class_='td-module-meta-info').h3.a['href']
                        permalinkArrayARY.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayARY
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0],headers=headers).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div', class_='tdi_74'):
                try:
                    detail_title = div.find('div',class_='tdb_title').div.h2.text
                except:
                    detail_title = ''

                try:  
                    start = div.find('div',class_='tdb_single_bg_featured_image').style.find_next_sibling().text.find('url')
                    end = div.find('div',class_='tdb_single_bg_featured_image').style.find_next_sibling().text.find(')')
                    high_resolution_img_data = div.find('div',class_='tdb_single_bg_featured_image').style.find_next_sibling().text
                    high_resolution_image = high_resolution_img_data[start:end][5:-1]
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.div.div.find('div',class_='td_block_wrap tdb_single_content tdi_78 td-pb-border-top td_block_template_1 td-post-content test tagdiv-type').div.find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[4]:


try:
    sources3 = [
                ["https://www.geo.tv/category/world", "International", "GEO"],
                ["https://www.geo.tv/category/sci-tech", "IT-Science", "GEO"], 
                ["https://www.geo.tv/category/sports", "Sports", "GEO"],
                ["https://www.geo.tv/category/entertainment", "Entertainment", "GEO"],
                ["https://www.geo.tv/category/business","Business","GEO"],
                ["https://www.geo.tv/food","Gourmet","GEO"],
               ]
    if Geo == True:
        print('Getting GEO News...')
        i = 1
        counter = 0
        permalinkArrayGeoNews = []
        for source in sources3:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div', class_='col-xs-6 col-sm-6 col-lg-6 col-md-6 singleBlock'):
                if i <= 6:
                    try:
                        permalink = div.div.ul.li.a['href']
                        permalinkArrayGeoNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayGeoNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='column-right'):
                try:
                    detail_title = div.find('div',class_='left').find('div',class_='story-area').h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='story-area').find('div',class_='content-area').find('div',class_='medium-insert-images').figure.img['src']
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='left').find('div',class_='story-area').find('div',class_='content-area').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:     ' + detail_page_source[0].strip())
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image.strip())
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[5]:


try:
    sources4 = [
                ["https://ptv.com.pk/ptvWorld/news/National", "National-Local", "PTV"],
                ["https://ptv.com.pk/ptvWorld/news/Cricket", "Sports", "PTV"], 
                ["https://ptv.com.pk/ptvWorld/news/International", "International", "PTV"]
                ]
    if Ptv == True:
        print('Getting PTV News...')
        counter = 0
        i = 1
        permalinkArrayPTV = []
        for source in sources4:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('ul', class_='big'):
                if i <= 6:
                    try:
                        permalink = article.li.div.div.h4.a['href']
                        permalinkArrayPTV.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayPTV
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='page'):
                try:
                    detail_title = div.find('div',class_='row').find('div',class_='column_2_3').find('div',class_='row').div.div.h3.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='row').find('div',class_='column_2_3').find('div',class_='row').div.img['src']
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description = div.find('div',class_='row').find('div',class_='column_2_3').find('div',class_='row').div.div.div.p.text.replace('\n','')
                except:
                    detail_description = '.'
                counter = counter + 1
                language = 'English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': permalink,
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[6]:


try:
    sources5 = [["https://www.express.pk/health/", "Health", "Express"],
                ["https://www.express.pk/sports/", "Sports", "Express"],
                ["https://www.express.pk/world/", "International", "Express"],
                ["https://www.express.pk/science/", "IT-Science", "Express"],
                ["https://www.express.pk/pakistan/", "National-Local", "Express"],
                ["https://www.express.pk/religion/", "Islam", "Express"]
               ]
    if Express == True:
        print('Getting Express News...')
        counter = 0
        i = 1
        permalinkArrayExpressNews = []
        for source in sources5:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='cstoreyitem'):
                if i <= 6:
                    try:
                        permalink = div.div.a['href']
                        permalinkArrayExpressNews.append([permalink,source[1],source[2]])
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayExpressNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='primary'):
                try:
                    detail_title = div.div.h1.text.replace('\xa0','')
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.div.find('div',class_='span-10').div.div.img['src']
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.div.find('div',class_='span-16 story-cont').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\n','').replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': permalink,
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[7]:


try:
    sources6 = [
                ["https://www.samaa.tv/lifeandstyle/", "National-Local", "SAMAA"],
                ["https://www.samaa.tv/sports/", "Sports", "SAMAA"], 
                ["https://www.samaa.tv/news/", "National-Local", "SAMAA"],
                ["https://www.samaa.tv/technology/", "IT-Science", "SAMAA"]
                ]
    if Sama == True:
        print('Getting SAMA News...')
        counter = 0
        i = 1
        permalinkArraySAMANews = []
        for source in sources6:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='categorycolumn'):
                if i <= 6:
                    try:
                        permalink = div.find('div',class_='row').find('div',class_='respnb1').a['href']
                        permalinkArraySAMANews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArraySAMANews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='col-md-8'):
                try:
                    detail_title = div.div.h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = ''
                    high_resolution_img_parent = div.find('div',class_='detail-10 detailnews').center
                    high_resolution_img_text = high_resolution_img_parent.find(text=lambda text:isinstance(text, Comment))
                    high_resolution_img_soup = BeautifulSoup(high_resolution_img_text , 'lxml')
                    high_resolution_image = high_resolution_img_soup.img['src']
                except:
                    high_resolution_img = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='detailnews').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\n','').replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1   
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources7 = [
                ["https://dunyanews.tv/en/World", "International", "Dunya"],
                ["https://dunyanews.tv/en/Cricket", "Sports", "Dunya"], 
                ["https://dunyanews.tv/en/Pakistan", "National-Local", "Dunya"],
                ["https://dunyanews.tv/en/Technology", "IT-Science", "Dunya"],
                ["https://dunyanews.tv/en/Business","Business","Dunya"]
               ]
    if Duniya == True:
        counter = 0
        i = 1
        print('Getting Duniya News...')
        permalinkArrayDuniyaNews = []
        for source in sources7: 
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article'):
                if i <= 6:
                    if article.div.a['href']:
                        try:
                            permalink = 'https://dunyanews.tv' + article.div.a['href']
                            permalinkArrayDuniyaNews.append([permalink,source[1],source[2]])
                        except:
                            permalink = ''
                    else:
                        try:
                            permalink = 'https://dunyanews.tv' + article.h3.a['href']
                            permalinkArrayDuniyaNews.append([permalink,source[1],source[2]])
                        except:
                            permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayDuniyaNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')

            for div in soup.find_all('div',{'id':'main-heading'}):

                try:
                    detail_title = div.find('div',class_='date').h2.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='date').find('div',{'id':'post_content'}).article.find('div',class_='pic').img['src']
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='date').find('div',{'id':'post_content'}).article.find('div',class_='post_content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\n','').replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1

                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': permalink,
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources8 = [
                ["https://www.bolnews.com/sports", "Sports", "Bol"],
                ["https://www.bolnews.com/international/", "International", "Bol"],
                ["https://www.bolnews.com/health/", "Health", "Bol"],
                ["https://www.bolnews.com/entertainment/", "Entertainment", "Bol"],
                ["https://www.bolnews.com/technology/", "IT-Science", "Bol"],
                ["https://www.bolnews.com/business/","Business","Bol"]
                ]
    if Bol == True:
        counter = 0
        print('Getting Bol News...')
        i = 1
        permalinkArrayBolNews = []
        for source in sources8:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='catesquarebox'):
                if i <= 6:
                    try:
                        permalink = div.a['href']
                        permalinkArrayBolNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayBolNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for main in soup.find_all('main'):
                try:
                    detail_title = main.article.find('div',class_='headingsec').h1.text
                except:
                    detail_title = ''

                try:
                    if('https' in main.article.find('figure',class_='featuredimg').img['src']):
                        high_resolution_image = main.article.find('figure',class_='featuredimg').img['src']

                    else:
                        high_resolution_image = 'https://bolnews.s3.amazonaws.com/' + main.find('article',class_='infinite-post active').find('figure',class_='featuredimg').img['src']

                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = main.article.find('div',class_='content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\n','').replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1     
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources22 = [
                ['https://abbtakk.tv/en/category/entertainment/','Entertainment','AbbTakk'],
                 ['https://abbtakk.tv/en/category/world/','International','AbbTakk'],
                 ['https://abbtakk.tv/en/category/pakistan/','National-local','AbbTakk'],
                 ['https://abbtakk.tv/en/category/sports/','Sports','AbbTakk'],
                ]
    if Abbtak == True:
        print('Getting Abbtakk News...')
        counter = 0
        i = 1
        permalinkArrayAbbtakNews = []
        for source in sources22:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article',class_='penci-imgtype-landscape'):
                if i <= 6:
                    try:
                        permalink = article.find('div', class_='entry-text').header.h2.a['href']
                        permalinkArrayAbbtakNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
                i = 1
        detail_source = permalinkArrayAbbtakNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for main in soup.find_all('main'):
                try:
                    detail_title = main.find('div',class_='entry-media').div.div.find('div',class_='penci-featured-col-1').div.div.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = main.find('div',class_='entry-media').div.div.find('div',class_='penci-featured-col-2').div.div['style'][22:-24]       
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = main.find('div',class_='penci-entry-content entry-content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }      

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))   
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources19 = [
                 ['https://92newshd.tv/category/pakistan','National-local','92News'],
                 ['https://92newshd.tv/category/sports','Sports','92News'],
                 ['https://92newshd.tv/category/Health','Health','92News'],
                 ['https://92newshd.tv/category/Entertainment','Entertainment','92News']
                ]
    if Ninetytwonews == True:
        counter = 0
        print('Getting 92 News...')
        i = 1
        permalinkArray92News = []
        for source in sources19:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='sub-posts'):
                if i <= 6:
                    try:
                        permalink = 'https://92newshd.tv' + div.a['href']
                        permalinkArray92News.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
                i = 1
        detail_source = permalinkArray92News
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='post-details'):
                try:
                    detail_title = div.h1.text

                except:
                    detail_title = ''

                try:
                    high_resolution_image = div.img['data-src']      
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='content_detail').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1 
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter)) 
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources15 = [
                 ['https://www.24newshd.tv/pakistan','Local','24NewsHD'],
                 ['https://www.24newshd.tv/world','International','24NewsHD'],
                 ['https://www.24newshd.tv/sports','Sports','24NewsHD'],
                 ['https://www.24newshd.tv/entertainment','Entertainment','24NewsHD'],
                 ['https://www.24newshd.tv/opinion','Blog','24NewsHD']
                ]
    if Twentyfournews == True:
        counter = 0
        print('Getting 24News Channel...')
        i = 1
        permalinkArray24News = []
        for source in sources15:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('div',class_='category-post-block'):
                if i <= 6:
                    try:
                        permalink = article.div.div.a['href']
                        permalinkArray24News.append([permalink,source[1],source[2]])
                        counter = counter + 1
                        print(permalink)
                    except:
                        permalink = ''
                        print('exp')
                    i = i + 1
                i = 1
        detail_source = permalinkArray24News
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='detail-page'):
                try:
                    detail_title = div.h1.text

                except:
                    detail_title = ''

                try:
                    high_resolution_image = div.img['data-src']

                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='content_detail').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                language='English'
                counter = counter + 1
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if False:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources11 = [
                 ['https://gnnhd.tv/category/pakistan','National-local','GNN'],
                 ['https://gnnhd.tv/category/regional','National-local','GNN'],
                 ['https://gnnhd.tv/category/technology','IT-science','GNN'],
                 ['https://gnnhd.tv/category/business','Business','GNN']
                ]
    if Gnnnews == True:
        counter = 0
        i = 1
        print('Getting GNN News...')
        permalinkArrayGNNnews = []
        for source in sources11:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for a in soup.find('div',class_='mvp-feat5-small-sub').find_all('a'):
                if i <= 6:
                    try:
                        permalink = 'https://gnnhd.tv' + a['href']
                        permalinkArrayGNNnews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
            for a in soup.find('div',class_='mvp-feat5-mid-sub-wrap').find_all('a'):
                if i <= 6:
                    try:
                        permalink = 'https://gnnhd.tv' + a['href']
                        permalinkArrayGNNnews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayGNNnews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',{'id':'mvp-post-main'}):
                try:
                    detail_title = div.header.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = 'https://gnnhd.tv'+div.find('div',{'id':'mvp-post-feat-img'}).img['src'] 
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',{'id':'mvp-content-main'}).find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources9 = [
                 ['https://en.dailypakistan.com.pk/pakistan','National-local','DailyPakistan'],
                 ['https://en.dailypakistan.com.pk/sports','Sports','DailyPakistan'],
                 ['https://en.dailypakistan.com.pk/world','International','DailyPakistan'],
                 ['https://en.dailypakistan.com.pk/opinion','Blog','DailyPakistan'],
                 ['https://en.dailypakistan.com.pk/national','National-local','DailyPakistan'],
                 ['https://en.dailypakistan.com.pk/business','Business','DailyPakistan'],
                ]
    if Dailypakistan == True:
        print('Getting Daily Pakistan News...')
        i = 1
        counter = 0
        permalinkArrayDPnews = []
        for source in sources9:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='col-sm-6'):
                if i <= 6:
                    try:
                        permalink =  div.div.div.find('div',class_='tt-news-img').a['href']
                        permalinkArrayDPnews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayDPnews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',{'id':'mvp-post-main'}):
                try:
                    detail_title = div.header.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = 'https://gnnhd.tv'+div.find('div',{'id':'mvp-post-feat-img'}).img['src'] 
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',{'id':'mvp-content-main'}).find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }    
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if False:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources18 = [
                 ['https://www.newsone.tv/pakistan-news','National-local','Newsone'],
                 ['https://www.newsone.tv/sports','Sports','Newsone'],
                 ['https://www.newsone.tv/world','International','Newsone'],
                 ['https://www.newsone.tv/blogs','Blog','Newsone'],
                 ['https://www.newsone.tv/entertainment','Entertainment','Newsone'],
                 ['https://www.newsone.tv/technology','IT-Science','Newsone'],
                 ['https://www.newsone.tv/lifestyle','Health','Newsone'],
                ]
    if True == True:
        print('Getting Newsone...')
        i = 1
        counter = 0
        permalinkArrayNewsOne = []
        for source in sources18:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('div',class_='eq-blocks'):
                if i <= 6:
                    try:
                        permalink =  article.div.div.h2.a['href']
                        permalinkArrayNewsOne.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1   
        detail_source = permalinkArrayNewsOne
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='single-page-tem'):
                try:
                    detail_title = div.section.div.div.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = div.section.div.find('div', class_='single-post').find('div', class_='post-content').div.img['src'] 
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.section.div.find('div', class_='single-post').find('div', class_='post-content').article
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title.strip(),
                            'description': detail_description.strip(),
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description.strip()[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources10 = [
                 ['https://www.urdupoint.com/pakistan','National-local','Urdupoint'],
                 ['https://www.urdupoint.com/sports','Sports','Urdupoint'],
                 ['https://www.urdupoint.com/international','International','Urdupoint'],
                 ['https://www.urdupoint.com/showbiz','Entertainment','Urdupoint'],
                ]
    if Urdupoint == True:
        print('Getting Urdupoint News...')
        i = 1
        counter = 0
        permalinkArrayUrduPoint = []
        for source in sources10:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for a in soup.find('div',class_='list_hlaf_block').find_all('a'):
                if i <= 6:
                    try:
                        permalink = a['href']
                        permalinkArrayUrduPoint.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayUrduPoint
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',{'id':'main_content'}):
                try:
                    detail_title = div.find('div',class_='main_bar').div.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = div.find('div',class_='news_article').find('div', class_='ac').picture.img['src']
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description = div.find('div',class_='main_bar').div.find('div',class_='detail_txt').a.text.replace('\n','').replace('\xa0','') + div.find('div',class_='main_bar').div.find('div',class_='detail_txt').text.replace('\n','').replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }  

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources12 = [
                 ['https://www.neonetwork.pk/international','International','NeoNetwork'],
                 ['https://www.neonetwork.pk/blogs','Blog','NeoNetwork'],
                 ['https://www.neonetwork.pk/entertainment','Entertainment','NeoNetwork'],
                ]
    if Neonews == True:
        print('Getting Neo News...')
        i = 1
        permalinkArrayNeoNews = []
        for source in sources12:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='min_height_for_large_widget'):
                if i <= 6:
                    try:
                        permalink = div.article.div.a['href']
                        permalinkArrayNeoNews.append([permalink,source[1],source[2]])
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayNeoNews

        # for detail_page_source in detail_source:
        #     sourceHtml = requests.get(detail_page_source[0]).text
        #     soup = BeautifulSoup(sourceHtml, 'lxml')
        #     for div in soup.find_all('div',{'id':'main_content'}):
        #         try:
        #             detail_title = div.find('div',class_='main_bar').div.h1.text
        # #             
        #         except:
        #             detail_title = ''
        #             
        #         try:
        #             high_resolution_image = div.find('div',class_='main_bar').div.figure.img['src']
        #                        
        #         except:
        #             high_resolution_image = 'no-image'
        #         try:
        #             date_time = time.ctime()
        #         except:
        #             date_time = ''
        #         try:
        #             detail_description = div.find('div',class_='main_bar').div.find('div',class_='detail_txt').a.text.replace('\n','') + div.find('div',class_='main_bar').div.find('div',class_='detail_txt').text.replace('\n','')
        # #             print(description)
        # #             detail_description_all = div.find('div',class_='content_detail').find_all('p')
        # #             detail_description = ''
        # #             for p in detail_description_all:
        # #                 detail_description = detail_description + p.text
        #         except:
        #             
        #         language='Urdu'
        #         values = {
        #                     'title': detail_title,
        #                     'description': detail_description,
        #                     'date': date_time,
        #                     'channel': source[2],
        #                     'image': high_resolution_image,
        #                     'permalink': detail_page_source[0],
        #                     'category': detail_page_source[1],
        #                     'fetching_date': date.today(),
        #                     'no_of_comments': 0,
        #                     'rating': 0,
        #                     'language':language,
        #                     'created_at': date.today(),
        #                     'updated_at': date.today(),
        #                     'comments': [],
        #                     'resgistered_views':[],
        #                     'no_of_registered_views':0,
        #                     'no_of_nonregistered_views':0,
        #                     }
        #         
        #         print('----------------')       
            # if(developmentMode):
            #         data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
            #         
            #         response = requests.post(url, data=values)
            #         if response.status_code == 429:
            #             time.sleep(int(response.headers["Retry-After"]))
            #     else:
            #         data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
            #         url = "http://3.142.50.232:5000/api/news/all"
            #         response = requests.post(url, data=values)
            #         if response.status_code == 429:
            #             time.sleep(int(response.headers["Retry-After"]))

except:
    print('exception in ' + source[2])
            
            


# In[ ]:


try:
    sources20 = [
                 ['https://royalnews.tv/?cat=2','National-local','Royalnews'],
                 ['https://royalnews.tv/?cat=3','International','Royalnews'],
                 ['https://royalnews.tv/?cat=4','Sports','Royalnews'],
                 ['https://royalnews.tv/?cat=5','Entertainment','Royalnews'],    
                ]
    if Royal == True:
        print('Getting Royal News...')
        i = 1
        counter = 0
        permalinkArrayNeoNews = []
        for source in sources20:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article',class_='format-standard'):
                if i <= 6:
                    try:
                        permalink = article.header.h1.a['href']
                        permalinkArrayNeoNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
                i = 1
        detail_source = permalinkArrayNeoNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article',class_='format-standard'):
                try:
                    detail_title = article.header.h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = article.header['style'][15:-45]
                except:
                    high_resolution_image = 'no-image'
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description = article.find('div',class_='entry-content').p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }        

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:   ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2]) 


# In[ ]:


try:
    sources23 = [
                 ['https://mashion.pk/category/mashup/fashion/','Fashion','Mashion'],
                 ['https://mashion.pk/category/mashup/celebrity/','Entertainment','Mashion'],    
                ]
    if Mashion == True:
        counter = 0
        print('Getting Mashion(showbiz) News...')
        i = 1
        permalinkArrayNeoNews = []
        for source in sources23:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='large-4'):
                if i<= 6:
                    try:
                        permalink = div.h2.a['href']
                        permalinkArrayNeoNews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayNeoNews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find('div',{'id':'content'}):
                try:
                    detail_title = div.div.find('div',class_='title').h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.div.div['data-bg'][4:-1]
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description = soup.find('div', class_='wpb_wrapper').div.div.p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
                break
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources24 = [
                 ['https://www.mangobaaz.com/recents','Blog','Mangobaaz'],
                 ['https://www.mangobaaz.com/category/showsha','Blog','Mangobaaz'],    
                ]
    if Mangobaaz == True:
        print('Getting Mangobaaz News...')
        i = 1
        counter = 0
        permalinkArrayMangobaaz = []
        for source in sources24:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')

            for a in soup.find_all('a',class_='block focus:outline-none'):
                if i <= 6:
                    try:
                        permalink ='https://www.mangobaaz.com' + a['href']
                        permalinkArrayMangobaaz.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayMangobaaz
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div', class_='leading-normal'):
                try:
                    detail_title = div.main.h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.div['style'][21:-2]
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description = div.main.article.p.text
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  

                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter)) 
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources25 = [
                 ['https://www.hellopakistanmag.com/fashion','Fashion','HelloPakistanMagazine'],
                 ['https://www.hellopakistanmag.com/entertainment','Entertainment','HelloPakistanMagazine'],
                ]
    if Hellopakistanmag == True:
        print('Getting HelloPakistanMagazine News...')
        i = 1
        counter = 0
        permalinkArrayHelloPakistanMag = []
        for source in sources25:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='col-md-6'):
                if i<= 6:
                    try:
                        permalink = div.find('div',class_='featured-content').a['href']
                        permalinkArrayHelloPakistanMag.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayHelloPakistanMag
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='article-content'):
                try:
                    detail_title = div.h3.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='article-image').img['src']
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources24 = [
                 ['https://sunday.com.pk/category/fashion/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/fashion-news/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/best-dressed/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/fashion-shoot/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/fashion-week/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/look-of-the-day/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/fashion/style-jury/','Fashion','SundayNews'],
                 ['https://sunday.com.pk/category/lifestyle/food/','Gourmet','SundayNews'],
                ]
    if Sunday == True:
        print('Sunday News...')
        i = 1
        counter = 0
        permalinkArraySundaynews = []
        for source in sources24:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='post'):
                if i<= 6:
                    try:
                        permalink = div.find('div',class_='row').find('div',class_='medium-7').div.find('div',class_='post-title').h5.a['href']
                        permalinkArraySundaynews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArraySundaynews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article'):
                try:
                    detail_title = article.find('div',class_='post-title-container').header.h1.text.replace('\t','').replace('\n','')   
                except:
                    detail_title = 'pakteki'
                try:
                    high_resolution_image = article.find('div',class_='thb-article-featured-image').img['data-src']

                except:
                    high_resolution_image = 'pakteki'

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = article.find('div',class_='thb-post-share-container').find('div',class_='post-content-container').find('div',class_='post-content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\xa0','')
                except:
                    detail_description = 'pakteki'
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:80])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources27 = [
        ["https://www.zaiqa.com/recipes/pakistani/","Gourmet","Zaiqatv"],
        ["https://www.zaiqa.com/recipes/sweets-desserts/","Gourmet","Zaiqatv"],
        ["https://www.zaiqa.com/recipes/masala-tv/","Gourmet","Zaiqatv"],
        ["https://www.zaiqa.com/recipes/indian/","Gourmet","Zaiqatv"],
        ["https://www.zaiqa.com/recipes/zaiqa-tv/","Gourmet","Zaiqatv"],
    ]
    if Zaiqa == True:
        print('Getting Zaiqa News...')
        i = 1
        counter = 0
        permalinkArrayZaiqa = []
        for source in sources27:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for li in soup.find_all('li',class_='group'):
                if i <= 6:
                    try:
                        permalink = source[0][:-19] + li.a['href']
                        permalinkArrayZaiqa.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayZaiqa
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for a in detail_source:
            print(a)
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='recipes'):
                try:
                    detail_title = div.h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = ''
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='recipebox').ul.find_all('li')
                    detail_description_ingredients = ''
                    for li in detail_description_all:
                        detail_description_ingredients = detail_description_ingredients + ' ' + li.text.replace('\xa0','')
                    detail_description = div.find('div',class_='recipebox').h2.text + ':' + detail_description_ingredients
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources16 = [
        ["https://www.city42.tv/district-government","National-local","city42"],
        ["https://www.city42.tv/blog","Blog","city42"],
        ["https://www.city42.tv/lahore","National-local","city42"],
        ["https://www.city42.tv/government-of-punjab","National-local","city42"],     
    ] 
    if City42 == True:
        print('Getting Mashion(showbiz) News...')
        i = 1
        counter = 0
        permalinkArrayCity42 = []
        for source in sources16:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='row'):
                if i <= 6:
                    try:
                        permalink = div.div.article.find('div',class_='zm-post-dis').div.h2.a['href']
                        permalinkArrayCity42.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayCity42
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='recipes'):
                try:
                    detail_title = div.h1.text

                except:
                    detail_title = ''
                try:
                    high_resolution_image = ''

                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='articles').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources28 = [
                  ['https://www.urdunews.com/sections/%D9%BE%D8%A7%DA%A9%D8%B3%D8%AA%D8%A7%D9%86','National-local','Urdunews'],
                  ['https://www.urdunews.com/sections/%D8%AF%D9%86%DB%8C%D8%A7','International','Urdunews'],
                  ['https://www.urdunews.com/sections/%D8%B4%D9%88%D8%A8%D8%B2','Entertainment','Urdunews'],
                  ['https://www.urdunews.com/sections/%DA%A9%DA%BE%DB%8C%D9%84','Sports','Urdunews']
                 ]
    if Urdunews == True:
        i = 1
        counter = 0
        print('Getting Urdu News...')
        permalinkArrayUrdunews = []
        for source in sources28:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='column'):
                if i<=6:
                    try:
                        permalink = 'https://www.urdunews.com' + div.article.find('div',class_='article-item-title').h5.a['href']
                        permalinkArrayUrdunews.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
                i = 1
        detail_source = permalinkArrayUrdunews
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article'):
                try:
                    detail_title = article.find('div',class_='entry-title').h1.text   
                except:
                    detail_title = ''
                try:
                    high_resolution_image = article.find('div',class_='entry-media').img['src']  
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = article.find('div',class_='field-items').div.find_all('h5')
                    detail_description = ''
                    for h5 in detail_description_all:
                        detail_description = detail_description + h5.text.replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter)
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources29 = [
                  ['https://www.samaa.tv/urdu/pakistan/','Pakistan','SamaUrdu'],
                  ['https://www.samaa.tv/urdu/international/','International','SamaUrdu'],
                  ['https://www.samaa.tv/urdu/entertainment/','Entertainment','SamaUrdu'],
                  ['https://www.samaa.tv/urdu/sports/','Sports','SamaUrdu'],
                  ['https://www.samaa.tv/urdu/tag/coronavirus/','Health','SamaUrdu']
                 ]
    if Sama == True:
        i = 1
        counter = 0
        permalinkArraySama = []
        for source in sources28:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='column'):
                if i<=6:
                    try:
                        permalink = 'https://www.urdunews.com' + div.article.find('div',class_='article-item-title').h5.a['href']
                        permalinkArraySama.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArraySama
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article'):
                try:
                    detail_title = article.find('div',class_='entry-title').h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = article.find('div',class_='entry-media').img['src']
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = article.find('div',class_='field-items').div.find_all('h5')
                    detail_description = ''
                    for h5 in detail_description_all:
                        detail_description = detail_description + h5.text.replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources30 = [
                  ['https://jang.com.pk/category/latest-news/national','National-local','Jangnews'],
                  ['https://jang.com.pk/category/latest-news/world','International','Jangnews'],
                  ['https://jang.com.pk/category/latest-news/entertainment','Entertainment','Jangnews'],
                  ['https://jang.com.pk/category/latest-news/sports','Sports','Jangnews'],
                  ['https://jang.com.pk/category/latest-news/health-science','Health','Jangnews']
                 ]
    if Jang == True:
        print('Getting Jang(showbiz) News...')
        i = 1
        counter = 0
        permalinkArrayJang = []
        for source in sources30:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for li in soup.find_all('li'):
                if i <= 6:
                    try:
                        permalink = li.find('div',class_='main-heading').a['href']
                        print(permalink)
                        permalinkArrayJang.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayJang
        print(detail_source)
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='detail-right'):
                try:
                    detail_title = div.div.h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='detail-content').find('div',class_='description-area').find('div',class_='detail_view_content').div.figure.img['src']
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='detail-content').find('div',class_='description-area').find('div',class_='detail_view_content').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\xa0','')
                except:
                    detail_description = ''
                counter = counter + 1
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if False:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources33 = [
                 ['https://tribune.com.pk/life-style/art-books','Fashion','Express Tribune'],
                 ['https://tribune.com.pk/life-style/fashion','Fashion','Express Tribune'],
                 ['https://tribune.com.pk/life-style/film','Entertainment','Express Tribune'],
                 ['https://tribune.com.pk/life-style/bollywood','Entertainment','Express Tribune'],
                 ['https://tribune.com.pk/life-style/gossip','Entertainment','Express Tribune'],
                 ['https://tribune.com.pk/life-style/theatre','Entertainment','Express Tribune'],
                 ['https://tribune.com.pk/life-style/tv','Entertainment','Express Tribune'],

                ]
    if Tribune == True:
        print('Getting Tribune Express News...')
        i = 1
        counter = 0
        permalinkArrayTribune = []
        for source in sources33:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for li in soup.find('ul',class_='listing-page').find_all('li'):
                if i <= 6:        
                    try:
                        permalink = li.find('div',class_='row').find('div',class_='col-md-8').find('div',class_='horiz-news3-caption').a['href']
                        permalinkArrayTribune.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayTribune
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='maincontent-customwidth'):
                try:
                    detail_title = div.find('div',class_='story-box-section').h1.text
                except:
                    detail_title = ''
                try:
                    high_resolution_image = div.find('div',class_='story-box-section').find('div',class_='mainstorycontent-parent').div.div.find('span',class_='top-big-img').div.div.div.img['data-src']
                except:
                    high_resolution_image = ''

                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.find('div',class_='story-box-section').find('div',class_='mainstorycontent-parent').div.div.find('span',class_='story-text').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text.replace('\xa0','')
                except:
                    detail_description = detail_page_source[0]
                counter = counter + 1
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                }  
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources36 = [
                ['https://theislamicinformation.com/news/page/','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/2','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/3','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/4','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/5','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/6','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/7','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/8','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/9','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/10','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/11','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/12','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/13','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/14','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/15','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/16','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/17','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/18','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/19','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/20','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/21','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/22','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/23','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/24','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/25','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/26','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/27','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/28','Islam','The Islamic Information'],
                ['https://theislamicinformation.com/news/page/29','Islam','The Islamic Information'],
    ]
    if Islamicinfoenglish == True:
        i = 1
        counter = 0
        print('Getting Islamic info english...')
        permalinkArrayIslamicInformation = []
        for source in sources36:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for article in soup.find_all('article', class_='jeg_post'):
                if i <= 6:
                    try:
                        permalink = article.find('div',class_='jeg_thumb').a['href']
                        permalinkArrayIslamicInformation.append([permalink,source[1],source[2]])
                        counter = counter + 1
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayIslamicInformation
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='jeg_content'):
                try:
                    detail_title = div.div.find('div',class_='entry-header').h1.text
                except:
                    detail_title = ''

                try:
                    high_resolution_image = div.div.find('div',class_='jeg_main_content').find('div',class_='featured_image').a.div.img['data-src']
                except:
                    high_resolution_image = 'Pakteki'
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_all = div.div.find('div',class_='jeg_main_content').div.find('div',class_='entry-content').find('div',class_='content-inner').find_all('p')
                    detail_description = ''
                    for p in detail_description_all:
                        detail_description = detail_description + p.text
                except:
                    detail_description = ''
                counter = counter + 1    
                language='English'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])


# In[ ]:


try:
    sources37 = [
                ['https://islamqa.info/ur/latest','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=2','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=3','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=4','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=5','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=6','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=7','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=8','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=9','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=10','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=11','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=12','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=13','Islam','Islamicqa'],
                ['https://islamqa.info/ur/latest?page=14','Islam','Islamicqa'],
                ]
    if Islamicinfourdu == True:
        counter = 0
        print('Getting islamQA News...')
        i = 1
        permalinkArrayIslamicInformation = []
        for source in sources37:
            sourceHtml = requests.get(source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for a in soup.find_all('a', class_='card post-card'):
                if i<=6:
                    try:
                        permalink = a['href']
                        permalinkArrayIslamicInformation.append([permalink,source[1],source[2]])
                        counter = counter + 1 
                    except:
                        permalink = ''
                    i = i + 1
            i = 1
        detail_source = permalinkArrayIslamicInformation
        if developmentMode:
            print('total news found on listting page : ' + str(counter))
            df = pd.DataFrame(detail_source)
            df
        counter = 0
        for detail_page_source in detail_source:
            sourceHtml = requests.get(detail_page_source[0]).text
            soup = BeautifulSoup(sourceHtml, 'lxml')
            for div in soup.find_all('div',class_='single_fatwa'):
                try:
                    detail_title = div.find('div',class_='single-layout__title').h1.text.replace('\n','')
                except:
                    detail_title = ''
                try:
                    high_resolution_image = 'Pakteki'
                except:
                    high_resolution_image = ''
                try:
                    date_time = time.ctime()
                except:
                    date_time = ''
                try:
                    detail_description_answer_all = div.find('section',class_='single_fatwa__question').find_next_sibling().find('section',class_='single_fatwa__answer').find('section',class_='single_fatwa__answer__body').div.find_all('p')
                    detail_description_answer = ''
                    for p in detail_description_answer_all:
                        detail_description_answer = detail_description_answer + p.text
                    detail_description = div.find('section',class_='single_fatwa__question').h2.text + ' ' + div.find('section',class_='single_fatwa__question').div.p.text + ' ' + div.find('section',class_='single_fatwa__question').find_next_sibling().find('section',class_='single_fatwa__answer').h2.text + ' ' + detail_description_answer 
                except:
                    detail_description = ''
                counter = counter + 1    
                language='Urdu'
                values = {
                            'title': detail_title,
                            'description': detail_description,
                            'date': date_time,
                            'channel': source[2],
                            'image': high_resolution_image,
                            'permalink': detail_page_source[0],
                            'category': detail_page_source[1],
                            'fetching_date': date.today(),
                            'no_of_comments': 0,
                            'rating': 0,
                            'language':language,
                            'created_at': date.today(),
                            'updated_at': date.today(),
                            'comments': [],
                            'resgistered_views':[],
                            'no_of_registered_views':0,
                            'no_of_nonregistered_views':0,
                            }
                if developmentMode:
                    data.append([detail_title, source[1], source[2], permalink, high_resolution_image, date_time, detail_description, date.today(), language])
                    print('')
                    print('No:          ' + str(counter))
                    print('title:       ' + detail_title.strip())
                    print('description: ' + detail_description[0:20])
                    print('permalink:     ' + detail_page_source[0])
                    print('channel:     ' + source[2])
                    print('image:       ' + high_resolution_image)
                    print('category:    ' + detail_page_source[1])
                    print('-----------------------------------------------')
                    if callAPI:
                        response = requests.post(API, data=values)
                        if response.status_code == 429:
                            print('############ waiting response ..')
                            time.sleep(int(response.headers["Retry-After"]))
                        else:
                            print('inserted in DB')
                            print('-----------------------------------------------')
                else:
                    #data.append([detail_title.strip(), source[1], source[2], permalink, high_resolution_image, date_time, detail_description.strip(), date.today(), language])
                    response = requests.post(API, data=values)
                    if response.status_code == 429:
                        time.sleep(int(response.headers["Retry-After"]))
        if developmentMode:
            print('total news scraped page : ' + str(counter))
except:
    print('exception in ' + source[2])

