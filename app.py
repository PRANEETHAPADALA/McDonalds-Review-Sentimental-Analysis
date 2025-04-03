import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
import re
from sklearn.impute import SimpleImputer

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Initialize the TF-IDF vectorizer with the same parameters
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)

# Load vectorizer vocabulary if available, otherwise we'll fit it on first use
vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
if os.path.exists(vectorizer_path):
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

# Load PCA model if available
pca_path = os.path.join(os.path.dirname(__file__), 'pca.pkl')
if os.path.exists(pca_path):
    with open(pca_path, 'rb') as f:
        pca = pickle.load(f)
else:
    # Initialize PCA with same parameters as in training
    pca = PCA(n_components=30)

# Load imputer if available
imputer_path = os.path.join(os.path.dirname(__file__), 'imputer.pkl')
if os.path.exists(imputer_path):
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
else:
    # Initialize imputer with same parameters as in training
    imputer = SimpleImputer(strategy='mean')

# Function to convert review_time to days
def convert_review_time(time_str):
    if pd.isna(time_str):  # Handle missing values
        return None

    match = re.search(r'\d+', str(time_str))  # Ensure it's a string
    if not match:
        return None  # If no number is found, return None

    num = int(match.group())  # Extract number

    if "day" in time_str:
        return num
    elif "month" in time_str:
        return num * 30
    elif "year" in time_str:
        return num * 365
    else:
        return None  # Catch unexpected cases

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        review_text = request.form.get('review')
        store_address = request.form.get('store_address')
        latitude = float(request.form.get('latitude', 0))
        longitude = float(request.form.get('longitude', 0))
        rating_count = int(request.form.get('rating_count', 0).replace(',', ''))
        review_time = request.form.get('review_time', '')
        
        # Convert review_time to days
        review_time_days = convert_review_time(review_time)
        
        # Create a DataFrame with the input data
        input_data = pd.DataFrame({
            'store_address': [store_address],
            'latitude': [latitude],
            'longitude': [longitude],
            'rating_count': [rating_count],
            'review_time': [review_time_days]
        })
        
        # Encode store_address using LabelEncoder
        # Since we don't have the original encoder, we'll encode it as 0 (placeholder)
        input_data['store_address'] = 0
        
        # Transform review text using TF-IDF
        if not hasattr(vectorizer, 'vocabulary_'):
            # This is just a fallback, ideally you should have the fitted vectorizer
            vectorizer.fit([review_text])
            
        review_tfidf = vectorizer.transform([review_text])
        tfidf_df = pd.DataFrame(review_tfidf.toarray(), 
                                columns=vectorizer.get_feature_names_out())
        
        # Add missing columns with zeros (columns that exist in training but not in this input)
        expected_columns = [
            '10', '20', 'area', 'ask', 'asked', 'bad', 'best', 'better', 'big',
            'breakfast', 'burger', 'busy', 'came', 'chicken', 'clean', 'coffee',
            'cold', 'come', 'customer', 'customers', 'day', 'did', 'didn', 'dirty',
            'don', 'drive', 'eat', 'employees', 'excellent', 'experience', 'fast',
            'food', 'fresh', 'friendly', 'fries', 'gave', 'going', 'good', 'got',
            'great', 'homeless', 'horrible', 'hot', 'ice', 'inside', 'just', 'kids',
            'know', 'like', 'line', 'location', 'long', 'lot', 'love', 'make',
            'manager', 'mcdonald', 'mcdonalds', 'meal', 'minutes', 'need',
            'neutral', 'new', 'nice', 'night', 'open', 'order', 'ordered', 'orders',
            'people', 'place', 'poor', 'quick', 'really', 'restaurant', 'right',
            'rude', 'said', 'say', 'service', 'slow', 'staff', 'terrible', 'time',
            'times', 'told', 'took', 've', 'wait', 'waited', 'waiting', 'want',
            'way', 'went', 'window', 'work', 'worst', 'wrong', '½s', '½ï'
        ]
        
        for col in expected_columns:
            if col not in tfidf_df.columns:
                tfidf_df[col] = 0
        
        # Merge input data with TF-IDF features
        input_features = pd.concat([input_data, tfidf_df], axis=1)
        
        # Ensure column order matches training data
        # Note: In a production environment, you should save the exact column order
        
        # Apply imputation for missing values
        input_features_array = imputer.transform(input_features)
        
        # Apply PCA transformation
        input_features_pca = pca.transform(input_features_array)
        
        # Make prediction
        prediction = model.predict(input_features_pca)
        
        # Map prediction back to sentiment labels
        sentiment_map = {
            -1: "Negative",
            0: "Neutral",
            1: "Positive"
        }
        
        sentiment = sentiment_map.get(prediction[0], "Unknown")
        
        # Calculate confidence
        probabilities = model.predict_proba(input_features_pca)[0]
        confidence = round(float(max(probabilities)) * 100, 2)
        
        return render_template('index.html', 
                               prediction=sentiment, 
                               confidence=confidence,
                               review_text=review_text)
        
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)