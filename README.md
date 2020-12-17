# WAND-Top-k-Retrieval-Algorithm
This is a python implementation of the WAND algorithm presented in the [Exploring the Magic of WAND paper](http://culpepper.io/publications/pcm13-adcs.pdf). The algorithm is used top-k retrieval in web search
## Usage: 
For testing

> `python3 tc[1-4].py`

A query is made by calling

> `WAND_Algo(query_terms, top_k, inverted_index)`
### Inputs:
`query_terms` is a list of strings, `top_k` is an integer and `inverted_index` is a dictionary where terms point to a list of tuples [(doc_id, weight)]

The inverted index model accepts a document as input (a dictionary with with key: doc_id and value: document text)


