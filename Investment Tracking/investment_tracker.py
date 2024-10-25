import asyncio
import pyttsx3
import speech_recognition as sr
import json
import os
import requests

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# File to store investment data
DATA_FILE = "investment_data.json"

# Global variables to store investments and price alerts
investments = {}
price_alerts = {}

# Load data from file
def load_data():
    global investments, price_alerts
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                investments = data.get("investments", {})
                price_alerts = data.get("price_alerts", {})
        except (IOError, json.JSONDecodeError):
            print("Error loading data file. Starting with empty data.")
            investments = {}
            price_alerts = {}

# Save data to file
def save_data():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({"investments": investments, "price_alerts": price_alerts}, f)
    except IOError:
        print("Error saving data file.")

# Function to convert text to speech asynchronously
async def speak_async(text):
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0.5)

# Function to get user input through speech recognition
async def voice_to_text_async():
    recognizer = sr.Recognizer()
    await asyncio.sleep(0.5)
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            await speak_async("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            await speak_async("The speech recognition service is unavailable at the moment.")
            return None

# Fetch real-time stock price from Alpha Vantage API
def get_stock_price(stock_symbol):
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (5min)" in data:
            latest_time = list(data['Time Series (5min)'].keys())[0]
            price = data['Time Series (5min)'][latest_time]['4. close']
            return float(price)
        else:
            return None  # Stock symbol not found or API error
    except requests.RequestException:
        return None  # Handle request errors

# Log investments with input validation
async def log_investment(stock, quantity):
    stock = stock.strip()  # Trim whitespace
    if not stock.isalpha():
        await speak_async("Invalid stock symbol. Please provide a valid stock symbol.")
        return
    
    if quantity <= 0:
        await speak_async("Please provide a positive quantity.")
        return

    if stock not in investments:
        investments[stock] = 0
    investments[stock] += quantity
    save_data()
    await speak_async(f"Logged {quantity} shares for {stock}.")

# Set price alerts
async def set_price_alert(stock, target_price):
    stock = stock.strip()  # Trim whitespace
    if not stock.isalpha():
        await speak_async("Invalid stock symbol. Please provide a valid stock symbol.")
        return
    
    if stock not in price_alerts:
        price_alerts[stock] = target_price
    else:
        price_alerts[stock] = max(price_alerts[stock], target_price)

    save_data()
    await speak_async(f"Price alert for {stock} set at {target_price} dollars.")

# Check if any price alerts have been triggered
async def check_price_alerts():
    for stock, target_price in price_alerts.items():
        price = get_stock_price(stock)
        if price is None:
            await speak_async(f"Unable to fetch price for {stock}.")
            continue
        if price >= target_price:
            await speak_async(f"Alert! {stock} has reached {price} dollars, above your target of {target_price}.")

# Get portfolio summary with real-time prices
async def portfolio_summary():
    if investments:
        await speak_async("Here is your portfolio summary with real-time prices:")
        for stock, quantity in investments.items():
            price = get_stock_price(stock)
            if price is not None:
                await speak_async(f"You have {quantity} shares of {stock}, currently valued at {price * quantity:.2f} dollars.")
            else:
                await speak_async(f"Unable to fetch price for {stock}.")
    else:
        await speak_async("You do not have any investments logged yet.")

# Get total portfolio value
async def portfolio_value():
    total_value = 0
    for stock, quantity in investments.items():
        price = get_stock_price(stock)
        if price is not None:
            total_value += price * quantity
        else:
            await speak_async(f"Unable to fetch price for {stock}.")
    
    await speak_async(f"Your total portfolio is valued at {total_value:.2f} dollars.")

# Main function for the assistant
async def main():
    load_data()  # Load existing data at startup
    await speak_async("Welcome to your investment assistant! How can I assist you today?")
    
    while True:
        command = await voice_to_text_async()
        
        if command:
            if "log investment" in command:
                parts = command.split()
                if len(parts) == 4 and parts[1] == "investment":
                    stock = parts[2]
                    try:
                        quantity = int(parts[3])
                        await log_investment(stock, quantity)
                    except ValueError:
                        await speak_async("Please provide a valid quantity.")

            elif "set price alert" in command:
                parts = command.split()
                if len(parts) == 5 and parts[1] == "price" and parts[2] == "alert":
                    stock = parts[3]
                    try:
                        target_price = float(parts[4])
                        await set_price_alert(stock, target_price)
                    except ValueError:
                        await speak_async("Please provide a valid target price.")

            elif "check portfolio" in command:
                await portfolio_summary()

            elif "total value" in command:
                await portfolio_value()

            elif "check price alerts" in command:
                await check_price_alerts()
                
            elif "exit" in command:
                await speak_async("Goodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
