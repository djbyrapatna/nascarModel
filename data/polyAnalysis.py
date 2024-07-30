import pandas as pd
from linExport import createTestTrain, importXy, filterXy
from linAnalysis import linReg
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score

X, y = importXy("compiledDataX.pkl", "compiledDataY.pkl")

colList = ['Prevrace','Prev10race','Currqual','Currprac','Prev10DRIVERRATINGloop','Prev10AvgPosloop']
X_train_unfiltered, X_test_unfiltered, y_train, y_test =createTestTrain(X,y)

X_train, X_test = filterXy([X_train_unfiltered, X_test_unfiltered],colList)

degree = 2

poly = PolynomialFeatures(degree=degree, include_bias=False)

X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.fit_transform(X_test)

model = LinearRegression()

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

print(coeff_df)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

plt.plot(X_test['Prev10race'], y_test, color = 'blue', linestyle = "", marker = "o")
plt.plot(X_test['Prev10race'], y_pred, color = 'red', linestyle = "", marker = "o")
plt.show()



