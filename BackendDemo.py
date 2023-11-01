from psycopg2 import connect
import os
import csv
import simplejson
import json


def openConnection(dbName: str = None) -> type(connect()):
    conn = connect(
            host='seniordesign.cyzdvv3sqno4.us-east-1.rds.amazonaws.com',
            port='5432',
            database='sdp152024' if not dbName else dbName,
            user='postgres',
            password='Uconn!2024'
    )
    return conn


def searchByGene(gene: str, connection: type(connect())) -> tuple:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT * FROM \"GENE\" WHERE \"GeneID\" = '{gene}' ORDER BY \"p_Value\" ASC;")
    
    output = cursor.fetchall() 
    
    return list(output), simplejson.dumps(output, indent=2)
#   **returns tuple access the elements 0 and 1 accordingly**


def searchByMesh(mesh: str, connection: type(connect())) -> tuple:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT * FROM \"GENE\" WHERE \"MeSH\" LIKE '{mesh}' ORDER BY \"p_Value\" ASC;") #may need to change like depending
    
    output = cursor.fetchall() 

    return list(output), simplejson.dumps(output, indent=2)


def multipleByGeneId(geneList: list, connection: type(connect())) ->  tuple:
    cursor = connection.cursor()
    
    output = []
    for gene in geneList:
        cursor.execute(
            f"SELECT * FROM \"GENE\" WHERE \"GeneID\" = '{gene}' ORDER BY \"p_Value\" ASC;")
        tempregister = cursor.fetchall()
        if(tempregister): output+= tempregister

    return output, simplejson.dumps(output, indent=2)


def writeJsonToTxt(data: list, fileName: str = 'Demo.txt') -> None:
    with open(f"{fileName}","w") as f:
        f.write(data)

    return 


def writeToCsvFile(data: list, fileName: str = 'Demo.csv') -> None:
    with open(f"{fileName}","w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["GeneID", "MeSH", "p_value", "Enrich", "PMIDs"])
        csv_out.writerows(data)

    return 


def console() -> None:
    connection = openConnection()

    print("\nDemo 1")

    userInput = input("Enter Gene to search by: ").strip()
    output = searchByGene(gene=userInput, connection=connection) 
    
    writeToCsvFile(data=output[0])
    writeJsonToTxt(data=output[1])

    print("Done")


    return None


def main() -> None:
    connection = openConnection()

    output = multipleByGeneId(geneList=[34,37,128], connection=connection)

    # output = searchByMesh(mesh='Acyl-CoA Dehydrogenase', connection=connection) #* manual use *
    # output = searchByGene(gene=34, connection=connection)                       #* manual use *

    print(output[0])

    writeToCsvFile(data=output[0])
    writeJsonToTxt(data=output[1])



    print("\nDone!\n")
    connection.close()

    return
#}


if __name__ == "__main__":
    main()
    # console()

