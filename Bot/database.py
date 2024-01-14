from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy is a library that uses Object Relational Mapping (ORM) to interact with databases and treat columns as classes and rows as objects.
# create_engine is used to make a connection with the database, it takes database's details and returns an engine instance.
# sessionmaker is a factory that produces new Session objects when called.

SQLALCHEMY_DATABASE = 'sqlite:///database/clients.sqlite' # This actually is the path for the file with the database, and communication will be established later.

engine = create_engine(SQLALCHEMY_DATABASE, connect_args={'check_same_thread': False})

# What does sessionmaker do?
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # It generates new Session objects.

Base = declarative_base() # factory function that creates a base class for declarative class definitions.

# What is the definition of a factory function? A factory function is in charge of RETURNING functions or objects. It makes instances of objects or generates functions.

# What does sessionmaker do? Sessions are understood to be the period of interaction between the user and the application.
# What does the library sqlalchemy is used for?

# Does this bot require to use JAVASCRIPT and SQL or does notionAPI require them?
# The interaction with NOTION requires HTTP requests. HTTP stands for Hypertext Transfer Protocol. It is a client-server protocol used for transferring data
# over the internet. HTTP defines several types of requests known as methods:
# - GET
# - POST
# - PUT
# - DELETE
# - HEAD
# - PATCH
# A request consists of a general structure defined as follows:
# Sending a request: When typing a URL into a browser or when an application makes a request to an API, and HTTP request is sent to the server hosting the URL or the API.
# Recieving the request: The server processes the response and sends back and HTTP response. The response includes the status code, header and the a body containing the requested data.

# What does echo do for the engines? echo parameter in create_engine() will output all the SQL statements that get executed.
# What does the connect_args do? This parameter allows for connection from multiple threads to the same database. By default, there is an imposition that doesn't allow such operation.