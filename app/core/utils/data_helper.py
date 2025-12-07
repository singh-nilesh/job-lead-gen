''' Service Data operation Helper Functions '''

import re
from bson import ObjectId
from langchain.docstore.document import Document
from app.core.logger import service_logger as logger
from langchain.load import dumps, loads


def _construct_document(data: dict) -> list[Document]:
    """Construct langchain.Document objects from _insert_resume_sections() output.

    - Only extracts the `description` field from supported collections.
    - If description is a list, joins with ''.join(...) to form a single string.
    - Metadata: collection_name, coll_id, user_id
    """

    documents = []
    # Store embedings for description fields only
    embedd_for_coll= ["work_experience","projects", "extra_curricular"]
    
    for coll_name, content in data.items():

        # Skip collections not meant for embeddings
        if coll_name not in embedd_for_coll:
            continue
        if not isinstance(content, dict) or 'data' not in content:
            continue

        # Extract items and their there DB IDs
        items:list[dict] = content.get('data')
        ids:list[str] = [str(id) for id in content.get('_ids')]

        if not isinstance(items, list):
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


def set_user_id_all(resume: dict, user_id: str) -> dict:
    """
    Auto-detects dict sections and list-of-dict sections,
    and sets user_id everywhere it appears.
    """

    for key, value in resume.items():

        # Case 1: Value is a dict (profile)
        if isinstance(value, dict):
            value["user_id"] = user_id

        # Case 2: Value is a list (education, work_experience)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    item["user_id"] = user_id

    return resume


def _filter_unique_ids(docs:list[Document]) -> dict[str, list[ObjectId]]:
    ''' Retrieve unique documents metadata from document list
    Args:
        docs: List of langchain Document objects.
    Returns:
        list of ids for sections/table in app_db. - used for full data retrieval.
    '''
    logger.info("Filtering unique documents for retrived docs.")

    seen = set()
    results = {}
    for doc in docs:
        section = doc.metadata.get('section', None)
        db_id = doc.metadata.get('db_id', None)

        # check for uniqueness
        key = (section, db_id)
        if key in seen:
            continue
        seen.add(key)

        # init new section list
        if section not in results:
            results[section] = []
        
        results[section].append(ObjectId(db_id))

    return results
 

def _get_unique_union(documents: list[list]):
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # unique set
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]


def _find_section_boundaries(text:str, section_titles:list[str] = None) -> dict:
    """
    Finds section boundaries in the resume text.
    Args:
        text: The complete resume text.
        section_titles: List of title section to find.
    Returns:
        A dict: {section_title: section_text}
    """
    if section_titles is None:
        section_titles = [
            "What You Will Do",
            "Nice to have",
            "Minimum Qualifications",
            "Key Responsibilities",
            "Required Technical Skills",
        ]

    # escape, igniring special chars.
    escaped = [re.escape(t) for t in section_titles]

    # Create a regex pattern to match section titles
    pattern = r'(?im)^\s*(?:' + '|'.join(escaped) + r')\s*$'
    combined_pattern = re.compile(pattern)

    matches = list(combined_pattern.finditer(text))

    sections = {}
    for i,m  in enumerate(matches):

        title = m.group(0).strip() # matched title

        start_idx = m.end()

        if i+1 < len(matches): # in-between sections
            end_idx = matches[i+1].start()
            
        else: # last section
            end_idx = len(text)
        
        body = text[start_idx:end_idx].strip()

        sections[title] = body
    
    return sections