"""
MongoDB Connection and Database Operations
Developed by TEAM SPIDERMERN (SANJAY B, YASWANTH ST, ABISHECK AM)
"""

import pymongo
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            mongo_settings = settings.MONGODB_SETTINGS
            self._client = pymongo.MongoClient(mongo_settings['host'])
            self._db = self._client[mongo_settings['db']]
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @property
    def db(self):
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        return self.db[collection_name]
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# MongoDB Collections Manager
class MongoCollections:
    def __init__(self):
        self.mongo = MongoDBConnection()
        
    @property
    def staff(self):
        return self.mongo.get_collection('staff')
    
    @property
    def classes(self):
        return self.mongo.get_collection('classes')
    
    @property
    def subjects(self):
        return self.mongo.get_collection('subjects')
    
    @property
    def rooms(self):
        return self.mongo.get_collection('rooms')
    
    @property
    def timetables(self):
        return self.mongo.get_collection('timetables')
    
    @property
    def labs(self):
        return self.mongo.get_collection('labs')
    
    @property
    def electives(self):
        return self.mongo.get_collection('electives')
    
    @property
    def substitutions(self):
        return self.mongo.get_collection('substitutions')

# Global instance
mongo_collections = MongoCollections()