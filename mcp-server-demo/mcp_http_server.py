from fastapi import FastAPI, Request, HTTPException
from mcp.server.fastmcp import FastMCP
import aiohttp
import uvicorn
import json
import asyncio
import inspect

app = FastAPI()
mcp = FastMCP("Demo")

# Diccionario para mantener registro de las herramientas
registered_tools = {}

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
async def fetch_weather_3(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json"
        ) as response:
            data = await response.json()

        if not data.get("results"):
            return {
                "content": [
                    {"type": "text", "text": f"No se encontró respuesta para {city}"}
                ]
            }

        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]

        async with session.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&current=temperature_2m,precipitation"
        ) as weather_response:
            weather_data = await weather_response.json()

        return {
            "content": [
                {"type": "text", "text": json.dumps(weather_data, indent=2)}
            ]
        }

# Función para registrar herramientas manualmente
def register_tool(name: str, func):
    registered_tools[name] = func

# Registrar las herramientas
register_tool("add", add)
register_tool("fetch_weather_3", fetch_weather_3)

@app.post("/mcp")
async def call_tool(request: Request):
    try:
        body = await request.json()
        tool_name = body.get("tool")
        input_data = body.get("input", {})
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name is required")
        
        # Buscar la herramienta en nuestro registro
        tool_fn = registered_tools.get(tool_name)
        if tool_fn is None:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        # Ejecutar la herramienta
        if inspect.iscoroutinefunction(tool_fn):
            # Si es una función asíncrona
            result = await tool_fn(**input_data)
        else:
            # Si es una función síncrona
            result = tool_fn(**input_data)
        
        return {"success": True, "result": result}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/tools")
async def list_tools():
    """Endpoint para listar todas las herramientas disponibles"""
    tools_info = {}
    for name, func in registered_tools.items():
        # Obtener información sobre los parámetros
        sig = inspect.signature(func)
        params = {}
        for param_name, param in sig.parameters.items():
            params[param_name] = {
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "any",
                "required": param.default == inspect.Parameter.empty
            }
        
        tools_info[name] = {
            "parameters": params,
            "is_async": inspect.iscoroutinefunction(func)
        }
    
    return {"tools": tools_info}

# Alternativa usando introspección del objeto FastMCP (si funciona)
@app.post("/mcp_alt")
async def call_tool_alt(request: Request):
    try:
        body = await request.json()
        tool_name = body.get("tool")
        input_data = body.get("input", {})
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name is required")
        
        # Intentar acceder a las herramientas a través del servidor MCP
        # Esto puede variar dependiendo de la implementación exacta de FastMCP
        if hasattr(mcp, '_tools'):
            tool_fn = mcp._tools.get(tool_name)
        elif hasattr(mcp, 'server') and hasattr(mcp.server, 'tools'):
            tool_fn = mcp.server.tools.get(tool_name)
        else:
            # Fallback al registro manual
            tool_fn = registered_tools.get(tool_name)
        
        if tool_fn is None:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        # Ejecutar la herramienta
        if hasattr(tool_fn, 'run'):
            # Si es un objeto Tool con método run
            result = await tool_fn.run(input_data)
        elif inspect.iscoroutinefunction(tool_fn):
            result = await tool_fn(**input_data)
        else:
            result = tool_fn(**input_data)
        
        return {"success": True, "result": result}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run("mcp_http_server:app", host="0.0.0.0", port=8000, reload=True)