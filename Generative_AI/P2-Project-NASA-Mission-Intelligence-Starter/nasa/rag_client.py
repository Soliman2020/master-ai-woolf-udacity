import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path
from openai import OpenAI
import os

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    chroma_dirs = list(current_dir.glob("**/chroma_db*"))
    print(chroma_dirs)
    # TODO: Loop through each discovered directory
    for chroma_dir in chroma_dirs:
        if not chroma_dir.is_dir():
            continue
        # TODO: Wrap connection attempt in try-except block for error handling
        try:
            # TODO: Initialize database client with directory path and configuration settings
            client = chromadb.PersistentClient(path=chroma_dir)
            
            # TODO: Retrieve list of available collections from the database
            collections = client.list_collections()

            # TODO: Loop through each collection found
            for collection in collections:
                # TODO: Create unique identifier key combining directory and collection names
                key = f"{chroma_dir.name}_{collection.name}"
                
                # TODO: Build information dictionary containing:
                try:
                    doc_count = collection.count()
                except Exception as e:
                    doc_count = "unknown"
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
                backends[key] = {
                    "directory": str(chroma_dir),
                    "collection_name": collection.name,
                    "display_name": f"{chroma_dir.name} / {collection.name} ({doc_count} docs)",
                }
        except Exception as e:
            error_msg = str(e)
            # print(error_msg)
            key = f"{chroma_dir.name}_error"
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information
            backends[key] = {
                "directory": str(chroma_dir),
                "collection_name": None,
                "display_name": f"{chroma_dir.name} ({error_msg})",
            }
    # TODO: Return complete backends dictionary with all discovered collections
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""
    try:
        # TODO: Create a chomadb persistentclient with the chroma_dir path
        client = chromadb.PersistentClient(path=chroma_dir)
        # TODO: Get the collection with the collection_name
        collection = client.get_collection(name=collection_name)

        # TODO: Return the collection with the collection_name
        return collection, True, None

    except Exception as e:
        error_msg = str(e)
        return None, False, error_msg


def get_embedding(text: str, openai_key: str = None) -> List[float]:
    """Get embedding for text using OpenAI API"""
    api_key = openai_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not provided")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openai.vocareum.com/v1"
    )

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def retrieve_documents(collection, query: str, n_results: int = 3,
                      mission_filter: Optional[str] = None, openai_key: str = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # Initialize filter variable to None (represents no filtering)
    filter = None

    # Check if filter parameter exists and is not set to "all" or equivalent
    if mission_filter and mission_filter != "all":
        filter = {"mission": mission_filter}

    # Get embedding for the query using OpenAI
    query_embedding = get_embedding(query, openai_key)

    # Execute database query with the embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=filter
    )

    return results


def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section
    context_parts = ["# Context"]
    
    # TODO: Loop through paired documents and their metadata using enumeration
    for i, (doc, meta) in enumerate(zip(documents, metadatas),1):
        
        # TODO: Extract mission information from metadata with fallback value
        mission = meta.get("mission", "unknown")
        
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        mission = mission.replace("_", " ").title()
 
        # TODO: Extract source information from metadata with fallback value  
        source = meta.get("source", "unknown")
        
        # TODO: Extract category information from metadata with fallback value
        category = meta.get("category", "unknown")
        
        category = category.replace("_", " ").title()
        
        # TODO: Add source header to context parts list
        # TODO: Create formatted source header with index number and extracted information
        source_header = f"\n[Source{i}] Mission: {mission} - File: {source} - Category: {category}"
        context_parts.append(source_header)

        
        # TODO: Check document length and truncate if necessary
        max_doc_length = 4000
        # if len(doc) > max_doc_length:
        #     doc = doc[:max_doc_length] + "..."
        # else:
        #     doc = doc
        truncated_doc = doc[:max_doc_length] + "..." if len(doc) > max_doc_length else doc
        # TODO: Add truncated or full document content to context parts list
        context_parts.append(truncated_doc)
        
    # TODO: Join all context parts with newlines and return formatted string
    return "\n".join(context_parts)