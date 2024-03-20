from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

jobs = []
jobNames = []
pay = []
nextPage = 2
jobsScraped = 0
paymentScrape = 0
def scrapeData(driver, maxim):
    global jobs, jobNames, nextPage, jobsScraped,paymentScrape
        
    for a in driver.find_elements(By.XPATH, "//*[@class='jcs-JobTitle css-jspxzf eu4oa1w0']"):
        if maxim != "all":
            if jobsScraped >= int(maxim):
                break
        if a not in jobs:
            jobs.append(a.get_attribute('href'))
            jobsScraped += 1
        if a not in jobNames:
            jobNames.append(a.get_attribute('aria-label'))
    listEle = driver.find_elements(By.XPATH, ".//div[@class='heading6 tapItem-gutter metadataContainer css-z5ecg7 eu4oa1w0']")
    for i in listEle:
        if maxim != "all":
            if jobsScraped >= int(maxim):
                break
        if "$" in i.text:
            txt = str(i.text)
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
        
    #print(jobs, jobNames)
    #for num in driver.find_elements(By.XPATH, "//*[@class='css-227srf eu4oa1w0']"):
        #if str(nextPage) in num.get_attribute('aria-label'):
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
        f.write(formatStringJobName[15:] + f" Pay: {pay[i]}\n Link: \n {jobs[i]} \n\n")
    f.close()
        



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
    returnResult()
    
    
    
if __name__ == '__main__':
    search = str(input("Type in a job role/position you want to search on Indeed: "))
    maximum = str(input("How many jobs would you like to return? (if you want to search for all jobs type 'all'): "))
    searchIndeed(search, maximum)
