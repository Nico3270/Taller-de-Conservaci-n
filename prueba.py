from cgi import print_arguments
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
chrome_driver_path = "C:\Portafolio\chromedriver_win32\chromedriver.exe"

def final(latitud, longitud):
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get('https://www.google.com/maps/@-33.569697,-70.62996,17z?hl=es-ES')
    search_bar = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    search_bar.click()
    search_bar.send_keys(str(latitud) + " " + str(longitud))
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    coordenada = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')
    coor = coordenada.text
    link = driver.current_url
    driver.close()
    return link, coor

coor_1 = final(5.50822, -73.34938) 
print(coor_1[0])
print(coor_1[1])
