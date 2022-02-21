from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
import time
import csv


# URL = 'https://www.mcxac.ru/digital-cx/tsifrovye-resheniya-partnerov/bigdata/'
# FILE_NAME = 'mcxac_bigdata.csv'
# URL = 'https://www.mcxac.ru/digital-cx/tsifrovye-resheniya-partnerov/iot/'
# FILE_NAME = 'mcxac_iot.csv'
URL = 'https://www.mcxac.ru/digital-cx/tsifrovye-resheniya-partnerov/robotic/'
FILE_NAME = 'mcxac_robotic.csv'
# URL = 'https://www.mcxac.ru/digital-cx/tsifrovye-resheniya-partnerov/services/'
# FILE_NAME = 'mcxac_services.csv'

СHROME_DIRVER_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # driver path

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(СHROME_DIRVER_PATH, options=options)

driver.get(URL)

csvfile = open(FILE_NAME, 'w+', newline='', encoding="utf-8")

requests = requests.get(URL)
soup = BeautifulSoup(requests.text, "html.parser")
temes = soup.find_all("div", class_="solution")


ids = []


for teme in temes:
	if teme is not None:
		ids.append(teme.get("data-id"))


def catcher(tag, opt_tag, opt_class, href=False):
	
	try:
		if href is False:
			return(tag.find(opt_tag, {"class": f"{opt_class}"}).text.strip())
		else:
			return(tag.find(opt_tag, {"class": f"{opt_class}"}).get("href").strip())
	except:
		return("None")


def write_to_csv(file, company, delimeter=";"):
	csvwriter = csv.writer(file, delimiter=delimeter, quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow([company["HEADER"],
						company["SUB_HEADER"],
						company["NAME"],
						company["LOCATION"],
						company["PPT"],
						company["SITE"],
						company["EMAIL"],
						company["TEL"]])

for id in ids:
	element = driver.find_element(By.XPATH, f"//div[@data-id='{id}']")
	driver.execute_script("arguments[0].click();", element)
	time.sleep(0.1)

	source = driver.page_source
	soup = BeautifulSoup(source, "html.parser")
	temes = soup.find_all("div", {"id": "modal-item"})
	for teme in temes:
		company = dict()

		company["HEADER"] = catcher(teme, "h4", "modal-title")
		company["SUB_HEADER"] = catcher(teme, "div", "modal-subheader")
		company["NAME"] = catcher(teme, "div", "modal-company-name")
		company["LOCATION"] = catcher(teme, "div", "modal-company-text")
		company["PPT"] = "https://www.mcxac.ru" + catcher(teme, "a", "ftext-lnk", href=True)
		company["SITE"] = catcher(teme, "a", "modal-contact-url")
		company["EMAIL"] = catcher(teme, "a", "modal-contact-email")
		company["TEL"] = catcher(teme, "a", "modal-contact-tel")

		write_to_csv(csvfile, company)

driver.quit
csvfile.close()
