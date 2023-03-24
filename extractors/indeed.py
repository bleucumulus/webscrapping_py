from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#터미널에서 chrome Manager 설치 완료 (pip3 install chromeManager)

chrome_options = Options()

# browser 꺼짐 방지
chrome_options.add_experimental_option("detach", True)


browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                           options = chrome_options)

def get_page_count(keyword):
    base_url = "https://uk.indeed.com/jobs"
    final_url = f"{base_url}?q={keyword}"
    browser.get(final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")    
    pagination = soup.find('nav', attrs={"aria-label" : "pagination"})
    
    # 왜 필요한지 모르겠음
    if pagination == None:
        return 1
    pages = pagination.select("div a")
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    results = []
    pages = get_page_count(keyword)
    base_url = "https://uk.indeed.com/jobs"
    for page in range(pages):
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        jobs = soup.find('ul', class_="jobsearch-ResultsList")
        job_list = jobs.find_all('li', recursive=False)
        for job in job_list:
            zone = job.find('div', class_="mosaic-zone")
            if zone == None:
                """
                h2 = job.find_all('h2', class_="jobTitle")
                anchor = h2.find("a")
                """
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find('span', class_="companyName")
                location = job.find('div', class_="companyLocation")
                job_data = {
                    "link" : f"https://uk.indeed.com{link}",
                    "company" : company.string,
                    "location" : location.string,
                    "position" : title
                }
                results.append(job_data)

    return results

    

"""
for job_list in job_lists:
    #if mosaic != "mosaic-afterFifthJobResult":
    info = job_list.find_all('h2', class_="jobTitle")
    job_title = info.find('span')
    link = info.find('href')
    company_and_location = job_list.find_all('div', class_="company_location")
    company = company_and_location.find('span', class_="companyName")
    location = company_and_location.find('div', class_="companyLocation")
    job_data = {
        "Title" : job_title.string,
        "Link" : f"https://uk.indeed.com{link}",
        "Company" : company.string,
        "location" : location.string
    }
"""