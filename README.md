# LangChain Database Agent

A conversational AI agent that manages PostgreSQL database operations with human-in-the-loop approval for sensitive actions. Built with LangChain, LangGraph, and Google's Gemini model.

## Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Stevealila/LangChain-Database-Agent.git
cd LangChain-Database-Agent
```

2. **Create and activate virtual environment:**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Sync dependencies:**
```bash
uv sync
```

4. **Configure environment variables:**

Create a `.env` file with your PostgreSQL and Google AI credentials:
```env
PG_HOST=your_postgres_host
PG_DATABASE=your_database_name
PG_USER=your_username
PG_PASSWORD=your_password
GOOGLE_API_KEY=your_google_api_key
```

5. **Initialize the database:**

The agent will automatically create the `users` table on first run if it doesn't exist.

## Run

```bash
uv run main.py
```

## Example Usage

The agent understands natural language. Here are example interactions:

**List users:**
```
You: How many users are there?
You: Who are they?
You: List all users
```

**Add a user (requires approval):**
```
You: Can you add John Doe, john.doe@company.net?
```
The agent will pause and ask for approval before inserting the record.

**Delete a user:**
```
You: Remove John Doe, john.doe@company.net?
```

**Exit:**
```
You: exit
You: quit
You: q
```
