import chromadb
from mcp.server.fastmcp import FastMCP
import os, uuid
from typing import List

mcp = FastMCP('chroma')

chroma_client = None

def get_chroma_client()->chromadb.PersistentClient:
    global chroma_client
    if chroma_client is None:
        if not os.path.exists(os.path.join(os.getcwd(), 'chroma_db/chroma.sqlite3')):
            print("Initializing ChromaDB client...")
            chroma_client = chromadb.PersistentClient(
                path=os.path.join(os.getcwd(), 'chroma_db')
            )
            print("ChromaDB client initialized.")
        else:
            print("ChromaDB client already exists.")
            chroma_client = chromadb.PersistentClient(
                path=os.path.join(os.getcwd(), 'chroma_db')
            )
    return chroma_client
    
@mcp.tool()
async def add_document(collection_name: str, document: str)->str:
    global chroma_client
    if not chroma_client:
        print("ChromaDB client not initialized. Initializing now...")
        chroma_client = get_chroma_client()
        print("ChromaDB client initialized.")
    try:
        collection_obj = chroma_client.get_or_create_collection(name=collection_name)
        for file in os.listdir(document):
            if file.endswith(".txt"):
                with open(os.path.join(document, file), 'r') as f:
                    content = f.read().splitlines()
                    collection_obj.add(
                        ids=[str(uuid.uuid4()) for _ in content],
                        documents=content
                    )
            else:
                print(f"Skipping non-text file: {file}")
                continue
        return f"Documents added to collection '{collection_name}' successfully."
    except Exception as e:
        return f"Error adding documents to collection '{collection_name}': {str(e)}"
    

@mcp.tool()
async def query_documents(collection_name: str, query: List[str], limit: int = 5)->dict:
    global chroma_client
    if not chroma_client:
        print("ChromaDB client not initialized. Initializing now...")
        chroma_client = get_chroma_client()
        print("ChromaDB client initialized.")
    try:
        collection_obj = chroma_client.get_collection(name=collection_name)
        results = collection_obj.query(
            query_texts=query,
            n_results=limit
        )
        ans = {}
        for i, query_result in enumerate(results['documents']):
            ans[f'Query {i}'] = query_result
        print(f"Retrieved documents from collection '{collection_name}': {ans}")
        return ans
    except Exception as e:
        return {'error': f"Error querying collection '{collection_name}': {str(e)}"}
    
def main():
    print("Starting FastMCP server...")
    try:
        

        global chroma_client
        chroma_client = get_chroma_client()
        print("ChromaDB client initialized.")
        print("Starting FastMCP server...")
        mcp.run(transport='stdio')
        print("FastMCP server is running.")
    except Exception as e:
        print(f"Failed to start FastMCP server: {str(e)}")

if __name__ == "__main__":
    main()