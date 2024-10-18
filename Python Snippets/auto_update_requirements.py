import subprocess

def generate_requirements():
    try:
        subprocess.check_call(["pipreqs", ".", "--force"])
        print("requirements.txt generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements.txt: {e}")

def main():
    generate_requirements()
    
if __name__ == "__main__":
    main()
    
#install pipreqs if not installed with the commands below
#pip install pipreqs