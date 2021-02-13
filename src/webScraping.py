from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

#Team Statistics per match scraping
data=[]
for i in range(19, 7, -1):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #url of the page we want to scrape 
    url = "https://www.nba.com/stats/teams/boxscores/?Season=20"+str(i//10)+str(i%10)+"-" + str((i+1)//10)+ str((i+1)%10) + "&SeasonType=Regular%20Season"
    print(url)
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    driver.get(url)  
    time.sleep(5) 
    (driver.find_elements_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[@value="string:All"]')[0]).click()
    time.sleep(5)
    html = driver.page_source 
    soup = BeautifulSoup(html, "html.parser")
    table= soup.find('table') 
    tr= table.find_all('tr')
    for row in tr:
        td= row.find_all('td')
        if len(td)!=0:
            example=[((i.text).replace('\n', '')).strip() for i in td]
            example= ["20"+str(i//10)+str(i%10)+"-"+str((i+1)//10)+str((i+1)%10) if text=='' else text for text in example]
            data.append(example)
    print(len(data))
    driver.close() # closing the webdriver

heading= table.find_all('th')
headers=[]
for header in heading:
    heading_text= (header.text.strip()).replace('\xa0', ' ')
    headers.append(heading_text)
print(headers)

pd.DataFrame(data).to_csv("./schedule.csv", header=headers, index=None)

#Player Statustics per matching scraping
for i in range(19, 7, -1):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #url of the page we want to scrape 
    url= "https://www.nba.com/stats/players/boxscores/?Season=20"+str(i//10)+str(i%10)+"-" + str((i+1)//10)+ str((i+1)%10) + "&SeasonType=Regular%20Season"
    print(url)
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    driver.get(url)  
    time.sleep(10) 
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table= soup.find('table')
    pages= soup.find("div", class_="stats-table-pagination__info").find('select').find_all('option')
    heading= table.find_all('th')
    headers=[]
    data=[]
    for header in heading:
        heading_text= (header.text.strip()).replace('\xa0', ' ')
        headers.append(heading_text)
    for page in range(len(pages)-1):
        html = driver.page_source 
        soup = BeautifulSoup(html, "html.parser")
        table= soup.find('table') 
        tr= table.find_all('tr')
        for row in tr:
            td= row.find_all('td')
            if len(td)!=0:
                example=[((i.text).replace('\n', '')).strip() for i in td]
                example= ["20"+str(i//10)+str(i%10)+"-"+str((i+1)//10)+str((i+1)%10) if text=='' else text for text in example]
                data.append(example)
        print(len(data))
        nextButton= driver.find_elements_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]')[0]
        driver.execute_script("arguments[0].click();", nextButton)
        time.sleep(5)
    pd.DataFrame(data).to_csv("./PlayerSchedule"+str(i//10)+str(i%10)+"-" + str((i+1)//10)+ str((i+1)%10)+".csv", header=headers, index=None)
    driver.close() # closing the webdriver



