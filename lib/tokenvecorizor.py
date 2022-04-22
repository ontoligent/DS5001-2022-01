class TokenVectorizer():
    
    item_type:str = 'term_str'
    tf_method:str = 'max'
    df_method:str = 'standard'
    V:pd.DataFrame = None
    
    
    def __init__(self, CORPUS:pd.DataFrame, VOCAB:pd.DataFrame):
        self.CORPUS = CORPUS
        self.VOCAB = VOCAB
        self.OHCO = list(CORPUS.index.names)
    
    def create_bow(self, ohco_level):
        self.bag = self.OHCO[:ohco_level]
        self.BOW = self.CORPUS.groupby(self.bag+[self.item_type])\
            [self.item_type].count().to_frame('n')
        
    def get_tfidf(self):
        
        DTCM = self.BOW.n.unstack() # Create Doc-Term Count Matrix w/NULLs
        self.V = pd.DataFrame(index=DTCM.columns)

        if 'max_pos' in VOCAB:
            self.V['max_pos'] = self.VOCAB.max_pos
        
        if self.tf_method == 'sum':
            TF = (DTCM.T / DTCM.T.sum()).T
        elif self.tf_method == 'max':
            TF = (DTCM.T / DTCM.T.max()).T
        elif self.tf_method == 'log':
            TF = (np.log2(1 + DTCM.T)).T
        elif self.tf_method == 'raw':
            TF = DTCM
        elif self.tf_method == 'bool':
            TF = DTCM.astype('bool').astype('int')
        else:
            raise ValueError(f"TF method {tf_method} not found.")

        DF = DTCM.count()
        N_docs = len(DTCM)

        if self.df_method == 'standard':
            IDF = np.log2(N_docs/DF) # This what the students were asked to use
        elif self.df_method == 'textbook':
            IDF = np.log2(N_docs/(DF + 1))
        elif self.df_method == 'sklearn':
            IDF = np.log2(N_docs/DF) + 1
        elif self.df_method == 'sklearn_smooth':
            IDF = np.log2((N_docs + 1)/(DF + 1)) + 1
        else:
            raise ValueError(f"DF method {df_method} not found.")
    
        TFIDF = TF * IDF
        
        self.BOW['tfidf'] = TFIDF.stack()
        self.BOW['tf'] = TF.stack()
        self.V['df'] = DF
        self.V['idf'] = IDF
        self.N_docs = N_docs
        
        
    def get_dfidf(self):
        self.V['dfidf'] = self.V.df * self.V.idf
        
    def get_mean_tfidf_for_VOCAB(self):
        self.V['mean_tfidf'] = self.BOW.groupby('term_str').tfidf.mean()
