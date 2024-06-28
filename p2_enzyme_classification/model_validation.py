# import required libraries

# validation of model
class ModelValidation():
    
    def __init__(self, classifier, X, y, test_size=0.2, random_state=42):
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        self.Xtrain = X_train
        self.ytrain = y_train
        self.Xtest = X_test
        self.ytest = y_test
        self.x = X
        self.y = y
        self.clf = classifier
        self.ypred = classifier.predict(X_test) 
        
    def clf_report(self):
        
        from sklearn.metrics import classification_report
        
        print('Here is the classification report: \n\n\n', 
              classification_report(self.ytest, self.ypred), '\n')
        
    def scores(self, avg='macro'):
        
        from sklearn.metrics import accuracy_score, f1_score, recall_score 
        from sklearn.metrics import precision_score, roc_auc_score, matthews_corrcoef
        from sklearn.metrics import balanced_accuracy_score, hamming_loss
        from tabulate import tabulate
        
        score_dict = [
            ['Metrics', 'Scores (%)'],
            ['Accuracy score', round(accuracy_score(self.ytest, self.ypred)*100, 2)],
            ['Balanced accuracy score', round(balanced_accuracy_score(self.ytest, self.ypred)*100, 2)],
            ['Precision score', round(precision_score(self.ytest, self.ypred, average=avg)*100, 2)],
            ['Recall score', round(recall_score(self.ytest, self.ypred, average=avg)*100, 2)],
            ['f1 score', round(f1_score(self.ytest, self.ypred, average=avg)*100, 2)],
            ['Mathews coefficient', round(matthews_corrcoef(self.ytest, self.ypred), 2)],
            ['Hamming loss', round(hamming_loss(self.ytest, self.ypred)*100, 2)]
        ]
        
        print(tabulate(score_dict, headers='firstrow', tablefmt='github'))
        
    def cvs(self, cv=10):
        
        from sklearn.model_selection import cross_val_score
        
        cv_score = cross_val_score(self.clf, self.x, self.y, cv=cv)
        
        print(f'\nCross validation score: {round(cv_score.mean()*100, 2)}% \n')
        
        return cv_score
    
    def cm(self):
        
        from sklearn.metrics import confusion_matrix
        
        print('\nConfusion matrix: \n', confusion_matrix(self.ytest, self.ypred), '\n')


##########################################################################################
# main code

assessment = ModelValidation(classifier, X, y)

assessment.scores()
assessment.cm()
assessment.cvs()

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
