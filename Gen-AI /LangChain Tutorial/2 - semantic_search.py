# End Objective: To get understanding of LangChain's document loader, embedding, and vector store abstractions. These abstractions are designed to support retrieval of data-- from (vector) databases and other sources-- for integration with LLM workflows. 

# Task: We will build a search engine over PDF document. Based on our input query, we will retrieve relevant documents from the PDF and display them.

# STEP 1: Import necessary libraries
from dotenv import load_dotenv
_ = load_dotenv()  # Load environment variables from .env file

from langchain_community.document_loaders import PyPDFLoader # Document loader for PDF files. It loads the content of PDF files into LangChain's document format.

file_path = "/Users/saikiran/Desktop/Generative-AI-Learning/Gen-AI /LangChain Tutorial/nke-10k-2023.pdf" # Path to the PDF file
loader = PyPDFLoader(file_path) # Create a loader instance for the PDF file

docs = loader.load() # Load the documents from the PDF file

print(f"No of documents loaded: {len(docs)}") # Print the number of documents loaded

# In LangChain, a document is a structured representation of text data. It includes the page content and metadata such as page number, source, and other relevant information. 
# Documents are used to represent the text data that will be processed by language models or other components in a LangChain workflow.

# For testing purpose: 
# print(docs[0].page_content[:200]) # Printing 200 words in the first document loaded from the PDF file
# print(docs[0].metadata) # Printing metadata of the first document loaded from the PDF file 

# STEP 2: Import library to do splitting of the document. 

# We are going to use RecursiveCharacterTextSplitter to split the document into chunks each having 1000 characters and 200 overlap. Overlap means that the last 200 characters of one chunk will be included in the next chunk. This is useful for maintaining context between chunks.
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Size of each chunk in characters
    chunk_overlap=200,  # Overlap between chunks in characters
    add_start_index=True  # Adds the index of the characteer where the chunk starts in the metadata of the particular document
)

all_splits = text_splitter.split_documents(docs)  # Split the loaded documents into chunks
print(f"No of chunks created: {len(all_splits)}")  # Print the number of chunks created

# STEP 3: Import libraries for embedding 

# Embedding helps in converting our chunks into vector representations or numerical representations. Later, 
# once user inputs the query, the same gets embedded into the same dimension and can find the related embeddings using similarity search (cosine similarity).

from langchain_ollama import OllamaEmbeddings  # Import OllamaEmbeddings for embedding text

embeddings_model = OllamaEmbeddings(model="nomic-embed-text:latest")  # Create an instance of OllamaEmbeddings with the specified model

# print(embeddings_model.embed_query(all_splits[0].page_content))

# STEP 4: Import libraries for vector store

# Now since our embeddings are ready to be created, we then create a vector store to store these embeddings which can be used for similarity search later.
from langchain_core.vectorstores import InMemoryVectorStore # Its an in-memory vector store that allows us to store and retrieve embeddings efficiently.

# We will initialize our vector store with our embeddings model 
vector_store = InMemoryVectorStore(embeddings_model)  # Create an instance of InMemoryVectorStore with the embeddings model

# Adding all our chunks (splitted documents) to the vector store
ids = vector_store.add_documents(all_splits)  # Add the split documents to the vector store and get their IDs

# Searching the vector store based on user input 

# Type 1: Using vector_store.similarity_search() method 
query = "What is the revenue of the company?"  # User input query
print(vector_store.similarity_search(query, k=3))  # Perform similarity search in the vector store and print the top 3 results.

# Type 2: Using vector_store.similarity_search_with_score() method
results_with_score = vector_store.similarity_search_with_score(query)  # Perform similarity search with scores mentioning the similarity score of each result (Remember the score varies from each vector store)
data, score = results_with_score[0]  # Get the first result and its score
print(f"Score: {score} \n {data}")  # Print the score of the first result

# Type 3: Using vector_store.similarity_search_by_vector() method
query_vector = embeddings_model.embed_query(query)  # Embed the query to get its vector representation
results_by_vector = vector_store.similarity_search_by_vector(query_vector)  # Perform similarity search using the query vector
print(f"Results by vector: {results_by_vector}")  # Print the results obtained by searching with the query vector