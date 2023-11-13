from flask import Flask, render_template, jsonify, request, send_file
from Backend import openConnection, searchByGene
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#example api run, this will return all genes with id '34' from the database
#will add functionality to take an input later --Isaiah
@app.route('/api-test', methods = ['GET'])
def hello():
    dbConection = openConnection()
    gene = searchByGene('34', dbConection)
    return gene[1]

if __name__ == '__main__':
    app.run(debug=True)