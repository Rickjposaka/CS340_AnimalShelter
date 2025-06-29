from pymongo import MongoClient

class AnimalShelter:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        """
        Initialize connection to the MongoDB database and collection.
        """
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33923
        DB = 'AAC'
        COL = 'animals'

        self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        """
        Insert a single document into the collection.
        Returns True if insertion is successful, otherwise False.
        """
        if data:
            self.collection.insert_one(data)
            return True
        return False  

    def read(self, query):
        """
        Retrieve documents from the collection that match the query.
        Returns a list of documents or an empty list on error.
        """
        try:
            return list(self.collection.find(query, {"_id": False}))
        except Exception as e:
            print("Read error:", e)  
            return []

    def update(self, query, new_values):
        """
        Update documents matching the query with new values.
        Returns the number of modified documents.
        """
        try:
            result = self.collection.update_many(query, {'$set': new_values})
            return result.modified_count
        except Exception as e:
            print("Update error:", e)
            return 0

    def delete(self, query):
        """
        Delete documents matching the query from the collection.
        Returns the number of deleted documents.
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print("Delete error:", e)
            return 0

    # -----------------------------
    # Project Two Custom Queries
    # -----------------------------

    def read_water_rescue(self):
        """
        Retrieve animals suitable for water rescue: Intact Female and breeds containing 'Retriever' or 'Newfoundland'.
        """
        query = {
            "breed": {"$regex": "Retriever|Newfoundland", "$options": "i"},
            "sex_upon_outcome": "Intact Female"
        }
        return list(self.collection.find(query, {"_id": False}))

    def read_mountain_rescue(self):
        """
        Retrieve animals suitable for mountain/wilderness rescue: Intact Male, age 26+ weeks, breed contains key terms.
        """
        query = {
            "breed": {"$regex": "Collie|Cattle Dog|Australian Shepherd|Husky", "$options": "i"},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26}
        }
        return list(self.collection.find(query, {"_id": False}))

    def read_disaster_rescue(self):
        """
        Retrieve animals suitable for disaster/individual tracking: Intact Male, Shepherd breed, age 26-156 weeks.
        """
        query = {
            "breed": {"$regex": "Shepherd", "$options": "i"},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return list(self.collection.find(query, {"_id": False}))
