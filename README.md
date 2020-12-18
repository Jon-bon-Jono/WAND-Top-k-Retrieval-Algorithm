# WAND-Top-k-Retrieval-Algorithm
This is a python implementation of the WAND algorithm presented in the [Exploring the Magic of WAND](http://culpepper.io/publications/pcm13-adcs.pdf) paper. The algorithm is used top-k retrieval in web search
## Usage: 
For testing

> `python3 tc[1-4].py`

A query is made by calling

> `WAND_Algo(query_terms, top_k, inverted_index)`
### Inputs:
`query_terms` is a list of strings, `top_k` is an integer >= 1 and `inverted_index` is a dictionary with key : term; value : list of tuples [(doc_id, weight)]

The inverted index model `InvertedIndex(documents).get_inverted_index()` accepts a document as input (a dictionary with with key: doc_id and value: document text and returns the `inverted_index`

No preprocessing methods are used, only `split` to get terms.

The normalized tf-idf is calculated in `Inv_index.py` from the formula:


### Output:
Outputs a list of the form (score, doci_id) where score corresponds to the sum of tf-idf scores among all the term based on the intersection of the query and document. Also outputs full_evaluation_count, the number of documents fully evaluated in the WAND algorithm




