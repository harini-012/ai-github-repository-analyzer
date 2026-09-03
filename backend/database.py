import oracledb
from config import Config

oracledb.init_oracle_client(
    lib_dir=r"C:\app\oracle\product\11.2.0\server\bin"
)

def get_db_connection():
    return oracledb.connect(
        user=Config.ORACLE_USER,
        password=Config.ORACLE_PASSWORD,
        dsn=Config.ORACLE_DSN
    )