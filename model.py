import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn2pmml import sklearn2pmml
from sklearn2pmml.pipeline import PMMLPipeline

# Load dataset
customers = pd.read_csv('https://github.com/araj2/customer-database/raw/master/Ecommerce%20Customers.csv')

# Prepare data
X = customers[['Avg. Session Length', 'Time on App', 'Time on Website', 'Length of Membership']]
y = customers['Yearly Amount Spent']

# Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# Linear regression model
lm = LinearRegression()
lm.fit(X_train, y_train)

# Example prediction
X_new = np.array([[30, 12, 16, 4]])  # Input without feature names
predictions = lm.predict(X_new)
print(predictions)  # Output prediction

# Create PMML pipeline
pipeline = PMMLPipeline([('regressor', lm)])

# Export the model to PMML
try:
    sklearn2pmml(pipeline, "linear_regression_model.pmml", with_repr=True)
    print("Model exported successfully!")
except Exception as e:
    print(f"Error occurred: {e}")
