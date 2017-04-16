# Blog webapplication

This project is for the Udacity full stack developer course spring 2017. The project features a functioning blog web app deployment ready for google app engine. The application uses jinja for templating and app engine for development and deployment.

## Getting started

Instructions on getting a local copy of the project running for development and testing purposes.

### Prerequists

- Python
- jinja2
- Gcloud sdk
- app-engine-python component for gcloud

### Installing

1. Clone this repository `$ git clone https://github.com/Andurshurrdurr/Udacity_blog.git`
2. Download and install the gcloud SDK. Follow the instructions given by google for your OS:
https://cloud.google.com/sdk/docs/quickstarts
3. Go to the project folder (where you cloned the repo) in your terminal `$ cd ~/projectfolder/`
5. Run `$ dev_appserver.py ./`
4. Gcloud should prompt you to install the python app engine extensions now, otherwise install the sdk app-engine-python components manually: `gcloud component install app-engine-python`
6. Open your browser and go to localhost:8080 and/or :8000

### Deploying to google app engine

1. Go to https://console.cloud.google.com/appengine and start a new project.
2. Open the console on google cloud
3. From the console you can clone this repository by typing

`$ git clone https://github.com/Andurshurrdurr/Udacity_blog.git`

4. Move the terminal into the directory and deploy it to app engine by running:

`$ cd Udacity_blog && cloud app deploy app.yaml`

5. Follow the instructions given by the terminal

### Running example

The project is currently publicly running at https://basic-blog-158212.appspot.com

## About Udacity

![Udacity](https://in.udacity.com/assets/images/svgs/logo_wordmark.svg)

Udacity is a for-profit educational organization founded by Sebastian Thrun, David Stavens, and Mike Sokolsky offering massive open online courses. [Wikipedia](https://en.wikipedia.org/wiki/Udacity)

This project is a part of my Udacity Full stack webdeveloper nanodegree.

## License

The MIT License (MIT)

Copyright (c) 2017 Anders Hurum

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
