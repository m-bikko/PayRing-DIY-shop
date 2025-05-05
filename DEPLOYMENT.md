# Deploying PayRing to Google Cloud

This guide walks through deploying the PayRing application to Google Cloud Platform using Docker and Cloud Run.

## Prerequisites

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured
2. [Docker](https://docs.docker.com/get-docker/) installed
3. Git repository with your application code
4. Google Cloud Platform account with billing enabled

## Step 1: Update Configuration Files

1. Update the `SECRET_KEY` in `docker-compose.yml` with a secure random string
2. Make sure gunicorn is in your dependencies (it's added in requirements-prod.txt)

## Step 2: Build and Test Locally

```bash
# Install production dependencies
pip install -r requirements-prod.txt

# Build and run with docker-compose
docker-compose up --build
```

Access the application at `http://localhost:8080` to verify it works correctly.

## Step 3: Deploy to Google Cloud

### Set Up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create payring-app --name="PayRing App"

# Set as current project
gcloud config set project payring-app

# Enable required services
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Create Container Registry Repository

```bash
# Create Artifact Registry repository
gcloud artifacts repositories create payring-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="PayRing application repository"
```

### Build and Push Docker Image

```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker us-central1-docker.pkg.dev

# Build the image with Cloud Build
gcloud builds submit --tag us-central1-docker.pkg.dev/payring-app/payring-repo/payring-app:latest
```

### Deploy to Cloud Run

```bash
# Deploy the container to Cloud Run
gcloud run deploy payring-service \
  --image us-central1-docker.pkg.dev/payring-app/payring-repo/payring-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars="SECRET_KEY=your-secure-secret-key"
```

After successful deployment, Cloud Run will provide a URL to access your application.

## Step 4: Set Up Persistent Storage (Optional)

For a production application, you might want to use Cloud SQL instead of SQLite:

1. Create a Cloud SQL instance:
```bash
gcloud sql instances create payring-db \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1
```

2. Create a database:
```bash
gcloud sql databases create payring_prod \
  --instance=payring-db
```

3. Update your application configuration to use PostgreSQL and update the deployment.

## Step 5: Set Up Continuous Deployment (Optional)

You can set up continuous deployment using Cloud Build triggers:

1. Connect your Git repository to Cloud Build
2. Create a build trigger for your repository
3. Configure the trigger to build and deploy on pushes to main branch

## Troubleshooting

- **Application crashes**: Check Cloud Run logs
- **Database connection issues**: Verify database credentials and connectivity
- **Permission errors**: Check IAM permissions for your service account

For more detailed information, refer to Google Cloud documentation:
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)