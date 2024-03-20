# Boehringer Ingelheim MeSH Senior Design Project

Welcome to the MeSH Mining Github repo. Instructions, user manuals, and various other info can be found in the `info` directory.

## Running the MeSH Mining Website

1. Download a zip file of the Group15SDP repo

Navigate to the main branch, click the "Code" dropdown button, click `Download ZIP` and navigate to the downloaded folder (`Group15SDP-main`).

2. Making a virtual environment (optional)

Making a python virtual environment is optional, but recommended as there are a number of dependencies that need to be installed. Once in the `Group15SDP-main` folder, run the following command (MacOS or Linux, Windows commands given later):

MacOS or Ubuntu
```sh
python3 -m venv .venv
```

Windows
```sh
py -3 -m venv .venv
```

Activate the environment from within the `Group15SDP-main` directory, by typing the following command:

MacOS or Ubuntu
```sh
. .venv/bin/activate
```
Windows
```sh
.venv\Scripts\activate
```

3. Installing the dependencies

From within the `Group15SDP-main` folder, install the dependencies by typing the following command (activate the environment first if step 2 was completed):
```sh
pip install -r requirements.txt
```

4. Start the server for the website

Finally, start the website by runnning the following command:
```sh
flask --app UserInterface.py run
```

This will start a development server and provide a url (usually `http://127.0.0.1:5000`) where the website can be accessed.
