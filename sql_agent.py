
import sqlite3

DB_PATH = "data/insurance_demo.db"

def run_sql_action(user_data, action_type="query"):
    if action_type == "query":
        return query_policy(user_data)
    elif action_type == "update_info":
        return update_client_info(user_data)
    elif action_type == "file_claim":
        return insert_new_claim(user_data)
    else:
        return "Unknown action type."

def query_policy(user_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        name = user_data.get("name")
        dob = user_data.get("dob")
        email = user_data.get("email")

        cursor.execute("""
        SELECT c.name, c.dob, c.email, i.vehicle_make, i.vehicle_model, i.vehicle_year, 
               i.coverage_type, i.start_date, i.end_date
        FROM client_info c
        JOIN insurance_coverage_and_car_details i ON c.client_id = i.client_id
        WHERE c.name = ? AND c.dob = ? AND c.email = ?
        """, (name, dob, email))

        rows = cursor.fetchall()
        if not rows:
            return "No matching insurance records found."

        response = ""
        for row in rows:
            response += (f"\nName: {row[0]}\nEmail: {row[2]}\nVehicle: {row[3]} {row[4]} ({row[5]})\n"
                         f"Coverage: {row[6]}\nActive: {row[7]} to {row[8]}\n---\n")

        return response.strip()

    except Exception as e:
        return f"Database error: {e}"
    finally:
        conn.close()

def update_client_info(user_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        name, dob, email = user_data["name"], user_data["dob"], user_data["email"]
        field, new_value = user_data["field_to_update"], user_data["new_value"]

        if field not in ["address", "phone"]:
            return "Only address and phone number updates are supported."

        cursor.execute(f"""
        UPDATE client_info
        SET {field} = ?
        WHERE name = ? AND dob = ? AND email = ?
        """, (new_value, name, dob, email))

        conn.commit()
        return "Your information has been updated." if cursor.rowcount else "No matching record found."

    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def insert_new_claim(user_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        name, dob, email = user_data["name"], user_data["dob"], user_data["email"]
        vehicle = user_data["vehicle"]
        date, location = user_data["date"], user_data["location"]
        desc = user_data.get("description", "N/A")
        report = user_data.get("police_report")
        status = "open"

        cursor.execute("""
        SELECT i.policy_id FROM client_info c
        JOIN insurance_coverage_and_car_details i ON c.client_id = i.client_id
        WHERE c.name = ? AND c.dob = ? AND c.email = ?
        AND i.vehicle_make || ' ' || i.vehicle_model = ?
        """, (name, dob, email, vehicle))

        result = cursor.fetchone()
        if not result:
            return "Policy not found for the provided client and vehicle."

        policy_id = result[0]

        cursor.execute("""
        INSERT INTO claims (policy_id, date, location, description, police_report, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (policy_id, date, location, desc, report, status))

        conn.commit()
        return f"✅ Claim submitted. ID: {cursor.lastrowid}"

    except Exception as e:
        return f"Claim error: {e}"
    finally:
        conn.close()
