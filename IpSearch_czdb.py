from czdb.db_searcher import DbSearcher
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

database_path = "czdb/cz88_public_v4.czdb"
query_type = "BTREE"
# 从环境变量获取密钥
key = os.getenv("IPDB_API_KEY")
if not key:
    raise ValueError("IPDB_API_KEY 环境变量未配置，请在.env文件中设置该变量")
db_searcher = DbSearcher(database_path, query_type, key)


def czdb_search(ip: str):
    request = db_searcher.search(ip)
    result = [item.strip() for item in request.split("\t")]
    return result
