'''Module for serving API requests'''

from app import app
from bson.json_util import dumps, loads
from flask import request, jsonify
import json
import ast # helper library for parsing data from string
from importlib.machinery import SourceFileLoader
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

##############################################################################################################################
# 1. Connect to the client 
client = MongoClient(host="localhost", port=27017) 

# Import the utils module
utils = SourceFileLoader('*', './app/utils.py').load_module() # utils.py is in the same directory as jobs.py

# 2. Select the database
db = client.careerhub # 'use careerhub'
# 3. Select the collection
collection = db.final_jobs

##############################################################################################################################
@app.route("/")
def get_initial_response():
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to your Flask App, this is for MP2 CareerHub!'
    }
    return jsonify(message)
##############################################################################################################################
# Create a Job Post
# When a user visits this page http://localhost:5000/create/jobPost, they can create a new job posting with details, including title, description, industry, average salary, and location.
# In the corresponding view function, make sure to include logic to validate the data and ensure that essential fields like title and industry are not empty.
# Insert the validated data into the MongoDB collection.
@app.route("/create/jobPost", methods=['POST'])
def create_job_post():
    try:
        # Get job post data from the request JSON body
        #job_post_data = request.get_json()
        job_post_data = ast.literal_eval(json.dumps(request.get_json()))

        # Validate essential fields (title and industry)
        if "title" not in job_post_data or "industry" not in job_post_data or not job_post_data["title"] or not job_post_data["industry"]:
            return jsonify({"error": "Title and industry are required fields."}), 400

        # Insert the validated job post data into the MongoDB 'jobs' collection
        record_created = collection.insert_one(job_post_data)

        if record_created:
            inserted_id = record_created.inserted_id
            # Prepare the response
            response_data = {
                "message": f"Job post created successfully with ID: {inserted_id}",
                "job_post_id": str(inserted_id)
            }
            return jsonify(response_data), 201

    except Exception as e:
        # Error while trying to create a job post
        print(e)
        return 'Server error', 500
