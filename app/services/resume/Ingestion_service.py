from motor.motor_asyncio import AsyncIOMotorClient
from langchain_qdrant import QdrantVectorStore
from langchain_core.output_parsers import PydanticOutputParser

from app.core.logger import service_logger as logger
from app.core.exception import ServiceException
from app.core.utils import get_if_awaitable, set_user_id_all, _insert_resume_sections, _extract_pdf_text, _extract_docx_text, _construct_document

from app.llm.prompts.ingest_resume import get_ingest_resume_prompt
from app.llm.schema import ResumeOutputSchema
from app.llm.models import get_llm_model


class ResumeIngestionService:
    """ Resume Ingestion Service
    Handles the ingestion of resumes into individual sections for better processing.
    """

    def __init__(self, db: AsyncIOMotorClient, vector_store: QdrantVectorStore):
        self.db = db
        self.vector_store = vector_store

    async def ingest(self, resume_filepath: str, user_id: str) -> bool:
        """Ingest the resume document into sections, process and store.
        Args:
            resume_filepath: The path to the resume document.
            user_id: The user ID associated with the resume.

        Returns:
            True if ingestion is successful, False otherwise.
        """
        res = False
        logger.info("Starting resume ingestion process.")
        if not resume_filepath:
            logger.error("No resume document provided for ingestion.")
            return False

        try:
            # Step 1: Extract text from resume
            text = self._extract_text(resume_filepath, user_id)

            # Step 2: Parse resume text using LLM chain
            resume_dict = await self._llm_parser(text)

            # Step 3: Save to APP database
            id_dict = await self._save_resume(resume_dict, user_id)

            # Step 4: Compute and store vector embeddings
            res = await self._save_embeddings(id_dict)

            if res:
                logger.info(f"Resume ingestion process completed successfully for user_id:{user_id}")
            return res

        except Exception as e:
            logger.error(f"Unexpected error during resume ingestion: {e} for user_id:{user_id}")
            raise ServiceException("Resume ingestion failed.", logger=logger)


    async def _llm_parser(self, text: str) -> dict:
        """Parse the resume text into structured format using LLMs."""
        logger.info("Parsing resume text using LLM chain.")

        parser = PydanticOutputParser(pydantic_object=ResumeOutputSchema)
        llm = get_llm_model()

        prompt = get_ingest_resume_prompt()
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())

        # Langchain LLM chain
        extract_chain = prompt | llm | parser

        # Invoke the chain (async)
        result = await extract_chain.ainvoke({"resume_input": text})
        if not result:
            logger.error("LLM failed to parse resume text into structured format.")
            raise ServiceException("LLM failed to parse resume text.", logger=logger)

        logger.info("Successfully parsed resume text into structured format.")
        return result.dict()


    def _extract_text(self, path: str, user_id: str) -> str:
        """Extract text from the resume document based on file type."""
        logger.info(f"Extracting text from resume document: {path} for user_id:{user_id}")

        if path.endswith(".pdf"):
            logger.info(f"Extracting text from PDF resume document: {path} for user_id:{user_id}")
            return _extract_pdf_text(path)

        if path.endswith(".docx"):
            logger.info(f"Extracting text from DOCX resume document: {path} for user_id:{user_id}")
            return _extract_docx_text(path)

        raise ServiceException(
            f"Unsupported file format for resume extraction, use .pdf OR .docx: {path} for user_id:{user_id}",
            logger=logger,
        )


    async def _save_resume(self, resume: dict, user_id: str):
        """Save resume to the App database (NoSQL)."""
        logger.info(f"Saving resume for user_id: {user_id}")

        # Ensure user_id is set in all sections
        set_user_id_all(resume, user_id)

        id_dict = await _insert_resume_sections(self.db, resume)
        if id_dict:
            logger.info(f"Successfully saved resume sections for user_id: {user_id}")
            return id_dict

        logger.error(f"Failed to save resume sections for user_id: {user_id}")
        return None


    async def _save_embeddings(self, id_dict: dict) -> bool:
        """Compute and save vector embeddings for resume sections."""
        if not id_dict:
            logger.error("No ID dictionary provided for embedding storage.")
            return False

        logger.info("Starting to compute and save vector embeddings for resume sections.")
        documents = _construct_document(id_dict)
        if not documents:
            logger.error("No documents constructed for embedding storage.")
            return False
        
        # ---------- Log vector store details
        try:
            logger.debug(f"VectorStore Type: {type(self.vector_store)}")
            logger.debug(f"Collection Name: {self.vector_store.collection_name}")

            # Log Qdrant client connection details
            client = self.vector_store.client
            logger.debug(f"Qdrant Client: {client}")
            logger.debug(f"Qdrant Host: {getattr(client, 'host', None)}")
            logger.debug(f"Qdrant Port: {getattr(client, 'port', None)}")
            logger.debug(f"Qdrant URL: {getattr(client, 'url', None)}")

            # Log embedding model used
            logger.debug(f"Embedding Model: {self.vector_store.embeddings}")
            first_emb = self.vector_store.embeddings.embed_query(documents[0].page_content)
            logger.debug(f"Embedding dimension: {len(first_emb)}")

            # Log collection parameters (very useful)
            try:
                collection_info = client.get_collection(self.vector_store.collection_name)
                logger.debug(f"Collection Info: {collection_info}")
            except Exception as e:
                logger.warning(f"Unable to fetch collection info: {e}")

        except Exception as e:
            logger.error(f"Error while logging vector store details: {e}")
        # ------------- End ---------
        
        try:
            result = self.vector_store.add_documents(documents)
            logger.debug(f"VectorStore.add_documents() returned: {result}")
            logger.info("Successfully saved vector embeddings for resume sections.")
            return True
        except Exception as e:
            logger.error(f"Error saving vector embeddings: {e}")
            return False


