from jose import JWTError, jwt
# JOSE is a framework that is used to provide methods to securely transfer claims (such as authorization information) between parties.
from passlib.context import CryptContext
import datetime
import os

# JOSE stands for JavaScript Object Signing and Encryption


# run openssl rand -hex 32
# get key from dotenv
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(key):
    """
    Create a new access token
    :param user_id:
    :return:
    """
    payload = {
        "sub": key,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# What does this function do?

def getKey(token):
    """
    Verify the token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # jwt.decode() is in charge of decrypting information. For decryption, a key is used and an algorithm that will review the signature
        # of the information, if it is valid it will return the payload, if it isn't, it will return an error.
        # JWT is used to transfer information safely through JSON objects
    except JWTError:
        return None
    return payload.get("sub")
    # 'sub' typically stands for subject. sub is the name of the key and the value is the key.
    # .get() is used for dictinoaries and is used with keys to obtain the values.

# create access token for notion db and api key
# create a script to migrate existing database to encrypted one. 
# decryption at the time of storing stuff in guild_info is required