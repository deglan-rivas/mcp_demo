import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "demo-server",
  version: "1.0.0"
});

// Add an addition tool
// server.registerTool("add",
//   {
//     title: "Addition Tool",
//     description: "Add two numbers",
//     inputSchema: { a: z.number(), b: z.number() }
//   },
//   async ({ a, b }) => ({
//     content: [{ type: "text", text: String(a + b) }]
//   })
// );

// server.registerTool(
//     "calculate-bmi",
//     {
//       title: "BMI Calculator",
//       description: "Calculate Body Mass Index",
//       inputSchema: {
//         weightKg: z.number(),
//         heightM: z.number()
//       }
//     },
//     async ({ weightKg, heightM }) => ({
//       content: [{
//         type: "text",
//         text: String(weightKg / (heightM * heightM))
//       }]
//     })
//   );

// Add a dynamic greeting resource
// server.registerResource(
//   "greeting",
//   new ResourceTemplate("greeting://{name}", { list: undefined }),
//   { 
//     title: "Greeting Resource",      // Display name for UI
//     description: "Dynamic greeting generator"
//   },
//   async (uri, { name }) => ({
//     contents: [{
//       uri: uri.href,
//       text: `Hello, ${name}!`
//     }]
//   })
// );

// server.tool(
//     "fetch-weather",
//     "Tool to fetch the weather of a city",
//     {
//         city: z.string().describe("The city to fetch the weather for"),
//     },
//     async ({ city }) => {
//         return {
//             content: [
//                 {
//                     type: "text",
//                     text: `The weather in ${city} is sunny`
//                 }
//             ]
//         }
//     }
// )

// server.registerTool(
//     "fetch-weather",
//     {
//         title: "Fetch Weather Tool",
//         description: "Fetch weather based on city from local api",
//         inputSchema: {
//             city: z.string() // 👈 Esto SÍ es un ZodRawShape
//         }
//     },
//     async ({ city }) => {
//         return {
//             content: [
//                 {
//                     type: "text",
//                     text: `The weather in ${city} is sunny`
//                 }
//             ]
//         }
//     }
// )

// server.registerTool(
//     "fetch-weather",
//     {
//         title: "Fetch Weather Tool",
//         description: "Fetch weather based on city from local api",
//         inputSchema: z.object({
//             city: z.string()
//         })
//     },
//     async ({ city }) => {
//         return {
//             content: [
//                 {
//                     type: "text",
//                     text: `The weather in ${city} is sunny`
//                 }
//             ]
//         }
//     }
// );

// server.tool(
//     "fetch-weather",
//     "Tool to fetch the weather of a city",
//     {
//         city: z.string().describe("The city to fetch the weather for"),
//     },
//     async ({ city }) => {
//         return {
//             content: [
//                 {
//                     type: "text",
//                     text: `The weather in ${city} is sunny`
//                 }
//             ]
//         }
//     }
// )
server.tool(
    "fetch-weather-3",
    "Tool to fetch the weather of a city",
    // {
    //     city: z.string().describe("The city to fetch the weather for"),
    // },
    z.object({
        city: z.string().describe("The city to fetch the weather for"),
    }),
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

server.tool(
    "getMyCalendarDataByDate",
    {
        date: z.string().refine((val) => !isNaN(Date.parse(val)), {
            message: "Invalid date format. Please provide a valid date string.",
        }),
    },
    async ({ date }) => {
        return {
            content: [
                {
                    type: "text",
                    // text: JSON.stringify(await getMyCalendarDataByDate(date)),
                    text: (date),
                },
            ],
        };
    }
);

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);