from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)
titles = []
trailerGenres = []
release = []

# Opens trailersaddict coming soon page.
driver.get("https://www.traileraddict.com/comingsoon")

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")
li = soup.find(id="top_features")
children = li.findChildren("a" , recursive=True)
for child in children:
    link = child.get('href')
    driver.get(link)
    subPageContents = driver.page_source
    soup2 =  BeautifulSoup(subPageContents, "html.parser")

    movie_name = soup2.title.string
    titles.append(movie_name)

    genre= []
    for a in soup2.find_all('span', attrs={'itemprop':'genre'}):
        genre.append(a.string)
    trailerGenres.append(genre)

    soup2.find()

trailers = pd.DataFrame({
'movie': titles,
'Genre':trailerGenres
})

trailers.to_csv('Our_trailers.csv')
driver. quit() 


