from psycopg2 import connect
import os
import csv


def openConnection(dbName: str = None) -> type(connect()):
    conn = connect(
        host="localhost",
        port=5432,
        database = dbName if dbName else os.environ.get('USER')
    )
    return conn


def searchByGene(gene: str, connection: type(connect())) -> list:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT * FROM GENE WHERE GeneID = '{gene}';")
    output = cursor.fetchall() 

    return list(output)


def searchByMesh(mesh: str, connection: type(connect())) -> list:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT * FROM GENE WHERE MeSH = '{mesh}';")
    output = cursor.fetchall() 

    return list(output)


def multipleByGeneId(geneList: list, connection: type(connect())) ->  list:
    cursor = connection.cursor()
    
    for gene in geneList:
        cursor.execute(
            f"SELECT * FROM GENE WHERE GeneID = '{gene}';")
        
    return cursor.fetchall()


def multipleByGeneMesh(meshList: list, connection: type(connect())) ->  list:
    cursor = connection.cursor()
    
    for mesh in meshList:
        cursor.execute(
            f"SELECT * FROM GENE WHERE MeSH = '{mesh}';")
        
    return cursor.fetchall()


def writeRows(data : list, fileName : str):
    with open(f"{fileName}","w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["GeneID", "MeSH", "p_value", "Enrich", "PMIDs"])
        csv_out.writerows(data)


def main() -> None:
    connection = openConnection()

    print("\nDemo 1")

    # userInput = input("Enter Gene to search by: ").strip()
    # data = searchByGene(gene=userInput, connection=connection)

    data = searchByGene(gene=34, connection=connection)
    writeRows(data=data, fileName='Demo.csv')



    print("\nDone!\n")
    connection.close()
#}


if __name__ == "__main__":
    main()

    #todo: combine gene/mesh search singular and multiple into one function with sql statement selectors
    #      allow for single or multiple user inputs


