# addAPI
This readme file explains the usage of the APIs in `UserInterface.py`

First, start the UserInterface.py by using the following command:
```sh
flask --app UserInterface.py run
```

## Search by Gene
The `searchByGene_api` function is setup to use the GET http request method. Two of the ways it can be tested are shown below.  
1. Directly through the browser using the url `http://127.0.0.1:5000/searchGene?geneID=90`. This url will return all items in the table that match the geneID '90'.
2. Using the curl command from terminal:
```sh
curl 'http://127.0.0.1:5000/searchGene?geneID=90'
```
## Search by Mesh
The `searchByMesh_api` function also uses the GET http request method but takes the input as a header rather than as a query string. An example test using curl is shown below:  
```sh
curl 'http://127.0.0.1:5000/searchMesh' \
-H 'content-type: application/json' \
-H 'meshTerm: Genetic Predisposition to Disease'
```
## Search by Multiple Gene IDs
The `searchByMultipleGenes_api` function is setup to use the GET http request method and functions similar to the "Search by Gene" API. Two of the ways it can be tested are shown below.  
1. Directly through the browser using the url `http://127.0.0.1:5000/searchMultipleGenes?geneIDs=34,90,175`. This url will return all items in the table that match the geneIDs '34, 90, and 175'.
2. Using the curl command from terminal:
```sh
curl 'http://127.0.0.1:5000/searchMultipleGenes?geneIDs=34,90,175'
```
