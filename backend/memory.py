import sqlite3

def get_connection():
    conn = sqlite3.connect('database/memory.db')
    cursor = conn.cursor()
    return conn, cursor

def create_memory_table():
    """Create the memory table in the database if it doesn't exist."""
    
    q1 = """ CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
            memory_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        ); """
    
    conn, cursor = get_connection()
    cursor.execute(q1)
    conn.commit() 
    conn.close()
    

def insert_memory(user_id, role, memory_text):
    """Insert a new memory into the memory table.
    expects two arguments: user_id (str),role['user','assistant'] memory_text (str)"""
    
    create_memory_table()
    q2 = """ INSERT INTO memory (user_id, role, memory_text)
             VALUES (?, ?, ?); """
             
    conn, cursor = get_connection()

    cursor.execute(q2, (user_id, role, memory_text))
    conn.commit()
    conn.close()
    


def fetch_memories_by_user(user_id):
    """ Fetch memories from the memory table by user_id.
    expects one argument: user_id (str)
    """
    
    q3 = "SELECT * FROM memory WHERE user_id = ?;"
    conn, cursor = get_connection()
    cursor.execute(q3, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_memories_by_user(user_id):
    """ Clear all memories from the memory table for a specific user.
    expects one argument: user_id (str)
    """
    
    q4 = "DELETE FROM memory WHERE user_id = ?;"
    conn, cursor = get_connection()
    cursor.execute(q4, (user_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_memory_table()