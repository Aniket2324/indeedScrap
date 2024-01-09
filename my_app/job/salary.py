# average_salary.py
import numpy as np
from pymongo import MongoClient

def calculate_average_salary(city):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['job_listings']
    collection = db['jobs']

    # Query MongoDB for job listings in the specified city
    job_listings = collection.find({'companyLocation': {'$regex': f'.*{city}.*', '$options': 'i'}})

    # Extract salaries from job listings
    salaries = [job['salary'] for job in job_listings if 'salary' in job]
    numeric_salaries = [float(salary.replace('USD', '').replace(',', '').strip()) for salary in salaries]

    # Use NumPy to calculate the average salary
    average_salary = np.mean(numeric_salaries)

    return average_salary

if __name__ == "__main__":
    city = input("Enter the city: ")
    average_salary = calculate_average_salary(city)

    if np.isnan(average_salary):
        print(f"No salary data available for {city}.")
    else:
        print(f"The average salary for Python developers in {city} is: ${average_salary:,.2f}")
