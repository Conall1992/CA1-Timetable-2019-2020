#!/usr/bin/env python3


'''
Uses selenium to grab how long it takes to complete a game(named game is grabed from command line) 
from the website "https://www.howlongtobeat.com/"

'''

import sys
import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "./chromedriver" # this is optional
webpage = ("https://www.howlongtobeat.com/") 
game = " ".join(sys.argv[1:])
driver = webdriver.Chrome('./chromedriver')


driver.get(webpage)
search_bar = driver.find_element_by_id("global_search_box")
search_bar.send_keys(game)
search_bar.send_keys(Keys.RETURN)



try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search_list_details_block"))) # checks whether id actually exists in the html for the webpage
   
    info = main.find_elements_by_tag_name("div") #this is wrong
    i = 1
    
    game_stats = []
    for j in info[1:]:
      
        if i % 2 == 1:
        
            s = str(j.text) + ":"
        
        else:
          
            s = s + " " + j.text
          
            game_stats.append(s)
        i += 1
    for i in game_stats:
        print(i)
    

except:
    print("Unable to reach website!")
    driver.quit()

finally:
    driver.quit()

#driver.close() #closes the tab not the browser
#driver.quit()