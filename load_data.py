# https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/mongodb_atlas

from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
import params

# Step 1: Load
loaders = [
    WebBaseLoader("https://en.wikipedia.org/wiki/Morgan_Stanley")
]
data = []
for loader in loaders:
    data.extend(loader.load())

# Step 2: Transform (Split)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[
                                               "\n\n", "\n", "(?<=\. )", " "], length_function=len)
docs = text_splitter.split_documents(data)
print('Split into ' + str(len(docs)) + ' docs')

# Step 3: Embed
# https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html
embeddings = OpenAIEmbeddings(openai_api_key=params.openai_api_key)

# Step 4: Store
# Initialize MongoDB python client
client = MongoClient(params.mongodb_conn_string)
collection = client[params.db_name][params.collection_name]

# Insert the documents in MongoDB Atlas with their embedding
docsearch = MongoDBAtlasVectorSearch.from_documents(
    docs, embeddings, collection=collection, index_name=params.index_name
)