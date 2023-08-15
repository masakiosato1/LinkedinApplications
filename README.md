# LinkedinApplications

## Summary
Use the Selenium python library to navigate the Linkedin website and scrape job listings. In order to reduce the server load as much as possible, skip any irrelevant listings. Listings are then stored in a PostgreSQL database.

### Process Breakdown
1. Start driver
2. Load the login page
3. Login by finding the text boxes and submit button
4. Go to premade search urls from "personalize_results.py"
5. Get a count of listings on the page
6. Click each listing and determine if each one should be skipped or fully scraped
    - Listing ID
    - Job Title
    - Job Description
    - Company Name
    - Company Size
    - Job Type (Full Time/Contract, Salary estimate if provided)
    - Application URL (Since it's blocked by javascript, we must have the selenium driver click the button and get the link)
7. After the page is done scraping, organize the data into an array and load into a postgres database
8. Start the next page, until 8 pages or the final page is finished
### Listings to skip
- Listings with Easy Apply
- Listings that have already been scraped before (using "currentJobId" in the url)
- Listings that are no longer taking any applicants
- Listings that don't have any important keywords in the description
### Available Columns
- listing_id (bigint, primary key)
- scrape_date (date)
- position_title (varchar(255))
- job_type (varchar(255))
- company_name (varchar(255))
- company_size (varchar(255))
- application_url (varchar(255))
- keyword_score (int)
- years (varchar(255))
