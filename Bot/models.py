import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from database import Base

try:
    PREFIX = os.environ["PREFIX"]
except:
    PREFIX = "*"

class Clients(Base):
    __tablename__ = 'URI Clients'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    guild_id = Column(Integer, index=True, nullable=False)
    notion_api_key = Column(String, nullable=False)
    notion_db_id = Column(String, nullable=False)
    tag = Column(Boolean, default=False)
    prefix = Column(String, default=PREFIX)

    def __init__(self, guild_id, notion_api_key, notion_db_id, tag, prefix=PREFIX):
        self.guild_id = guild_id
        self.notion_api_key = notion_api_key
        self.notion_db_id = notion_db_id
        self.tag = tag
        self.prefix = prefix

    @property # This is a built-in decorator for the property(), it allows methods to be treated as attributes, 
    # as well as for defining getters, setters and deleters better. 
    def serialize(self):
        return {
            "guild_id": self.guild_id,
            "notion_api_key": self.notion_api_key,
            "notion_db_id": self.notion_db_id,
            "tag": self.tag,
            "prefix": self.prefix,
        }

# What is the purpose of using @ ? Decorators. 
    
# The index parameter is in charge of indexing a column for improving the retrieval of data.
# The nullable parameter is for specifying whether the column can accept null values.
# The deafult parameter is for specifying a default value if none is provided.
    
class List(Base):
    __tablename__ = 'List Clients'
    id = Column(Integer,primary_key=True, index=True)
    guild_id = Column(String, nullable=False)
    notion_api_key = Column(String,nullable=False)
    notion_db_id = Column(String, nullable=False)
    prefix = Column(String,default=PREFIX)

    def __init__(self, GUILD_ID, NOTION_API_ID, NOTION_DB_ID, preFIX):
        self.guild_id = GUILD_ID 
        self.notion_api_key = NOTION_API_ID
        self.notion_db_id = NOTION_DB_ID
        self.prefix = preFIX

    @property 
    def serialize(self):
        return {
            "guild_id": self.guild_id,
            "notion_api_key": self.notion_api_key,
            "notion_db_id": self.notion_db_id,
            "prefix": self.prefix,
        }
    