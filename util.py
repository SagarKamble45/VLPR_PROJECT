from mysql.connector import errorcode
from datetime import datetime
import os
import zipfile
import csv
import shutil
from add_data_to_db import *


# function to delete the images presnet in the VIDEO_IMG folder 
def delete_images():
    folder = 'F:\MAIN_PROJECT\VLPR WEB FLASK\output\IMAGES\VIDEO_IMG' #remove this and add your local directory
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) and filename.endswith('.jpg'):
                os.unlink(file_path)
            else:
                print("File not deleted: ", file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# function to convert all the monogodb data presnet in the livecam db  into a CSV format 
def livedata_to_csv ():

    success, db =create_connection()
    if success:
        collection = 'license_plate_collection_livecam'
        collection = db[collection]
        documents = collection.find({})

        # Initialize empty lists to store data
        Ids = []
        names = []
        texts = []
        confs = []
        date_times = []

        # Iterate over each document
        for document in documents:
            # Append data from each document to respective lists
            Ids.append(document['id'])
            names.append(document['license_plate_name'])
            texts.append(document['license_plate_text'])
            confs.append(document['confidence'])
            date_times.append(document['date_time'])

        # Define column names
        fieldnames = ['id', 'license_plate_name', 'license_plate_text', 'confidence', 'date_time']
        csv_path = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\CSV_DATA\\LIVE_CSV\\live_data.csv' #remove this and add your local directory
        # Write data to CSV file
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write rows
            for i in range(len(Ids)):
                writer.writerow({
                    'id': Ids[i],
                    'license_plate_name': names[i],
                    'license_plate_text': texts[i],
                    'confidence': confs[i],
                    'date_time': date_times[i]
                })

# function to convert all the monogodb data presnet in the video db  into a CSV format 
def video_data_to_csv ():

    success, db =create_connection()
    if success:
        collection = 'license_plate_collection_video'
        collection = db[collection]
        documents = collection.find({})

        # Initialize empty lists to store data
        Ids = []
        names = []
        texts = []
        confs = []
        date_times = []

        # Iterate over each document
        for document in documents:
            # Append data from each document to respective lists   './output/CSV_DATA/VIDEO_CSV/video_data.csv'
            Ids.append(document['id'])
            names.append(document['license_plate_name'])
            texts.append(document['license_plate_text'])
            confs.append(document['confidence'])
            date_times.append(document['date_time'])

        # Define column names
        fieldnames = ['id', 'license_plate_name', 'license_plate_text', 'confidence', 'date_time']
        csv_path = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\CSV_DATA\\VIDEO_CSV\\video_data.csv' #remove this and add your local directory
        # Write data to CSV file
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write rows
            for i in range(len(Ids)):
                writer.writerow({
                    'id': Ids[i],
                    'license_plate_name': names[i],
                    'license_plate_text': texts[i],
                    'confidence': confs[i],
                    'date_time': date_times[i]
                })



def create_folder(folder_path ):

    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # If the folder exists, delete it
            shutil.rmtree(folder_path)
            print(f"Deleted existing folder: {folder_path}")

        os.makedirs(folder_path)
        print(f"Created new folder: {folder_path}")
        return True
    except OSError as e:
        print(f"Error creating folder: {e}")
        return False




#function to donwload video cam imges and video cam data csv file in one zip file 
def download_video_data():
    # Step 1: Create the video_data folder 
    video_data_folder = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\TEMP\\video_data_folder' #remove this and add your local directory
    # if not os.path.exists(video_data_folder):
    #     os.makedirs(video_data_folder)

    if create_folder(video_data_folder):

        # Step 2: Create the images folder inside video_data
        images_folder = os.path.join(video_data_folder, 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # Step 3: Copy all images from another folder to images folder
        source_images_folder = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\IMAGES\\VIDEO_IMG' #remove this and add your local directory
        for filename in os.listdir(source_images_folder):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                shutil.copy(os.path.join(source_images_folder, filename), images_folder)

        # Step 4: Copy CSV file from another folder to video_data folder
        source_csv_file = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\CSV_DATA\\VIDEO_CSV\\video_data.csv' #remove this and add your local directory
        shutil.copy(source_csv_file, video_data_folder)

        # Step 5: Create zip file of the video_data folder 
        zip_filename = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\TEMP\\video_data.zip' #remove this and add your local directory
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(video_data_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), video_data_folder))

        return zip_filename


#function to donwload live cam imges and live cam data csv file in one zip file 
def download_livecam_data():
    # Step 1: Create the video_data folder
    video_data_folder = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\TEMP\\livecam_data_folder' #remove this and add your local directory
    # if not os.path.exists(video_data_folder):
    #     os.makedirs(video_data_folder)

    if create_folder(video_data_folder):

        # Step 2: Create the images folder inside video_data
        images_folder = os.path.join(video_data_folder, 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # Step 3: Copy all images from another folder to images folder
        source_images_folder = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\IMAGES\\LIVE_CAM_IMG' #remove this and add your local directory
        for filename in os.listdir(source_images_folder):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                shutil.copy(os.path.join(source_images_folder, filename), images_folder)

        # Step 4: Copy CSV file from another folder to video_data folder
        source_csv_file = 'f:\\MAIN_PROJECT\\VLPR WEB FLASK\\output\\CSV_DATA\\LIVE_CSV\\live_data.csv' #remove this and add your local directory
        shutil.copy(source_csv_file, video_data_folder)

        # Step 5: Create zip file of the video_data folder
        zip_filename = 'video_data.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(video_data_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), video_data_folder))

        return zip_filename

 
 
 
#function is to find the owners name form the database and this function is return the owners name 
def check_number_plate(number_plate):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["dummy_data"]
    collection = db["vehicles"]

    # Query the database for the given number plate
    query = {"number_plate": number_plate}
    result = collection.find_one(query)

    # If the number plate is found, return the owner's name
    if result:
        return result['owner_name']
    else:
        return "This number plate is not in the database."
