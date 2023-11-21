from flask import Flask, render_template, jsonify, request, send_file
from Backend import openConnection, searchByGene, searchByMesh, multipleByGeneId
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


#search by gene api, use by appending '/searchGene?geneID=<geneID input>'
#to the end of the website url.
@app.route('/searchGene', methods = ['GET'])
def searchByGene_api():
    #gets geneID from url
    geneID = request.args.get('geneID')
    data = "no parameter in request"

    if geneID is None:
        return data
    else:
        dbConnection = openConnection()
        gene = searchByGene(geneID, dbConnection)
        data = gene[1]
        return data

#search by mesh api, use by appending '/searchMesh?mesh=<mesh string>'
#to the end of the website url
#this function currently only works with a mesh that does not contain
#a space in it
@app.route('/searchMesh', methods = ['GET'])
def searchByMesh_api():
    #gets mesh from url
    mesh = request.args.get('mesh')
    data = "no parameter in request"
    
    if mesh is None:
        return data
    else:
        dbConnection = openConnection()
        gene = searchByMesh(mesh, dbConnection)
        data = gene[1]
        return data

#search for multiple genes api, this method uses post and 
#requires the header to be set to 'content-type: application/json'
#the body of the post request uses the format 'geneIDs': ['<ID1>', '<ID2>']
@app.route('/searchMultipleGenes', methods = ['POST'])
def searchByMultipleGenes_api():
    #gets list of genes from post body
    requestData = request.get_json()
    geneList = requestData['geneIDs']
    data = "no parameter in request"

    if geneList is None:
        return data
    else:
        dbConnection = openConnection()
        gene = multipleByGeneId(geneList, dbConnection)
        data = gene[1]
        return data
    
if __name__ == '__main__':
    app.run(debug=True)