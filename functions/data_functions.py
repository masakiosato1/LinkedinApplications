from definitions.data_filtering import *
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