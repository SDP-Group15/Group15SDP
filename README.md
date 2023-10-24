# backendDemoCode
Install postgreSQL locally and use the database labeled after your pc username for this code.

Create table SQL command:
CREATE TABLE GENE(GeneID INT NOT NULL, MeSH TEXT NOT NULL, p_Value TEXT, Enrich NUMERIC, PMIDs TEXT);

\copy GENE FROM '/path/to/csv/combined_testset.csv' DELIMITER ',' CSV;

--change 'path/to/csv' to the where you have the test data stored.

