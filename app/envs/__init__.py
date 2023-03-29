from app.envs.clients import ClientsEnv
from app.envs.db import DBEnv


class _Env:
    db: DBEnv = DBEnv()
    client: ClientsEnv = ClientsEnv


Env = _Env()
