import sqlite3

def create_database():
    connection = sqlite3.connect("nexus.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT UNIQUE,
            origin TEXT,
            destination TEXT,
            carrier TEXT,
            status TEXT,
            estimated_days INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM shipments")

    if cursor.fetchone()[0] == 0:
        sample_shipments = [
            ("NX1001", "China", "Morocco", "DHL", "In Transit", 5),
            ("NX1002", "USA", "France", "FedEx", "Delayed", 8),
            ("NX1003", "Germany", "Spain", "UPS", "Delivered", 0)
        ]

        cursor.executemany("""
            INSERT INTO shipments
            (tracking_number, origin, destination, carrier, status, estimated_days)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_shipments)

    connection.commit()
    connection.close()


def get_shipments():
    connection = sqlite3.connect("nexus.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM shipments ORDER BY id DESC")

    shipments = cursor.fetchall()

    connection.close()
    return shipments
