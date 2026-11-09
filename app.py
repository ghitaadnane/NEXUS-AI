from flask import Flask, render_template, request, redirect, flash
import sqlite3
from database import create_database, get_shipments

app = Flask(__name__)
app.secret_key = "nexus_secret_key"

# Create the database
create_database()


@app.route("/")
def dashboard():
    shipments = get_shipments()

    connection = sqlite3.connect("nexus.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM shipments")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'In Transit'")
    in_transit = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'Delayed'")
    delayed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'Delivered'")
    delivered = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        shipments=shipments,
        total=total,
        in_transit=in_transit,
        delayed=delayed,
        delivered=delivered
    )


@app.route("/add-shipment", methods=["POST"])
def add_shipment():
    tracking_number = request.form.get("tracking_number")
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    carrier = request.form.get("carrier")
    status = request.form.get("status")
    estimated_days = request.form.get("estimated_days")

    try:
        connection = sqlite3.connect("nexus.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO shipments
            (tracking_number, origin, destination, carrier, status, estimated_days)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tracking_number,
            origin,
            destination,
            carrier,
            status,
            int(estimated_days)
        ))

        connection.commit()
        connection.close()

        flash("Shipment added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("This tracking number already exists!", "error")

    except (ValueError, TypeError):
        flash("Please enter a valid number of estimated days.", "error")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True) 