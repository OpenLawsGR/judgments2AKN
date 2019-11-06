# -*- coding: utf-8 -*-

import os
import errno
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
 
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 20)
    return driver
 
 
def lookup(driver, year):
    
    try:
    	os.makedirs(year)
    except OSError as e:
    	if e.errno != errno.EEXIST:
            raise
    
    driver.get("http://www.adjustice.gr/webcenter/portal/ste/ypiresies/nomologies")
    try:
        #prepare search form to submit
        box = driver.wait.until(EC.presence_of_element_located((By.ID, "dec_year")))
        button = driver.wait.until(EC.element_to_be_clickable((By.ID, "form1submit")))
        box.clear()        
        box.send_keys(year)
        #submit form
        button.click()

        #get last item of pagination list and read the page number
        pages_elem = driver.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.paginate_button:nth-child(8) > a:nth-child(1)")))
        pages = int(pages_elem.text)

        counter = 1

        while (counter<=pages):
                #wait until processing gif is invisible -> loading of results has finished
                driver.wait.until(EC.invisibility_of_element_located((By.ID, "cldResultTable_processing")))

                links = []
                #find "see more" links
                links = driver.find_elements_by_class_name("doc_opener")

                for link in links:
                        #visit decision page
                        link.click()
                        #get decision text div
                        decision_text_div = driver.wait.until(EC.presence_of_element_located((By.ID, "full_display_dec_text")))
                        if len(decision_text_div.text) > 100:			
                                ar_apofasis = driver.find_element_by_id("display_dec_number").text.split("/")[0]
                                f = open(year + '/' + ar_apofasis + '.txt','w')
                                #write some metadata at the top of the file
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
                                #write the decision text
                                f.write(decision_text_div.text.encode('utf-8'))
                                f.close()
                        #go back one level
                        back = driver.wait.until(EC.element_to_be_clickable((By.ID, "cld-single-back")))
                        back.click()
                links[:] = []
                print(year + ": " + str(counter))
                counter = counter+1
                #visit next page	
                newpage = driver.find_element_by_link_text(str(counter))
                newpage.click()

    except TimeoutException as ex:
        print("Timeout: " + str(ex))
 
 
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, str(sys.argv[1]))
    driver.quit()
