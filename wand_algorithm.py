#By Jonathan Williams, written November 2020
import math
import bisect
iterators = {}

class Iterator:
    def __init__(self,postings,term,term_string):
        self.postings = postings
        self.docs, _ = zip(*self.postings)
        self.cursor = 0
        self.term = term
        self.term_string = term_string
    #return posting at current cursor position
    def current(self):
        return self.postings[self.cursor]
    #advance cursor position if not at last posting
    def next(self):
        if self.last():
            return False
        else:
            self.cursor += 1
            return True
    #advance cursor to nearest position less than doc
    def gallop_to(self, doc):
        if doc == self.postings[self.cursor][0]: return True
        if doc < self.postings[self.cursor][0]:
            return False
        elif doc > self.postings[-1][0]:
            self.cursor = len(self.postings)-1
            return False
        else: 
            i = bisect.bisect_left(self.docs, doc, self.cursor)
            self.cursor = i
            return True
    def last(self):
        if self.cursor == len(self.postings)-1:
            return True
        else:
            return False
    def __str__(self):
        return "IT:: t:{}, cursor: {}\n postings: {}\nAt last element: {}\n".format(self.term, self.cursor, self.postings,self.last())
        

#creates iterator for term t, adds it to the list, returns first posting
def first_posting(postings, t, term_string):
    it = Iterator(postings, t, term_string)
    iterators[term_string] = it
    return it.current()
#return next posting or None
def next_posting(term_string):
    it = iterators[term_string]
    if it.next():
        return it.current()
    else:
        return None
#return nearest posting that is larger than or equal to doc or None
def seek_to_document(term_string, doc):
    it = iterators[term_string]
    if it.gallop_to(doc):
        return it.current()
    else: 
        return None

def WAND_Algo(query_terms, top_k, inverted_index):
    max_weights = {}
    candidates = []
    for t in range(0, len(query_terms)):
        qterm = query_terms[t]
        if not inverted_index[qterm]: continue
        #collect upper bound weight amongst all docs in index for the query term
        max_weights[qterm] = max(inverted_index[qterm], key=lambda x: x[1])[1]
        #get first candidate (first posting in the iterator) for the query term
        c_did, c_w = first_posting(inverted_index[qterm], t, query_terms[t])
        candidates.append((c_did, c_w, query_terms[t]))
    theta = float("-inf")
    ans = []
    fully_evaluated = 0
    while candidates:
        candidates = sorted(candidates, key=lambda c: c[0])
        score_limit = 0
        pivot = 0
        pivot_found = False
        while pivot < len(candidates):
            tmp_s_lim = score_limit + max_weights[candidates[pivot][2]]
            if tmp_s_lim > theta:
                pivot_found = True
                break
            score_limit = tmp_s_lim
            pivot += 1
        #if pivot term is the last term then DONE
        if not pivot_found:
            break
        pivot_doc = candidates[pivot][0]

        if candidates[0][0] == pivot_doc:
            fully_evaluated+=1
            s = 0
            t = 0
            cand_len = len(candidates)
            removed_candidates = []
            while t < cand_len: 
                if candidates[t][0] == pivot_doc:
                    s += candidates[t][1]
                    next_candidate = next_posting(candidates[t][2])
                    if not next_candidate: #candidate has reached end of posting list
                        removed_candidates.append(candidates[t])
                    else:
                        candidates[t] = next_candidate + (candidates[t][2],)
                    t += 1
                else:
                    break
            #remove candidates that are at the end of their posting list
            for r in removed_candidates:
                candidates.remove(r)
            #if pivot doc contains all query terms needed for its accumulated upper bound to be greater than threshold
            if s > theta:
                ans.append((s,pivot_doc))
                if len(ans) > top_k:
                    #the list should be sorted by score in decrease order, if two documents have same score, smaller document id precedes larger one
                    ans.remove(min(ans, key=lambda  x: (x[0],-x[1])))
                    theta = min(ans, key=lambda  x: x[0])[0]
        else:
            removed_candidates = []
            for t in range(0,pivot):
                seeked_candidate = seek_to_document(candidates[t][2],pivot_doc)
                if not seeked_candidate: #remove candidates if they need to be advanced past their posting list bounds
                    removed_candidates.append(candidates[t])
                else:
                    candidates[t] = seeked_candidate + (candidates[t][2],)
            #remove candidates
            for r in removed_candidates:
                candidates.remove(r)
    ans = sorted(ans, key=lambda x: (-x[0],x[1]))    
    return (ans,fully_evaluated)