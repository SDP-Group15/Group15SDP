from flask import Flask, render_template, jsonify, request, send_file
from Backend import openConnection, searchByGene, searchByMesh, searchByGeneIDs
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def format_results(raw_results):
    formatted = []
    for result in raw_results:
        formatted_result = {
            'id': result[0],  # Assuming result[0] is the id
            'description': result[1],  # Assuming result[1] is the description
            # Add more fields based on your actual database result structure
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