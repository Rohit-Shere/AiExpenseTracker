# AI Expense Tracker

A full-stack expense tracking application with AI-powered chatbot assistance, built with FastAPI backend and vanilla JavaScript frontend.

## Features

### Backend (FastAPI)
- RESTful API for expense management
- AI chatbot integration using Google Gemini
- SQLite database for expenses and chat memory
- Support for date filtering and category-based queries
- Multiple visualization data endpoints

### Frontend
- **Home Page**: 
  - Latest expense display
  - Category-wise expense cards
  - Interactive AI chatbot for adding/querying expenses
  
- **Dashboard Page**:
  - Summary cards (Total, Average Daily, Top Category, Transaction Count)
  - Donut chart for category distribution
  - Line chart for daily spending trends
  - Bar charts for monthly and category spending
  - Dynamic duration filters (1 month, 3 months, 6 months, all time)
  - CSV data export functionality

## Tech Stack

- **Backend**: FastAPI, SQLite, LangChain, Google Gemini AI
- **Frontend**: Vanilla JavaScript, HTML5, CSS3, Chart.js
- **Database**: SQLite (expense.db, memory.db)

## Setup Instructions

### Backend Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   The server will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start a local HTTP server (choose one):
   
   **Python:**
   ```bash
   python -m http.server 3000
   ```
   
   **Node.js:**
   ```bash
   npx http-server -p 3000
   ```
   
   **VS Code Live Server:**
   - Install "Live Server" extension
   - Right-click on `index.html` and select "Open with Live Server"

3. Access the application:
   - Home: `http://localhost:3000/index.html`
   - Dashboard: `http://localhost:3000/dashboard.html`

### Configuration

Update the API URL and user ID in frontend JavaScript files if needed:

**frontend/app.js** and **frontend/dashboard.js**:
```javascript
const API_BASE_URL = 'http://localhost:8000';
const USER_ID = 'user1'; // Change this to use different users
```

## Usage

### Adding Expenses

Use the chatbot on the home page:
- "I spent ₹500 on groceries today"
- "Add ₹1200 for transport"
- "Bought a T-shirt for ₹800"
- "Paid ₹2000 for electricity bill"

### Querying Expenses

Ask the chatbot:
- "Show me my expenses this month"
- "What did I spend on food?"
- "How much did I spend last week?"
- "List all my transport expenses"

### Dashboard

1. Select a duration from the dropdown (Last Month, 3 Months, 6 Months, All Time)
2. View visualizations that update dynamically
3. Click "Export Data" to download expenses as CSV

## API Endpoints

### Expenses
- `GET /expenses?user_id={user_id}` - Get all expenses
- `GET /expenses?user_id={user_id}&start_date={date}&end_date={date}` - Get expenses between dates
- `GET /expenses/latest?user_id={user_id}` - Get latest expense
- `GET /expenses/category-summary?user_id={user_id}` - Get category summary
- `GET /expenses/daily-spending?user_id={user_id}` - Get daily spending data
- `GET /expenses/monthly-spending?user_id={user_id}` - Get monthly spending data

### Chatbot
- `POST /chatbot/{user_id}` - Send message to chatbot
  ```json
  {
    "user_input": "I spent ₹500 on groceries"
  }
  ```

### Memory
- `GET /memory/{user_id}` - Get chat history

## Database Schema

### Expenses Table
- `id` (INTEGER PRIMARY KEY)
- `user_id` (TEXT)
- `date` (TEXT)
- `category` (TEXT)
- `amount` (REAL)
- `description` (TEXT)

### Memory Table
- `id` (INTEGER PRIMARY KEY)
- `user_id` (TEXT)
- `role` (TEXT) - 'user' or 'assistant'
- `memory_text` (TEXT)
- `timestamp` (DATETIME)

## Design

The frontend features a modern dark theme with vibrant gradient colors, optimized for users aged teens to 30s. The UI is fully responsive and works seamlessly on desktop and mobile devices.

## Development

### Backend Structure
```
backend/
├── main.py          # FastAPI application and routes
├── expense.py       # Expense database operations
├── memory.py        # Chat memory operations
├── chatbot.py       # AI chatbot service
└── visuals.py       # Visualization utilities
```

### Frontend Structure
```
frontend/
├── index.html       # Home page
├── dashboard.html   # Dashboard page
├── app.js           # Home page logic
├── dashboard.js     # Dashboard logic
├── styles.css       # Global styles
└── README.md        # Frontend documentation
```

## Notes

- The application uses SQLite databases stored in the `database/` directory
- Make sure CORS is properly configured in `backend/main.py` for your frontend URL
- The chatbot uses Google Gemini API - ensure you have a valid API key
- User IDs are strings - you can implement user authentication later

## License

MIT

