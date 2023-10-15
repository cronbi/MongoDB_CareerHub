# CareerHub: Building a Mini Job Portal with MongoDB and Flask

## Overview
This project, CareerHub, is a mini job portal built using MongoDB as the database and Flask as the web framework. It allows users to create, view, update, and delete job postings. This README provides detailed information on setting up the project, usage instructions, examples, and the development process.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
- [Development Process](#DevelopmentProcess)


## Setup

### Prerequisites
- Python 3.x installed
- MongoDB installed and running
- Docker and Docker Compose
- Postman

### Installation
1. Clone the repository
    - `git clone <repository-url>`
2. Navigate to the project directory
    - `cd <CareerHub-project>`
3. Install dependencies 
    - `pip install -r requirements.txt`
4. A `Dockerfile` and `docker-compose.yml` are provided for containerization.
    - `docker-compose up -d`
5. Start the Flask App in your terminal
   - `python run-app.py `
   - Note: The Flask app will be running at http://127.0.0.1:5000/ (or your local host)
6. Access the API Endpoints
   - Use tools like Postman to interact with the API endpoints.
   - Refer to the Postman Integration section for detailed instructions on using Postman with CareerHub API.


## Usage

### Endpoints
- Homepage: `GET /`
- Create a Job Post: `POST /create/jobPost`
- View Job Details by ID: `GET /search_by_job_id/<job_id>`
- Update Job Details by Title: `POST /update_by_job_title`
- Delete Job Listing by Title: `DELETE /delete_by_job_title`
- Query Jobs by Salary Range: `GET /jobs_by_salary`
- Query Jobs by Experience Level: `GET /jobs_by_experience_level`
- Top Companies in an Industry: `GET /top_companies_by_industry`

### API Endpoints In-Depth
1. Welcome Message
- Endpoint: /
- Method: GET
- Purpose: Displays a welcome message to the user.
- Parameters: None
- Response: 
    - Success (200 OK)
- Possible Errors: None

2. Create a Job Post
- Endpoint: /create/jobPost
- Method: POST
- Purpose: Allows users to create a new job posting.
- Parameters:
    - title (string, required): Job title.
    - description (string, required): Job description.
    - industry (string, required): Industry of the job.
    - average_salary (integer, required): Average salary for the job.
    - location (string, required): Job location.
- Response:
    - Success (201 Created)
- Possible Errors:
    - 400 Bad Request: If any of the required parameters are missing or empty.

3. View Job Details by ID
Endpoint: /search_by_job_id/<job_id>
Method: GET
Purpose: Allows users to search for a job by its unique ID.
Parameters:
job_id (integer, required): Unique identifier for the job.
Response:
Success (200 OK):Not Found (404 Not Found):
Possible Errors:
404 Not Found: If the specified job_id does not exist in the database.

4. Update Job Details by Title
Endpoint: /update_by_job_title
Method: POST
Purpose: Allows users to update job details by providing the job title.
Parameters:
job_title (string, required): Job title to be updated.
description (string, optional): Updated job description.
average_salary (integer, optional): Updated average salary.
location (string, optional): Updated job location.
Response:
Success (200 OK):Not Found (404 Not Found):



## Development Process

### Schema Design
- The schema design was crafted to represent companies and job postings in a way that allows for efficient querying and retrieval of data. A normalized schema approach was used, separating companies and job posts, and others into distinct collections.
- An example schema of the final job collection would look like this:
{
  "_id": "<ObjectId>",
  "id": 1,
  "company_name": "Vanderbilt",
  "title": "IT Consultant",
  "description": "This role is at the forefront of the company's...",
  "industry": "Higher Ed",
  "average_salary": 44003,
  "location": "Nashville, TN",
  "level": "Entry Level"
}

### Data Transformation and Import
- Data from provided CSV files was transformed into JSON format and imported into the MongoDB careerhub database using a `csv_json.py` Python script. Pandas was utilized for data manipulation, and PyMongo was used for MongoDB integration.

### Flask App
- The Flask app was developed under `jobs.py`, incorporating various endpoints to handle job-related operations. Input validation, error handling, and MongoDB interactions were carefully implemented to ensure reliability and functionality.

- Obstacles faced included validating user input, handling edge cases, and implementing proper error messages and responses. Detailed testing and debugging were performed to resolve issues.



