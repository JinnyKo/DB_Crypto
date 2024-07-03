import mysql.connector
from encryption_utils import encrypt, decrypt

def connect_db(user="testuser", password="1234", database="card_company"):
    return mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database=database
    )

def initialize_db():
    db_init_script = """
    DROP TABLE IF EXISTS card_info;

    CREATE TABLE card_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        card_number VARBINARY(256) NOT NULL,
        card_holder_name VARBINARY(256) NOT NULL,
        expiration_date VARBINARY(256) NOT NULL,
        cvv VARBINARY(256) NOT NULL
    );
    """

    db = connect_db()
    cursor = db.cursor()
    for result in cursor.execute(db_init_script, multi=True):
        pass
    cursor.close()
    db.close()

def insert_card_info(card_number, card_holder_name, expiration_date, cvv):
    db = connect_db()
    cursor = db.cursor()
    
    encrypted_card_number = encrypt(card_number)
    encrypted_card_holder_name = encrypt(card_holder_name)
    encrypted_expiration_date = encrypt(expiration_date)
    encrypted_cvv = encrypt(cvv)

    sql = "INSERT INTO card_info (card_number, card_holder_name, expiration_date, cvv) VALUES (%s, %s, %s, %s)"
    val = (encrypted_card_number, encrypted_card_holder_name, encrypted_expiration_date, encrypted_cvv)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

def get_card_info(card_id):
    db = connect_db()
    cursor = db.cursor()
    
    sql = "SELECT card_number, card_holder_name, expiration_date, cvv FROM card_info WHERE id = %s"
    val = (card_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result:
        encrypted_card_number, encrypted_card_holder_name, encrypted_expiration_date, encrypted_cvv = result
        card_number = decrypt(encrypted_card_number)
        card_holder_name = decrypt(encrypted_card_holder_name)
        expiration_date = decrypt(encrypted_expiration_date)
        cvv = decrypt(encrypted_cvv)
        return {
            'encrypted': {
                'card_number': encrypted_card_number,
                'card_holder_name': encrypted_card_holder_name,
                'expiration_date': encrypted_expiration_date,
                'cvv': encrypted_cvv
            },
            'decrypted': {
                'card_number': card_number,
                'card_holder_name': card_holder_name,
                'expiration_date': expiration_date,
                'cvv': cvv
            }
        }
    else:
        return None

def get_all_card_info():
    db = connect_db()
    cursor = db.cursor()
    
    sql = "SELECT id, card_number, card_holder_name, expiration_date, cvv FROM card_info"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    db.close()

    card_infos = [] 
    for result in results:
        card_id, encrypted_card_number, encrypted_card_holder_name, encrypted_expiration_date, encrypted_cvv = result
        card_number = decrypt(encrypted_card_number)
        card_holder_name = decrypt(encrypted_card_holder_name)
        expiration_date = decrypt(encrypted_expiration_date)
        cvv = decrypt(encrypted_cvv)
        card_infos.append({
            'id': card_id,
            'encrypted': {
                'card_number': encrypted_card_number,
                'card_holder_name': encrypted_card_holder_name,
                'expiration_date': encrypted_expiration_date,
                'cvv': encrypted_cvv
            },
            'decrypted': {
                'card_number': card_number,
                'card_holder_name': card_holder_name,
                'expiration_date': expiration_date,
                'cvv': cvv
            }
        })

    return card_infos
