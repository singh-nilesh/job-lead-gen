
import json
from docxtpl import DocxTemplate
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_qdrant import QdrantVectorStore
from app.core.logger import service_logger as logger
from app.core.utils import _get_unique_union
from app.core.config import Settings
from app.core.exception import ServiceException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser

from app.llm.prompts.ingest_job_data import get_cover_letter_multi_query_prompt
from app.llm.prompts.generate_coverletter import get_generate_coverletter_prompt
from app.llm.models import get_llm_model
from app.llm.schema import CoverLetterOutputSchema


class CoverLetterService:
    """ Cover Letter Generation Service
    Handles the generation of cover letters based on user data and job descriptions.
    """
    def __init__(self, db: AsyncIOMotorClient, vector_store: QdrantVectorStore):
        self.db = db
        self.vector_store = vector_store

    async def generate_from_text(
            self, 
            user_id: str, 
            job_data: str,
            file_path: str,
            user_personalized_input: str = ""):
        ''' generate cover letter from text input ( Job Description ) '''

        if not file_path.endswith(".docx"):
            raise ServiceException("Invalid file format. Only .docx files are supported for cover letter output.", status_code=400)
        
        logger.info(f"Generating cover letter for user_id:{user_id}")
        try:
            user_context = await self._multi_query_retrival(user_id, job_data, user_personalized_input)
            cover_letter_data = await self._generate_cover_letter(job_data, user_context, user_personalized_input)
            output_path = self._convert_to_docx(cover_letter_data, file_path)

            return output_path
        
        except ServiceException as se:
            raise se
        except Exception as e:
            logger.error(f"Unexpected error during cover letter generation for user_id:{user_id}: {e}")
            raise ServiceException("An unexpected error occurred during cover letter generation.", status_code=500)

    

    async def generate_from_job_id(self):
        ''' generate cover letter for existing job in DB'''
        pass
     

    async def _multi_query_retrival(self, user_id: str, job_data: str, user_personalized_input: str = ""):
        ''' Multi-Query Retrieval for relevant experience snippets '''
        
        logger.info(f"cover letter Multi-Query Retrieval for user_id:{user_id}")
        llm = get_llm_model()
        retriver = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k":4})

        # Multi-Query chain
        prompt_perspective = get_cover_letter_multi_query_prompt()
        generate_querys = (
            prompt_perspective
            | llm
            | StrOutputParser()
            | (lambda x: x.split("\n"))
        )

        # Retrieval chain
        retrieval_chain = (
            generate_querys
            | retriver.map()
            | _get_unique_union
        )
        # run
        docs = await retrieval_chain.ainvoke({
            "job_data": job_data,
            "user_personalized_input": user_personalized_input
        })

        if not docs:
            raise ServiceException("No relevant experience found for cover letter generation.", status_code=404)
        logger.info(f"Retrieved {len(docs)} relevant experience snippets for cover letter generation.")

        # Retrive User Profile Data
        user_profile_docs = await self.db["profile"].find_one({"user_id": user_id}, {"_id": 0, "user_id": 0})
        user_profile_docs = json.dumps(user_profile_docs)

        if not user_profile_docs:
            raise ServiceException("User profile data not found for cover letter generation.", status_code=404)
        logger.info(f"User profile data retrieved for user_id:{user_id}.")

        return '\n'.join([user_profile_docs] + [doc.page_content for doc in docs])
    

    async def _generate_cover_letter(
            self, 
            job_data: str, 
            user_context: str,
            user_personalized_input: str = ""
            ):
        ''' Generate cover letter data structure '''
        
        logger.info("Generating and compiling cover letter using LLM.")
        # LLM Cover Letter Generation.
        llm = get_llm_model()
        parser = PydanticOutputParser(pydantic_object=CoverLetterOutputSchema)
        
        main_prompt = get_generate_coverletter_prompt().partial(
            format_instructions=parser.get_format_instructions()
        )
        cover_letter_chain = main_prompt | llm | parser

        cover_letter_data = await cover_letter_chain.ainvoke({
            "job_data": job_data,
            "user_context": user_context,
            "personalization_instructions": user_personalized_input
        })

        if cover_letter_data is None:
            raise ServiceException("Failed to generate cover letter.", status_code=500)
        logger.info("Cover letter data structure generated successfully.")

        return cover_letter_data.dict()

    
    def _convert_to_docx(self, cover_letter_data: dict, file_path: str):
        ''' Convert cover letter  to .docx format'''

        logger.info("Converting cover letter to .docx format.")
        template_path = f"{Settings.ARTIFACTS_DIR}/coverletter_template.docx"
        
        document = DocxTemplate(template_path)
        document.render(cover_letter_data)
        document.save(file_path)

        logger.info(f"Cover letter saved to {file_path}.")
        return file_path