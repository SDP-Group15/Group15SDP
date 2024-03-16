from psycopg2 import connect
import csv
import math
import scipy
from decimal import Decimal, getcontext


def openConnection(dbName: str = None) -> type(connect()):
    conn = connect(
            host='seniordesign.cyzdvv3sqno4.us-east-1.rds.amazonaws.com',
            port='5432',
            database='sdp152024' if not dbName else dbName,
            user='postgres',
            password='Uconn!2024'
    )
    return conn


def searchByGene(gene: str, connection: type(connect()), page: int, per_page: int) -> dict:
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    cursor.execute(
        f"""
        SELECT *
        FROM "GENE"
        WHERE "GeneID" = '{gene}'
        ORDER BY "p_Value" ASC
        LIMIT {per_page} OFFSET {offset};
        """
    )

    # Fetching the results for the current page
    output = cursor.fetchall()

    # Fetching the total number of records for pagination
    cursor.execute(f"SELECT COUNT(*) FROM \"GENE\" WHERE \"GeneID\" = '{gene}'")
    total_records = cursor.fetchone()[0]

    # Constructing the response
    results = [{
        'id': row[0],
        'description': row[1],
        'pVal': row[2],
        'enrichment': row[3],
        'references': row[4].split(',') if row[4] else []
    } for row in output]

    return {
        'results': results,
        'total': total_records,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_records / per_page)
    }


def searchByMesh(mesh: str, connection: type(connect()), page: int, per_page: int) -> dict:
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    # Adjusted query using the 'MeSH' column
    cursor.execute("""SELECT * FROM "GENE" WHERE "MeSH" = %s ORDER BY "p_Value" ASC LIMIT %s OFFSET %s;""",
                   (mesh, per_page, offset) )

    output = cursor.fetchall()

    # Counting records for pagination
    cursor.execute("SELECT COUNT(*) FROM \"GENE\" WHERE \"MeSH\" LIKE %s", (f"%{mesh}%",))
    total_records = cursor.fetchone()[0]

    results = [{
        'id': row[0],
        'description': row[1],
        'pVal': row[2],
        'enrichment': row[3],
        'references': row[4].split(',') if row[4] else []
    } for row in output]

    return {
        'results': results,
        'total': total_records,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_records / per_page)
    }


def searchByGeneIDs(gene_ids_str: str, connection: type(connect()), page: int = 0, per_page: int = 0) -> dict:
    cursor = connection.cursor()
    offset = (page - 1) * per_page

    # Process input string to create a list of gene IDs
    geneList = [x.strip() for x in gene_ids_str.split(',')]
    geneString = "("
    for gene in geneList:
        geneString += "'" + gene + "'" + ","
    geneString = geneString[:-1]
    geneString += ")"

    # Constructing the query
    query="""
    SELECT DISTINCT ARRAY_AGG("p_Value")AS pVals,A."MeSH",COUNT(DISTINCT "GeneID")AS numGenes,ARRAY_AGG("GeneID" ORDER BY "GeneID")AS listGenes
    FROM "GENE"AS A
    WHERE A."MeSH"IN(SELECT B."MeSH"FROM "GENE"AS B WHERE B."GeneID" = %s)
    GROUP BY A."MeSH"
    ORDER BY 4
    ASC LIMIT %s OFFSET %s;"""

    cursor.execute(query, (gene, per_page, offset) )
    queryResult = cursor.fetchall()
    output = []
    for row in queryResult:
        row = list(row)
        row[0] = multipleByGeneHelp(row[0])
        
        i = 0
        ids = ""
        for id in row[3]:
            ids += str(id) +","
            i += 1
            if i > 4:
                break
        ids+= "..."
        row[3] = ids

        output.append(row)

    # Counting records for pagination
    cursor.execute("SELECT COUNT(*) FROM \"GENE\" WHERE \"GeneID\" IN %s", (tuple(geneList),))
    total_records = cursor.fetchone()[0]

    # Constructing results
    results = [{
        'combined_pval': row[0],
        'mesh': row[1],
        'num_genes': row[2],
        'genes': row[3]
    } for row in output]

    return {
        'results': results,
        'total': total_records,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_records / per_page)
    }


def multipleByGeneHelp(curCol):
    size = len(curCol)

    if(size>1):
        #curcol is a list of multiple pvalues which we need to combine
        return fishers_method(curCol)
    else:
        #See sql query *array_agg: curCol is a list with just one element, return that element
        return curCol[0]
    

def fishers_method(p_values: list) -> str:
    #Precision set based on smallest value i.e. ~1.0e-319
    getcontext().prec = 319

    #cast trickery frontloads decimal places otherwise it would approximate to 0
    p_values_decimal = [Decimal(p) for p in p_values]
    p_values_float = [float(p) for p in p_values_decimal]
    try:
        combined_result = scipy.stats.combine_pvalues(p_values_float, method="fisher")

        #returns as string -- can be changed with 
        combined_p_value = str(float(combined_result[1]))
        return combined_p_value
    except Exception as e:
        return str(0.0) #change this cast if changing to float
    

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