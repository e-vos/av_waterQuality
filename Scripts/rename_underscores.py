import os

def rename(directory):
    files = os.listdir(directory)
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            filename, extension = os.path.splitext(file)
            new_name = filename.replace('.', '_') + extension
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {file} to {new_name} in {directory}.")

directory_path = r"D:\University\AmericaView_HLS\2021_HLS_data\ndvi"

rename(directory_path)
