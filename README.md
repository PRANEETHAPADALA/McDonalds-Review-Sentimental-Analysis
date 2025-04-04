# McDonalds-Review-Sentimental-Analysis
# Render Deployment Guide for McDonald's Sentiment Analysis App

This guide provides step-by-step instructions for deploying your McDonald's Review Sentiment Analysis application to [Render](https://render.com/).

## Prerequisites

Before starting, ensure you have:

1. A [Render account](https://render.com/) (free tier available)
2. Your code in a Git repository (GitHub, GitLab, or Bitbucket)
3. All necessary files for your application (app.py, templates/index.html, requirements.txt, etc.)
4. Your trained model files (model.pkl or ability to generate it)

## Step 1: Project Setup

Make sure your project has the following structure:

```
your-project-folder/
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── create_model.py          # Script to generate model files
├── render.yaml              # Render configuration
├── .gitignore               # Git ignore file
├── model.pkl                # Your trained model (or will be generated)
├── templates/
│   └── index.html           # HTML template
```

## Step 2: Generate Model Files (if needed)

If you already have your trained model file (model.pkl) from your Jupyter notebook, you can use it directly. If not, run the create_model.py script to generate the necessary model files:

```bash
python create_model.py
```

This will create:
- model.pkl
- vectorizer.pkl
- pca.pkl
- imputer.pkl

## Step 3: Push to Git Repository

Initialize and push your project to a Git repository:

```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git remote add origin <your-repository-url>
git push -u origin main
```

## Step 4: Deploy to Render

### Option 1: Deploy from Render Dashboard (Manual)

1. Log in to your Render account
2. Click on the "New +" button and select "Web Service"
3. Connect your repository
4. Configure the service:
   - **Name**: mcdonalds-sentiment-analysis
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Select Python Version**: 3.10.0 (or your preferred version)
5. Click "Create Web Service"

### Option 2: Deploy using render.yaml (Blueprint)

1. If you have the render.yaml file in your repository, you can use the Render Blueprint feature.
2. Go to your Render dashboard
3. Click on "New +" and select "Blueprint"
4. Connect your repository
5. Render will automatically detect the render.yaml file and create the defined services
6. Review the configuration and click "Apply"

## Step 5: Monitor Deployment

1. Render will build and deploy your application
2. You can monitor the build process in the Render dashboard
3. Once deployment is complete, Render will provide you with a URL (e.g., https://mcdonalds-sentiment-analysis.onrender.com)
4. Your application is now live!

## Step 6: Testing Your Deployment

1. Open the provided URL in your browser
2. Enter a review in the form
3. Submit the form to see sentiment analysis results
4. Check that the application is working correctly

## Common Issues and Solutions

### Model File Size

If your model.pkl file is large, you may encounter issues with Git repository size limits. Consider:

1. Using Git LFS (Large File Storage)
2. Creating a simpler model for demonstration
3. Setting up a workflow to generate the model during the build process

### Environment Variables

If your app requires environment variables, add them in Render dashboard:
1. Go to your web service
2. Navigate to the "Environment" tab
3. Add your environment variables

### Custom Domain

To use a custom domain:
1. Go to your web service
2. Navigate to the "Settings" tab
3. Scroll to "Custom Domain"
4. Follow the instructions to set up your domain

## Maintenance and Updates

To update your deployed application:

1. Make changes to your code locally
2. Commit and push changes to your Git repository
3. Render will automatically detect changes and rebuild your application

## Monitoring and Scaling

- Monitor application performance in the Render dashboard
- Upgrade to a paid plan for better performance if needed
- Enable auto-scaling for high-traffic applications (paid plans only)

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://render.com/docs/deploy-flask)
- [Render Blueprint Docs](https://render.com/docs/blueprint-spec)
