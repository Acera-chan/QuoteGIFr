# QuoteGIFr
CSCI540 FA2019 Project

## Configuration:
1. Install [ImageMagick](https://imagemagick.org/script/download.php)
2. Edit "QuoteGIFr/codebase/moviepy/config_defaults.py" to point to your ImageMagick binary

## Using videoTester.py
1. Edit file locations in "QuoteGIFr/codebase/videoTester.py" to point to correct folders on your local machine
2. Run videoTester.py, and your web browser should open with the GIF having been uploaded to giphy.com

## Using app.py (The Flask app: aka the backend of our QuoteGIFr web application)
1. app was built on Python 3.7.4
2. run command "pip install -r requirements.txt" from the main directory (with requirements.txt present). This will install all necessary modules.
3. run command "python app.py" from within the codebase directory on the command line, then go to localhost:5000 in your browser, and you should see the homepage being hosted on your local machine.
