# Boehringer Ingelheim MeSH Senior Design Project

Welcome to the MeSH Mining Github repo. Instructions, user manuals, and various other info can be found in the `info` directory.

## Running the MeSH Mining Website

1. Making a virtual environment (optional)
Making a python virtual environment is optional, but recommended as there are a number of dependencies that need to be installed. Instructions to create the python virtual environment for MacOS are as follows:
```sh
mkdir meshMining
```
```sh
cd meshMining
```
```sh
python3 -m venv .venv
```
to activate the environment on MacOS, from within the `meshMining` directory type the following command:
```sh
. .venv/bin/activate
```

In order to create a python virtual environment on Windows, use the following commands:
```sh
mkdir meshMining
```
```sh
cd meshMining
```
```sh
py -3 -m venv .venv
```
To activate the environment on Windows, from within the `meshMining` directory, type the following command:
```sh
.venv\Scripts\activate
```

2. Installing the dependencies
Once the python virtual environment has been activated, the dependencies for the project need to be installed. In order to install the dependencies, run the following command in the home directory of the project:
```sh
pip install -r requirements.txt
```

3. Start the server for the website

Finally, start the website by runnning the following command:
```sh
flask --app UserInterface.py run
```

This will start a development server and provide a url (usually `http://127.0.0.1:5000`) where the website can be accessed.