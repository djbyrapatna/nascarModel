import pandas as pd
from .linExport import createTestTrain, importXy, filterXy
from .linAnalysis import linReg, cleanTotal
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score

def createPolyX(X_train, X_test, degree=2):
    poly = PolynomialFeatures(degree=degree, include_bias=False)

    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)
    return X_train_poly, X_test_poly


def polyReg(X_train, X_test, y_train, y_test, poly, model, graphCol=None, plot = False, printOption=False):
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)    
    model.fit(X_train_poly,y_train)
    y_pred = model.predict(X_test_poly)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    coefficients = model.coef_
    feature_names = poly.get_feature_names_out(X_train.columns)
    print (len(feature_names), len(coefficients.flatten()))
    # Create a DataFrame to display the coefficients alongside feature names
    coeff_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients.flatten()})
    coeff_df['Absolute Coefficient'] = coeff_df['Coefficient'].abs()

    # Sort the DataFrame by the absolute value of the coefficients
    coeff_df = coeff_df.sort_values(by='Absolute Coefficient', ascending=False)

    if printOption:
        print(coeff_df)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')
    
    if plot:
        if not graphCol:
            graphCol = X_train.columns[0]
        plt.plot(X_test[graphCol], y_test, color = 'blue', linestyle = "", marker = "o")
        plt.plot(X_test[graphCol], y_pred, color = 'red', linestyle = "", marker = "o")
        plt.show()
    return coeff_df

def polyRegRun(xFile, yFile, model, colList, scale = None, graphCol = None, plot=False, degree=2, clean=False, printOption=False):
    X, y = importXy(xFile,yFile)

    if clean:
        X, y= cleanTotal(X,y)

    #colList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
    X_train_unfiltered, X_test_unfiltered, y_train, y_test =createTestTrain(X,y,scale=scale)

    X_train, X_test = filterXy([X_train_unfiltered, X_test_unfiltered],colList)

    poly = PolynomialFeatures(degree=degree, include_bias=False)

    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)

    return polyReg(X_train, X_test, y_train, y_test, poly, model, graphCol, plot, printOption)

from sklearn.feature_selection import RFE

def polyFeatureRanking(xFile, yFile, model, colList, scale = None, degree=2, features = 5, clean=False):
    X, y = importXy(xFile, yFile)
    if clean:
        X, y= cleanTotal(X,y)
    X_train_unfiltered, X_test_unfiltered, y_train, y_test =createTestTrain(X,y,scale=scale)
    X_train, X_test = filterXy([X_train_unfiltered, X_test_unfiltered],colList)
    
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)

    selector = RFE(model, n_features_to_select=features, step=1)
    selector = selector.fit(X_train_poly, y_train)
    # Get the ranking of features
    ranking = selector.ranking_
    # Create a DataFrame to display the ranking alongside feature names
    feature_names = poly.get_feature_names_out(X_train.columns)
    ranking_df = pd.DataFrame({'Feature': feature_names, 'Ranking': ranking})
    ranking_df = ranking_df.sort_values(by='Ranking')

    return ranking_df
    





