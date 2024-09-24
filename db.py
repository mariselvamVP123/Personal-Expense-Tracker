import mysql.connector

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mariselvam@123",
        database="expensetracker"
    )
    return connection

def create_tables():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            date DATE,
            category VARCHAR(255),
            amount DECIMAL(10, 2),
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2)
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

def add_expense(date, category, amount, description):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)"
    values = (date, category, amount, description)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def get_expenses():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT date, category, amount, description FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    connection.close()
    return expenses

def delete_expense(date, category, amount, description):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = "DELETE FROM expenses WHERE date = %s AND category = %s AND amount = %s AND description = %s"
    values = (date, category, amount, description)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def update_expense(old_date, old_category, old_amount, old_description, new_date, new_category, new_amount, new_description):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = """
        UPDATE expenses
        SET date = %s, category = %s, amount = %s, description = %s
        WHERE date = %s AND category = %s AND amount = %s AND description = %s
    """
    values = (new_date, new_category, new_amount, new_description, old_date, old_category, old_amount, old_description)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

# Set the budget
def set_budget(amount):
    connection = connect_to_db()
    cursor = connection.cursor()
    
    # Check if a budget already exists
    cursor.execute('SELECT COUNT(*) FROM budget')
    if cursor.fetchone()[0] == 0:
        # Insert a new budget if none exists
        cursor.execute('INSERT INTO budget (amount) VALUES (%s)', (amount,))
    else:
        # Update the existing budget
        cursor.execute('UPDATE budget SET amount=%s WHERE id=1', (amount,))
    
    connection.commit()
    cursor.close()
    connection.close()

# Get the budget
def get_budget():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT amount FROM budget WHERE id=1')
    budget = cursor.fetchone()
    cursor.close()
    connection.close()
    return budget[0] if budget else None




# Example usage
if __name__ == "__main__":
    create_tables()



