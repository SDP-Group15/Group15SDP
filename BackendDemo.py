from psycopg2 import connect
import os
import csv
import simplejson
import json
import scipy


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
    
    pValIndex = 2
    output = []
    pvals = []
    for gene in geneList:
        cursor.execute(
            f"SELECT * FROM \"GENE\" WHERE \"GeneID\" = '{gene}' ORDER BY \"p_Value\" ASC;")
        tempregister = cursor.fetchall()
        if(tempregister):
            output += tempregister
            for row in tempregister:
                pvals.append(float(row[pValIndex]))  

    print(combinePVals(pValues=pvals))

    return output, simplejson.dumps(output, indent=2)


def combinePVals(pValues: list) -> float:
    res = None
    try:
        res = scipy.stats.combine_pvalues(pValues, method='fisher',weights=None)
    except:
        print("Exception occured")
        return None

    return res[1] if res else None
    

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


def listAllGene(connection: type(connect())) -> list:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT DISTINCT \"GeneID\" FROM \"GENE\" ORDER BY \"GeneID\" ASC;")
    
    data = cursor.fetchall()

    return [str(i[0]) for i in data]


def listAllMesh(connection: type(connect())) -> list:
    cursor = connection.cursor() 

    cursor.execute(
        f"SELECT \"MeSH\" FROM (SELECT * FROM \"GENE\" ORDER BY \"p_Value\" ASC) AS A;")
    
    data = cursor.fetchall()
    
    return [str(i[0]) for i in data]


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

    # output = multipleByGeneId(geneList=[34,37], connection=connection)

    # print(listAllGene(connection=connection))
    print(listAllMesh(connection=connection))


    # output = searchByMesh(mesh='Acyl-CoA Dehydrogenase', connection=connection) #* manual use *
    # output = searchByGene(gene=34, connection=connection)                       #* manual use *

    # print(output[0])

    # writeToCsvFile(data=output[0])
    # writeJsonToTxt(data=output[1])



    print("\nDone!\n")
    connection.close()

    return
#}


if __name__ == "__main__":
    main()
    # console()

