from array import array
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.g4a.g4a import g4aKey

import csv

СHROME_DIRVER_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # driver path

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

FURL = dict()

g4aKey(FURL)

def		tag_to_listdict(tag: Tag) -> list:
	lst = []
	tag = tag.find("li")
	while tag is not None:
		body_dict = dict()
		body_dict["LINK"] = tag.find("a").get("href") if tag.find("a") is not None else "None"
		body_dict["HEADER"] = tag.find("a").text.strip() if tag.find("a") is not None else "None"
		body_dict["BODY"] = tag.text.strip()
		lst.append(body_dict)
		tag = tag.find_next("li")
	return(lst)

def		write_to_csv(file, year: str, dictlist: list, delimeter: str=";") ->None:
	csvwriter = csv.writer(file, delimiter=delimeter, quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow([year])
	for body in dictlist:
		csvwriter.writerow([body["HEADER"],
							body["BODY"],
							body["LINK"]])
	csvwriter.writerow([""])

for csvname in FURL:
	driver = webdriver.Chrome(СHROME_DIRVER_PATH, options=options)
	URL = FURL[csvname]
	driver.get(URL)
	csvfile = open(csvname, 'w+', newline='', encoding="utf-8")
	soup = BeautifulSoup(driver.page_source, "html.parser")
	driver.close()
	driver.quit
	body = soup.find("div", {"id" : "1516"})
	teme_tag = body.find("ol")
	year_tag = body.find("p", {"class" : "large"})
	while teme_tag is not None:
		year = year_tag.text
		teme = tag_to_listdict(teme_tag)
		write_to_csv(csvfile, year, teme)
		year_tag = year_tag.find_next("p", class_="large")
		teme_tag = teme_tag.find_next("ol")
	csvfile.close()
	
