from psycopg2 import connect
import os
import csv


def openConnection(dbName: str = None) -> type(connect()):
    conn = connect(
            host='seniordesign.cyzdvv3sqno4.us-east-1.rds.amazonaws.com',
            port='5432',
            database='bi' if not dbName else dbName,
            user='postgres',
            password='Uconn!2024'
    )

    return conn


def searchByGene(gene: str, connection: type(connect())) -> list:
    cursor = connection.cursor() 

    
    cursor.execute(
        f"SELECT * FROM \"GENE\" WHERE \"GeneID\" = '{gene}' ORDER BY \"p_Value\" ASC;")
    output = cursor.fetchall() 

    
    return list(output)


def searchByMesh(mesh: str, connection: type(connect())) -> list:
    cursor = connection.cursor() 

    
    cursor.execute(
        f"SELECT * FROM \"GENE\" WHERE \"MeSH\" LIKE '{mesh}' ORDER BY \"p_Value\" ASC;") #may need to change like depending
    output = cursor.fetchall() 

    
    return list(output)


def multipleByGeneId(geneList: list, connection: type(connect())) ->  list:
    cursor = connection.cursor()

    
    for gene in geneList:
        cursor.execute(
            f"SELECT * FROM \"GENE\" WHERE \"GeneID\" = '{gene}' ORDER BY \"p_Value\" ASC;")

    
    return cursor.fetchall()


# def multipleByGeneMesh(meshList: list, connection: type(connect())) ->  list:
#     cursor = connection.cursor()
    
#     for mesh in meshList:
#         cursor.execute(
#             f"SELECT * FROM GENE WHERE MeSH = '{mesh}' ORDER BY p_value ASC;")
        
#     return cursor.fetchall()


def writeToCsvFile(data: list, fileName: str) -> None:
    with open(f"{fileName}","w") as f:
        csv_out = csv.writer(f)
        csv_out.writerow(["GeneID", "MeSH", "p_value", "Enrich", "PMIDs"])
        csv_out.writerows(data)

    return


def main() -> None:
    connection = openConnection()

    print("\nDemo 1")


    # userInput = input("Enter Gene to search by: ").strip()
    # data = searchByGene(gene=userInput, connection=connection)
    # data = searchByMesh(mesh='Acyl-CoA Dehydrogenase', connection=connection)   #* manual use *
    data = searchByGene(gene=34, connection=connection)                       #* manual use *
    writeToCsvFile(data=data, fileName='Demo.csv')


    print("\nDone!\n")
    connection.close()
#}


if __name__ == "__main__":
    main()

