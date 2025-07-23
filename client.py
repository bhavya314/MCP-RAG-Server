from contextlib import AsyncExitStack
import asyncio
import logging, inspect
from typing import Optional, List


from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -{%(filename)s:%(lineno)d} %(message)s')
class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.session: Optional[ClientSession] = None

    async def connect_to_server(self, path_to_server):
        print(path_to_server)
        if not path_to_server.endswith('.py'):
            raise ValueError("The server file should be a Python script")
        
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[path_to_server]
        )
        print(f"Connecting to server: {server_params}")
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        print("Stdio transport established, creating session...")
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        print("Session created, initializing...")
        await self.session.initialize()
        print("Session initialized successfully.")
        response = await self.session.list_tools()
        tools = response.tools
        print(f"Available tools: {', '.join(tool.name for tool in tools)}")

    async def add_document(self, collection: str, document: str):
        print(f'Adding document to collection: {collection}, document: {document}')
        response = await self.session.list_tools()
        tools = response.tools
        if not any(tool.name == 'add_document' for tool in tools):
            raise ValueError("Tool 'add_document' not found in the server.")
        result = await self.session.call_tool('add_document', {"collection_name": collection, "document": document})
        print(f"Result from add_document: {result}")
        return result
    
    async def query_documents(self, collection: str, query: List[str]):
        print(f'Retrieving documents from collection: {collection}, query: {query}')
        response = await self.session.list_tools()
        tools = response.tools
        if not any(tool.name == 'query_documents' for tool in tools):
            raise ValueError("Tool 'query_documents' not found in the server.")
        result = await self.session.call_tool('query_documents', {'collection_name': collection, 'query': query})
        print(f"Result from query_documents: {result}")
        return result
    
    async def chat_loop(self):
        print("Starting chat loop. Type 'exit' or 'quit' to exit.")
        count = 0
        while True:
            count += 1
            if count <=1:
                response = await self.session.list_tools()
                tools = response.tools
                print(f"Available tools: {', '.join(tool.name for tool in tools)}\n")
                for tool in tools:
                    print(f"Tool: {tool.name} - Input Schema: {tool.inputSchema}\n")
            print("Please choose a tool to use or type 'exit' to quit.\n")
            user_input = input("Query:\n").strip().lower()
            if user_input in ['exit', 'quit']:
                print("Exiting chat loop.")
                break
            try:
                
                if user_input == 'add_document':
                    collection_name = input("Enter collection name: ").strip()
                    document_path = input("Enter document path: ").strip()
                    result = await self.add_document(collection_name, document_path)
                    print(f"Documents added to collection '{collection_name}': {result}")
                elif user_input == 'query_documents':
                    collection_name = input("Enter collection name: ").strip()
                    query = input("Enter query (comma-separated): ").strip().split(',')
                    result = await self.query_documents(collection_name, query)
                    print(f"Retrieved documents: {result}")
                else:
                    print(f"Tool '{user_input}' not recognized. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

    async def close(self):
        await self.exit_stack.aclose()
        print("Client session closed and exit stack cleaned up.")


async def main():
    import os
    client = MCPClient()
    path_to_server = os.path.join(os.getcwd(), 'server.py')
    try:
        print("Connecting to the server...")
        await client.connect_to_server(path_to_server)
        print("Connected to the server successfully.")
        await client.chat_loop()
        
    except Exception as e:
        print("Failed to connect to the server. Error:", e)
    finally:
        await client.close()
        print("Client closed.")


if __name__ == "__main__":
    asyncio.run(main())