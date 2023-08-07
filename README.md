# LinkedinApplications

## Summary
Scrape job listings from Linkedin with specific search commands and save the data in a PostgreSQL database.

## Process Breakdown
Use the Selenium python library to navigate the Linkedin website and scrape job listings. In order to reduce the server load as much as possible, skip any irrelevant listings. Listings are then stored in a PostgreSQL database.
### Listings to skip
- Listings with Easy Apply
- Listings that have already been scraped before (using "currentJobId" in the url)
- Listings that are no longer taking any applicants
### Available Columns
- listing_id (bigint, primary key)
- scrape_date (date)
- position_title (varchar(255))
- job_type (varchar(255))
- company_name (varchar(255))
- company_size (varchar(255))
- application_url (varchar(255))

## Potential Ideas
- Job Description
    - potentially use to skip irrelevant listings
    - keyword scoring
    - find the sentence with year