<div align="center">

# `Python-Voice-Assistant-Suryanshsk`

<i>A Python-based virtual assistant using Gemini AI. This assistant is capable of voice recognition, text-to-speech, fetching weather updates, retrieving news, delivering jokes, pulling information from Wikipedia, and managing music. The project also includes an interactive web interface and is designed to be customizable and extendable.
</i>

</div>

<div align = "center">
<br>

<table align="center">
    <thead align="center">
        <tr border: 1px;>
            <td><b>🌟 Stars</b></td>
            <td><b>🍴 Forks</b></td>
            <td><b>🐛 Issues</b></td>
            <td><b>🔔 Open PRs</b></td>
            <td><b>🔕 Close PRs</b></td>
            <td><b>🛠️ Languages</b></td>
        </tr>
     </thead>
    <tbody>
         <tr>
            <td><img alt="Stars" src="https://img.shields.io/github/stars/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&logo=github"/></td>
            <td><img alt="Forks" src="https://img.shields.io/github/forks/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&logo=github"/></td>
            <td><img alt="Issues" src="https://img.shields.io/github/issues/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&logo=github"/></td>
            <td><img alt="Open Pull Requests" src="https://img.shields.io/github/issues-pr/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&logo=github"/></td>
           <td><img alt="Close Pull Requests" src="https://img.shields.io/github/issues-pr-closed/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&color=critical&logo=github"/></td>
           <td><img alt="GitHub language count" src="https://img.shields.io/github/languages/count/suryanshsk/Python-Voice-Assistant-Suryanshsk?style=flat&color=critical&logo=github"></td>
        </tr>
    </tbody>
</table>
</div>
<br>

## 📋 Participating Programs

| Name                  | Logo                                                      | Purpose                                                                                                      |
|-----------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| GSSoC'2024-Extd       | ![GSSoC Logo](assets/GSSoC-Ext.png)                       | The coding period is from October 1st to October 30th, during which contributors make contributions and earn points on the platform. |
| Hacktoberfest 2024    | ![Hacktoberfest Logo](assets/hacktoberfest.png)           | Hacktoberfest is a month-long October event welcoming all skill levels to join the open-source community.     |

---



<!--<p align="center">
 <img height='80%' src="Banner.png" alt="Suryanshsk Python Voice Assistant" > </p> -->


## Features

- **Voice Recognition**: Processes and understands spoken commands.
- **Text-to-Speech**: Converts text responses into spoken output.
- **Weather Information**: Provides real-time weather updates.
- **News Updates**: Fetches the latest news headlines.
- **Jokes**: Delivers a variety of jokes.
- **Wikipedia Information**: Retrieves data from Wikipedia.
- **Music Management**: Handles and plays music.
- **Web Interface**: Interactive frontend with animations.
- **Your Question**: It Give Answer OF Your Questions.


# Virtual Assistant with Gemini AI


A sophisticated Python-based virtual assistant utilizing Gemini AI. This project integrates various functionalities to create a versatile and interactive assistant.

# Table of Contents

