from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

jobs = []
jobNames = []
pay = []
nextPage = 2
jobsScraped = 0
paymentScrape = 0
popFlag = True
def scrapeDataZip(driver, maxim):
    global jobs, jobNames, nextPage, jobsScraped,paymentScrape, popFlag
    elements = driver.find_element(By.XPATH, "//div[@class='flex items-center justify-center bg-black bg-opacity-50 transition-opacity z-max fixed inset-0 max-h-full w-full overflow-hidden']")
    if elements and popFlag:
        popFlag = False
        action = ActionChains(driver)
        action.move_by_offset(700, 100)
        action.click()
        action.perform()
        
    for a in driver.find_elements(By.XPATH, ".//article[@class='group flex w-full flex-col text-black']"):
        if a not in jobs:
            jobs.append(a.find_element(By.XPATH, ".//a").get_attribute('href'))
            jobsScraped += 1
        if a not in jobNames:
            jobNames.append(a.find_element(By.XPATH, ".//h2").get_attribute('aria-label'))
        try:
            listEle = a.find_element(By.XPATH, ".//div[@class='flex flex-col']")
            if "$" in listEle.text:
                txt = str(listEle.text)
                tempStr = ""
                for x in txt:
                    if x == "\n":
                        break
                    else:
                        tempStr += x
                        paymentScrape += 1
                        continue
                pay.append(tempStr)
            else:
                pay.append("Pay Info Not Provided.")
                if maxim != "all":
                    if jobsScraped >= int(maxim):
                        break
            if maxim != "all":
                if jobsScraped >= int(maxim):
                    break
        except:
            pay.append("Pay Info Not Provided.")
    
    if maxim != "all":
        if jobsScraped >= int(maxim):
            return False

        
    try:
        buttonEle = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//a[@title='Page: {nextPage}']")))
        driver.execute_script("arguments[0].click();", buttonEle)
        nextPage += 1
        
        return True
    except:
        print("no more results")
        return False
    
def scrapeData(driver, maxim):
    global jobs, jobNames, nextPage, jobsScraped,paymentScrape
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, ".//td[@class='resultContent css-1qwrrf0 eu4oa1w0']")))
    for a in driver.find_elements(By.XPATH, ".//td[@class='resultContent css-1qwrrf0 eu4oa1w0']"):
        if a not in jobs:
            jobs.append(a.find_element(By.XPATH, ".//a").get_attribute('href'))
            jobsScraped += 1
        if a not in jobNames:
            temp = str(a.find_element(By.XPATH, ".//a").get_attribute('aria-label'))
            jobNames.append(temp[15:])
        try:
            listEle = a.find_element(By.XPATH, ".//div[@class='heading6 tapItem-gutter metadataContainer css-z5ecg7 eu4oa1w0']")
            if "$" in listEle.text:
                txt = str(listEle.text)
                tempStr = ""
                for x in txt:
                    if x == "\n":
                        break
                    else:
                        tempStr += x
                        paymentScrape += 1
                        continue
                pay.append(tempStr)
            else:
                pay.append("Pay Info Not Provided.")

            if maxim != "all":
                if jobsScraped >= int(maxim):
                    break
        except:
            pay.append("Pay Info Not Provided.")
            if maxim != "all":
                if jobsScraped >= int(maxim):
                    break
    
    if maxim != "all":
        if jobsScraped >= int(maxim):
            return False

        
    try:
        buttonEle = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//li[@class='css-227srf eu4oa1w0']//a[@data-testid='pagination-page-{nextPage}']")))
        driver.execute_script("arguments[0].click();", buttonEle)
        nextPage += 1
        
        return True
    except:
        print("no more results")
        return False

def returnResult():
    global jobs, jobNames
    f = None
    try:
        f = open("JobResults.txt", "x")
    except:
        f = open("JobResults.txt", "a")
    for i in range(len(jobNames)):
        formatStringJobName = str(jobNames[i])
        f.write(formatStringJobName + f" Pay: {pay[i]}\n Link: \n {jobs[i]} \n\n")
    f.close()
        

def searchZip(searchJob, maxim):
    driver = webdriver.Chrome()
    driver.get('https://www.ziprecruiter.com/Search-Jobs-Near-Me')
    inputEle = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'title')))
    inputEle.send_keys(searchJob)
    inputEle.send_keys(Keys.ENTER)
    if maxim.isalpha():
        maxim.lower()
    fetchResult = scrapeDataZip(driver, maxim)
    while fetchResult == True:
        fetchResult = scrapeDataZip(driver, maxim)

def searchIndeed(searchJob, maxim):
    driver = webdriver.Chrome()
    driver.get('https://www.indeed.com/')
    inputEle = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'q')))
    inputEle.send_keys(searchJob)
    
    inputEle.send_keys(Keys.ENTER)
    if maxim.isalpha():
        maxim.lower()
    fetchResult = scrapeData(driver, maxim)
    while fetchResult == True:
        fetchResult = scrapeData(driver, maxim)

    
    
    
if __name__ == '__main__':
    search = str(input("Type in a job role/position you want to search: "))
    maximum = str(input("How many jobs would you like to return? (if you want to search for all jobs type 'all'): "))
    searchPlat = str(input("Search on (1) Indeed, or (2) ZipRecruiter? (type 'all' if you want to search all, or type in corresponding number): " ))
    
    if searchPlat.lower() == '1':
        print("Searching Indeed.")
        searchIndeed(search, maximum)
        print(len(jobNames), len(jobs), len(pay))
        
        returnResult()
    elif searchPlat.lower() == '2':
        print("Searching ZipRecruiter.")
        searchZip(search, maximum)
        print(len(jobNames), len(jobs), len(pay))
        returnResult()
    elif searchPlat.lower() == "all":
        print("Searching Indeed.")
        searchIndeed(search, maximum)
        nextPage = 2
        jobsScraped = 0
        print("Searching ZipRecruiter.")
        searchZip(search, maximum)
        print(len(jobNames), len(jobs), len(pay))
        returnResult()
    else:
        print("Invalid response")
        exit(1)

