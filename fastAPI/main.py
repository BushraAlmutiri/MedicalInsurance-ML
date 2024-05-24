import numpy as np
import pandas as pd
import uvicorn
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pickle
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


#database: password:103217s name:setah55

# Define the Pydantic model for request data validation
class PredictionRequest(BaseModel):
    age: int
    sex: int  # 0 for male, 1 for female
    bmi: float
    children: int
    smoker: int  # 0 for no, 1 for yes
    region: int  # 1 for southwest, 2 for southeast, 3 for northwest, 4 for northeast

# Create the FastAPI app instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Email(BaseModel):
    email: str

# Load and preprocess the dataset
df = pd.read_csv("insurance.csv")
df['sex'] = df['sex'].apply({'male': 0, 'female': 1}.get)
df['smoker'] = df['smoker'].apply({'yes': 1, 'no': 0}.get)
df['region'] = df['region'].apply({'southwest': 1, 'southeast': 2, 'northwest': 3, 'northeast': 4}.get)

# Split the data into features and target variable
X = df[['age', 'sex', 'bmi', 'children', 'smoker', 'region']]
y = df['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and save the models
linear_regression_model = LinearRegression().fit(X_train, y_train)
svr_model = SVR().fit(X_train, y_train)
decision_tree_model = DecisionTreeRegressor().fit(X_train, y_train)

# Save the trained models using pickle
pickle.dump(linear_regression_model, open("linear_regression_model.pkl", "wb"))
pickle.dump(svr_model, open("svr_model.pkl", "wb"))
pickle.dump(decision_tree_model, open("decision_tree_model.pkl", "wb"))

# Load models just once when the app starts
with open("linear_regression_model.pkl", "rb") as f:
    linear_regression_model = pickle.load(f)
with open("svr_model.pkl", "rb") as f:
    svr_model = pickle.load(f)
with open("decision_tree_model.pkl", "rb") as f:
    decision_tree_model = pickle.load(f)

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Prepare the input data
        input_data = np.array([[request.age, request.sex, request.bmi, request.children, request.smoker, request.region]])

        # Make predictions using the models
        predictions = {
            "Linear Regression": linear_regression_model.predict(input_data)[0],
            "SVR": svr_model.predict(input_data)[0],
            "Decision Tree": decision_tree_model.predict(input_data)[0]
        }

        best_model = min(predictions, key=predictions.get)
        best_prediction = predictions[best_model]

        # Connect to the database
        conn = sqlite3.connect('predictions.db')

        # Create a cursor
        cursor = conn.cursor()

        # Insert the data into the database
        cursor.execute("""
        INSERT INTO predictions (age, sex, bmi, children, smoker, region, linear_regression_prediction, svr_prediction, decision_tree_prediction, best_model)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (request.age, request.sex, request.bmi, request.children, request.smoker, request.region, predictions["Linear Regression"], predictions["SVR"], predictions["Decision Tree"], best_model))

        # Commit the transaction
        conn.commit()

        return JSONResponse(content={"best_model": best_model, "best_prediction": float(best_prediction)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/")
async def add_email(email: Email):
    # Connect to the database
    conn = sqlite3.connect('predictions.db')

    # Create a cursor
    cursor = conn.cursor()

    # Insert the email into the database
    cursor.execute("""
    INSERT INTO emails (email)
    VALUES (?)
    """, (email.email,))

    # Commit the transaction
    conn.commit()

    return {"message": "Email added successfully"}



# Run the FastAPI application (assuming uvicorn is installed)
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000) # Replace with desired port