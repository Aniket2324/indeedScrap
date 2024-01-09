import requests
from pymongo import MongoClient

url = "https://api.scrapingdog.com/indeed"
api_key = "659c2ba359e84b61df74f959"
job_search_url = "https://in.indeed.com/jobs?q=python+developer&l=&from=searchOnHP&vjk=dbbb8e5838436fb6"

params = {"api_key": api_key, "url": job_search_url}

# Make the HTTP GET request
response = requests.get(url, params=params)

if response.status_code == 200:
    # Parse the JSON content
    json_response = response.json()

    # Check for user not found error
    if 'success' in json_response and not json_response['success']:
        print(f"Error: {json_response['message']}")
    else:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['job_listings']
        collection = db['jobs']

        # Extract job listings from the response
        job_listings = json_response

        # Save the job listings in MongoDB
        for job in job_listings:
            collection.insert_one(job)

        print(f"Successfully stored {len(job_listings)} job listings in MongoDB.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
