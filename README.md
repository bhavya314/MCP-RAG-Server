# MCP Document Management System

This project demonstrates a client-server application built using the Model Context Protocol (MCP). It provides a simple document management system where a server, powered by ChromaDB, exposes tools to add and query documents. A command-line client allows users to interact with these tools.

## Features

- **MCP-based Communication:** Utilizes the Model Context Protocol for robust client-server interaction.
- **Tool-based Architecture:** The server exposes functionalities as "tools" (`add_document`, `query_documents`) that the client can discover and call.
- **Vector-based Document Storage:** Uses ChromaDB to store and retrieve documents based on semantic similarity.
- **Asynchronous:** Built with Python's `asyncio` for efficient, non-blocking I/O.
- **Interactive CLI:** A simple command-line interface for users to interact with the document management system.

## Prerequisites

- Python 3.11+

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Create a `requirements.txt` file with the following content:**
    ```txt
    mcp.py
    chromadb
    sentence-transformers
    ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You should see output indicating that the ChromaDB client is initialized and the FastMCP server is running.

### Running the Client

The client connects to the server, discovers the available tools, and provides an interactive prompt for you to use them.

```bash
python client.py
```

## Example Session

Before running the example, create a directory named `sample_data` and place some `.txt` files inside it.

```bash
mkdir sample_data
echo "The Model Context Protocol (MCP) is for AI agent-to-tool communication." > sample_data/mcp.txt
```

Now, you can interact with the client:

```sh
$ python client.py
Connecting to the server...
# ... connection logs ...
Connected to the server successfully.
Starting chat loop. Type 'exit' or 'quit' to exit.
# ... tool information ...

Please choose a tool to use or type 'exit' to quit.

Query:
add_document
Enter collection name: my_docs
Enter document path: ./sample_data
Result from add_document: {'content': [], 'structuredContent': None, 'isError': False, 'result': "Documents added to collection 'my_docs' successfully."}

Please choose a tool to use or type 'exit' to quit.

Query:
query_documents
Enter collection name: my_docs
Enter query (comma-separated): what is mcp
Result from query_documents: {'content': [], 'structuredContent': {'Query 0': ['The Model Context Protocol (MCP) is for AI agent-to-tool communication.']}, 'isError': False, 'result': None}

Please choose a tool to use or type 'exit' to quit.

Query:
exit
Exiting chat loop.
Client session closed and exit stack cleaned up.
Client closed.
```

## Project Structure

```
.
├── client.py        # The MCP client application
├── server.py        # The MCP server application
└── chroma_db/       # Directory for ChromaDB persistent storage (auto-generated)
```