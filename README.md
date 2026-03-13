<p align="center">
  <img src="static/resources/logo.png" alt="Stocxsim Logo" width="180"/>
</p>

<h1 align="center">Stocxsim</h1>

<p align="center">
  A web-based stock trading simulation platform — practice algorithmic trading with virtual money using live market data.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/flask-2.3.3-lightgrey" alt="Flask"/>
  <img src="https://img.shields.io/badge/postgresql-12%2B-blue" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License"/>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

---

## Overview

**Stocxsim** is a full-stack paper trading simulator that connects to [Angel One (SmartAPI)](https://smartapi.angelbroking.com/) for real-time NSE/BSE market data. Users can sign up, fund a virtual account, place simulated buy/sell orders, and track their portfolio — all without risking real money.

---

## Features

| Feature | Description |
|---|---|
| 📈 Live Market Data | Real-time NSE/BSE prices via Angel One SmartAPI WebSocket |
| 💸 Virtual Trading | Place market orders (100% cash) or MTF orders (25% margin) |
| 📊 Technical Indicators | RSI (14-period) and EMA (9 & 20-period) for any stock |
| 📁 Portfolio Management | Track holdings, P&L, order history, and transactions |
| 👀 Watchlist | Subscribe to stocks for live price updates |
| 🔒 Authentication | Email-based sign-up with OTP verification |
| 🖥️ Real-time Dashboard | WebSocket-powered live ticker and interactive Plotly charts |
| 💰 Fund Management | Add or withdraw virtual funds from your account |

---

## Screenshots

<p align="center">
  <img src="static/resources/hero.png" alt="Dashboard" width="700"/>
</p>

<p align="center">
  <img src="static/resources/hero2.png" alt="Stock Detail" width="700"/>
</p>

---

## Tech Stack

### Backend
- **Python 3** — application language
- **Flask 2.3** — web framework
- **Flask-SocketIO 5.3** — WebSocket server for real-time price streaming
- **PostgreSQL 12+** — relational database (thread-pooled via `psycopg2`)
- **SmartAPI (smartapi-python)** — Angel One broker integration
- **NumPy** — RSI / EMA calculations
- **Plotly** — interactive charts

### Frontend
- **HTML5 / CSS3 / JavaScript**
- **Jinja2** — server-side templating
- **Socket.IO client** — live price updates in the browser

---

## Prerequisites

- Python **3.8+**
- PostgreSQL **12+**
- An [Angel One](https://www.angelone.in/) broker account (for live market data)
  - API Key, Client ID, Client Password
  - TOTP secret (for 2-FA login)
- A Gmail account (used to send OTP emails)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Stocxsim/stocxsim.git
cd stocxsim
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .env
source .env/bin/activate        # macOS / Linux
# .env\Scripts\activate         # Windows
```

> **Note:** The project uses `.env` as the virtual environment directory (as configured in `.gitignore`). This is different from the `.env` file convention used in some projects. Your environment variable file should be named `secrets.env` as described in the [Configuration](#configuration) section.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
# Create the database
createdb stocxsim

# Load the schema and seed data
psql stocxsim < resources/db.sql
psql stocxsim < resources/data.sql
```

---

## Configuration

Create a `secrets.env` file in the project root (this file is git-ignored):

```env
# Angel One broker credentials
API_KEY=your_angel_one_api_key
CLIENT_ID=your_angel_one_client_id
CLIENT_PASSWORD=your_angel_one_password
TOTP_SECRET=your_totp_2fa_secret

# PostgreSQL connection
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=stocxsim
POSTGRES_USER=postgres
DB_PASSWORD=your_postgres_password

# Gmail SMTP (for OTP emails)
SENDER_EMAIL=your_gmail_address@gmail.com
SENDER_PASSWORD=your_gmail_app_password   # Use a Gmail App Password, not your account password
```

> **Important:** Never commit `secrets.env` to version control. It is already listed in `.gitignore`.

---

## Running the Application

```bash
python main.py
```

The server starts on `http://0.0.0.0:5000`.

Open your browser and navigate to `http://localhost:5000`.

> `main.py` starts the Angel One WebSocket in a background daemon thread before launching the Flask-SocketIO server. `use_reloader=False` is set to prevent duplicate broker logins during development.

---

## Project Structure

```
stocxsim/
├── main.py                  # Entry point — starts Angel One WS + Flask server
├── app.py                   # Flask app factory, blueprint registration, SocketIO
├── config.py                # Loads credentials from secrets.env
├── extensions.py            # Shared Flask extensions (SocketIO instance)
├── requirements.txt         # Python dependencies
│
├── routes/                  # HTTP route handlers (blueprints)
│   ├── user_routes.py       # Login, signup, OTP, dashboard, funds
│   ├── stock_routes.py      # Stock search, detail, indicators
│   ├── trade_routes.py      # Place buy/sell orders
│   ├── holding_route.py     # Portfolio holdings
│   ├── order_route.py       # Order history
│   ├── watchlist_route.py   # Watchlist management
│   ├── transaction_route.py # Transaction history
│   └── profile_route.py     # User profile & password
│
├── service/                 # Business logic layer
│   ├── angle_service.py     # Angel One auth & startup
│   ├── trade_service.py     # Order placement, tax/fee calculations
│   ├── market_data_service.py # SmartAPI data fetching, historical data
│   ├── stockservice.py      # Stock search, RSI, EMA
│   ├── dashboard_service.py # Plotly chart generation
│   ├── userservice.py       # Auth, OTP generation/validation
│   ├── watchlist_service.py # Watchlist operations
│   ├── order_service.py     # Order retrieval
│   ├── transaction_service.py # Transaction recording
│   └── indicator_cache.py   # Cache for technical indicators
│
├── database/                # Data Access Objects (DAOs)
│   ├── connection.py        # Thread-safe PostgreSQL connection pool
│   ├── userdao.py           # User CRUD
│   ├── stockdao.py          # Stock queries
│   ├── order_dao.py         # Order persistence
│   ├── holding_dao.py       # Holdings CRUD, average price
│   ├── transaction_dao.py   # Transaction recording
│   └── watchlist_dao.py     # Watchlist management
│
├── modal/                   # Data models
│   ├── User.py              # User entity
│   ├── Stock.py             # Stock entity + indicators
│   ├── Order.py             # Order entity
│   ├── Holding.py           # Holding entity
│   └── History.py           # Trade history entity
│
├── websockets/
│   └── angle_ws.py          # Angel One SmartWebSocketV2 client
│
├── data/
│   └── live_data.py         # In-memory live price dictionaries
│
├── utils/
│   ├── tokens.py            # Index token constants (NIFTY, SENSEX, …)
│   └── market_time.py       # Market hours utilities
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── stock.html
│   ├── funds.html
│   ├── holding.html
│   ├── orders.html
│   ├── profile.html
│   └── watchlist.html
│
├── static/                  # Frontend assets (CSS, JS, images)
├── resources/               # Database SQL files and UI assets
└── datastructure/
    └── stack.py             # Utility data structure
```

---

## API Endpoints

### Authentication — `/login`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login/check` | Check if an email is already registered |
| `POST` | `/login/signup` | Register a new user |
| `POST` | `/login/send-otp` | Send OTP verification email |
| `POST` | `/login/verify-otp` | Verify OTP and create session |
| `GET` | `/login/dashboard` | Main dashboard (requires login) |
| `POST` | `/login/add-funds` | Deposit virtual money |
| `POST` | `/login/withdraw` | Withdraw virtual money |

### Trading — `/trade`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/trade/order` | Place a buy/sell order |

**Order payload:**

```json
{
  "symbol_token": "3045",
  "quantity": 10,
  "order_type": "market",
  "price": 0,
  "transaction_type": "buy"
}
```

`order_type` can be `"market"` (100% cash) or `"mtf"` (25% margin).

### Stocks — `/stocks`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/stocks/index/snapshot` | Live NIFTY / SENSEX prices |
| `GET` | `/stocks/search?q=<query>` | Full-text stock search |
| `GET` | `/stocks/detail/<token>` | Stock details, RSI, EMA chart |
| `POST` | `/stocks/subscribe/<token>` | Add to watchlist and subscribe |

### Holdings — `/holding`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/holding/list` | Full portfolio |
| `GET` | `/holding/data/<token>` | Single holding details |

### Orders — `/order`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/order/orders` | Order history (supports filters) |

### Watchlist — `/watchlist`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/watchlist/list` | Watchlist stocks with live prices |
| `POST` | `/watchlist/add` | Add a stock to watchlist |
| `DELETE` | `/watchlist/remove/<token>` | Remove from watchlist |

### Transactions — `/transactions`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/transactions/list` | Fund transaction history |

### Profile — `/profile`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/profile/details` | User profile page |
| `POST` | `/profile/update-password` | Change password |

---

## Database Schema

| Table | Purpose |
|-------|---------|
| `users` | Accounts (email, password hash, virtual balance) |
| `stocks` | Stock master data (token, name, exchange) |
| `orders` | Order records (user, symbol, quantity, price, type) |
| `holdings` | Current open positions (user, token, qty, avg buy price) |
| `transactions` | Fund deposit / withdrawal history |
| `user_stocks` | User ↔ watchlist mapping |

> Full schema is available in [`resources/db.sql`](resources/db.sql).

---

## Trading Logic

### Order Types

| Type | Description | Cost |
|------|-------------|------|
| **Market** | Executed at live LTP | Full trade value debited |
| **MTF** | Margin Trading Facility | 25% upfront; 75% simulated loan |

### Fee Structure

| Fee | Rate |
|-----|------|
| Buy tax | 0.0190% of trade value |
| Sell tax | 0.1039% of trade value |
| DP charge (per sell) | ₹15.93 (fixed) |

### Technical Indicators

- **RSI (14-period):** Momentum oscillator — >70 overbought, <30 oversold.
- **EMA-9 / EMA-20:** Exponential moving averages used for crossover signals.

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

Please make sure your code follows the existing style and does not include any credentials or `secrets.env` files.
