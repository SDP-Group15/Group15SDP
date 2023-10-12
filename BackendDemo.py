from psycopg2 import connect
#pip install psycopg2
import os

print(os.environ.get('USERNAME'))

def openConnection(dbName: str)->type(connect()):
    conn = connect(
        host="localhost",
        port=5432,
        database = dbName
    )
    return conn

def searchByGene(gene: str, connection: type(connect()))->str:
    cursor = connection.cursor() 
    cursor.execute(
        f"SELECT * FROM GENE WHERE GeneID = '{gene}';")
    output = cursor.fetchall() 
    return output


if __name__ == "__main__":
    conn = openConnection(dbName='jmatura') 
    #replace with your pc username
    #make sure to when using postgresql to use the database that is named after this username

    userInput = input('Enter GENE to search by: ').strip()

    output = searchByGene(gene=userInput, connection=conn)
    for lst in output:
        print(lst)

    conn.close()


 
