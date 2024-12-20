#######################
## Dependências 
#######################

from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    dbname: str
    # environment: str
    host: str
    version: str
