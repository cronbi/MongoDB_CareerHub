import pandas as pd
import json

# Read data from CSV files
companies_df = pd.read_csv('/Users/qlin/Desktop/Fall2023/NoSQL/Project/mp2-data/companies.csv')
education_skills_df = pd.read_csv('/Users/qlin/Desktop/Fall2023/NoSQL/Project/mp2-data/education_and_skills.csv')
employment_details_df = pd.read_csv('/Users/qlin/Desktop/Fall2023/NoSQL/Project/mp2-data/employment_details.csv')
industry_info_df = pd.read_csv('/Users/qlin/Desktop/Fall2023/NoSQL/Project/mp2-data/industry_info.csv')
jobs_df = pd.read_csv('/Users/qlin/Desktop/Fall2023/NoSQL/Project/mp2-data/jobs.csv')

# Transform data to JSON format
companies_json = companies_df.to_json(orient='records')
education_skills_json = education_skills_df.to_json(orient='records')
employment_details_json = employment_details_df.to_json(orient='records')
industry_info_json = industry_info_df.to_json(orient='records')
jobs_json = jobs_df.to_json(orient='records')

# Save JSON data to files
with open('/Users/qlin/Desktop/Fall2023/NoSQL/Project/MP2/companies.json', 'w',encoding='utf-8') as outfile:
    outfile.write(companies_json)

with open('/Users/qlin/Desktop/Fall2023/NoSQL/Project/MP2/education_skills.json', 'w',encoding='utf-8') as outfile:
    outfile.write(education_skills_json)

with open('/Users/qlin/Desktop/Fall2023/NoSQL/Project/MP2/employment_details.json', 'w',encoding='utf-8') as outfile:
    outfile.write(employment_details_json)

with open('/Users/qlin/Desktop/Fall2023/NoSQL/Project/MP2/industry_info.json', 'w',encoding='utf-8') as outfile:
    outfile.write(industry_info_json)

with open('/Users/qlin/Desktop/Fall2023/NoSQL/Project/MP2/jobs.json', 'w',encoding='utf-8') as outfile:
    outfile.write(jobs_json)

print("JSON files created successfully.")

print(companies_json)



