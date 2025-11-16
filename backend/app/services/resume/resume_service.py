
from sqlalchemy.orm import Session
from app.models.resmue import Resmue
from app.core.utils import load_json_file
import json
import os

class ResumeService:
    def __init__(self, db:Session):
        self.db = db
    
    def process_resume(self, resume_data:dict):
        pass

    def save_resume(self, resume_data:Resmue):
        # Inserting records into the database

        self.db.add(resume_data)
        self.db.commit()



if __name__ == "__main__":
    
    # load test data
    file_path = os.path.join(os.path.dirname(__file__), "test_data.json")
    with open(file_path, "r") as f:
        resume_json = json.load(f)
    resume_data = Resmue(**resume_json)

    from app.db.sqlalchemyConfig import get_db

    with get_db() as db:
        resume_service = ResumeService(db)
        res = resume_service.save_resume(resume_data)

    