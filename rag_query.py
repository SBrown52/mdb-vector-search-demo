import argparse
import params
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import warnings

# Filter out the UserWarning from langchain
warnings.filterwarnings("ignore", category=UserWarning, module="langchain.chains.llm")

# Process arguments
parser = argparse.ArgumentParser(description='Atlas Vector Search Demo')
parser.add_argument('-q', '--question', help="The question to ask")
args = parser.parse_args()

if args.question is None:
    # Some questions to try...
    query = "How big is MS company?"
    query = "Who started MS?"

else:
    query = args.question

print("\nYour question:")
print("-------------")
print(query)

# Initialize MongoDB python client
client = MongoClient(params.mongodb_conn_string)
collection = client[params.db_name][params.collection_name]

# initialize vector store
vectorStore = MongoDBAtlasVectorSearch(
    collection, OpenAIEmbeddings(openai_api_key=params.openai_api_key), index_name=params.index_name
)

qa_retriever = vectorStore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10, "post_filter_pipeline": [{"$limit": 1}]}
    )
    
llm = OpenAI(openai_api_key=params.openai_api_key, temperature=0)

    # Load "stuff" documents chain. Stuff documents chain takes a list of documents,
    # inserts them all into a prompt and passes that prompt to an LLM.

prompt_template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    {context}
    
    Question: {question}
    """
    
PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=qa_retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": PROMPT}
)

    # Execute the chain

retriever_output = qa.invoke(query)


# perform a similarity search between the embedding of the query and the embeddings of the documents
print("---------------")

print("\nAI Response:")
print("-----------")
print(retriever_output["result"])