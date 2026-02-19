from db.connection import connect_to_db

def init_db():    
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    
    db.commit()
    cursor.close()
    db.close()
    print("Tables initialized")