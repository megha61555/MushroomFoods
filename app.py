from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import mysql.connector 

app = Flask(__name__)
app.secret_key = "87da2ec21cba208505b1f39fdf39b68a"  # for flash messages

# ---------- Email Configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'megha61555@gmail.com'     # 🔹 your Gmail
app.config['MAIL_PASSWORD'] = 'vlqwxmhjnndahulx'        # 🔹 your Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = ('Mushroom Foods', 'megha61555@gmail.com')

mail = Mail(app)
# ---------- MySQL Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # your MySQL username
        password="Megha@1995",  # your MySQL password
        database="food_db",    # your database name
         auth_plugin="mysql_native_password"
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/products")
def products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("products.html", products=products)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

       
        # ---------- Save to MySQL ----------
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        db.commit()
        cursor.close()
        db.close()

        msg = Message(
            subject=f"New Contact Form Message from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['megha61555@gmail.com'],  # where you want to receive
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
    
        # ---------- Send Email ----------    
        mail.send(msg)

        # flash("✅ Your message has been sent successfully!", "success")

        return render_template("contact.html", success=True)
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
