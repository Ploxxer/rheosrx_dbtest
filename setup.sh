#!/bin/bash

# Create and initialize a Python Virtual Environment
echo "Creating virtual env - .env"
virtualenv .env

echo "sourcing virtual env - .env"
source .env/bin/activate

# Create a directory to put things in
echo "Creating 'setup' directory"
mkdir setup

# Move the relevant files into setup directory
echo "moving relevant files into setup directory"
cp db_record_create.py setup/
cp test_file_2.csv setup/
cd ./setup

# Install requirements 
echo "pip installing requirements from requirements file in target directory"
pip install -r ../requirements.txt -t .

# Prepares the deployment package
echo "Zipping package"
zip -r ../package.zip ./* 

# Remove the setup directory used
echo "Removing setup directory and virtual environment"
cd ..
rm -rf ./setup
deactivate
rm -rf ./.env
# changing dirs back to dir from before
echo "Opening folder containg function package - 'package.zip'"
open .
