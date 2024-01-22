
######################################################################################################################
##### A .py for combining all of the AUV files into one big one with pictures and the coordinates
#####################################################################################################################

#Installing libraries
import os
import shutil
import random

#defining necessary paths
path=r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images_nephrops/"
destination_directory= r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images_nephrops/Processed"
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
            destination_path = os.path.join(destination_directory, new_filename)

            # Move the CSV file to the destination directory
            source_path = os.path.join(path_2, new_filename)
            shutil.move(source_path, destination_path)
            print(f"File '{csv_filename}' moved successfully.")
        else:
            # Create the CSV file in the destination directory if it doesn't exist
            destination_path = os.path.join(path_2, csv_filename)
            with open(destination_path, 'x') as file:
                print(f"File '{csv_filename}' created and moved successfully. but new")
    except shutil.Error as e:
            print(f"Error moving or creating file: {e}")
    except IOError as e:
            print(f"Error accessing or creating file: {e}")

    def sample_images(source_folder, destination_folder, sample_size):
    # Ensure the source folder exists
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist.")
            return

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Get a list of all files in the source folder
        all_images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

        # Check if there are enough images to sample
        if len(all_images) < sample_size:
            print("Not enough images to sample.")
            return

        # Sample random images from the list
        sampled_images = random.sample(all_images, sample_size)

        # Copy the sampled images to the destination folder
        for image in sampled_images:
            source_path = os.path.join(source_folder, image)
            destination_path = os.path.join(destination_folder, image)
            shutil.copyfile(source_path, destination_path)

        print(f"{sample_size} images sampled and copied to '{destination_folder}'.")

# Example usage:
source_folder = r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images_nephrops/Processed"
destination_folder = r"C:/Users/phd01tm/OneDrive - SAMS/Strangford loch AUV data/AUV data/Images_nephrops/Processed_sampled"
sample_size = 200  # Adjust this to the desired number of sampled images

sample_images(source_folder, destination_folder, sample_size)
