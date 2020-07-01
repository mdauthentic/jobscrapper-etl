from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException
import time


class FetchJobDetails:

    def __init__(self, config):
        self.job_url = 'https://www.indeed.fr/?r=us'
        self.job_title = config.job_title
        self.location = config.location

        self.driver_path = config.driver_path
        self.wait = WebDriverWait(webdriver, 20)
        self.webdriver = self.configure_driver()

        self.num_pages_to_crawl = 1

    def configure_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        web_driver = webdriver.Chrome(self.driver_path, options=options)
        return web_driver

    def go_to_page(self, update_url=None):
        driver = self.webdriver
        # open url
        if update_url is not None:
            # print(f'visiting {update_url}')
            # driver.get('https://dev.to/')
            sing = driver.get(update_url)
            print(driver, update_url)
            # driver.execute_script("return document.getElementByClassName('content');")
            driver.get(update_url)
            self.wait
        else:
            driver.get(self.job_url)
            self.wait
        
        while True:
            try:
                self.wait.until(lambda x: x.find_element(By.ID, 'jobsearch_nav_body').is_displayed())
                # WebDriverWait(driver, 10).until(presence_of_element_located(By.ID, "jobsearch_nav_body"))
                # self.wait.until(presence_of_element_located((By.ID, "jobsearch_nav_body")))
            except TimeoutException:
                break
        return True

    # def search_job(self):
    #     # visit page
    #     visit_page = self.go_to_page()
    #     if not visit_page:
    #         # better close if page is unresponsive
    #         self.webdriver.close()

    #     job_title = webdriver.find_element(By.ID, "text-input-what")
    #     job_title.send_keys(self.job_title + Keys.RETURN)
        
    #     self.wait.until(presence_of_element_located((By.ID, "text-input-what")))

    
    def get_job_details(self):
        # self.search_job() # I might want to replace this with go_to_page

        all_jobs = []
        # https://www.indeed.fr/jobs?q=software+engineer&l=
        # https://www.indeed.fr/jobs?q=software+engineer&start=10
        
        def get_single_job(page_num):
            # visit page
            # visit_page = self.go_to_page()
            # if not visit_page:
            #     # better close if page is unresponsive
            #     self.webdriver.close()

            single_page_job = self.webdriver.find_element(By.ID, 'resultsCol').find_elements(By.CLASS_NAME, 'jobsearch-SerpJobCard')
            result = []

            for item in range(single_page_job):
                job_title = single_page_job[item].find_element(By.TAG_NAME, 'h2').text
                company = single_page_job[item].find_element(By.CLASS_NAME, 'company').text
                date_posted = single_page_job[item].find_element(By.CLASS_NAME, 'date').text
                try: 
                    salary = single_page_job[item].find_element(By.CLASS_NAME, 'salary').text # remember to clean
                except:
                    salary = 'None'

                try:
                    job_description = single_page_job[item].find_element(By.CLASS_NAME, 'summary').click()
                except: # close popup
                    close_popup = self.webdriver.find_element(By.CLASS_NAME, 'popover-x-button-close')[0]
                    close_popup.click()
                    job_description = single_page_job[item].find_element(By.CLASS_NAME, 'summary').click()
                    # webdriver.find_element(By.CLASS_NAME, 'icl-LegalConsentBanner-action').click()

                print(f'Fetched {page_num} out of {self.num_pages_to_crawl} total pages.')
                result.append(job_title, company, date_posted, job_description)
            return result

        for page_num in range(self.num_pages_to_crawl):
            job_title = self.job_title
            nospace_job_title = job_title.replace(' ', '+')
            if page_num == 0:
                page_url = f"https://www.indeed.fr/jobs?q={nospace_job_title}&l="

                # self.go_to_page(page_url)
                print(f'visting page {page_num+1} at url {page_url}')
                visit_page = self.webdriver.get(page_url)
                self.wait

                # visit_page = self.go_to_page(page_url)
                print(self.webdriver.find_element(By.CLASS_NAME, 'input_text'))
                if not visit_page:
                    # better close if page is unresponsive
                    self.webdriver.close()
                time.sleep(5)
                job_details = get_single_job(page_num)
                for a_job in job_details:
                    all_jobs.append(a_job)
                # all_jobs.append(job_details)
            else:
                next_page_start = page_num * 10
                page_url = f"https://www.indeed.fr/jobs?q={nospace_job_title}&start={next_page_start}"
                # self.go_to_page(page_url)
                print(f'visting page {page_num-1} at url {page_url}')

                visit_page = self.go_to_page(page_url)
                if not visit_page:
                    # better close if page is unresponsive
                    self.webdriver.close()

                time.sleep(5)
                job_details = get_single_job(page_num)
                for a_job in job_details:
                    all_jobs.append(a_job)
            
        return all_jobs
