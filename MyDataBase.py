import mysql.connector
import easyocr
import io

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Function to insert image data into the database
def insert_image_to_db(image_path):
    with open(image_path, 'rb') as image_file:
        img_data = image_file.read()
    
    conn = mysql.connector.connect(
        host='localhost',       # e.g., 'localhost'
        user='Senpai',   # your MySQL username
        password='qwerty123',  # your MySQL password
        database='image_text_db'  # the database we created
    )

    cursor = conn.cursor()
    cursor.execute("INSERT INTO image_text (img) VALUES (%s)", (img_data,))
    conn.commit()
    image_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return image_id

# Function to extract text from image using EasyOCR
def extract_text_from_image(img_data):
    with open('temp_image.png', 'wb') as img_file:
        img_file.write(img_data)
    result = reader.readtext('temp_image.png', detail=0)
    extracted_text = ' '.join(result)
    return extracted_text

# Function to update text in the database
def update_text_in_db(image_id, extracted_text):
    conn = mysql.connector.connect(
        host='localhost',       # e.g., 'localhost'
        user='Senpai',   # your MySQL username
        password='qwerty123',  # your MySQL password
        database='image_text_db'  # the database we created
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE image_text SET text = %s WHERE id = %s", (extracted_text, image_id))
    conn.commit()
    cursor.close()
    conn.close()

# Complete workflow
def process_image(image_path):
    image_id = insert_image_to_db(image_path)
    
    conn = mysql.connector.connect(
        host='localhost',       # e.g., 'localhost'
        user='Senpai',   # your MySQL username
        password='qwerty123',  # your MySQL password
        database='image_text_db'  # the database we created
    )
    cursor = conn.cursor()
    cursor.execute("SELECT img FROM image_text WHERE id = %s", (image_id,))
    img_data = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    extracted_text = extract_text_from_image(img_data)
    update_text_in_db(image_id, extracted_text)
    print(extracted_text)
# Example usage:
process_image('D:\Sen-core/5/images/13.jpg')

