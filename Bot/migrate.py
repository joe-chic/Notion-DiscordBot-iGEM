from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine) # The engine is necessary to establish a connection between the SQLAlchemy and the database.

# >>> This application happens when using MetaData() function ::: On the metadata object, the create_all() function is used to issue different queries that will check the existence of each individual
# table, if not found it will issue CREATE statements.

# create_all() simply creates the table based on how it was defined in the metadata object, it is not populated with values yet.
# To insert data into these type of tables, one needs to use session objects and methods to create instances to the database. 
# For example, one can use the session.add() [add instances to the session] or the session.commit() [persist changes to the database] methods


# What does the metadata option is about? 

# What do database and models do ?