#By Jonathan Williams, written November 2020

import pickle
from Inv_Index import InvertedIndex
from wand_algorithm import WAND_Algo


fname = './Data/sample_documents.pickle'
documents = pickle.load(open(fname,"rb"))

inverted_index = InvertedIndex(documents).get_inverted_index()
query_terms = ["President","New","York"]
top_k = 2

#WAND algorithm
topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)

print('Top-k result = ', topk_result)
print('Evaluation Count = ', full_evaluation_count)
