from sqlalchemy.orm import Session
from app.models.resmue import Resmue
from app.core.utils import load_json_file
from app.db import schema
import json
import os

class ResumeService:
    def __init__(self, db:Session):
        self.db = db
    
    def save_resume(self, resume_data:dict | Resmue):
        """ Save resume data into the database """

        # ensure we have a Pydantic model instance
        if isinstance(resume_data, Resmue):
            data = resume_data
        else:
            data = Resmue(**resume_data)

        # build user dict (exclude nested lists)
        user_data = data.dict(exclude={"education", "work_experience"}, exclude_none=True)

        # create and persist user ORM to obtain id
        user_orm = schema.Users(**user_data)
        try:
            self.db.add(user_orm)
            self.db.commit()
            self.db.refresh(user_orm)
            user_id = user_orm.id

            # set user_id on nested pydantic objects
            data._set_user_id(user_id)

            # prepare child rows for bulk insert
            edu_rows = [e.dict(exclude_none=True) for e in (data.education or [])]
            we_rows = [w.dict(exclude_none=True) for w in (data.work_experience or [])]

            if edu_rows:
                self.db.bulk_insert_mappings(schema.Education, edu_rows)
            if we_rows:
                self.db.bulk_insert_mappings(schema.WorkExp, we_rows)

            self.db.commit()
            return user_orm

        except Exception as e:
            self.db.rollback()
            print(f"Error inserting resume data: {e}")
            return None






if __name__ == "__main__":
    
    # load test data
    file_path = os.path.join(os.path.dirname(__file__), "test_data.json")
    with open(file_path, "r") as f:
        resume_json = json.load(f)
    resume_data = Resmue(**resume_json)

    from app.db.sqlalchemyConfig import get_db

    with get_db() as db:
        resume_service = ResumeService(db)
        resume_service.save_resume(resume_data)

