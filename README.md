# mdb-vector-search-demo
Really quick and simple python demo to show off MongoDB Atlas Vector Search using langchain for a RAG demo.

We download pages from wikipedia, send it to MongoDB, and can then run chatbot style queries.

## Setup
You will need a MongoDB Atlas cluster running. You can use a M10 cluster as this demo will not use much data.
We use OpenAI to create the embeddings, but another platform could also be used. 

The URL for MongoDB cluster and OpenAI key can be found in `params.py`

## Loading Data
We load data from wikipedia, but we could load data from any website.
The code for loading data is in `load_data.py`, and you can change the URL you want to load from.

We use langchain to chunk and load data into MongoDB (and then use langchain to query it)

## Create Vector Search Index
With the data now loaded in, you'll need to create the vector search index. From the Atlas UI, create the following index definition on the (by default collection) `vector_search_demo.data`. Call the index `vsearch_index`.

```
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "dotProduct",
      "type": "vector"
    }
  ]
}
```

## Query Data
With the data now loaded in with embeddings, we can query the data and ask questions (through Langchain). To run queries, you need to run the `rag_query.py` script with your question as a parameter. Examples:

```
python rag_query.py -q "where is Morgan Stanley's office?"
````
Result:
```
Your question:
-------------
Where is Morgan Stanley's office?
---------------

AI Response:
-----------
Morgan Stanley's office is located at 1585 Broadway in Midtown Manhattan, New York City.
```