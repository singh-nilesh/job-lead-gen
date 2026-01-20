
from langchain_qdrant import QdrantVectorStore
from motor.motor_asyncio import AsyncIOMotorDatabase
from langchain_core.output_parsers import PydanticOutputParser

from app.llm.prompts.ingest_job_data import get_ingest_job_data_prompt
from app.llm.prompts.generate_resume import get_generate_resume_prompt
from app.core.logger import service_logger as logger
from app.core.exception import ServiceException
from app.db.mongo.types import JobDescription
from app.llm.models import get_llm_model
from app.llm.schema import ResumeOutputSchema

from app.core.utils import _filter_unique_ids, _get_user_data
from .helper_text_to_docx import _parse_to_docx
import asyncio


class ResumeGenerationService:
    """ Resume Generation Service
    Handles the generation of resumes based on user data and job descriptions.
    """
    def __init__(self, db: AsyncIOMotorDatabase, vector_store: QdrantVectorStore):
        self.db = db
        self.vector_store = vector_store
    

    async def generate(self, user_id:str, job_data:str, output_path:str, job_url:str = None) -> str:
        """Generate a resume document based on user data and job description.
        Args:
            user_id: The user ID for whom the resume is to be generated.
            job_data: The job description or data to tailor the resume.

        Returns:
            A .docx file path, preferibly provide output_path to save the file. else: /tmp/resume_{user_id}.docx
        """

        if not output_path:
            output_path = f"/tmp/resume_{user_id}.docx" if user_id else "/tmp/resume.docx"
        
        try:
            # Step 1: Process job data
            processed_job_data = await self._job_data_processing(job_data)

            # Step 2: Query user data relevant to job description
            user_data = await self._query_user_data(user_id, processed_job_data)
            
            # Step 3: Generate resume content using LLM
            resume_content = await self._llm_resume_generation(user_data, processed_job_data)

            # Step 4: Convert resume content to DOCX
            docx_path = _parse_to_docx(resume_content, output_path, user_id)

            logger.info(f"Resume generated successfully for user_id:{user_id} at {docx_path}")
            return docx_path
        
        except ServiceException as se: # re-throw service exceptions to api layer
            raise se
        except Exception as e:
            logger.error(f"Unexpected error during resume generation: {e} for user_id:{user_id}")
            raise ServiceException("Resume generation failed due to unexpected error.", logger=logger)


    async def _job_data_processing(self, job_data:str) -> dict:
        """ Process job data to extract relevant points"""
        logger.info("pre-Processing job data for resume generation.")

        # LLM chain to processs job data
        parser = PydanticOutputParser(pydantic_object=JobDescription)
        llm = get_llm_model()
        prompt = get_ingest_job_data_prompt().partial(
            format_instructions=parser.get_format_instructions()
            )

        chain = prompt | llm | parser

        result = await chain.ainvoke({"job_data": job_data})
        if not result:
            raise ServiceException("LLM failed to process job data for resume generation.", status_code=422, logger=logger) #unprocessable entity
        
        logger.info("Job data pre-processed successfully for resume generation.")
        return result.dict()
    

    async def _async_vector_search(self, texts:str):
        """ Async async vector search for multiple texts."""
        doc = await self.vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k":2}
            ).aget_relevant_documents(texts)
        
        if not doc:
            logger.warning(f"No matching documents found for query text: '{texts[:50]}...'")
            return None
        return doc


    async def _query_user_data(self, user_id:str, job_data:dict) -> dict:
        """ Use similarity search to query user data relevant to the job description."""
        logger.info("Similarity searching user data as per job description.")

        texts = job_data.get("description")

        # vector db search
        async_searches = [ self._async_vector_search(texts) for texts in texts]
        res = await asyncio.gather(*async_searches)

        docs = []
        for group in res:
            if group:
                docs.extend(group)

        if not docs:
            raise ServiceException("Insufficient user data found. Please upload or add more profile details before generating a resume.", status_code=404, logger=logger)
        else:
            db_ids = _filter_unique_ids(docs)
            if not db_ids:
                raise ServiceException("User data exists in vector DB but metadata is missing or corrupted. Please re-ingest your profile/resume.", logger=logger)
        
        # main db query
        result = await _get_user_data(db_ids, user_id, self.db)
        if not result:
            raise ServiceException("Failed to retrieve user data from main_db.", logger=logger)
        
        logger.info(f"User data retrieved successfully for resume generation. {len(result)} records found.")
        return result


    async def _llm_resume_generation(self, user_data:list, job_data:str) -> str:
        """ Use LLM to generate resume content based on user data."""
        logger.info("Generating resume content using LLM.")

        try: # LLM chain for resume generation
            llm = get_llm_model()
            parser = PydanticOutputParser(pydantic_object=ResumeOutputSchema)
            prompt = get_generate_resume_prompt().partial(
                format_instructions=parser.get_format_instructions(),
                job_posting = job_data
                )

            chain = prompt | llm | parser

            res = await chain.ainvoke({"user_data": user_data})
            if not res:
                raise ServiceException("LLM failed to generate resume content.", logger=logger)
            
            logger.info("Resume content generated successfully using LLM.")
            logger.debug(f"Generated Resume Content: {res}")
            return res.dict()

        except Exception as e:
            logger.error(f"Error during LLM resume generation: {e}")
            raise ServiceException("LLM resume generation failed.", logger=logger)

        