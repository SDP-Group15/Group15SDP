from flask import Flask, render_template, jsonify, request
from static.python.Backend import openConnection, searchByGene, searchByMesh, searchByGeneIDs
from static.python.dropdownLists import geneIDs, meshTerms
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', geneIDs=geneIDs, meshTerms=meshTerms)

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html')


@app.route('/searchGene', methods=['GET'])
def searchByGene_website():
    geneID = request.args.get('geneID')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    if geneID is None:
        return jsonify({'error': 'No parameter in request'}), 400

    dbConnection = openConnection()
    response = searchByGene(geneID, dbConnection, page, per_page)
    dbConnection.close()

    return jsonify(response)

@app.route('/searchMesh', methods = ['GET'])
def searchByMesh_website():
    #mesh_term needs to be a header so that the mesh term can contain spaces
    mesh_term = request.headers.get('meshTerm')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    if mesh_term is None:
        return jsonify({'error': 'No MeSH term provided'}), 400

    dbConnection = openConnection()
    response = searchByMesh(mesh_term, dbConnection, page, per_page)
    dbConnection.close()

    return jsonify(response)

@app.route('/searchMultipleGenes', methods=['GET'])
def searchMultipleGenes_website():
    gene_ids = request.args.get('geneIDs')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=20, type=int)

    if gene_ids is None:
        return jsonify({'error': 'No gene IDs provided'}), 400

    dbConnection = openConnection()
    response = searchByGeneIDs(gene_ids, dbConnection, page, per_page)  # Adjust function name if different
    dbConnection.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)