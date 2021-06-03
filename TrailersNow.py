from typing import List, Dict
from selenium import webdriver
from bs4 import BeautifulSoup 
import json  
import requests 

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])



def getMovieList(tag: str, n : int) -> List[Dict[str, str]]:
    movieList = []
    movieInfo = {}
    pageInd = 1
    url = "Add_base_URL"
    driver = webdriver.Chrome('./chromedriver', options=options)
  
    driver.get(url + '/movie/' + tag)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    while(len(movieList) < n):
        for movie in soup.find_all('img', {'class':'poster'}, limit=n-len(movieList)):
            movieInfo['poster'] = url + movie.get('src')
            movieInfo['title'] = movie.parent.get('title')
            movieInfo['href'] =url + (movie.parent.get('href') + " " + (movie.parent.get('title')).lower()).replace(" ","-") 
            movieList.append(movieInfo.copy())
        pageInd += 1 
    driver.quit()    
    return movieList

def getTrailerDetails(url : str) -> Dict[str, str]:
    driver = webdriver.Chrome('./chromedriver', options=options)
    trailer = {}
    movieCast = []
    baseURL = "Add_base_url"
    href = url.replace(baseURL,"")
  
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    
    # Get movie id
    # trailer['id'] = (href.split("-", 1)[0]).replace('/movie/',"")
    
    # Gets movie title 
    trailer['name'] = (soup.head.title.text).replace("— The Movie Database (TMDb)","")
    
    # Gets the description about the movie.
    trailer['info'] = [overview.string for overview in soup.find('div', {'class' : 'overview'}) if overview != '\n']
     
    for releaseDate in soup.find('span', {'class' : 'release'}): 
        trailer['movierelease'] = ((releaseDate.string).replace("\n  ","")).replace("(DE)","").strip()
    
    
    genre = soup.find('span', class_="genres")
    trailer['genre'] = [g.string for g in genre.find_all('a')]
    
    trailer['director'] = soup.find('li', {'class' : 'profile'}).a.text
    
    cast =  soup.find('ol', {'class' : 'people scroller'})
    for cst in cast.find_all('li'):
        for c in cst.find('p').a:
            movieCast.append(c.string)
    trailer['lead_cast'] = [x for x in movieCast if x != 'View More ' and x != None]
   
    youTubeID = soup.find('a', class_="play_trailer")
    trailer['url_video'] = "https://www.youtube.com/watch?v="+youTubeID.get('data-id')
    
    # Gets the portrait image.
    trailer['url_portrait_photo'] = baseURL + soup.find('img', class_="poster").get('src')
    
    #Gets the landscape image.
    trailer['url_photo'] = baseURL + soup.find('img', class_="backdrop").get('src')
      
    trailer['other_info'] = ""
    trailer['stars'] = ""
    trailer['imdb'] = ""
    trailer['description'] =""
    trailer['category'] =""
    trailer['method'] =""
    
    driver.quit()
    return trailer
    

movies = getMovieList("upcoming", 1)

#sorts movies by title
movies_sorted = sorted(movies, key=lambda k: k['title']) 
for movie in movies_sorted:
    trailer = getTrailerDetails(movie['href'])
    json_object = json.dumps(trailer, indent = 4)  
    print(json_object)
    r = requests.post('Add post url', json=json_object)
    print(r.status_code)
    
    
