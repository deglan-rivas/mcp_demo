from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import oracledb

oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient_19_27")
app = FastAPI()

# Hardcoded Oracle connection string
ORACLE_DSN = "eleccia/desarrollo@oda-x8-2ha-vm1:1521/OPEXTDESA"

# Input schema
class QueryRequest(BaseModel):
    query: str

@app.post("/execute-query")
async def execute_query(request: QueryRequest):
    try:
        with oracledb.connect(ORACLE_DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(request.query)
                # Try to fetch results (e.g., for SELECTs)
                try:
                    results = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    return {
                        "columns": columns,
                        "rows": results
                    }
                except oracledb.InterfaceError:
                    # No results to fetch (e.g., INSERT/UPDATE)
                    return {"message": "Query executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
