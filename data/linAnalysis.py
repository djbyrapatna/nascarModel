import pandas as pd
from linExport import createTestTrain, importXy
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge

import warnings
warnings.filterwarnings("ignore")

def cleanTotal(X, y):
    X = X.drop_duplicates()

    X = X.dropna()
    y = y[y['Driver'].isin(X['Driver'])]

    
    X.iloc[:, 1:-5] = X.iloc[:, 1:-5].apply(lambda x: pd.to_numeric(x, errors='coerce')).astype('float64')
    X = X.iloc[:, :-6]
    X = X.drop(columns=['Yearrace', 'Yearprac', 'Yearloop', 'Yearqual'])
    return X,y


def linReg(X_train, X_test, y_train, y_test, model, plot = False, printOption=False):
    #model = Ridge()
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    coefficients = model.coef_

    # Create a DataFrame to display the coefficients alongside feature names
    coeff_df = pd.DataFrame({'Feature': X_train.columns, 'Coefficient': coefficients.flatten()})
    coeff_df['Absolute Coefficient'] = coeff_df['Coefficient'].abs()

    # Sort the DataFrame by the absolute value of the coefficients
    coeff_df = coeff_df.sort_values(by='Absolute Coefficient', ascending=False)
    if printOption:
        print(coeff_df)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')
    if plot:
        plt.plot(X_test['PrevAllrace'], y_test, color = 'blue', linestyle = "", marker = "o")
        plt.plot(X_test['PrevAllrace'], y_pred, color = 'red', linestyle = "", marker = "o")
        plt.show()
    return coeff_df

def linAnalysisRun(xFile, yFile, model, scale = None, plot=False, clean = False, printOption=False):
    X, y = importXy(xFile, yFile)
    
    if clean:
       X, y = cleanTotal(X,y)

    X_train, X_test, y_train, y_test = createTestTrain(X,y, scale = scale)

    #print(X_train.columns)

    return linReg(X_train, X_test, y_train, y_test, model, plot, printOption=True)

from sklearn.feature_selection import RFE

def linFeatureRanking(xFile, yFile, model, scale = None, features=5, clean=True):
    X, y = importXy(xFile, yFile)
    if clean:
        X, y = cleanTotal(X,y)
    X_train, X_test, y_train, y_test = createTestTrain(X,y, scale = scale)
    selector = RFE(model, n_features_to_select=features, step=1)
    selector = selector.fit(X_train, y_train)

    # Get the ranking of features
    ranking = selector.ranking_
    # Create a DataFrame to display the ranking alongside feature names
    ranking_df = pd.DataFrame({'Feature': X_train.columns, 'Ranking': ranking})
    ranking_df = ranking_df.sort_values(by='Ranking')
    return ranking_df
