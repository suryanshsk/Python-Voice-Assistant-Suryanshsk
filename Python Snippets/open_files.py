FILES = {
    "file1": "path1",

}


import os

def open_file(file):
    file_path = FILES.get(file)
    if file_path:
        os.open(file_path)
    else:
        if os.exists(file):
            os.open(file)
        else:
            print("Please specify file path coorectly")
            file = input("Enter file path:")
            try:
                os.open(file)
            except:
                print("Error opening file!.")