# addAPI
This readme file explains the usage of the APIs in `UserInterface.py`

First, start the UserInterface.py by using the following command:
```sh
flask --app UserInterface.py run
```

## Search by Gene
The `searchByGene_api` function is setup to use the GET http request method. Two of the ways it can be tested are shown below.

    1. Directly through the browser using the url `http://127.0.0.1:5000/searchGene?geneID=90`. This url will return all items in the table that match the geneID '90'.

    2. Using curl command from terminal.

    curl 'http://127.0.0.1:5000/searchGene?geneID=90'

## Search by Mesh
The `searchByMesh_api` function also uses the GET http request method and functions the same way as above.

    1. `http://127.0.0.1:5000/searchMesh?mesh=Humans` will return all items that have a mesh equal to 'Humans'

    2. Using curl command from terminal

    curl 'http://127.0.0.1:5000/searchMesh?mesh=Humans'

## Search by Multiple Gene IDs
The `searchByMultipleGenes_api` function is setup to use the POST http request method. This function requires data to be passed as a payload rather than within the url. This function can be tested with curl as shown below.

```sh
curl 'http://127.0.0.1:5000/searchMultipleGenes' \
-H 'content-type: application/json' \
-d '{
    "geneIDs": ["90", "175"]
}'
```
