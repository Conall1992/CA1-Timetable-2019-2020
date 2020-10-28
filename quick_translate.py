import sys
import requests 
from bs4 import BeautifulSoup


'''
Used as a quick way to translate a word in english to Japanese using Webscraping 
'''
def main():
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",}
    my_url = "https://translate.google.com/m?hl=en&sl=en&tl=ja&ie=UTF-8&prev=_m&q=" + " ".join(sys.argv[1:])
   

    page_html = requests.get(my_url, headers=headers)

    #html parsing
    page_soup = BeautifulSoup(page_html.content, "lxml")

    #grabs each product
    container = page_soup.find("div", class_="o1").getText()
        
    print(container)

if __name__ == '__main__':
    main()