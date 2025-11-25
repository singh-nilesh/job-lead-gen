from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_qdrant import QdrantVectorStore
from langchain_core.output_parsers import PydanticOutputParser

from app.core.logger import service_logger as logger
from app.core.exception import ServiceException
from app.core.utils import set_user_id_all, get_if_awaitable
from .helpers.db_helpers import _insert_resume_sections, _construct_document
from .helpers.file_helpers import _extract_pdf_text, _extract_docx_text

from app.llm.prompts.ingest_resume import get_ingest_resume_prompt
from app.llm.schema import ResumeOutputSchema
from app.llm.models import get_llm_model


class ResumeIngestionService:
    ''' Resume Ingestion Service
    Handles the ingestion of resumes into individual sections for better processing.
    '''
    def __init__(self, db: AsyncIOMotorClient, vector_store: QdrantVectorStore):
        self.db = db
        self.vector_store = vector_store


    async def ingest(self, resume_doc: Any, user_id: str) -> bool:
        ''' Ingest the resume document into sections, process and store 
        Args:
            resume_doc (Any): The resume document object containing path and metadata.
            user_id (str): The user ID associated with the resume.
        Returns:
            bool: True if ingestion is successful, False otherwise.
        '''

        res = False
        logger.info("Starting resume ingestion process.")
        if not resume_doc:
            logger.error("No resume document provided for ingestion.")
            return False

        # Extract text from resume
        text = self._extractText(resume_doc.path, user_id)

        # LLM chain resume parser
        resume_dict = await self._llm_parser(text)

        # Save to APP database
        id_dict = await self._save_resume(resume_dict, user_id)

        # Compute and store vector embeddings
        res = await self._save_embeddings(id_dict)

        if res:
            logger.info(f"Resume ingestion process completed successfully. for user_id:{user_id}")
        return res
    

    async def _llm_parser(self, text:str) -> dict:
        ''' Parse the resume text into structured format using LLMs '''
        logger.info("Parsing resume text using LLM chain.")
        
        # pydantic output parser
        parser = PydanticOutputParser(pydantic_object=ResumeOutputSchema)
        
        # Get LLM model
        llm = get_llm_model()
        
        # Prompt construction
        prompt = get_ingest_resume_prompt()
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())

        # Langchain LLM chain
        extract_chain = (
            prompt | llm | parser
        )

        # Invoke the chain
        result = await extract_chain.invoke({"resume_input": text})
        logger.info("Successfully parsed resume text into structured format.")
        return result



    async def _save_embeddings(self, id_dict: dict) -> bool:
        ''' Compute and save vector embeddings for resume sections '''

        if not id_dict:
            logger.error("No ID dictionary provided for embedding storage.")
            return False
        logger.info("Starting to compute and save vector embeddings for resume sections.")

        documents = _construct_document(id_dict)
        if not documents:
            logger.error("No documents constructed for embedding storage.")
            return False

        try:
            # Conditional Await for async or sync method
            await get_if_awaitable(
                self.vector_store.add_documents(documents)
            )
            logger.info("Successfully saved vector embeddings for resume sections.")
            return True
        
        except Exception as e:
            logger.error(f"Error saving vector embeddings: {str(e)}")
            return False    


    def _extractText(self, path: str, user_id: int) -> str:
        ''' Extract text from the resume document based on file type '''
        if path.endswith('.pdf'):
            return _extract_pdf_text(path)
        
        elif path.endswith('.docx'):
            return _extract_docx_text(path)
        
        else:
            raise ServiceException(f"Unsupported file format for resume extraction, use .pdf OR .docx: {path}, for user_id:{user_id}")
        

    async def _save_resume(self, resume: dict, user_id: int):
        ''' Save resume to the App database (NOSQL) '''
        logger.info(f"Saving resume for user_id: {user_id}")

        # Ensure user_id is set in all sections
        set_user_id_all(resume, user_id)
        logger.debug(f"User_ID after setting user_id: {resume.profile.get('user_id')}")

        id_dict = await _insert_resume_sections(self.db, resume)
        if id_dict:
            logger.info(f"Successfully saved resume sections for user_id: {user_id}")
            return id_dict
        
        logger.error(f"Failed to save resume sections for user_id: {user_id}")
        return
        