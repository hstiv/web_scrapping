from queue import Full
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.bigdata.bigdata import bigDataKey
from pages.iot.iot import iotKey
from pages.robotic.robotic import roboticKey
from pages.services.services import servicesKey

import requests
import time
import csv

FURL = dict()

bigDataKey(FURL)
iotKey(FURL)
roboticKey(FURL)
servicesKey(FURL)


СHROME_DIRVER_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # driver path

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(СHROME_DIRVER_PATH, options=options)

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

for csvname in FURL:

	driver.get(FURL[csvname])

	csvfile = open(csvname, 'w+', newline='', encoding="utf-8")

	request = requests.get(FURL[csvname])
	soup = BeautifulSoup(request.text, "html.parser")
	temes = soup.find_all("div", class_="solution")

	ids = []

	for teme in temes:
		if teme is not None:
			ids.append(teme.get("data-id"))

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

	csvfile.close()

driver.close()
driver.quit
