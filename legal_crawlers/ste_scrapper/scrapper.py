# -*- coding: utf-8 -*-
import time
import re
import os
import errno
import math
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
 
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 10)
    return driver
 
 
def lookup(driver, year):
    
    try:
        os.makedirs(os.path.join(os.pardir,"data/ste",year))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    driver.get("http://www.adjustice.gr/webcenter/portal/ste/ypiresies/nomologies")
    try:
        box = driver.wait.until(EC.presence_of_element_located((By.ID, "dec_year")))
        button = driver.wait.until(EC.element_to_be_clickable((By.ID, "form1submit")))
        box.clear()        
        box.send_keys(year)
        button.click()
        time.sleep(3)
        num_result_div = driver.wait.until(EC.presence_of_element_located((By.ID, "cldResultTable_info")))
        m = re.search(ur'από (.+?) αποτελέσματα', num_result_div.text)
        if m:
            num_result = m.group(1).replace(',','')
            #print((int(num_result)))
            pagination = 10
            pages = int(math.floor(int(num_result)/pagination))
            counter = 1	
            while (counter <= pages):
                links = []
                links = driver.find_elements_by_class_name("doc_opener")
                for link in links:
                    link.click()
                    decision_text_div = driver.wait.until(EC.presence_of_element_located((By.ID, "full_display_dec_text")))
                    if len(decision_text_div.text) > 100:			
                        ar_apofasis = driver.find_element_by_id("display_dec_number").text.split("/")[0]
                        #f = open(year + '/' + ar_apofasis + '.txt','w')
                        f = open(os.path.join(os.pardir,"data/ste",year) + '/' + ar_apofasis + '.txt','w')
                        f.write(driver.find_element_by_id("display_dec_number").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_chamber").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_dec_category").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_dec_date").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_init_category").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_init_number").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("display_composition").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("ecli").text + '\n')
                        f.write(driver.find_element_by_id("full_display_litig1").text.encode('utf-8') + '\n')
                        f.write(driver.find_element_by_id("full_display_litig2").text.encode('utf-8') + '\n')
                        f.write('\n')
                        f.write(decision_text_div.text.encode('utf-8'))
                        f.close()
                    back = driver.wait.until(EC.element_to_be_clickable((By.ID, "cld-single-back")))
                    back.click()
                links[:] = []
                print(year + ": " + str(counter))
                counter = counter+1	
                newpage = driver.find_element_by_link_text(str(counter))
                newpage.click()
                time.sleep(1)	
    except TimeoutException:
        print("Timeout")
 
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, str(sys.argv[1]))
    time.sleep(5)
    driver.quit()
