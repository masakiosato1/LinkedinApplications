login_url = 'https://www.linkedin.com/'

#all xpaths
job_description_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[2]"
company_name_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/a"
company_size_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/section/section/div[1]/div[2]/span[1]"
job_type_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span"
submit_button_xpath = "/html/body/main/section[1]/div/div/form[1]/div[2]/button"
skip_button_xpath = "/html/body/div[2]/div[1]/section/div[2]/div/article/footer/div/div/button"
apply_button_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/div/div/div/button"
list_of_listings_xpath = "/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[1]/div/ul/li"
page_xpath = f"/html/body/div[contains(@class, 'application-outlet')]/div[3]/div[4]/div/div/main/div/div[1]/div/div[contains(@class, 'jobs-search-results-list__pagination')]/ul/li"

#linkedin login credentials
username = "beckysalert@gmail.com"
password = "Belarusian5234!"

#email login credentials
email_user = 'beckysalert@gmail.com'
email_password = 'qkxjfucmdsfhgooo'

#search url
exp_level_code = '2%2C3'
job_type_code = 'F'
search_key = 'data%20analyst'
wt_code='2'
geo_id_code='103644278'

search_url = f'''
    https://www.linkedin.com/jobs/search/
    ?keywords={search_key}
    &location=United%20States
    &locationId=
    &geoId={geo_id_code}
    &f_TPR=r86400
    &f_JT={job_type_code}
    &f_E={exp_level_code}
    &f_WT={wt_code}
    &position=1
    &pageNum=0
'''.replace("\n    ", "")


#Data filtering rules
bad_application_domains = ['talentify', 'myworkday']
company_names_ignore = ['talentify', 'dice']
company_sizes = ['51-200 employees', '201-500 employees', '501-1,000 employees']
