from personalize_results import *
from urllib.parse import urlparse
import pandas as pd

#Filter by company_size
def filter_company_size(df_original):
    df_new = df_original[df_original['company_size'].isin(company_sizes)]
    return df_new

#Company names to ignore
def filter_company_name(df_original):
    df_new = df_original[~df_original['company_name'].isin(company_names_ignore)]
    return df_new

#Application URLs to ignore
def filter_application_url(df_original):
    df_original['domain'] = (
        df_original["application_url"]
        .astype(str)
        .apply(lambda x: urlparse(x).netloc.split("."))
        .apply(lambda x: x[len(x)-2])
    )
    df_new = df_original[~df_original['domain'].isin(bad_application_domains)]
    return df_new


#This function will be applied to the job description of each row
def word_check(job_description):
    counter = 0
    for word in preferred_keywords:
        if word in job_description:
            counter += 1
    return counter
    

#Add a keyword score column, the more keywords included the better
def find_description_keywords(df_original):
    df_original['keyword_score'] = (
        df_original['job_description']
        .astype(str)
        .apply(lambda x: word_check(x.lower()))
    )
    return df_original