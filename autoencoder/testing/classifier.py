'''
Created on Dec, 2016

@author: hugo

'''
from __future__ import absolute_import
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold


def basemodel(input_size, n_class):
    model = Sequential()
    model.add(Dense(n_class, input_dim=input_size, init='glorot_normal', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def classifier(X, Y, n_splits=10, nb_epoch=200, batch_size=10, seed=7):
    encoder = LabelEncoder()
    encoder.fit(Y)
    Y = encoder.transform(Y)
    Y = np_utils.to_categorical(Y)
    estimator = KerasClassifier(build_fn=basemodel, input_size=X.shape[1], n_class=Y.shape[1], nb_epoch=nb_epoch, batch_size=batch_size, verbose=2)
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, X, Y, cv=kfold)
    print "accuracy: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100)
    return results