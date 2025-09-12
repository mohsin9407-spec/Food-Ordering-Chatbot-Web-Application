Project: Food Ordering Chatbot Web Application (Flask)

## Overview

A lightweight Flask-based demo application that provides a simple food-ordering chatbot UI and API. Users can log in, place orders by messaging the chatbot, check order status, simulate delays/ready states, and cancel orders. Prices are shown in Indian Rupees (₹).

## Files

* app.py            - Main Flask application (routes, in-memory data).
* templates/        - HTML templates (login.html, index.html expected).
* static/           - Static assets (JS, CSS, images) used by the UI.

## Features

* Simple username/password login (demo users in code).
* Chat-style API (/chat) that accepts JSON messages and returns bot replies.
* In-memory food menu with prices (₹).
* Order lifecycle simulation: preparing, delayed, ready, cancel.
* Basic brute-force protection on login (3 attempts -> 3 minute lock).

## Demo credentials

* Username: ***  Password: ***
* Username: customer Password: ***

## Requirements

* Python 3.8+
* Flask

## Installation

1. Create a virtual environment (recommended):

   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   venv\Scripts\activate     # Windows

2. Install dependencies:

   pip install Flask

3. Ensure the project structure includes the templates and static folders.

## Running locally

From the project root (where app.py is):

export FLASK\_APP=app.py       # macOS / Linux
set FLASK\_APP=app.py          # Windows
flask run                     # or `python app.py` to run with debug=True

The app listens on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default.

## Environment / Config

* app.secret\_key is set directly in app.py for demo. For production, set a secure secret via an environment variable and never commit it to source control.

## How the Chat API works

Endpoint: POST /chat
Content-Type: application/json

Request example:
{
"message": "I want pizza"
}

Response example:
{
"reply": "✅ Added Pizza to your order. Current total: ₹299.00."
}

Supported user messages (examples):

* Ordering items by mentioning menu keywords: pizza, burger, fries, pasta, salad, drink, dessert
* "status" or "track" — check current order status
* "cancel" or "delete" — cancel active order
* "rain" or "delay" — simulate a delay (order status becomes "delayed")
* "ready" — mark order ready

## Notes & Limitations

* All data (users, menu, order status) is stored in memory — suitable only for demo/prototyping. Restarting the server clears all orders and sessions.
* Authentication is minimal and for demonstration only. Do not use demo credentials in production.
* No persistence, no database, and no real payment processing.

## Security Recommendations

* Move secret values (secret\_key, credentials) to environment variables.
* Use HTTPS in production and configure proper session cookie flags.
* Replace demo user store with a proper user database and hashed passwords (e.g., bcrypt).
* Add CSRF protection for form submissions if you keep server-rendered templates.

## Extending the project

Ideas for next steps:

* Add a database (SQLite/Postgres) to persist users, orders, and menu items.
* Add user registration and password reset flows.
* Add admin interface to update menu/prices and view orders.
* Integrate a real messaging frontend (WebSocket or polling) for real-time updates.
* Add tests (unit and integration) and a CI pipeline.

## Contributing

This is a simple demo — open an issue or submit a PR with improvements. Keep changes focused and include tests when possible.

## License

Use/modify as you like for learning and demo purposes. Add an open-source license file (e.g., MIT) if you plan to publish.

## Contact

Project created by the repository owner. For questions, reply here or add an issue on the repo.
