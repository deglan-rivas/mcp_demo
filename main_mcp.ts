import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "demo-server",
  version: "1.0.0"
});

server.registerTool(
    "fetch-weather-mcp-origin",
    // "Tool to fetch the weather of a city",
    // z.object({
    //     city: z.string().describe("The city to fetch the weather for"),
    // }),
    {
        title: "Addition Tool",
        description: "Add two numbers",
        inputSchema: { city: z.string() }
    },
    async ({ city }) => {
        const response = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=10&language=en&format=json`)
        const data = await response.json()

        if (data.length === 0) {
            return {
                content: [
                    {
                        type: "text",
                        text: `no se encontró respuesta para la ciudad ${city}`
                    }
                ]
            }
        }

        const { latitude, longitude } = data.results[0]

        const weatherResponse = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m&current=temperature_2m,precipitation,rain,is_day,relative_humidity_2m,snowfall`)
        const weatherData= await weatherResponse.json()

        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(weatherData, null, 2)
                }
            ]
        }
    }
)

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);