""" Resume Service Helper Functions """

from app.core.logger import service_logger as logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from langchain.docstore.document import Document

async def _insert_resume_sections(db: AsyncIOMotorClient, data: dict):
    ''' 
    Insert multiple resume sections into their respective collections 
    Auto-detects:
        - dict sections (profile)
        - list sections (education, work_experience)
    Returns:
        - dict of inserted IDs on success
        - False on failure
    '''
    doc_ids = {}
    try:
        logger.info("Inserting resume sections into collections")
        for key, value in data.items():
            collection = db[key]

            if isinstance(value, dict):
                # Single document (profile)
                result = await collection.insert_one(value)
                doc_ids[key] = {
                    "_id": result.inserted_id,
                    "data": value
                }
                logger.info(f"Inserted profile section into collection: {key}")

            elif isinstance(value, list):
                # Multiple documents (education, work_experience)
                if value:
                    results = await collection.insert_many(value)
                    doc_ids[key] = {
                        "_ids": results.inserted_ids,
                        "data": value
                    }
                    logger.info(f"Inserted {len(value)} items into collection: {key}")

        logger.info("Finished inserting resume sections successfully")
        return doc_ids

    except PyMongoError as pe:
        logger.error(f"PyMongo error while inserting resume sections - {str(pe)}")
        return False
    except Exception as e:
        logger.error(f"Error inserting resume sections - {str(e)}")
        return False



def _construct_document(data: dict) -> list[Document]:
    """Construct langchain.Document objects from _insert_resume_sections() output.

    - Only extracts the `description` field from supported collections.
    - If description is a list, joins with ''.join(...) to form a single string.
    - Metadata: collection_name, coll_id, user_id
    """

    documents = []
    # Store embedings for description fields only
    embedd_for_coll= ["education", "work_experience","projects", "certifications"]
    
    for coll_name, content in data.items():

        # Skip collections not meant for embeddings
        if coll_name not in embedd_for_coll:
            continue
        if not isinstance(content, dict) or 'data' not in content:
            continue

        # Extract items and their there DB IDs
        items:list[dict] = content.get('data')
        ids:list[str] = [str(id) for id in content.get('_id')]

        if not isinstance(items, list[dict]):
            continue

        # Process each item in the collection
        for idx, item in enumerate(items):
            
            #Assuming description field is a List[str], always
            desc = item.get('description', None)
            if isinstance(desc, list):
                desc = ' '.join(str(d) for d in desc)

                metadata = {
                "section": coll_name,
                "db_id": ids[idx],
                "user_id": item.get('user_id', None)
                }
                documents.append(
                    Document(page_content=desc, metadata=metadata)
                )

    return documents




if __name__ == "__main__":
    
    # Test data
    sample_data = {
        "education": [
            {
                "user_id": 1,
                "institution_name": "University A",
                "degree": "Computer Science",
                "field_of_study": "Computer Science",
                "start_date": "2015-09-01",
                "end_date": "2019-06-30",
                "grade": "3.8",
                "description": "Studied various computer science topics."
            }
        ],
        }
