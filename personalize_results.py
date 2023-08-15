#Running for who?

running_for = "alex" #forest or alex

if running_for == "masaki":
    search_keys = ['Data Analyst', 'Data Engineer', 'Analytics Engineer']
    wt_code='2' #Remote 
    geo_id_code='103644278' #US
    distance=''
    exp_level_code = '2%2C3' #Entry level or Associate

    company_sizes = ['1,001-5,000 employees', '10,001+ employees', '5,001-10,000 employees']
    preferred_keywords = ['data', 'analyst', 'engineer', 'sql', 'python', 'pyspark']
    keyword_match_matters = True
elif running_for == "forest":
    search_keys = ['frontend', 'javascript', 'fullstack']
    wt_code='1%2C3' # On-site or Hybrid. '2' for remote 
    geo_id_code='102277331' #San Francisco City. '103644278' for US
    distance='&distance=5'
    exp_level_code = '2%2C3' #Entry level or Associate

    company_sizes = ['51-200 employees', '201-500 employees', '501-1,000 employees']
    preferred_keywords = ['javascript', 'typescript', 'react', 'redux', 'node', 'mongo', 'html', 'css', 'sass', 'frontend', 'fullstack']
    keyword_match_matters = True
elif running_for == "alex":
    search_keys = ['Data Analyst', 'Data', 'Excel', 'Tableau', 'SQL', 'Junior']
    wt_code='2' #Remote 
    geo_id_code='103644278' #US
    distance=''
    exp_level_code = '1%2C2' #Intern and Entry level
    
    preferred_keywords = ['data', 'analyst', 'analysis', 'bachelors', 'excel', 'microsoft', 'sql', 'tableau']
    keyword_match_matters = False



#search url
job_type_code = 'F'
tpr='r604800' #Past week. r86400 for past 24 hours

search_url_list = []
for search_key in search_keys:
    new_url = f'''
    https://www.linkedin.com/jobs/search/
    ?keywords={search_key}
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
    search_url_list.append(new_url)



#Data filtering rules
bad_application_domains = ['talentify', 'myworkdayjobs', 'dice']
company_names_ignore = ['Talentify.io', 'Dice', 'Forward']



#Data output
output_db_dict = {
    "host": "localhost",
    "database": "linkedin",
    "user": "masakiosato",
    "password": "5234"
}

output_table_dict = {
    "table_name": f"{running_for}_jobs",
    "column_names": [
        'scrape_date',
        'listing_id', 
        'listing_title',
        'job_type',
        'company_name',
        'company_size',
        'application_url',
        'keyword_score',
        'years'
    ],
    "column_types": [
        'DATE', 
        'BIGINT',
        'VARCHAR(255)', 
        'VARCHAR(255)', 
        'VARCHAR(255)', 
        'VARCHAR(255)', 
        'VARCHAR(255)', 
        'INT', 
        'VARCHAR(255)'
    ],
    "column_conditions": [
        '',
        'PRIMARY KEY', 
        '', 
        '', 
        '', 
        '', 
        '', 
        '', 
        ''
    ]
}
