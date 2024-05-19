# import required libraries

# predict test set
y_pred = classifier.predict(X_test)

# validation of model
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score

print('Classification report: \n\n', classification_report(y_test, y_pred), '\n')
print('Accuracy score: \n', accuracy_score(y_test, y_pred), '\n')
print('Cross validation score: \n', np.round(cross_val_score(classifier, X, y, cv=10).mean())*100, 2)

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
