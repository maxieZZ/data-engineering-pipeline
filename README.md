## Simple CI/CD Data Engineering Pipeline

# Purpose
When the ETL (Extract Load Transform) that a pipeline continuously performs on incoming data is critical to company operations, stopping the pipeline to perform required updates, fixes, or improvements is detrimental to the companies success. To make edits without stopping the pipeline, changes must first be implemented in parallel and deployed only after rigorously testing each component (including data ingestion, transformation, & storage). This concept, known as Continuous Integration and Continuous Deployment (CI/CD), is fundamental to successful pipeline operation and is what I will be exploring in this repository.

# Pipeline Overview
To define a general ETL pipeline, one must begin with the data source which, in this case, will be a database I created with random values using PostgreSQL. After pulling the newest values from this database, there is often a transformation that takes place (e.g. organizing specific pieces of data into a tabular format and discarding the rest). Once the data is transformed, it can be saved and stored in a warehouse or lake of your choice (often in the cloud to preserve space). In order to ensure that this process is working, tests are often employed at each step to error check. For example, before transforming, we need to make sure that data was in fact successfully pulled from the source, otherwise an error should occur. The transformed data should also be checked to insure that it is transformed into the data format we are expecting. Once errors are checked, the pipeline should be triggered to run and the results should be archived somewhere accessible (e.g. data lake or warehouse). Each time changes are made and pushed to the remote repository master, an automated pipeline (jenkins) should be triggered to test the changed ETL pipeline before deploying. A visual depiction of this process is given in the image below.

<img src="images/overview.png?raw=true"/>

Adding a bit more detail to the image above, I have created a database in PostgreSQL with a single table and some made up features. This database will be accessed by a python script (etl.py) which (1) extracts data, (2) transforms the extracted data into a python list of dictionaries, and (3) saves a csv version of the transformed data to a data lake on MinIO (an open-source object storage solution compatible with AWS S3). Next, the built in testing framework in python known as UnitTest can be utilized to create two tests, one to test the functionality of the extraction process and one to test the functionality of the transformation process (test_etl.py). Ideally, running test_etl.py in a python virtual environment should leave no errors which would indicate that the pipeline performs as expected. The pipeline scripts themselves (e.g. etl.py, test_etl.py, and requirements.txt) should be stored on some kind of version control site like GitHub to allow for safe collaboration and edits. 

Now that the pipeline and testing procedures are in place, the next step is to run the code in a way that is machine independent and allows each process to communicate (e.g. python script needs a consistent way to communicate with the database and MinIO needs to communicate with the load portion of the python script. Since docker provides a consistent environment for applications (ensuring they run the same way no matter the system), each of these components is run in a docker container. 

Finally, an open source automation server known as Jenkins (which should also be run in its own docker container) can be used to tie all these components of the pipeline together and facilitate the integration of new updates into the pipeline after performing the required testing. For example, in the case of the pipeline described above, Jenkins can be used to write an automated pipeline with 5 stages that triggers whenever a change in the GitHub code repository is made (via GitHub webhooks). These steps are outlined in the image above and listed below in more detail…

* (1) Clone the repository where the code is stored (includes test_etl.py, etl.py, and requirements.txt)
* (2) Install the required dependencies from requirements.txt (effectively creating the virtual environment needed to run the code)
* (3) Run the tests from etl.py to make sure the code is effective
* (4) Run the ETL pipeline to continue extracting, transforming, and loading data
* (5) Archive the collected data (to make accessible after pipeline runs).


First, make sure MinIO (9000:9001) and PostgreSQL (5432) are set up (DBeaver can be used to access PostgreSQL and create database) and running in their respective docker containers. Next, set up jenkins which should run locally in a docker container on your desired port of choice (in my case port 8080) and then make sure that github credentials are set up on jenkins so that jenkins is able to access your github repo. Next, run ngrok locally on the SAME port of choice (command: ngrok http 8080) which creates a dynamic URL (i.e. a secure and public facing URL which you find under "Forwarding"). To enable github to use this tunnel created by ngrok, set up a webhook on your remote github repo which uses the dynamic url. REMEMBER: Copy and paste the forwarding url to the "Payload URL" field on Github BUT ALSO remember to add "/github-webhook/" to the end of that URL as well (otherwise the webhook won’t work properly). Once this has all been set up, you can test out the pipeline by triggering a Jenkins build via a local push to your remote repository. 

# NOTE: This pipeline is still a work in progress and needs the following…
* Upload Jenkinsfile to GitHub and configure the pipeline to pull instructions from there (rather than writing in the Jenkins groovy UI)
* Figure out how to install python requirements.txt file in jenkins-docker image before performing testing and deployment (to do this, either update and rebuild docker image or run the jenkins job on a docker python node)

This project was made possible by the following medium post: https://towardsdev.com/ci-cd-for-modern-data-engineering-e2e7d2d0a694 
Thank you!:)
