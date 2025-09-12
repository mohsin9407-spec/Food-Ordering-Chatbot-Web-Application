from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import time

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "mysecretkey"

# Demo users (login system)
users = {"mohsin": "password123", "customer": "foodlover"}
login_attempts = {}

# ✅ Food menu with prices in Rupees
food_menu = {
    "pizza": {"name": "Pizza", "price": 299},     # ₹299
    "burger": {"name": "Burger", "price": 199},   # ₹199
    "fries": {"name": "Fries", "price": 99},      # ₹99
    "pasta": {"name": "Pasta", "price": 249},     # ₹249
    "salad": {"name": "Salad", "price": 149},     # ₹149
    "drink": {"name": "Drink", "price": 59},      # ₹59
    "dessert": {"name": "Dessert", "price": 129}  # ₹129
}

# Order status (in-memory for demo)
order_status = {"active": False, "items": [], "status": None}

# ✅ Login route
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in login_attempts:
            login_attempts[username] = {"count": 0, "lock_time": 0}

        # Check lock
        if login_attempts[username]["lock_time"] > time.time():
            remaining = int(login_attempts[username]["lock_time"] - time.time())
            error = f"⛔ Too many failed attempts. Try again in {remaining} seconds."
            return render_template("login.html", error=error)

        # Successful login
        if username in users and users[username] == password:
            session["user"] = username
            login_attempts[username] = {"count": 0, "lock_time": 0}
            return redirect(url_for("home"))
        else:
            # Wrong login
            login_attempts[username]["count"] += 1
            if login_attempts[username]["count"] >= 3:
                login_attempts[username]["lock_time"] = time.time() + 180  # 3 minutes lock
                login_attempts[username]["count"] = 0
                error = "⛔ Too many failed attempts. Locked for 3 minutes."
            else:
                remaining = 3 - login_attempts[username]["count"]
                error = f"❌ Invalid credentials. {remaining} attempts left."

    return render_template("login.html", error=error)

# ✅ Logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ✅ Home page (Chatbot UI)
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", menu=food_menu, user=session["user"])

# ✅ Chatbot API (all replies in English + Rupees)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    reply = ""

    # 🔹 Order placement
    for key, item in food_menu.items():
        if key in user_message:
            order_status["active"] = True
            order_status["items"].append(item["name"])
            order_status["status"] = "preparing"
            total = sum(
                food_menu[i.lower()]["price"]
                for i in order_status["items"]
                if i.lower() in food_menu
            )

            # ✅ Reply in Rupees
            reply = f"✅ Added {item['name']} to your order. Current total: ₹{total:.2f}."
            return jsonify({"reply": reply})

    # 🔹 Order status check
    if "status" in user_message or "track" in user_message:
        if not order_status["active"]:
            reply = "⚠️ You don’t have any active orders."
        elif order_status["status"] == "preparing":
            reply = "👨‍🍳 Your order is being prepared."
        elif order_status["status"] == "delayed":
            reply = "☔ Your order is delayed due to rain."
        elif order_status["status"] == "ready":
            reply = "✅ Your order is ready!"
        return jsonify({"reply": reply})

    # 🔹 Cancel order
    if "cancel" in user_message or "delete" in user_message:
        if order_status["active"]:
            order_status.update({"active": False, "items": [], "status": None})
            reply = "❌ Your order has been canceled."
        else:
            reply = "⚠️ No active orders to cancel."
        return jsonify({"reply": reply})

    # 🔹 Delay (simulate)
    if "rain" in user_message or "delay" in user_message:
        if order_status["active"]:
            order_status["status"] = "delayed"
            reply = "☔ Your order is delayed due to rain. Please wait 15 minutes."
        else:
            reply = "⚠️ No active orders found."
        return jsonify({"reply": reply})

    # 🔹 Ready (simulate)
    if "ready" in user_message:
        if order_status["active"]:
            order_status["status"] = "ready"
            reply = "✅ Your order is ready for pickup or delivery!"
        else:
            reply = "⚠️ No active orders."
        return jsonify({"reply": reply})

    # 🔹 Default reply
    reply = "🤖 You can order Pizza, Burgers, Pasta, Drinks, etc. or ask about your order status!"
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
