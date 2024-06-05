import datetime
import easyocr
from datetime import datetime
import pymongo
import os


# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)



dict_char_to_int = {'O': '0',
                    'o': '0',
                    'T': '1',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}




def license_complies_format(text):


    if len(text) != 10:
        return False

    # Check each position for the required format
    if text[:2].isalpha() and text[2:4].isdigit() and text[4:6].isalpha() and text[6:].isdigit():
        return True
    else:
        return False
    
def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_char_to_int,
                7: dict_char_to_int, 8: dict_char_to_int, 9: dict_char_to_int,
               2: dict_char_to_int, 3: dict_char_to_int}
    
    if text.startswith(('HH', 'NH','NA','HA')):
        text = 'MH' + text[2:]

    if len(text) > 9:
        text=text.replace(" ", "")
        for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if text[j] in mapping[j].keys():
                license_plate_ += mapping[j][text[j]]
            else:
                license_plate_ += text[j]


    return license_plate_

def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')
        text1=text

        if license_complies_format(text1):
            return format_license(text1), score

    return None, 0

# creating the collection or checking the collection exists in the databse 
def create_new_collection(db, collection_name):
        
        if collection_name in db.list_collection_names():
            db.drop_collection(collection_name)
        
        collection=db.create_collection(collection_name)

        return collection


# check the connection is eastablish or not 
def create_connection():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/") #here add your local mangodb localhost link 
        # Check if the connection is successful by getting the database names
        dbnames =  client.list_database_names()
        return True, client.get_database('license_plate_db') #here add your mongodb database name from mongodb app or website 
    except Exception as e:
        return False,None


success, db = create_connection()
if success:
    collection_name = 'license_plate_collection_video' #here add your collection name 
    collection = create_new_collection(db,collection_name)
    



def video_to_database(license_plate_name, license_plate_text, confidence):
 
    if success:
        # Check if entry already exists
        existing_entry = collection.find_one({'license_plate_text': license_plate_text})
        if existing_entry:
            print("Entry already exists. Skipping insertion.")
            return False, license_plate_text

        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

        # Auto-increment ID
        last_entry = collection.find_one(sort=[("id", -1)])
        if last_entry:
            new_id = last_entry['id'] + 1
        else:
            new_id = 1

        # Insert new record
        new_record = {
            'id': new_id,
            'license_plate_name': license_plate_name,
            'license_plate_text': license_plate_text,
            'confidence': confidence,
            'date_time': current_datetime
        }
        collection.insert_one(new_record)
        print("Data inserted successfully.")

        return True,license_plate_text
    else:
        print("Failed to coonect with databse")
        return False, 0



def livecam_to_database(license_plate_name, license_plate_text, confidence):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")#here add your local mangodb localhost link 
    db = client['license_plate_db']#here add your mongodb database name from mongodb app or website 
    collection = db['license_plate_collection_livecam']  #here add your collection name 

    # Check if entry already exists
    existing_entry = collection.find_one({'license_plate_text': license_plate_text})
    if existing_entry:
        print("Entry already exists. Skipping insertion.")
        return False, license_plate_text

    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    # Auto-increment ID
    last_entry = collection.find_one(sort=[("id", -1)])
    if last_entry:
        new_id = last_entry['id'] + 1
    else:
        new_id = 1

    # Insert new record
    new_record = {
        'id': new_id,
        'license_plate_name': license_plate_name,
        'license_plate_text': license_plate_text,
        'confidence': confidence,
        'date_time': current_datetime
    }
    collection.insert_one(new_record)
    print("Data inserted successfully.")

    return True,license_plate_text


