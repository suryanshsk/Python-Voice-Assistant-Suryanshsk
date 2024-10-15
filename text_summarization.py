import os
import json
from transformers import pipeline

# Set up the summarization model
summarizer = pipeline("summarization")

# File to store texts for summarization
TEXT_FILE = "texts.json"
texts_list = []

def load_texts():
    global texts_list
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r") as file:
            texts_list = json.load(file)
        print("Loaded texts for summarization.")
    else:
        print("No texts to load.")

def save_texts_to_file():
    with open(TEXT_FILE, "w") as file:
        json.dump(texts_list, file, indent=4)

def show_texts():
    if texts_list:
        print("Texts to Summarize:")
        for idx, text in enumerate(texts_list, 1):
            print(f"{idx}. {text}")
    else:
        print("No texts available for summarization!")

def submit_text():
    text = input("Enter the text to summarize (type 'exit' to stop): ")
    if text.lower() != 'exit':
        texts_list.append(text)
        print("Text added for summarization!")
        save_texts_to_file()

def summarize_texts():
    show_texts()
    if texts_list:
        try:
            choice = int(input("Enter the number of the text you want to summarize: ")) - 1
            if 0 <= choice < len(texts_list):
                text_to_summarize = texts_list[choice]
                summary = summarizer(text_to_summarize, max_length=130, min_length=30, do_sample=False)
                print(f"Summary: {summary[0]['summary_text']}")
            else:
                print("Invalid choice, no text summarized.")
        except ValueError:
            print("Please enter a valid number.")

def clear_texts():
    if texts_list:
        texts_list.clear()
        print("All texts have been cleared.")
        save_texts_to_file()
    else:
        print("No texts to clear.")

def feedback_system():
    load_texts()
    while True:
        print("\nText Summarization System")
        print("1. Submit Text")
        print("2. Show Texts")
        print("3. Summarize Text")
        print("4. Clear All Texts")
        print("5. Exit")

        choice = input("Please select an option (1-5): ")

        if choice == "1":
            submit_text()
        elif choice == "2":
            show_texts()
        elif choice == "3":
            summarize_texts()
        elif choice == "4":
            clear_texts()
        elif choice == "5":
            print("Exiting text summarization system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    feedback_system()
