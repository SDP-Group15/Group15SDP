import psycopg2 #db connection
import simplejson #json formatting

#for fishers_method:
import scipy
import decimal


#***main functions--------------------------------------------------------------------------------------------------***


def openConnection() -> type(tuple()):
    try:
        # Establish a connection to the database
        db_config = {
        'host': 'seniordesign.cyzdvv3sqno4.us-east-1.rds.amazonaws.com',
        'database': 'sdp152024',
        'user': 'postgres',
        'password': 'Uconn!2024'
        }

        #Connect to the database with config
        connectionInstance = psycopg2.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = connectionInstance.cursor()

        # print("Connected to the database!")
        if connectionInstance.status == psycopg2.extensions.STATUS_READY:
            return connectionInstance, cursor

    except Exception as e:
        print(f"Error: Unable to connect to the database - {e}")
        raise


#Use Case #1
#         gene is type str     return type is tuple data(list) and str (json str)
def searchByGene(gene: str) -> tuple[list,str]:
    connection, cursor = openConnection()

    query = """SELECT * FROM \"GENE\" WHERE \"GeneID\" = %s ORDER BY \"p_Value\" ASC;"""

    cursor.execute(query, (gene,))
        
    output = cursor.fetchall() 
    
    connection.close()
    return list(output), simplejson.dumps(output, indent=2)
#   **returns tuple access the elements 0 and 1 accordingly**


#Use Case #2
def searchByMesh(mesh: str) -> tuple[list,str]:
    connection, cursor = openConnection()

    query = """SELECT * FROM \"GENE\" WHERE \"MeSH\" LIKE %s ORDER BY \"p_Value\" ASC;"""

    cursor.execute(query, (mesh,))
    
    output = cursor.fetchall() 

    connection.close()
    return list(output), simplejson.dumps(output, indent=2)


#Use Case #3
def multipleByGene(geneList: list) ->  tuple[list,str]:
    connection, cursor = openConnection()

    query="""
    SELECT DISTINCT ARRAY_AGG("p_Value")AS pVals,A."MeSH",COUNT(DISTINCT "GeneID")AS numGenes,ARRAY_AGG("GeneID" ORDER BY "GeneID")AS listGenes
    FROM "GENE"AS A
    WHERE A."MeSH"IN(SELECT B."MeSH"FROM "GENE"AS B WHERE B."GeneID"=%s)
    GROUP BY A."MeSH"
    ORDER BY 4;"""

    output = []
    for gene in geneList:
        cursor.execute(query, (gene,))  #format for query,data
        rows = cursor.fetchall()

        for row in rows:
            #row formatting
            row = list(row)
            row[0]=multipleByGeneHelp(row[0])

            #add to output list
            output.append(row) #default is tuple

    connection.close()
    return output, simplejson.dumps(output, indent=2)



#***Search Related Functions----------------------------------------------------------------------------------------***


def listAllGene() -> list[str]:
    connection, cursor = openConnection()

    cursor.execute(
        """SELECT DISTINCT \"GeneID\" FROM \"GENE\" ORDER BY \"GeneID\" ASC;""")
    
    data = cursor.fetchall()

    connection.close()
    return [str(i[0]) for i in data]


def listAllMesh() -> list[str]:
    connection, cursor = openConnection()

    cursor.execute(
        """SELECT \"MeSH\" FROM \"GENE\" ORDER BY \"MeSH\" ASC;""") #can be changed to order by pval
    
    data = cursor.fetchall()
    
    connection.close()
    return [str(i[0]) for i in data]



#***helper functions------------------------------------------------------------------------------------------------***


def multipleByGeneHelp(curCol):
    size = len(curCol)

    if(size>1):
        #curcol is a list of multiple pvalues which we need to combine
        return fishers_method(curCol)
    else:
        #See sql query *array_agg: curCol is a list with just one element, return that element
        return curCol[0]
    

def fishers_method(p_values: list) -> str:
    decimal.getcontext().prec = 319

    #cast trickery frontloads decimal places otherwise float() would approximate to 0
    p_values_decimal = [decimal.Decimal(p) for p in p_values]
    try:
        combined_result = scipy.stats.combine_pvalues(p_values_decimal, method="fisher")

        #returns as string -- can be changed with 
        combined_p_value = str(float(combined_result[1]))
        return combined_p_value
    except:
        return str(0.0) #change this cast if changing to float
    

def show_tables():
    connection, cursor = openConnection()
    query = "SELECT column_name FROM information_schema.columns WHERE table_name = \"sdp152024\""
    cursor.execute("SELECT \"PMIDs\" FROM \"GENE\"")
    data = cursor.fetchall()
    connection.close()
    return data


#***simple funcitonality test---------------------------------------------------------------------------------------***
def test():
    pass
    #,Combined pVals,MeSH Term,Num Genes,Genes,All pVals




if __name__ == "__main__":
    # print(multipleByGene(geneList=[18,25]))
    # print(searchByMesh('Humans') )
    print(show_tables() )




