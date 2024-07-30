import pandas as pd
from linExport import createTestTrain, importXy
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge

import warnings
warnings.filterwarnings("ignore")

def linReg(X_train, X_test, y_train, y_test, model):
    model = Ridge()
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

    print(coeff_df)

    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')

    plt.plot(X_test['PrevAllrace'], y_test, color = 'blue', linestyle = "", marker = "o")
    plt.plot(X_test['PrevAllrace'], y_pred, color = 'red', linestyle = "", marker = "o")
    plt.show()

def linAnalysisRun(xFile, yFile, scale, model):
    X, y = importXy("compiledDataX.pkl", "compiledDataY.pkl")
    #print(X.columns)
    X_train, X_test, y_train, y_test = createTestTrain(X,y, scale = "zScale")

    #print(X_train.columns)

    linReg(X_train, X_test, y_train, y_test, Ridge())