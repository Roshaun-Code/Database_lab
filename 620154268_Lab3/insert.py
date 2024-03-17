import csv

CSV_FILENAME = "Customers.csv"
SQL_FILENAME = "create.sql"

def createInsertQueries(filename):
    insert_header = "INSERT IGNORE INTO customer (customer_id, gender, age, annual_income, spending_score, profession, work_experience, family_size)\nVALUES"
    insert_values = ""
    try:
        with open(filename) as data:
            customer_data = csv.reader(data)
            next(customer_data)
            for customer in customer_data :
                insert_values +=  ",\n" + f"('{customer[0]}','{customer[1]}',{customer[2]},{customer[3]},{customer[4]},'{customer[5]}',{customer[6]},{customer[7]})"

        return insert_header + insert_values[1:] + ";"
    except FileNotFoundError:
        return ""


def createSqlFile(csv_filename, sql_filename) :
    insert_queries = createInsertQueries(csv_filename);
    
    if(insert_queries ==""):
        print("FileNotFound: please place file in folder")
    else:
        section_buffer = "\n\n"
        create_table = """CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    gender VARCHAR(6) NOT NULL,
    age INT NOT NULL,
    annual_income INT NOT NULL,
    spending_score INT NOT NULL,
    profession VARCHAR(255) NOT NULL,
    work_experience INT NOT NULL,
    family_size INT NOT NULL
);"""
        sql_code = section_buffer + create_table + section_buffer + insert_queries


        with open(sql_filename, "w") as sql:
            sql.write(sql_code)
            print("Success: "+sql_filename+" has been created")
   


createSqlFile(CSV_FILENAME, SQL_FILENAME)