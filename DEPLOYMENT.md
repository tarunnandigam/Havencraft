# Deployment Guide for HandmadeMart

This guide will walk you through deploying HandmadeMart to Render.com with a PostgreSQL database.

## Prerequisites

1. A GitHub account
2. A Render.com account (you can sign up with GitHub)
3. Git installed on your local machine

## Deployment Steps

### 1. Push to GitHub

First, commit all your changes and push them to a GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" and select "Web Service"
3. Connect your GitHub account if you haven't already
4. Select your repository
5. Configure the web service:
   - Name: `handmademart`
   - Region: Choose the one closest to your users
   - Branch: `main`
   - Build Command: `pip install -r HandmadeMart/requirements.txt`
   - Start Command: `gunicorn "HandmadeMart.app:app"`
6. Click "Advanced" and add the following environment variables:
   - `PYTHON_VERSION`: `3.9.0`
   - `FLASK_APP`: `app.py`
   - `FLASK_ENV`: `production`
   - `SESSION_SECRET`: Generate a strong secret key
7. Click "Create Web Service"

### 3. Set Up PostgreSQL Database

1. In the Render Dashboard, click "New" and select "PostgreSQL"
2. Configure the database:
   - Name: `handmademart-db`
   - Database: `handmademart`
   - User: `handmademart_user`
   - Region: Same as your web service
3. Click "Create Database"
4. Once created, go to the database details and copy the "Internal Database URL"
5. Go back to your web service settings
6. Add a new environment variable:
   - Key: `DATABASE_URL`
   - Value: The database URL you copied (starts with `postgresql://`)
7. Save the changes

### 4. Deploy the Application

1. In your web service on Render, go to the "Deploys" tab
2. Click "Trigger Manual Deploy"
3. Select "Deploy from main branch"
4. Wait for the deployment to complete

### 5. Initialize the Database

1. Once deployed, open the web URL of your application
2. Append `/health` to the URL to verify the application is running
3. The application will automatically create the database tables on first run

## Environment Variables

Create a `.env` file in the `HandmadeMart` directory with the following variables (use `.env.example` as a template):

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/handmademart
```

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r HandmadeMart/requirements.txt
   ```

3. Set up the database:
   ```bash
   cd HandmadeMart
   flask db upgrade
   ```

4. Run the development server:
   ```bash
   flask run
   ```

## Troubleshooting

- If you see database connection errors, verify the `DATABASE_URL` is correct
- Check the logs in the Render Dashboard for error messages
- Make sure all environment variables are set correctly

## Updating the Application

1. Make your changes locally
2. Commit and push to GitHub
3. Render will automatically deploy the changes

## Support

If you encounter any issues, please check the [Render documentation](https://render.com/docs) or contact support.
