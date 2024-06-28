# prerequisites
# install biopython, lightgbm[scikit-learn] 

# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from Bio import SeqIO

# optional: ignore not-so-relevant warnings
import warnings 
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# classes

class DfDetails():
    
    '''
    A class to explore structures of data frame.
    
    Parameters:
    -------------
    df: a pandas data frame
    gb: specifies column
    
    Attributes:
    -------------
    group: number of rows per cluster in gb-specified class
    shape: dimensions of data frame
    dtypes: data types in data frame
    nan: checks missing values in data frame
    '''

    def __init__(self, df, gb='class'):

        self.group = df.groupby(gb).size()
        self.shape = df.shape
        self.dtypes = df.dtypes
        self.nan = df.isnull().any()

class FragTokenizer():

    def __init__(self, df_train, kwargs**):
        
        '''
        Parameter
        -------------
        df_train: data frame to create tokenizer
        X_label = column to be fragmented and tokenized
        y_label = column to be assigned to y
        
        Attribute
        -------------
        X: values of X
        y: values of y
        '''
        
        self.Xlabel = X_label
        self.ylabel = y_label
        
        X = # nlp-based tokens [to be updated once project is published]

        # assignment of dependable variable

        y = df_train[self.ylabel]

        self.X = X
        self.y = y
        
    def test(self, df_test):
        
        '''
        This function would only tokenize the data on which the model would be tested.
        Needs tokenizer from training data set.
        
        Parameter
        -------------
        df_test: data set to be tested with trained model
        
        Returns
        -------------
        Xt: values of Xt
        yt: values of yt
        '''

        Xt = # nlp-based tokens [to be updated once project is published]
        
        yt = df_test[self.ylabel]
        
        print(f'X.shape: {Xt.shape} & y.shape : {yt.shape}\n')
        
        return Xt, yt

class TrainModel():
    
    def __init__(self, X, y, test_size=0.2, random_state=42):
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        self.Xtrain = X_train
        self.ytrain = y_train
        self.Xtest = X_test
        self.ytest = y_test
        
    def rf(self):
        
        from sklearn.ensemble import RandomForestClassifier
        
        rf_clf = RandomForestClassifier(tuned params [to be updated once project is published])
        
        rf_clf.fit(self.Xtrain, self.ytrain)
        
        return rf_clf
    
    def lgbm(self):
        
        from lightgbm import LGBMClassifier
        
        import os
        
        lgbm_clf = LGBMClassifier(tuned params [to be updated once project is published])
        
        lgbm_clf.fit(self.Xtrain, self.ytrain)
        
        return lgbm_clf

# functions

def fasta_reader(path):

    '''
    This function helps to extract data from fasta files downloaded
    from Uniprot or some other source. 

    For instance, for this model, 'ID' and 'sequences' have been retrieved
    from fasta files.
    '''

    fasta_sequences = SeqIO.parse(open(path), 'fasta')

    ids = list()
    sequences = list()

    for record in fasta_sequences:
        ids.append(record.id)
        sequences.append(str(record.seq))

    df = pd.DataFrame({'identifier': ids, 'sequence': sequences})

    return df

def load_excel(path):

    '''
    This function is useful for loading multiple Excel files to multiple
    data frames. Also, the loading can be concurrent, meaning, large
    files can be uploaded using multiple threads. 
    '''

    df = pd.read_excel(path)

    # get to know the shape of the data frame
    print(df.shape)

    return df

def seq_len_check(seqs):
    '''
    This function tries to check what is the distribution of protein length
    and helps in processing data set according to needs, say, limiting
    sequence length to a certain range.
    '''

    seq_len = [len(s) for s in seqs]

    # check mean and median of sequences
    seq_mean = np.mean(seq_len)
    seq_median = np.median(seq_len)

    print(seq_mean, '&&&', seq_median)

    seq_len.sort(reverse=True)
    
    return seq_len

def feature_selection(n1, n2, Xt, randomize=False):

    '''
    This function allows one to select the number of features from specific
    region.

    randomize: if features are to be fed in random order, set its value
    True. The default is False.
    '''

    if randomize == False:
        X = Xt[:, n1:n2]

    else:
        rand_features = list(range(n1, n2))
        random.shuffle(rand_features)
        X = Xt[:, rand_features]

    return X

def encoding_labels(y, visualizer=False):

    '''
    Sklearn has default support for labels fed as strings. However, dealing
    with other models may need the labels to be encoded and this function
    does that.

    visualizer: if the user needs to print the 'y' to check, they can set 
    this value to True. The default is False.
    '''

    from sklearn.preprocessing import LabelEncoder, OneHotEncoder

    le = LabelEncoder()
    encoded_y = le.fit_transform(y)

    ohe = OneHotEncoder(sparse=False)
    y = ohe.fit_transform(encoded_y.shape(-1, 1))

    if visualizer == True:
        print(y)

    return y

def subtract_df(df1, df2):

    '''
    This function aims to get samples of one data frame that doesn't exist in
    other data frame. In this case, data samples that exist in df1 but not 
    in df2 would be returned as a result.
    '''

    return df1[~df1['identifier'].isin(df2['identifier'])].copy()

def feature2accuracy(begin, end, step, length, Xt):

    '''
    This function provides a bird's eye view of which feature set works 
    the best. It checks the accuracy of the model by iteratively feeding features
    from a certain part of the feature list.

    begin = first feature index from feature subset
    end = last feature index from feature subset
    step = skip these many points to analyze the next subset of features
    length = total number of features to be fed to the model
    '''

    scores = list()

    for i in range(being, end, step):
        n1 = i
        n2 = n1 + length

        X = feature_selection(n1, n2, Xt)
        y = yt

        # data set splitting
        # model training

        scores.append(accuracy_score(y_test, classifier.predict(X_test)))

    # generate a plot to visualize the feature subset-accuracy relationship
    plt.plot(list(range(begin, end, step)), scores, color='r', marker='o')

    return list(range(begin, end, step)), scores 

# ................................................................................
# main code

df = load_excel('path')

# feature and independent variable assignment
xy_values = FragTokenizer(df_inp)
Xt = xy_values.X
yt = xy_values.y

# create an instance of classifier and train it
classifier = TrainModel(X, y).lgbm()
