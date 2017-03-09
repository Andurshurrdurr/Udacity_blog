# Blog webapplication

This project is for the Udacity full stack developer course spring 2017.

The project features a functioning blog web app deployment ready for google app engine.

The application uses jinja for templating and app engine for development and deployment

### Instructions for development

1. Clone this repository `$ git clone https://github.com/Andurshurrdurr/Udacity_blog.git´
2. Download and install the gcloud SDK. Follow the instructions given by google for your OS:
https://cloud.google.com/sdk/docs/quickstarts
3. Go to the project folder (where you cloned the repo) in your terminal ´$ cd ~/projectfolder/
4. Run ´$ dev_appserver.py ./´
5. Open your browser and go to localhost:8000

### Instructions for deployment

This project must be deployed on google app engine.

To do this go to https://console.cloud.google.com/appengine and start a new project.

From the console you can clone this repository by typing 

`$ git clone https://github.com/Andurshurrdurr/Udacity_blog.git`

and deploy it to app engine by running:

`$ gcloud app deploy app.yaml`

Then follow the instructions given by the terminal

### Running example

The project is currently publicly running at https://basic-blog-158212.appspot.com


