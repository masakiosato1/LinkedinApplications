#search url

exp_level_code = '2%2C3' #Entry level or Associate
job_type_code = 'F'
search_key = 'frontend%20engineer'
wt_code='1%2C3' # On-site or Hybrid. '2' for remote
geo_id_code='102277331' #San Francisco City. '103644278' for US
tpr='r604800' #Past week. r86400 for past 24 hours
distance='&distance=5'

search_url_list = [
    f'''
    https://www.linkedin.com/jobs/search/
    ?keywords={'javascript'}
    &location=United%20States
    &locationId=
    &geoId={geo_id_code}
    &f_TPR={tpr}
    &f_JT={job_type_code}
    &f_E={exp_level_code}
    &f_WT={wt_code}
    {distance}
    &position=1
    &pageNum=0'''.replace("\n    ", "")
]



#Data filtering rules
bad_application_domains = ['talentify', 'myworkdayjobs', 'dice']
company_names_ignore = ['Talentify.io', 'Dice', 'Forward']
company_sizes = ['51-200 employees', '201-500 employees', '501-1,000 employees']
preferred_keywords = ['javascript', 'typescript', 'react', 'redux']




#Data output
output_db_dict = {
    "host": "localhost",
    "database": "linkedin",
    "user": "masakiosato",
    "password": "5234"
}

output_table_dict = {
    "table_name": "jobs",
    "column_names": ['listing_title', 'company_name', 'company_size', 'job_type', 'application_url'],
    "column_types": ['VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)', 'VARCHAR(255)'],
    "column_conditions": ['','','','','','','']
}

