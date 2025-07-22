"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import aiohttp
from typing import TypedDict
import json

# Create an MCP server
mcp = FastMCP("Demo")

class FetchWeatherInput(TypedDict):
    city: str

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def fetch_weather_3(city: str) -> dict:
    """Tool to fetch the weather of a city"""

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json"
        ) as response:
            data = await response.json()

        if not data.get("results"):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No se encontró respuesta para la ciudad {city}"
                    }
                ]
            }

        first_result = data["results"][0]
        latitude = first_result["latitude"]
        longitude = first_result["longitude"]

        async with session.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&current=temperature_2m,precipitation,rain,is_day,relative_humidity_2m,snowfall"
        ) as weather_response:
            weather_data = await weather_response.json()

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(weather_data, indent=2)
                }
            ]
        }