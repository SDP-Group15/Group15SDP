from flask import Flask, render_template, jsonify, request, send_file
<<<<<<< HEAD
from Backend import openConnection, searchByGene, searchByMesh, multipleByGeneId
=======
from Backend import openConnection, searchByGene, searchByMesh, searchByGeneIDs
>>>>>>> origin/apinew
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


<<<<<<< HEAD
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
=======
def format_results(raw_results):
    formatted = []
    for result in raw_results:
        formatted_result = {
            'id': result[0],
            'description': result[1],

        }
        formatted.append(formatted_result)
    return formatted


@app.route('/searchGene', methods=['GET'])
def searchByGene_api():
    geneID = request.args.get('geneID')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if geneID is None:
        return jsonify({'error': 'No parameter in request'}), 400

    dbConnection = openConnection()
    response = searchByGene(geneID, dbConnection, page, per_page)
    dbConnection.close()

    return jsonify(response)



@app.route('/searchMesh', methods = ['GET'])
def searchByMesh_api():
    mesh_term = request.args.get('meshTerm')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    if not mesh_term:
        return jsonify({'error': 'No MeSH term provided'}), 400

    dbConnection = openConnection()
    response = searchByMesh(mesh_term, dbConnection, page, per_page)
    dbConnection.close()

    return jsonify(response)




@app.route('/searchMultipleGenes', methods=['GET'])
def searchMultipleGenes_api():
    gene_ids = request.args.get('geneIDs')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    if not gene_ids:
        return jsonify({'error': 'No gene IDs provided'}), 400

    dbConnection = openConnection()
    response = searchByGeneIDs(gene_ids, dbConnection, page, per_page)  # Adjust function name if different
    dbConnection.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> origin/apinew
