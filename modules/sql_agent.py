import sqlite3

DB_PATH = "data/insurance.db"

def run_sql_action(user_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        name = user_data.get("name")
        dob = user_data.get("dob")
        email = user_data.get("email")
        address = user_data.get("address")

        query = """
        SELECT * FROM policies
        WHERE name = ? AND dob = ? AND email = ? AND address = ?
        """
        cursor.execute(query, (name, dob, email, address))
        result = cursor.fetchone()

        if result:
            return f"Policy found: {result}"
        else:
            return "Sorry, no matching policy found. Please check your details."

    except Exception as e:
        return f"Database error: {e}"
    finally:
        conn.close()
