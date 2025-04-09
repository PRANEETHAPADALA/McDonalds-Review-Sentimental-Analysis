import os
import pickle
import numpy as np
import pandas as pd
import logging
import html
from flask import Flask, request, render_template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# File paths for local model files
MODEL_PATH = 'model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'
PCA_PATH = 'pca.pkl'

# Load pickle files safely
def load_pickle_file(path, name):
    try:
        with open(path, 'rb') as f:
            logger.info(f"{name} loaded successfully from {path}.")
            return pickle.load(f)
    except Exception as e:
        logger.error(f"Failed to load {name} from {path}: {e}")
        return None

model = load_pickle_file(MODEL_PATH, "Model")
vectorizer = load_pickle_file(VECTORIZER_PATH, "Vectorizer")
pca = load_pickle_file(PCA_PATH, "PCA")

# Store metadata
store_locations = {
    "Austin, TX (US-183 Hwy)": {"latitude": 30.3074624, "longitude": -97.7526805, "rating_count": 450},
    "Dallas, TX (Main St)": {"latitude": 32.7766642, "longitude": -96.7969879, "rating_count": 325},
    "Houston, TX (Westheimer Rd)": {"latitude": 29.7604267, "longitude": -95.3698028, "rating_count": 510},
    "San Antonio, TX (Riverwalk)": {"latitude": 29.4241219, "longitude": -98.4936282, "rating_count": 385}
}

visit_times = {
    "Today/Yesterday": "1 day ago",
    "This Week": "4 days ago",
    "This Month": "2 weeks ago",
    "Several Months Ago": "3 months ago"
}

# Rule-based sentiment detection
def get_text_sentiment(text):
    if not text or len(text.strip()) == 0:
        logger.info("Empty review text received")
        return "Neutral"

    text = text.lower()

    strong_negative = ['worst', 'terrible', 'horrible', 'awful', 'disgusting', 'pathetic', 
                       'garbage', 'waste', 'stinky', 'rotten', 'filthy', 'gross', 'never again', 
                       'avoid', 'disaster', 'hate', 'unacceptable', 'poor']
    negative = ['bad', 'slow', 'cold', 'rude', 'dirty', 'wrong', 'unfriendly',
                'unhelpful', 'ignored', 'careless', 'overpriced', 'frustrated']
    strong_positive = ['excellent', 'amazing', 'awesome', 'fantastic', 'wonderful',
                       'perfect', 'outstanding', 'love', 'best', 'superb', 'phenomenal']
    positive = ['good', 'nice', 'friendly', 'clean', 'fast', 'fresh', 'helpful',
                'pleasant', 'satisfied', 'great', 'tasty', 'recommend']

    hygiene_issues = ['hair', 'bug', 'roach', 'mold', 'expired', 'spoiled', 'raw',
                      'undercooked', 'plastic', 'metal', 'blood', 'spit', 'unwashed', 'contaminated']

    for issue in hygiene_issues:
        if issue in text:
            return "Negative"

    score = 0
    score += 2 * sum(text.count(w) for w in strong_positive)
    score += sum(text.count(w) for w in positive)
    score -= 2 * sum(text.count(w) for w in strong_negative)
    score -= sum(text.count(w) for w in negative)

    if "not " in text:
        for w in positive + strong_positive:
            if f"not {w}" in text:
                score -= 2

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# ML-based sentiment analysis
def get_ml_sentiment(text):
    if not model or not vectorizer:
        logger.warning("Model/vectorizer not loaded. Using rule-based sentiment.")
        return get_text_sentiment(text)

    try:
        vec = vectorizer.transform([text])
        if pca:
            vec = pca.transform(vec.toarray())
        prediction = model.predict(vec)[0]
        return {
            1: "Positive",
            0: "Neutral",
            -1: "Negative",
            "1": "Positive",
            "0": "Neutral",
            "-1": "Negative",
            "1.0": "Positive",
            "0.0": "Neutral",
            "-1.0": "Negative"
        }.get(str(prediction), str(prediction))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return get_text_sentiment(text)

@app.route('/')
def home():
    return render_template('index.html',
                           store_locations=list(store_locations.keys()),
                           visit_times=list(visit_times.keys()))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        review_text = html.escape(request.form.get('review', '').strip())
        store_location = request.form.get('store_location', '')
        visit_time = request.form.get('visit_time', '')

        logger.info(f"Review: '{review_text}' | Store: {store_location} | Time: {visit_time}")

        if not review_text:
            sentiment = "Neutral"
        else:
            sentiment = get_ml_sentiment(review_text)

        return render_template('index.html',
                               prediction=sentiment,
                               review_text=review_text,
                               store_locations=list(store_locations.keys()),
                               visit_times=list(visit_times.keys()),
                               selected_store=store_location,
                               selected_visit=visit_time)
    except Exception as e:
        logger.error(f"Error in /predict: {e}")
        return render_template('index.html',
                               error=str(e),
                               store_locations=list(store_locations.keys()),
                               visit_times=list(visit_times.keys()))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)