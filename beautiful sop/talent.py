import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json

def load_talent_jobs_div(job_title, location):
    getVars = {'k' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://in.talent.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="nv-jobs")
    
    return job_soup
    

def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='card__job-title')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('div',class_='card__job-empname-label')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'https://in.talent.com' + link
    return link


'''def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
  
    jobs.to_excel(filename)'''

def extract_job_information_talent(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='link-job-wrap')
    
    cols = []
    extracted_info = []
    
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)                    
    
    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)
    
    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
        
    
    num_listings = len(extracted_info[0])
   
    return  num_listings,titles,companies,links

    '''print('{} new job postings retrieved. Stored in {}.'.format(num_listings, filename='results.xlsx'))'''


def find_jobs_from(website, job_title, location, desired_characs, filename="results.xls"):  
      
    """
    This function extracts all the desired characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: to specify which website to search (options: 'Indeed' or 'CWjobs')
        - Job_title
        - Location
        - Desired_characs: this is a list of the job characteristics of interest,
            from titles, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Default is .xls file called 'results.xls'
    """
    if website == 'Talent':
        job_soup = load_talent_jobs_div(job_title, location)
        num_listings,titles,companies,links = extract_job_information_talent(job_soup, desired_characs)
        div_num=num_listings/3
        if div_num.is_integer():
            sum_num = int(div_num)
        else:
            sum_num=int(div_num)+1
        jsonData = {
           
            "titles": titles,
            "companies": companies,
            "links": links
        }
        json_object = json.dumps(jsonData, indent = 4) 
        with open("static/temporary.json", "w") as outfile: 
            outfile.write(json_object) 
    return sum_num



    '''if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)
    
    if website == 'CWjobs':
        # TO DO LATER'''
    
    '''save_jobs_to_excel(jobs_list, filename)'''
 