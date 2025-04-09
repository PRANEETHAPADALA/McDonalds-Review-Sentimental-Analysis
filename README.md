# McDonald's Sentiment Analysis App

This repository contains a Flask web application that analyzes McDonald's restaurant reviews and predicts sentiment as negative (-1), neutral (0), or positive (1).

## Table of Contents
- [Literature Survey & References](#literature-survey--references)
- [Project Structure](#project-structure)
- [Assignment Files](#assignment-files)
- [Running the App in VS Code](#running-the-app-in-vs-code)
  - [1. Open the Project](#1-open-the-project)
  - [2. Set Up a Virtual Environment](#2-set-up-a-virtual-environment)
  - [3. Install Required Dependencies](#3-install-required-dependencies)
  - [4. Run the Application](#4-run-the-application)
  - [5. Access the Web Interface](#5-access-the-web-interface)
- [Troubleshooting](#troubleshooting)
- [Notes for Developers](#notes-for-developers)

## Literature Survey & References

This project was inspired by and references the following research papers:

1. Doan, T. C., Dat, M. X., & Ninh, N. V. (2025). *Sentiment analysis of McDonald's store reviews in fast food restaurants using machine learning*. In Proceedings of the International Conference on Innovation and Challenges in Computing and Innovative Technologies (ICCIT-2024). ResearchGate. https://www.researchgate.net/publication/387959576

2. Butaney, I., Deo, A., Aggarwal, P., & Sinha, A. K. (2024). Examining McDonald's operational strategies: An integrated application of regression and social media sentiment analysis. *ResearchGate*. https://www.researchgate.net/publication/382879998

3. Setiawan, I., Widodo, A. M., Rahaman, M., Tugiman, Hadi, M. A., Anwar, N., Ulum, M. B., Mulyani, E. Y., & Erzed, N. (2022). Utilizing random forest algorithm for sentiment prediction based on Twitter data. In G. P. Suta Wijaya et al. (Eds.), *Proceedings of the First Mandalika International Multi-Conference on Science and Engineering 2022, MIMSE 2022 (Informatics and Computer Science)* (pp. 446–456). Atlantis Press. https://doi.org/10.2991/978-94-6463-084-8_37

## Project Structure

```
McDonaldsSentimentAnalysisApp/
│
├── Assignment_files/
│   ├── ML_Theory_Assignment1.ipynb
│   ├── ML_Theory_Assignment2.ipynb
│   ├── Mini_Project_final_notebook.ipynb
│   └── McDonald_s_Reviews.csv
│
├── static/
│   ├── mcdonalds-logo.png
│   └── style.css
│
├── templates/
│   └── index.html
│
├── venv/               # Will be created when following setup instructions
│
├── generated-icon.png
├── imputer.pkl
├── main.py
├── model.pkl
├── pca.pkl
├── requirements.txt
└── vectorizer.pkl
```

## Assignment Files

The `Assignment_files` folder contains the Jupyter notebooks and dataset used in the development of this project:

- **ML_Theory_Assignment1.ipynb**: Initial machine learning theory assignment
- **ML_Theory_Assignment2.ipynb**: Follow-up machine learning theory assignment
- **Mini_Project_final_notebook.ipynb**: The complete sentiment analysis project notebook with all data processing, model training, and evaluation steps
- **McDonald_s_Reviews.csv**: The dataset containing McDonald's restaurant reviews used for training and testing the model

These files document the progression of the project from theory to implementation and provide insight into the development process of the sentiment analysis model.

## Running the App in VS Code

### 1. Open the Project

1. Open VS Code
2. Go to File > Open Folder... and select the `McDonaldsSentimentAnalysisApp` folder
3. VS Code should display the project structure as shown above

### 2. Set Up a Virtual Environment

1. Open the VS Code terminal (Terminal > New Terminal)

2. Create a virtual environment within the project:
   ```bash
   # On Windows
   python -m venv venv

   # On macOS/Linux
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```
   
   You should see `(venv)` appear at the beginning of your terminal line, indicating the virtual environment is active.

### 3. Install Required Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file or encounter issues, you can install the necessary packages directly:

```bash
pip install flask pandas numpy scikit-learn imbalance-learners
```

### 4. Run the Application

With your virtual environment activated, run the Flask application:

```bash
python main.py
```

Your terminal should show that the Flask server is running, typically on http://127.0.0.1:5000/

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

You should now see the McDonald's Review Sentiment Analyzer interface where you can enter reviews to analyze.

## Troubleshooting

### Common Issues:

1. **Package not found errors**: 
   Ensure your virtual environment is activated and all dependencies are properly installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**: 
   If port 5000 is already being used, modify the port in main.py:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Change port to 5001 or another free port
   ```

3. **Missing module errors**:
   If you see "ModuleNotFoundError", check if all required libraries are installed:
   ```bash
   pip install flask pandas numpy scikit-learn imbalance-learners
   ```

4. **Pickle file errors**:
   Ensure all the model files (model.pkl, vectorizer.pkl, pca.pkl, imputer.pkl) are in the root directory of the project.

## Notes for Developers

- The app uses pre-trained models (stored in .pkl files) to analyze sentiment
- The main Flask application code is in main.py
- HTML templates are in the templates folder
- Static assets (CSS, images) are in the static folder
- The model classifies reviews as negative (-1), neutral (0), or positive (1)
