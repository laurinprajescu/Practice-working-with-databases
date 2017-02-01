from database.mysql import MySQLDatabase
from settings import db_config

"""
Retrieve the settings from the
`db_config` dictionary to connect to
our database so we can instantiate our
MySQLDatabase object
"""
db = MySQLDatabase(db_config.get('db_name'),
                   db_config.get('user'),
                   db_config.get('pass'),
                   db_config.get('host'))

# Get all the available tables for
# our database annd print them out.
tables = db.get_available_tables()
print tables

# Get all the available columns for our
# articles table and print them out
columns = db.get_columns_for_table('people')
print columns

# Get all the records from
# the people table
results = db.select('people')
for row in results:
    print row

#Selecting records with named tuples
results = db.select('people' , columns=['id' , 'first_name'], named_tuples=True)
for row in results:
    print row.id , row.first_name

#complex queries using CONCAT Aand SUM
people = db.select('people' , columns=["CONCAT(first_name, ' ', second_name)" \
                                       " AS full_name", "SUM(amount)" \
                                       " AS total_spend"],
                   named_tuples=True, where="people.id=1",
                   join="orders ON people.id=orders.person_id")
for person in people:
    print person.full_name, "spent ", person.total_spend

#inserting an order
db.insert('orders' , person_id="2", amount="120.00")

#updating information
#updating a person
person = db.select('people', named_tuples=True)[0]
db.update('profiles', where="person_id=%s" % person.id,
          address="1a some street")

#deleting a record
person = db.select('people', named_tuples=True)[0]
db.delete('orders', person_id="=%s" % person.id, id="=1")

# retreive the first_name column and get the average amount spent where the person id = 1
people = db.select('people', columns=["first_name", "AVG(amount)"
                                      " AS average_spent"],
                   named_tuples=True, where="people.id=1",
                   join="orders ON people.id=orders.person_id")

# print the result
for person in people:
    print person.first_name, "spends" , person.average_spent
