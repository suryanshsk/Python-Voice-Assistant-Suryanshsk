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



<p align="center">
<img height='80%' src="Banner.png" alt="Suryanshsk Python Voice Assistant" > </p>


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

   - Additionally, ensure you have the latest version of `google-generativeai`:
     ```bash
     pip install -U google-generativeai
     ```

6. **Configure API Keys**

    - Create a `.env` file in the root directory of your project and add your API keys as shown below:
      ```
      GEMINI_API_KEY=Your_Own_API_KEY_FOR_GEMINI_AI
      NEWS_API_KEY=YOUR_NEWS_API_KEY
      WEATHER_API_KEY=YOUR_WEATHER_API_KEY
      ```
    - reference to set get API keys
      - get Gemini api key from : https://aistudio.google.com/app/apikey
      - get news api key from : https://newsapi.org/
      - get weather api key from : https://openweathermap.org/api

    - How to access environment variables in a Python file which are set in a `.env` file:
        ```python
        # load environment variables from .env
        from dotenv import load_dotenv
        import os

        load_dotenv()

        # access the environment variables
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        news_api_key = os.getenv('NEWS_API_KEY')
        weather_api_key = os.getenv('WEATHER_API_KEY')

        print(f"Gemini API Key: {gemini_api_key}")
        print(f"News API Key: {news_api_key}")
        print(f"Weather API Key: {weather_api_key}")
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

## Our Valuable Contributors ❤️✨

We are grateful to all the contributors who have helped improve this project. Your contributions are what make this project better!

<!-- readme: contributors -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/suryanshsk">
                    <img src="https://avatars.githubusercontent.com/u/88218773?v=4" width="100;" alt="suryanshsk"/>
                    <br />
                    <sub><b>Suryansh singh</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/yashksaini-coder">
                    <img src="https://avatars.githubusercontent.com/u/115717039?v=4" width="100;" alt="yashksaini-coder"/>
                    <br />
                    <sub><b>Yash Kumar Saini</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Chin-may02">
                    <img src="https://avatars.githubusercontent.com/u/179141504?v=4" width="100;" alt="Chin-may02"/>
                    <br />
                    <sub><b>Vuppu Chinmay</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Dsmita03">
                    <img src="https://avatars.githubusercontent.com/u/123728188?v=4" width="100;" alt="Dsmita03"/>
                    <br />
                    <sub><b>Debasmita Sarkar</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/zsquare12">
                    <img src="https://avatars.githubusercontent.com/u/36557466?v=4" width="100;" alt="zsquare12"/>
                    <br />
                    <sub><b>Jitendra Kumar</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/djv554">
                    <img src="https://avatars.githubusercontent.com/u/174509658?v=4" width="100;" alt="djv554"/>
                    <br />
                    <sub><b>Deanne Vaz</b></sub>
                </a>
            </td>
		</tr>
		<tr>
            <td align="center">
                <a href="https://github.com/jaidh01">
                    <img src="https://avatars.githubusercontent.com/u/117927011?v=4" width="100;" alt="jaidh01"/>
                    <br />
                    <sub><b>Jai Dhingra</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Kritika75">
                    <img src="https://avatars.githubusercontent.com/u/142504516?v=4" width="100;" alt="Kritika75"/>
                    <br />
                    <sub><b>Kritika Singh </b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Codewithmeowmeow">
                    <img src="https://avatars.githubusercontent.com/u/182342654?v=4" width="100;" alt="Codewithmeowmeow"/>
                    <br />
                    <sub><b>codewithvibha</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/AnujSaha0111">
                    <img src="https://avatars.githubusercontent.com/u/153378181?v=4" width="100;" alt="AnujSaha0111"/>
                    <br />
                    <sub><b>Anuj Saha</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Deeptig9138">
                    <img src="https://avatars.githubusercontent.com/u/156528626?v=4" width="100;" alt="Deeptig9138"/>
                    <br />
                    <sub><b>Deepti Gupta</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/say-het">
                    <img src="https://avatars.githubusercontent.com/u/71073587?v=4" width="100;" alt="say-het"/>
                    <br />
                    <sub><b>Het Modi</b></sub>
                </a>
            </td>
		</tr>
		<tr>
            <td align="center">
                <a href="https://github.com/Herostomo">
                    <img src="https://avatars.githubusercontent.com/u/155301429?v=4" width="100;" alt="Herostomo"/>
                    <br />
                    <sub><b>Kshitij Vijay Hedau</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/ShrishtiSingh26">
                    <img src="https://avatars.githubusercontent.com/u/142707684?v=4" width="100;" alt="ShrishtiSingh26"/>
                    <br />
                    <sub><b>Shrishti</b></sub>
                </a>
            </td>
		</tr>
	<tbody>
</table>
<!-- readme: contributors -end -->

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For questions or feedback, reach out to [suryanshskcontact@gmail.com](mailto:suryanshskcontact@gmail.com).


## Reporting Issues

If you encounter any bugs or have suggestions for improvements, please open an [issue](https://github.com/suryanshsk/Python-Voice-Assistant-Suryanshsk/issues/new) on GitHub. We appreciate detailed and insightful reports that help us address the issue more effectively.