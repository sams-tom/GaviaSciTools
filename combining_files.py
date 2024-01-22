######################################################################################################################
##### A .py for combining all of the AUV files into one big one with pictures and the coordinates
#####################################################################################################################

#Installing libraries
import os
import shutil

#defining necessary paths
path=r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images/"
destination_directory= r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images/Processed"
csv_filename = 'coords.csv'
i=0

#Block checks/creates the directory for the files to   move to
try: 
    if os.path.exists(destination_directory):
       print(f"Folder processed already exists in '{destination_directory}'. Skipping...")
    else:
        os.makedirs(destination_directory, exist_ok=True)
        print(f"Directory '{destination_directory}' created successfully.")
except OSError as e:
    print(f"Error creating directory '{destination_directory}': {e}")


#this moves files
for files in os.listdir(path):
    #creaes paths
    save_folder='answers/'
    path_1 = os.path.join(path, files)
    path_2 = os.path.join(path_1, save_folder)
    path_2 = path_2.replace("\\", "/")
    print(path_2)

    print(path_2)
    print(f"{path_2}Average.png")
    #removes the average png so I can search for pngs
    try:
        os.remove(f"{path_2}Average.png")
        print(f"File '{path_2}' Average.png deleted successfully.")
    except OSError as e:
        print('bronk file')

    #this moves the images
    try:
        #lists all the images in a file
        jpg_files = [file for file in os.listdir(path_2) if file.lower().endswith('.jpg')]
        print(jpg_files)
        #this moves the files
        for jpg_file in jpg_files:
            source_path = os.path.join(path_2, jpg_file)
            destination_path = os.path.join(destination_directory, jpg_file)
            shutil.move(source_path, destination_path)
            print(f"File '{jpg_file}' moved successfully.")
    except shutil.Error as e:
        print(f"Error moving files: {e}")
    except OSError as e:
        print(f"Error listing or accessing files: {e}")



    try:
    # List all files in the source directory
        files = os.listdir(path_2)
        print(files)
    # Check if the CSV file exists in the source directory
        if csv_filename in files:
            i= i +1
            source_path = os.path.join(path_2, csv_filename)
            ##I think this is moving the wrong one (moves coords not coords_1)
            print(source_path)
            new_filename = f"coords_{i}.csv"
            print(new_filename)
            os.rename(source_path, os.path.join(path_2, new_filename))
            destination_path = os.path.join(destination_directory, csv_filename)

            # Move the CSV file to the destination directory
            source_path = os.path.join(path_2, new_filename)
            shutil.move(source_path, destination_path)
            print(f"File '{csv_filename}' moved successfully.")
        else:
            # Create the CSV file in the destination directory if it doesn't exist
            destination_path = os.path.join(path_2, csv_filename)
            with open(destination_path, 'x') as file:
                print(f"File '{csv_filename}' created and moved successfully.")
    except shutil.Error as e:
            print(f"Error moving or creating file: {e}")
    except IOError as e:
            print(f"Error accessing or creating file: {e}")
