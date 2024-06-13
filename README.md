# insurance_premium_prediction
The project is about estimating the hospitalization charges for a patient based on patient demographics so that the correct premium can be charged and this also helps to set a correct claim reserve upon notification.
## Prerequisites
Create a virtual environment and install the dependencies from the **requirements.txt** file. An you should also have an AWS account because this is where we are going to deploy the project.
>Note: replace \<venv\> with your environment name
```
conda create -n <venv> python=3.8 -y
pip install -r requirements.txt
```
## Dataset
The dataset can be downloaded from [kaggle](https://www.kaggle.com/datasets/noordeen/insurance-premium-prediction)

## Training the model localy (Triggering the training pipeline)
To test the code locally use below commands. This basically trains the model and pushes the model to the AWS S3 bucket (only if the current model is better than the one already present in the S3). The run triggers the training pipeline Data Ingestion-->Data Validation-->Data Transformation-->Model building-->Model Validation-->Model pusher. Each of these runs produces the logs for each pipeline step (under **Logs** folder). Each run produces artifacts such as train and test splits, preprocessor object, trained model in the respective paths under **Artifacts** folder. For more details please refer the HLD and LLD.
```
export MONGODB_URL="<mongo_db_connection_string>"
export AWS_ACCESS_KEY="<aws_access_key>
export AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>

python demo.py
```
**Important!!: These exports are ONLY while running locally. For the deployment the Git hub secrets are used to store the keys.**

## Predicting the results locally
To launch the application use
```
python app.py
```
Then application is accessed at [http://localhost:8080/], where we can fill the details and get the predicted output.

## CI/CD and deploying into AWS
1. Docker is used to containarize the application. AWS ECR is used for storing the docker image.
2. For CI/CD the Github actions are used. Two jobs are configured one for deploying the updated docker image to the AWS ECR (CI) and another for deploying (CD) the docker image of the application on AWS EC2

## Training the model on AWS

## Predicting the result on AWS

