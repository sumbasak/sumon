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

def df_details(df):

    '''
    This function helps to understand the data set.
    '''

    # to know classes of enzymes and samples in each class
    print('Classes of enzymes:\n', df.groupby('class').size(), '\n')

    # to know the total number of samples in all classes
    print('Shape of dataframe:\n', df.shape, '\n')

    # to know about data types of each column
    print('Data type:\n', df.dtypes, '\n')

    # to know if any data point is missing and requires support
    print('Check for missing values:\n', df.isnull().any(), '\n\n')

    return df.copy()

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

def get_k_mers(row, size):

    '''
    This function generates fragments of sequence with a specified parameter.
    '''

    result = 0 # to be updated once project is published

    return result 

def frag_tokenizer(df_inp, kmer):

    '''
    This function tokenizes fragments of sequence using natural language
    processing (NLP) method.
    '''

    Xt = 0 # to be updated once project is published

    yt = 0 # to be updated once project is published

    return Xt, yt

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
    plt.show()

    return list(range(begin, end, step)), scores 

# ................................................................................
# main code

df = load_excel('path')

# optional: check details of data frame
df_details(df)

X, y = frag_tokenizer(df, kmer)

# split data set into training and test sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create an instance of classifier and train it
from lightgbm import LGBMClassifier
classifier = LGBMClassifier() # params to be updated once project is published
classifier.fit(X_train, y_train)

# predict test set
y_pred = classifier.predict(X_test)

# validation of model
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score

print('Classification report: \n\n', classification_report(y_test, y_pred), '\n')
print('Accuracy score: \n', accuracy_score(y_test, y_pred), '\n')
print('Cross validation score: \n', np.round(cross_val_score(classifier, X, y, cv=10).mean())*100, 2)

# ................................................................................
# test overfitting
from sklearn.model_selection import learning_curve

# works with default train_size parameter
train_sizes, train_scores, test_scores = learning_curve(classifier, X, y, cv=10, n_jobs=-1,
                                                        random_state=42) 

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.plot(train_sizes, train_mean, color='b', marker='o', markersize=5, label='Training Accuracy')
plt.fill_between(train_sizes, train_mean*train_std, train_mean-train_std, alpha=0.15, color='b')

plt.plot(train_sizes, test_mean, color='g', linestyle='--', marker='s', markersize=5, 
         label='Validation Accuracy')
plt.fill_between(train_sizes, test_mean*test_std, test_mean-test_std, alpha=0.15, color='g')
plt.grid()
plt.legend(loc='lower right')
plt.show()
