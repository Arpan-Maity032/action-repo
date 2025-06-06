# db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# check the MONGO_URI is set
if not MONGO_URI:
    raise ValueError("No MONGO_URI environment variable set for MongoDB connection.")

# Create a MongoClient to connect to the running MongoDB instance
client = MongoClient(MONGO_URI)

# Get the database
db = client.webhook_db

# Get the collection 
collection = db.events