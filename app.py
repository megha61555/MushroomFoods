from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)
app.secret_key = "87da2ec21cba208505b1f39fdf39b68a"  # for flash messages

# ---------- Email Configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'megha61555@gmail.com'     # 🔹 your Gmail
app.config['MAIL_PASSWORD'] = 'vlqwxmhjnndahulx'        # 🔹 Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = ('Mushroom Foods', 'megha61555@gmail.com')

mail = Mail(app)

# ---------- SQLite Connection ----------
def get_db_connection():
    conn = sqlite3.connect('mushroom.db')
    conn.row_factory = sqlite3.Row  # allows dict-like access
    return conn

# ---------- Home Route ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- Products Route ----------
@app.route("/products")
def products():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("products.html", products=products)

# ---------- Contact Route ----------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # ---------- Save to SQLite ----------
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        db.commit()
        cursor.close()
        db.close()

        # ---------- Send Email ----------
        try:
            msg = Message(
                subject=f"New Contact Form Message from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=['megha61555@gmail.com'],  # your receiving email
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("✅ Your message has been sent successfully!", "success")
        except Exception as e:
            print("Email sending failed:", e)
            flash("⚠ Your message was saved, but email could not be sent.", "warning")

        return render_template("contact.html", success=True)

    return render_template("contact.html")

# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)

