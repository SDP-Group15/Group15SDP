from psycopg2 import connect
#pip install psycopg2
import os

def openConnection(dbName: str)->type(connect()):
    conn = connect(
        host="localhost",
        port=5432,
        database = dbName if dbName!=None else os.environ.get('USER')
    )
    return conn

def searchByGene(gene: str, connection: type(connect()))->str:
    cursor = connection.cursor() 
    cursor.execute(
        f"SELECT * FROM GENE WHERE GeneID = '{gene}';")
    output = cursor.fetchall() 
    return output


if __name__ == "__main__":
    conn = openConnection()
    #if the os getuser does not work in this function replace with your correct pc username
    #make sure to when using postgresql to use the database that is named after this username

    userInput = input('Enter GENE to search by: ').strip()

    output = searchByGene(gene=userInput, connection=conn)
    for lst in output:
        print(lst)

    conn.close()


 
