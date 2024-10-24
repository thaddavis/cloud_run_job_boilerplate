# TLDR

A simple Python boilerplate project for creating "Cloud Run Jobs" (CRJ)

## Table of Contents

1. [How to run the development environment](#1)
2. [How to run the job script in the Dev container](#2)
3. [How to deploy the job script to Cloud Run from the Dev container](#3)
4. [How to run the job in Cloud Run](#4)
5. [How to run the job on a schedule aka as a cron job](#5)
6. [How to redeploy a new docker image for the job in GCP](#6)

# 1 
## How to run the development environment

- Assuming you use VSCode...
  - SHIFT + CMD + P 
  - Dev Containers: Rebuild Container
- The included Dev container comes with `gcloud`, `Python 3.12`, `cURL`, and `Docker`
  - You can tweak the `Dockerfile.dev` & `.devcontainer/devcontainer.json` files if you need more software

# 2
## How to run the job script

- `pip install -r requirements.txt`
- `python main.py`

# 3
## How to deploy the job script to Cloud Run from the Dev container

```sh
gcloud -v # for checking that gcloud is installed
docker -v # for checking that Docker is installed
gcloud auth login # then follow the steps to authenticate the Dev container with GCP
gcloud config list account --format "value(core.account)" # for confirming you are authenticated
# The next command creates a repository in GCP's "Artifact Registry" service where you can store Docker images
gcloud artifacts repositories create crj-image-repo --repository-format=docker --location=us-east1 --project $YOUR_PROJECT_ID 
gcloud auth print-access-token # for getting an access token for authenticating Docker with the "Artifact Registry" service offered by GCP
docker login -u oauth2accesstoken https://us-east1-docker.pkg.dev # for connecting Docker to "Artifact Registry" (paste in the access token)
docker build --platform linux/amd64 -t crj-image . # for building the local code into a container for deployment to CRJ
docker tag crj-image us-east1-docker.pkg.dev/$YOUR_PROJECT_ID/crj-image-repo/crj-image:latest # for tagging the image in a way that aligns with "Artifact Registry"
docker push us-east1-docker.pkg.dev/$YOUR_PROJECT_ID/crj-image-repo/crj-image:latest # for storing the image into "Artifact Registry"
gcloud run jobs deploy my-job --image us-east1-docker.pkg.dev/$YOUR_PROJECT_ID/crj-image-repo/crj-image:latest --region us-east1 --project $YOUR_PROJECT_ID # deploy the job
```

# 4
## How to run the job in Google Cloud Run

- `gcloud run jobs execute my-job --region us-east1`

# 5
## How to run the job on a schedule aka as a cron job

- `gcloud scheduler jobs create http SCHEDULER_JOB_NAME \
  --location SCHEDULER_REGION \
  --schedule="SCHEDULE" \
  --uri="https://CLOUD_RUN_REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/PROJECT-ID/jobs/JOB-NAME:run" \
  --http-method POST \
  --oauth-service-account-email PROJECT-NUMBER-compute@developer.gserviceaccount.com`

# 6
## How to redeploy a new docker image for the job in GCP

```sh
gcloud auth login
gcloud auth print-access-token
docker login -u oauth2accesstoken https://us-east1-docker.pkg.dev
docker build --platform linux/amd64 -t us-east1-docker.pkg.dev/$YOUR_PROJECT_ID/crj-image-repo/crj-image:latest .
docker push us-east1-docker.pkg.dev/$YOUR_PROJECT_ID/crj-image-repo/crj-image:latest
gcloud run jobs execute my-job --region us-east1 --project $YOUR_PROJECT_ID
```