login_url = 'https://www.linkedin.com/'

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
