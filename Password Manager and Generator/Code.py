import random
import streamlit as st

st.title("Password Generator and Manager")

# Dropdown menu for options
option = st.selectbox("Choose an option", ["Generate Password", "Enter Password"])

# Password Generation Logic
if option == "Generate Password":
    password_length = st.number_input(
        "Enter the length of the password:", min_value=1, max_value=20
    )

    # Define character sets for password generation
    uppercase_letters = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
    lowercase_letters = [chr(x) for x in range(ord("a"), ord("z") + 1)]
    numbers = [str(x) for x in range(0, 10)]
    special_characters = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "+",
        "-",
        ".",
        "_",
        "}",
        "{",
        "[",
        "]",
        ":",
        ";",
        "'",
        "|",
    ]

    if st.button("Generate Password"):
        # Combine all character sets
        all_characters = (
            uppercase_letters + lowercase_letters + numbers + special_characters
        )
        password = "".join(
            random.choice(all_characters) for _ in range(password_length)
        )

        st.write(f"Generated Password: **{password}**")

# Enter Password Logic
if option == "Enter Password":
    account = st.text_input(
        "Enter the website or URL for which you want to store the password"
    )
    password = st.text_input("Enter your password")
    action = st.selectbox("Choose an action", ["Store Password", "Display Passwords"])

    # Store Password Logic
    if action == "Store Password" and st.button("Submit"):
        # Write the account and password to a text file
        with open("passwords.txt", "a") as file:  # Open the file in append mode
            file.write(f"Website/URL: {account}, Password: {password}\n")

        st.success("Password stored successfully")

    # Display Passwords Logic
    elif action == "Display Passwords":
        st.subheader("Stored Passwords")
        try:
            with open("passwords.txt", "r") as file:
                stored_passwords = file.readlines()
                if stored_passwords:
                    for line in stored_passwords:
                        st.write(line.strip())
                else:
                    st.write("No passwords stored yet.")
        except FileNotFoundError:
            st.write("No passwords stored yet.")
