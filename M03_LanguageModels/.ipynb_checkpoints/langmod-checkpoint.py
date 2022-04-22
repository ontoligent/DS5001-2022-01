#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
from dataclasses import dataclass

@dataclass
class LanguageModel:

    size:int = 3    # Max ngram size
    
    def __post_init__(self):

        # Define columns names for ngram elements
        self.WIDX = [f'w{i}' for i in range(self.size)]

    def _sents2ngrams(self, sents=[]):
        """Convert a list of sentences (docs) to a dataframe of ngrams"""

        # Build ngram list for each sentence
        # and preserve sentence number
        ngram_data = []
        for sn, sent in enumerate(sents): 
            
            # Tokenize the sentence
            W = sent.lower().split()
            W = [re.sub(r'[\W_]+', '', w) for w in W] # Get rid of non-alphanumerics 
            W = [w for w in W if w !=''] # Get rid of resulting blanks
            
            # Add sentence boundaries
            W = ['</s>', '<s>'] + W + ['</s>', '<s>']
            
            # Gather ngram slices with sliding self.size
            ngram_data.append([[sn]+W[x-self.size : x] for x in range(self.size, len(W)+1)])
            
        # Convert list to a dataframe and project token sequence numbers (`w*`) onto columns
        ngrams = pd.DataFrame(ngram_data).stack().to_frame('ngram').reset_index(drop=True)  
        
        IDX = ['s']+ self.WIDX #[f'w{i}' for i in range(self.size)]
        for i, key in enumerate(IDX):
            ngrams[key] = ngrams.ngram.apply(lambda x: x[i])
        ngrams = ngrams[IDX]
        
        # Create index using sentence number and ngram number within sentence
        ngrams['ngram_num'] = ngrams.groupby('s').cumcount()
        ngrams = ngrams.set_index(['s','ngram_num'])    
        return ngrams

    def _ngrams2models(self, ngrams):
        """Cnvert a dataframe of ngrams to a list of language models"""

        M = {} # A dict to hold the models
        for i in range(1, self.size+1):
            
            # Use to group ngrams into unique values with counts
            M[i] = ngrams.value_counts(self.WIDX[:i]).to_frame('n').sort_index()

            # Remove extra tags; these will inflate the sentence count
            if i == 1:
                M[1] = M[1].drop('<s>')
            if i == 2:
                M[2] = M[2].drop(('</s>','<s>'))

            # Estimate probs from counts
            # This is the joint probability for rank > 1
            M[i]['p'] = M[i].n / M[i].n.sum()
            M[i]['i'] = np.log2(1/M[i].p)
            M[i]['h'] = M[i].p * M[i].i
            
            # Conditional Probabilities for rank > 1
            # We compute using formuma of C(W_{n+1}) / C(W_{n})
            if i > 1:
                M[i]['cp'] = M[i].n / M[i].groupby(self.WIDX[:i-1]).n.sum()
                M[i]['ci'] = np.log2(1/M[i].cp)
                M[i]['ch'] = M[i].cp * M[i].ci
                            
        return M    

    def train_model(self, sents=[]):
        ngrams = self._sents2ngrams(sents)
        self.M = self._ngrams2models(ngrams)

    def test_model(self, sents=[]):
        """
        We apply the probabilities form our models to a test set of sentences.
        These 
        """
        
        # Create dataframe from sentence list
        # to be used to add info later
        S = pd.DataFrame(sents, columns=['sent_str'])
        S.index.name = 'sent_id'
        
        # Convert sentence strings into ngrams
        ngrams = self._sents2ngrams(S.sent_str) 
        
        # Create models from the test data (as it were)
        T = self._ngrams2models(ngrams)   
        
        # Compute number of tokens in test data
        # Based on J&M; count only endings (and remove first one)
        N = T[1].query("w0 != '<s>'").n.sum() - 1 
        
        # Define dicts to to store various results from the model and data
        X = {}     # The joined model and data
        E = {}     # Error; number of dropped words in test
        CH = {}    # The cross-entropy of the model
        PP = {}    # The perplexity of the model
        
        # Interate through each model
        for i in range(1, self.size+1):

            M = self.M[i]
            
            # Join model to data (or, trained model to test model) 
            # With "inner", we remove all new ngrams in the training set
            X[i] = T[i].join(M, how='inner', rsuffix='_model', lsuffix='_data')
            E[i] = round(((T[i].shape[0] - X[i].shape[0]) / T[i].shape[0]) * 100)
                            
            # Compute information of sentences
            S['n'] = ngrams.w0.groupby('s').count()
            G = ngrams.reset_index().merge(M, on=self.WIDX[:i]).groupby('s')
            S[f'p{i}'] = G.p.sum()
            S[f'i{i}'] = G.i.sum()
            S[f'h{i}'] = G.h.sum()
            S[f'pp{i}'] = S.apply(lambda x: (1/x[f"p{i}"])**(-1/x.n), 1)
            if i > 1:
                S[f'cp{i}'] = G.cp.sum()
                S[f'ci{i}'] = G.ci.sum()            
                S[f'ch{i}'] = G.ch.sum()
                S[f'cpp{i}'] = S.apply(lambda x: (1/x[f"cp{i}"])**(-1/x.n), 1)            
        
        # Compute cross-entropy of model
        CH[1] = round(((X[1].n_data * X[1].i_model).sum()) / N)
        for i in range(2, self.size+1):
            CH[i] = round(((X[i].n_data * X[i].ci_model).sum()) / N)

        # Computer perplexity
        PP[1] = round(np.power(2, S.i1.sum() / S.n.sum()))
        for i in range(2, self.size+1):        
            PP[i] = round(np.power(2, S[f"ci{i}"].sum() / S.n.sum()))

        self.N = N
        self.S = S 
        self.T = T 
        self.X = X 
        self.E = E 
        self.CH = CH
        self.PP = PP

    def generate_text(self, start_word='<s>', n=250):
        words = [start_word] # Pick most probable
        for i in range(n):
            if len(words) == 1:
                w = self.M[2].loc[start_word].p
                next_word = self.M[2].loc[start_word].sample(weights=w).index.values[0]
            elif len(words) > 1:
                bg = tuple(words[-2:])
                try:
                    w = self.M[3].loc[bg].p
                    next_word = self.M[3].loc[bg].sample(weights=w).index.values[0]
                except KeyError:
                    ug = bg[1]
                    if ug == '<s>':
                        next_word = self.M[1].sample(weights=M[1].p).index[0]
                    else:
                        w = M[2].loc[ug].p
                        next_word = self.M[2].loc[ug].sample(weights=w).index.values[0]
            words.append(next_word)
        text = ' '.join(words)
        text = re.sub(r'<s> ', '', text)
        text = re.sub(r' </s>', '.', text) + '.'
        text = re.sub(' s ', "'s ", text)
        text = text.upper() # To give that telegraph message look :-)
        print(text)

    # def save(self):
    #     NG.to_csv(f"{data_out}/austen-02-NGRAMS.csv", index=True)
    #     sents.to_csv(f"{data_out}/austen-02-SENTS.csv", index=True)
    #     for i in range(1, self.size+1):
    #         M[i].to_csv(f"{data_out}/austen-02-M{i}.csv", index=True)