1. [Installation](#installation)
2. [Notice](#notice)
3. [Contributors](#our-valuable-contributors-%EF%B8%8F)
4. [Contact](#contact)
5. [Reporting Issues](#reporting-issues)

## Installation

Follow these steps to set up the project on your local machine:

1. **Fork the Repository**

   - Click on the [Fork](https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/fork) button in the upper right corner of the page to create a copy of the repository under your GitHub account.

2. **Clone the Repository**

   - Open your terminal or command prompt and run the following command to clone the repository to your local machine:
     ```bash
     git clone https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk.git
     ```

3. **Navigate to the Project Directory**

   - Change your current directory to the project directory:
     ```bash
     cd Python-Voice-Assistant-Suryanshsk
     ```

4. **Set Up a Virtual Environment**

   - It is recommended to use a virtual environment to manage dependencies and avoid conflicts. Create and activate a virtual environment with the following commands:
     ```bash
     python -m venv venv
     source venv/bin/activate  # For Windows: venv\Scripts\activate
     ```

5. **Install Dependencies**

   - Install the required dependencies listed in the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

   - The `requirements.txt` file includes the following modules:
     ```
     speechrecognition==3.8.1
     gtts==2.2.3
     requests==2.28.1
     beautifulsoup4==4.12.0
     flask==2.3.2
     websocket-client==1.5.1
     google-generativeai==0.3.1
     request
     speechrecognition
     pyttsx3
     wikipedia
     requests
     pyjokes
     ```

   - Additionally, ensure you have the latest version of `google-generativeai`:
     ```bash
     pip install -U google-generativeai
     ```

    - To ensure your Python voice recognition assistant runs smoothly,
    here's a list of essential packages you should install:
      ```bash
        pip install SpeechRecognition
        pip install pyaudio
        pip install setuptools
       ```

    - To use gTTS (Google Text-to-Speech) in your Python project:
      ```bash
        pip install gtts
      ```
6. **Configure API Keys**

   - Replace the placeholder API keys in the code with your actual API keys:
     ```python
     genai.configure(api_key="Your_Own_API_KEY_FOR_GEMINI_AI")  # Replace with your actual API key
     api_key = 'YOUR_NEWS_API_KEY'  # Replace with a real news API key
     API_KEY = 'YOUR_WEATHER_API_KEY'  # Replace with your weather API key
     ```

7. **Run the Application**

   - Start the virtual assistant by running the main script:
     ```bash
     python main_assistant.py
     ```

**You are now ready to use the Python Voice Assistant with Gemini AI!**

---

## Notice

### API Key Configuration

To use the Python Voice Assistant with Gemini AI, you need to configure your API keys. Replace the placeholder keys in the code with your actual API keys as shown below:

1. **Gemini AI API Key**:
   ```python
   genai.configure(api_key="GEMINI_API_KEY")  # Replace with your actual API key
   ```

2. **News API Key**:
   ```python
   api_key = 'YOUR_NEWS_API_KEY'  # Replace with a real news API key
   ```

3. **Weather API Key**:
   ```python
   API_KEY = 'YOUR_WEATHER_API_KEY'  # Replace with your weather API key
   ```

Make sure to replace `"GEMINI_API_KEY"`, `'YOUR_NEWS_API_KEY'`, and `'YOUR_WEATHER_API_KEY'` with your actual API keys to enable the respective functionalities.

---

 # Project Admin⚡
 
<table>
<tr>
<td align="center"><a href="https://github.com/suryanshsk"><img src="https://avatars.githubusercontent.com/u/88218773?v=4" width=150px height=150px /></a></br> <h4 style="color:red;">Suryansh singh</h4>
 <a href="https://www.linkedin.com/in/avanishsinghengineer/"><img src="https://img.icons8.com/fluency/2x/linkedin.png" width="32px" height="32px"></img></a>
   </td>

</tr>
</table>
  
</div>

## Acknowledgements

We are grateful to all the contributors who have helped improve this project. Your contributions are what make this project better!

<p align ="center">
  <img src="https://api.vaunt.dev/v1/github/entities/suryanshsk/repositories/Python-Voice-Assistant-Suryanshsk/contributors?format=svg&limit=54" width="700" height= "250" />
</p>

<br>

## Contributors❤️

<p align ="center">
<a href="https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/graphs/contributors">
  <img align="center" src="https://contrib.rocks/image?max=100&repo=suryanshsk/Python-Voice-Assistant-Suryanshsk" />
</a>
</p>

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)



## Stargazers ❤️

<div align='left'>

[![Stargazers repo roster for @suryanshsk/Python-Voice-Assistant-Suryanshsk](https://reporoster.com/stars/dark/suryanshsk/Python-Voice-Assistant-Suryanshsk)](https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/stargazers)


</div>

## Forkers ❤️

[![Forkers repo roster for @suryanshsk/Python-Voice-Assistant-Suryanshsk](https://reporoster.com/forks/dark/suryanshsk/Python-Voice-Assistant-Suryanshsk)](https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/network/members)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)



## Contact

For questions or feedback, reach out to [suryanshskcontact@gmail.com](mailto:suryanshskcontact@gmail.com).


## Reporting Issues

If you encounter any bugs or have suggestions for improvements, please open an [issue](https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/issues/new) on GitHub. We appreciate detailed and insightful reports that help us address the issue more effectively.


## Main Project Link

https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/tree/29b12a535b599f7e1c6141058871dccfa38eadfa
