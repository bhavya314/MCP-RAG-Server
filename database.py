from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
import os
import asyncio
from typing import List, Optional

class VectorDatabase:
    def __init__(self, db_path: str='./chroma_db'):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        self.embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-mpnet-base-v2'
        )
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def initialize_vector_store(self):
        ''' check if vector store already exists'''
        if os.path.exists(os.path.join(self.db_path, 'chroma.sqlite3')):
            print("Vector store already exists, loading...")
            self.vector_store = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings
            )
            print("Vector store loaded successfully.")
        else:
            print("Creating a new vector store...")
            self.vector_store = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings
            )
            print("New vector store created successfully.")

    async def add_documents(self, dir_path: str):
        ''' Add Documents to the vector store '''
        if not self.vector_store:
            await self.initialize_vector_store()
        if not os.path.exists(dir_path):
            print(f"The directory {dir_path} does not exist.")
            raise FileNotFoundError(f"The directory {dir_path} does not exist.")
        documents: List[Document] = []

        # Load text files from the directory
        for file in os.listdir(dir_path):
            if file.endswith('.txt'):
                file_path = os.path.join(dir_path, file)
                loader = TextLoader(file_path=file_path)
                documents.extend(loader.load())
            else:
                print(f'Skipping {file}. Not a text file.')
                continue

        # Split documents into smaller chunks
        chunks = self.text_splitter.split_documents(documents)
        _ = self.vector_store.add_documents(chunks)
        self.vector_store.persist()
        print(f"Added {len(chunks)} chunks to the vector store.")
        return {'added_chunks': len(chunks), 'total_documents': len(documents)}

    async def similarity_search(self, query: str, k: int = 5, score_threshold: Optional[float] = None):
        ''' Perform similarity search in the vector store '''
        if not self.vector_store:
            await self.initialize_vector_store()
        results = self.vector_store.similarity_search(query=query, k=k)
        if score_threshold:
            results = [doc for doc in results if doc.metadata.get('score', 0) >= score_threshold]
        return {'query': query, 'results': results}
