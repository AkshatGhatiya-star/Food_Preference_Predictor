import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

try:
    # This will read the 'indian_food_recs_database.csv' file you just created.
    df = pd.read_csv('indian_food_recs_database.csv')
except FileNotFoundError:
    print("Error: 'indian_food_recs_database.csv' not found.")
    print("Please run 'python create_indian_database.py' first to generate it.")
    exit()
except Exception as e:
    print(f"A critical error occurred while reading the CSV: {e}")
    exit()

# This is the output you should see first
print("Indian Recommendation Dataset Loaded Successfully. Shape:", df.shape)

# --- This is the model training logic ---
features = [
    'Weight', 'City', 'State', 'Temperature', 'Season',
    'Income_Level', 'Stress_Level', 'Sleep_Hours', 'Work_Life_Balance', 'Context'
]
target = 'Recommended_Food'

X = df[features]
y = df[target]

X_encoded = pd.get_dummies(X, columns=[
    'City', 'State', 'Season', 'Income_Level',
    'Stress_Level', 'Work_Life_Balance', 'Context'
])

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# This is the output you should see next
print("\nModel training complete.")

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# And finally, you will see the high accuracy score!
print(f"\nModel Accuracy on Test Set: {accuracy:.2f}")

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("\nTrained model saved to 'model.pkl'")

model_columns = X_encoded.columns
with open('model_columns.pkl', 'wb') as f:
    pickle.dump(model_columns, f)
print("Model columns saved to 'model_columns.pkl'")

