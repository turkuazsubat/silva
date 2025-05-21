# Silva – Asynchronous TCP-Based Chatbot Application

**Silva** is a modular chatbot built with Python that operates over an asynchronous TCP connection. It responds to user messages and, when needed, fetches live data (such as weather or exchange rates) from external APIs. Thanks to its asynchronous architecture, it can serve multiple users simultaneously and execute background tasks. In future versions, a language model will be integrated to provide smarter, more dynamic AI-driven responses.

---

## Features

- Asynchronous TCP client-server architecture
- Multi-client support with concurrent communication
- Rich set of predefined responses (100+ entries in `response.py`)
- City-specific weather queries
- Real-time currency exchange rates
- Background task handling (data is fetched while chat continues)
- Simple terminal client for easy testing
- Extensible architecture for AI language model integration

---

## Technologies Used

| Technology   | Description                            |
|--------------|----------------------------------------|
| Python 3.10+ | Programming language                   |
| asyncio      | Asynchronous task and connection management |
| aiohttp      | Asynchronous API requests              |
| TCP Socket   | Base communication protocol            |
| JSON APIs    | Weather and exchange rate data sources |

---

## File Structure

```
silva/
├── server.py          # Asynchronous TCP server code
├── client.py          # Basic terminal client
├── response.py        # Dictionary with 100+ predefined responses
├── bot_utils.py       # Weather query helper module
├── doviz.py           # Currency exchange helper module
└── README.md          # Project documentation
```

---

## Installation

Install required dependencies before running the project:

```bash
pip install aiohttp
```

---

## Running the Application

**Start the server:**

```bash
python server.py
```

**Start the client (in a separate terminal):**

```bash
python client.py
```

---

## Example Usage

```
User: hello
Bot: Hello, how can I help you?

User: weather in izmir
Bot: Fetching weather for Izmir...
Bot: Izmir: Partly cloudy, 18°C

User: exchange
Bot: USD/TRY: 32.10 - EUR/TRY: 35.25
```

---

## How It Works

1. **TCP connection is established:** Each client connects directly to the server via TCP.
2. **Messages are parsed:** Incoming messages are checked against predefined responses in `response.py`.
3. **Task delegation:** Static replies are returned instantly; dynamic queries (weather, exchange) are routed to appropriate modules.
4. **API calls are run in the background:** `bot_utils.py` and `doviz.py` handle external requests using async functions.
5. **Tasks are combined with `asyncio.gather`:** Results are collected and sent back to the client.
6. **Chat flow continues uninterrupted:** While waiting for data, the user may continue chatting.

---

## Future Development

The current architecture allows easy integration of an AI-powered language model. Instead of relying solely on static replies from `response.py`, Silva will eventually support natural language processing and dynamically generate intelligent responses—transforming it into a true conversational agent.

---

## Internationalization

This project currently supports only Turkish.  
English language support is coming soon.

---