##############################################################################################################################
# View Job Details
# When a user visits this page http://localhost:5000/search_by_job_id /<job_id> users can search by a job id.
@app.route('/search_by_job_id/<job_id>', methods=['GET'])
def search_by_job_id(job_id):
    try:
        # Convert string to int
        job_id = int(job_id)

        # Query the document by job ID 
        result = collection.find_one({"id": job_id})

        # If document not found
        if not result:
            return jsonify({"message": "Job not found"}), 404

        # Convert ObjectId to string for JSON serialization
        result['_id'] = str(result['_id'])
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
##############################################################################################################################
# View Job Details
# Allow users to input a job title they wish to update via http://localhost:5000/update_by_job_title
# Search for the job in the database and, if found, display the current details. Provide an option to modify fields like description, average, salary, and location. 
# Update the MongoDB collection with the new details after validation.
@app.route('/update_by_job_title', methods=['POST'])
def update_job_by_title():
    try:
        # Get job title from the request
        job_title = request.form.get('job_title')

        # Query the database to find the job by title
        job = collection.find_one({"title": job_title})

        # If job not found, return appropriate response
        if job is None:
            return jsonify({"message": "Job not found"}), 404
        
        # Get updated fields from the request
        updated_description = request.form.get('description')
        updated_salary = request.form.get('average_salary')
        updated_location = request.form.get('location')
        
        # Output the current job details before updating
        current_job_details = {
            "title": job['title'],
            "description": job.get('description', ''),
            "average_salary": job.get('average_salary', ''),
            "location": job.get('location', '')
        }

        # Update the job details if fields are provided
        if updated_description:
            job['description'] = updated_description
        if updated_salary:
            job['average_salary'] = int(updated_salary)
        if updated_location:
            job['location'] = updated_location

        # Update the job details in the database
        collection.update_one({"title": job_title}, {"$set": job})

        return jsonify({"message": "Job details updated successfully",
                        "current_job_details": current_job_details}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##############################################################################################################################
# Remove Job Listing
# Provide an option for users to input a job title they wish to delete via http://localhost:5000/delete_by_job_title
# Validate the input and search for the job in the database. If found, display the job details and ask the user for confirmation before deletion. 
# Delete the job from the MongoDB collection upon confirmation
@app.route('/delete_by_job_title', methods=['DELETE'])
def delete_by_job_title():
    try:
        # Get job title and confirmation from the request body
        job_title = request.form.get('job_title')
        confirmation = request.form.get('confirmation')

        # Query the database to find the job by title
        job = collection.find_one({"title": job_title})

        # If job not found, return appropriate response
        if job is None:
            return jsonify({"message": "Job not found"}), 404

        # Job found, return current details and ask for confirmation
        job['_id'] = str(job['_id'])
        confirmation_message = f'Are you sure you want to delete the job with title: {job_title}? Enter Yes to confirm or No to cancel.'
        response_data = {
            "message": confirmation_message,
            "job_details": job
        }

        # If user confirms with 'Yes', delete the job from the database
        if confirmation and confirmation.lower() == 'yes':
            collection.delete_one({"title": job_title})
            response_data["message"] = f"Job '{job_title}' deleted successfully"
        else:
            response_data["message"] = "Deletion canceled"

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

##############################################################################################################################
# Salary Range Query
# Develop an endpoint to query jobs based on a salary range.
# The user should be able to provide min_salary and max_salary as query parameters, and the API should return jobs within that salary bracket.
@app.route('/jobs_by_salary', methods=['GET'])
def jobs_by_salary():
    try:
        # Get min_salary and max_salary from query parameters
        min_salary = float(request.args.get('min_salary', 0)) # default to 0 if not provided
        max_salary = float(request.args.get('max_salary', float('inf'))) # default to infinity if not provided

        # Query the database to find jobs within the salary range
        jobs = collection.find({
            "average_salary": {
                "$gte": min_salary,
                "$lte": max_salary
            }
        })

        # Convert ObjectId to string for each document
        results = []
        for job in jobs:
            job["_id"] = str(job["_id"])
            results.append(job)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##############################################################################################################################
## Job Experience Level Query
# Create an endpoint where users can query jobs based on experience levels such as 'Entry Level', 'Mid Level', 'Senior Level', etc. 
# Users should be able to provide an experience_level query parameter, and the API should list jobs that match the given experience requirement.
@app.route('/jobs_by_experience_level', methods=['GET'])
def jobs_by_experience_level():
    try:
        # Get experience_level from query parameters
        experience_level = request.args.get('experience_level')

        # Query the database to find jobs within the salary range
        jobs = collection.find({
            "Level": experience_level
        })

        # Convert ObjectId to string for each document
        results = []
        for job in jobs:
            job["_id"] = str(job["_id"])
            results.append(job)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##############################################################################################################################
# Top Companies in an Industry
# Develop an endpoint to fetch top companies in a given industry based on the number of job listings.
#Users should provide an industry query parameter, and the API should return companies in that industry ranked by the number of job listings they have.
@app.route('/top_companies_by_industry', methods=['GET'])
def top_companies_by_industry():
    try:
        # Get industry from query parameters
        industry = request.args.get('industry')

        # Pipeline to aggregate and sort companies by the number of job listings
        pipeline = [
            {"$match": {"industry": industry}},
            {"$group": {"_id": "$company_name", "job_count": {"$sum": 1}}}, # group by company_name and count the number of jobs
            {"$sort": {"job_count": -1}} # sort by job_count in descending order
            # change display name to 'company_name' and 'job_count'
            #{"$project": {"company_name": "$_id", "job_count": 1}} # 1 means true        
        ]

        # Aggregate the data based on the pipeline
        companies = collection.aggregate(pipeline)
        # Convert ObjectId to string for each document
        results = [{"company_name": company["_id"], "job_count": company["job_count"]} for company in companies]

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##############################################################################################################################
@app.errorhandler(404)
def page_not_found(e):
    '''Send message to the user if route is not defined.'''

    message = {
        "err":
            {
                "msg": "This route is currently not supported."
            }
    }

    resp = jsonify(message)
    # Sending 404 (not found) response
    resp.status_code = 404
    # Returning the object
    return resp