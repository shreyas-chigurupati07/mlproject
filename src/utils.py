import os
import sys
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    '''
    This function saves the object to the file path
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file:
            dill.dump(obj, file)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_model(X_train, y_train, X_test, y_test, models, param):
    '''
    This function evaluates the model
    '''
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            print(f"Evaluating model: {model}")
            print(f"Parameters: {para}")
            
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)
      
            

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)


            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            trian_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e, sys)