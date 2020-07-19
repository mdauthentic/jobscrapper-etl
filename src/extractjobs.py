from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time


class FetchJobDetails:

    def __init__(self, config):
        self.job_url = 'https://www.indeed.fr/?r=us'
        self.job_title = config.job_title
        self.location = config.location

        self.driver_path = config.driver_path
        self.wait = WebDriverWait(webdriver, 20)
        self.num_pages_to_crawl = 10

    def configure_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        web_driver = webdriver.Chrome(self.driver_path, options=options)
        return web_driver

    @staticmethod
    def navigate_to(driver, url, sleep_time=2):
        """ navigates to a given page and waits for a predefined time """
        driver.get(url)
        time.sleep(sleep_time)
        try:
            WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, 'input_text').is_displayed())
        except: # close popup
            close_popup = driver.find_element(By.CLASS_NAME, 'popover-x-button-close')[0]
            close_popup.click()
            WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, 'input_text').is_displayed())

    def get_job_details(self):
        all_jobs = []
        for page_num in range(self.num_pages_to_crawl):
            job_title = self.job_title
            nospace_job_title = job_title.replace(' ', '+')
            if page_num == 0:
                page_url = f"https://www.indeed.fr/jobs?q={nospace_job_title}&l="
                job_details = self.get_single_job(page_num+1, page_url)
                for a_job in job_details:
                    all_jobs.append(a_job)
            else:
                next_page_start = page_num * 10
                page_url = f"https://www.indeed.fr/jobs?q={nospace_job_title}&start={next_page_start}"
                job_details = self.get_single_job(next_page_start, page_url)
                for a_job in job_details:
                    all_jobs.append(a_job)
        return all_jobs

    def get_single_job(self, page_num, page_url, sleep_time=2):
            # get driver
            driver = self.configure_driver()
            # visit page
            self.navigate_to(driver, page_url)
            single_page_job = driver.find_element(By.ID, 'resultsCol').find_elements(By.CLASS_NAME, 'jobsearch-SerpJobCard')

            result = []
            for item in range(len(single_page_job)):
                job_title = single_page_job[item].find_element(By.TAG_NAME, 'h2').text
                company = single_page_job[item].find_element(By.CLASS_NAME, 'company').text
                date_posted = single_page_job[item].find_element(By.CLASS_NAME, 'date').text
                try: 
                    salary = single_page_job[item].find_element(By.CLASS_NAME, 'salary').text
                except:
                    salary = 'None'
                
                try:
                    job_description = single_page_job[item].find_element(By.CLASS_NAME, 'summary').text
                except: # close popup
                    close_popup = driver.find_element(By.CLASS_NAME, 'popover-x-button-close')[0]
                    close_popup.click()
                    job_description = single_page_job[item].find_element(By.CLASS_NAME, 'summary').text

                date_stamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")

                result.append((job_title, company, date_posted, salary, job_description, date_stamp))
            # close webdriver
            driver.close()

            print(f'Fetched {page_num} out of {self.num_pages_to_crawl} total pages.')
            return result
