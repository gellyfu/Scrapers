# coding: utf-8

# import packages

import pandas
import re
import os
import csv
import sys
import itertools
import fnmatch
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# get manager information

def getManagerData(driver, url, manager):
    # manager information
    bio = []
    edu = []

    # go to site
    driver.get(url)

    try:
        if driver.find_element_by_tag_name('pre').text == '{"error":{}}':
                print('site does not exist')
                bio = 'site does not exist'
                edu = 'site does not exist'
    except NoSuchElementException:
            # collect data
            try: 
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='" + manager + "']")))
                time.sleep(15)
                ActionChains(driver).move_to_element(driver.find_element_by_xpath("//*[text()='" + manager + "']")).perform()
                driver.find_element_by_xpath("//*[text()='" + manager + "']").click()

                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "sal-modal-biography")))
                    bioData = driver.find_element_by_class_name("sal-modal-biography").text
                except NoSuchElementException:
                    bioData = "no biography data"
                try:
                    eduData = driver.find_element_by_class_name("sal-modal-education").text
                    eduData = eduData.splitlines()
                except NoSuchElementException:
                    eduData = "no education data"

                # biography
                bio.append(bioData)
                bio = bio[0]

                # education
                if len(eduData) > 1:
                    tempEdu = []
                    for eachEdu in eduData:
                        tempEdu.append(eachEdu)
                        allEdu = ('; ').join(tempEdu)

                    edu.append(allEdu)
                else:
                    edu.append(eduData)

                edu = edu[0]

                print(manager)
            except TimeoutException:
                    print('manager does not exist')
                    bio = 'manager does not exist'
                    edu = 'manager does not exist'

    # package data
    name_data = manager
    fund_data = url
    bio_data = bio
    edu_data = edu

    # append to mother
    mother = {'name':name_data, 'url':fund_data, 'biography':bio_data, 'education':edu_data}

    return mother


# data maker

def dfmaker(dictionary, filename):
    # manager information
    name = []
    url = []
    bio = []
    edu = []

    for fc in dictionary:
        # name
        name.append(fc['name'])

        # url
        url.append(fc['url'])
        
        # biography
        bio.append(fc['biography'])

        # education
        edu.append(fc['education'])

    # construct data frame
    df = pandas.DataFrame({'manager':name, 'url':url, 'biography':bio, 'education':edu})

    # write to csv
    df.to_csv(r'C:\Users\gelly\Documents\All Data\Morningstar Data\output_' + filename)
    print ('done!!!')
    return df

# log in Morningstar

def loginMorningstar(url):
    driver = webdriver.Chrome(r"C:\Users\gelly\AppData\Local\Programs\Python\Python38-32\Scripts\chromedriver")

    driver.get(url)

    driver.find_element_by_id("directpl-text-field_4").send_keys("egenc@rsm.nl")
    driver.find_element_by_id("directpl-text-field_5").send_keys("Agemen123#")
    driver.find_element_by_xpath("//button[@type='button']").click()
    
    return driver


# loop through CSV files

os.chdir(r'C:\Users\gelly\Documents\All Data\Morningstar Data')
file_list = os.getcwd()

for filename in os.listdir(file_list):
    # initialization
    mothership = []
    mother = []
    
    if fnmatch.fnmatch(filename, 'manager*.csv'):
        # read URLs
        path_to_file = os.path.join(r'C:\Users\gelly\Documents\All Data\Morningstar Data', filename)
        inputFile = open(path_to_file, 'rt')
        paths = csv.reader(inputFile)
        print (filename)
        for i, path in enumerate(paths):
            if i == 0:
                continue
            else:
                # read NSAR and parse
                manager = path[0]
                url = path[1]
                url = 'https://direct.morningstar.com/research/mip/' + url + '/FO?culture=ENU&productCode=DIRECT'
                print (url)
                if i == 1:
                    driver = loginMorningstar(url)

                mother = getManagerData(driver, url, manager)
                mothership.append(mother)

        # create CSV file
        df = dfmaker(mothership, filename)

        # close driver
        driver.close()
                
