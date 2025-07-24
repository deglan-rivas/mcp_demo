# MCP Server Demo

Este proyecto fue clonado a partir del SDK oficial de MCP Server para Python:  
🔗 https://github.com/modelcontextprotocol/python-sdk

## Instalación

Usa los siguientes comandos para instalar las dependencias:

```bash
git clone https://github.com/deglan-rivas/mcp_demo.git
cd mcp-server-demo
uv sync
````


## A. Probar como agente en VSCode

1. Abre la configuración de usuario en formato JSON:
   *Ctrl + Shift + P* → `Preferences: Open User Settings (JSON)`

2. Copia el siguiente contenido en el archivo `settings.json`, actualizando la ruta local del `"command"` y del archivo `run_mcp.sh` según tu entorno (usa `pwd` para obtener la ruta):

```json
{
  "github.copilot.enable": {
    "*": false,
    "plaintext": false,
    "markdown": false,
    "scminput": false
  },
  "mcp": {
    "servers": {
      "python-mcp": {
        "type": "stdio",
        "command": "/home/deglanrivas/Escritorio/JNE_DCGI/mcp_demo/mcp-server-demo/run_mcp.sh",
        "args": []
      }
    }
  }
}
```

3. Activa la opción **Chat > Agent > Enabled** en los *User Settings* de Copilot.

4. Abre el chat con la opción **Open Chat** (*Ctrl + Alt + I* o *Ctrl + Alt + B*).

5. Selecciona el modo *ask a modo agent*, marca los **Tools requeridos**, y haz una pregunta relacionada.


## B. Probar como bloque en n8n (VSCode Ports o localhost)

1. Expón el puerto `5678` de n8n mediante **VSCode Ports** y cámbialo de *Private* a *Public*.

2. Ejecuta el siguiente comando para levantar el contenedor Docker de n8n (modifica `EDITOR_BASE_URL` y `WEBHOOK_URL` con la URL del túnel de VSCode Ports):

```bash
docker run -e N8N_SECURE_COOKIE=false \
  -e EDITOR_BASE_URL=https://wr8n3j80-5678.brs.devtunnels.ms/ \
  -e WEBHOOK_URL=https://wr8n3j80-5678.brs.devtunnels.ms/ \
  -e N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true \
  -e N8N_RUNNERS_ENABLED=true \
  -it --rm --name n8n -p 5678:5678 \
  -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

3. En n8n, crea un bloque del tipo `"HTTP Request Tool"` conectado a un nodo `"AI Agent"`.

### Ejemplo de bloque HTTP Request Tool

```json
{
  "parameters": {
    "toolDescription": "Makes an HTTP request and returns the response data when user ask about weather",
    "method": "POST",
    "url": "https://wr8n3j80-8000.brs.devtunnels.ms/mcp",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "{\n  \"tool\": \"fetch_weather_3\",\n  \"input\": {\n    \"city\": \"Lima\"\n  }\n}\n",
    "options": {}
  },
  "type": "n8n-nodes-base.httpRequestTool",
  "typeVersion": 4.2,
  "position": [
    480,
    384
  ],
  "id": "a6c41288-2973-40d1-83f1-ce772d6b1f53",
  "name": "HTTP Request"
}
```

Puedes conectarlo como **Tool** al bloque `AI Agent` y realizar preguntas como:

> *"¿Cuál es la humedad relativa de Berlín, hay precipitaciones o el cielo está despejado?"*
