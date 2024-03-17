# Roshaun Marshall
# 620154268

from flask import Flask, make_response
import mysql.connector

SERVER_NAME = "localhost"
USERNAME = "root"
PASSWORD = ""


def connectSql(database_name):
    return mysql.connector.connect( host = SERVER_NAME, user = USERNAME , password = PASSWORD, database = database_name)

def retunQueryResults(query):
    connection = connectSql("customer_db")
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        retval  = cursor.fetchall()
    except mysql.connector.Error as e:
        retval = make_response(f"Query Execution Error : {e}", 400)
    finally:
        cursor.close()
        connection.close()

    return retval
    
    

def executeQuery(query):
    connection = connectSql("customer_db")
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        retval  =  make_response({"success" : "Student added"}, 201)
    except mysql.connector.Error as e:
        retval = make_response(f"Query Execution Error : {e}", 400)
    finally:
        connection.commit()
        cursor.close()
        connection.close()
    
    return retval
    
    
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>CUSTOMER API</h1>"


# a
@app.route('/customers', methods=['GET'])
def getCustomers():
   customer_attributes = ("customer_id", "gender", "age", "annual_income", "spending_score", "profession", "work_experience", "family_size")
   customers = retunQueryResults("select * from customer")
   customer_retval = []
   for customer in customers:
       customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval

# b
@app.route('/customer/<customer_id>', methods=['GET'])
def getCustomerById(customer_id):
   customer_attributes = ("customer_id", "gender", "age", "annual_income", "spending_score", "profession", "work_experience", "family_size")
   customer = retunQueryResults(f"select * from customer where customer_id={customer_id}")[0]
   customer_retval = []
   customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval

# c
@app.route('/add_customer', methods=['POST'])
def addCustomer():
    return "<h1>Add Customer</h1>"

# d
@app.route('/update_profession/<customer_id>', methods=['PUT'])
def updateCustomerProfession():
    return "<h1>Customer Profession</h1>"

# e
@app.route('/highest_income_report', methods=['GET'])
def getHighestIncome():

   customer_attributes = ("customer_id", "annual_income", "profession")
   customers = retunQueryResults("select customer_id, annual_income, profession from customer order by annual_income desc limit 1;")
   customer_retval = []
   for customer in customers:
       customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval

# f
@app.route('/total_income_report', methods=['GET'])
def getTotalIncome():

   customer_attributes = ( "total_income", "profession")
   customers = retunQueryResults("select sum(annual_income), profession from customer group by profession;")
   customer_retval = []
   for customer in customers:
       customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval

# g
@app.route('/average_work_experience', methods=['GET'])
def getAvgExperience():
   customer_attributes = ( "work_experience", "profession")
   customers = retunQueryResults("select avg(work_experience), profession from customer group by profession;")
   customer_retval = []
   for customer in customers:
       customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval

# h
@app.route('/average_spending_score/<profession>', methods=['GET'])
def getSpendingScore(profession):
   customer_attributes = ( "spending_score", "gender")
   customers = retunQueryResults(f"select gender, avg(spending_score) from customer where profession ='{profession}' group by gender;")
   customer_retval = []
   for customer in customers:
       customer_retval.append({key:value for key,value in zip(customer_attributes, customer)})

   return customer_retval


if __name__ == '__main__':
    app.run(port="8000", debug=True)