import requests
import matplotlib.pyplot as plt
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import re
from colorama import Fore, Style, init

init(autoreset=True)

API_KEY = 'YOUR_API_KEY'  # Replace with your actual OpenWeatherMap API key

def fetch_uv_data(latitude, longitude, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/uvi?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if 'value' in data:
            uv_index = data['value']
            return uv_index
        else:
            print(f"{Fore.RED}Error: UV data not found - {data}")
            return 0  
    
    except Exception as e:
        print(f"{Fore.RED}Error in fetching UV data: {e}")
        return 0  


def fetch_nasa_solar_eclipse_data():
    url = "https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        eclipse_data = re.findall(r'<tr>(.*?)</tr>', content, re.DOTALL)

        eclipses = []
        for row in eclipse_data[1:]:  
            cells = re.findall(r'<td>(.*?)</td>', row)
            if len(cells) >= 3:  
                date = re.sub(r'<.*?>', '', cells[0]).strip()
                type_eclipse = re.sub(r'<.*?>', '', cells[1]).strip()
                location = re.sub(r'<.*?>', '', cells[2]).strip()

                if datetime.strptime(date, "%Y %b %d").year >= 2020:
                    eclipses.append((date, type_eclipse, location))

        return eclipses
    else:
        return f"Error fetching eclipse data: {response.status_code}"


def plot_uv_trends(uv_data):
    days = list(uv_data)
    uv_values = list(uv_data.values())
    
    plt.plot(days, uv_values, label='UV Index', color='orange')
    plt.xlabel('Days')
    plt.ylabel('UV Index')
    plt.title('UV Index Trends over Time')
    plt.axhline(y=6, color='red', linestyle='--', label="High UV Level (6+)")
    plt.legend()
    plt.grid(True)
    plt.show()


def skincare_tips(uv_index):
    try:
        uv_index = float(uv_index)
    except ValueError:
        return f"{Fore.RED}Invalid UV index value: {uv_index}"

    if uv_index < 3:
        return f"{Fore.BLUE}Low UV: No sunscreen needed. Enjoy the sun safely!"
    elif 3 <= uv_index < 6:
        return f"{Fore.YELLOW}Moderate UV: Wear sunglasses, stay hydrated, and consider using SPF 30."
    elif 6 <= uv_index < 8:
        return f"{Fore.YELLOW}High UV: Wear protective clothing, a wide-brimmed hat, and use SPF 50. Avoid direct sun exposure during peak hours."
    else:
        return f"{Fore.RED}Very High UV: Minimize outdoor time, wear UV-blocking sunglasses, and reapply sunscreen every 2 hours if exposed to the sun."


def send_notification(subject, message, to_email):
    sender_email = "yourid@gmail.com"  # Replace with your Gmail address
    sender_password = "your-app-password"  # Replace with your Gmail app-specific password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create SMTP session with Gmail's server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server and port
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)  # Login to the server
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)  
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        try:
            server.quit()  
        except Exception as e:
            print(f"Error closing server connection: {e}")

# Example usage:
send_notification(
    subject="Test Email",
    message="This is a test email sent using Gmail's SMTP server.",
    to_email="recipient@example.com"  # Replace with the recipient's email
)


def track_sun_exposure(user_id, latitude, longitude, uv_index):
    data_file = f"{user_id}_skin_health.json"
    
    try:
        with open(data_file, 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {} 

    location_key = f"{latitude},{longitude}"

    if location_key not in history:
        
        history[location_key] = {"total_exposure": 0, "days": 0}
    
    history[location_key]["total_exposure"] += uv_index
    history[location_key]["days"] += 1
    
    with open(data_file, 'w') as f:
        json.dump(history, f, indent=4)  

    return history


def solar_energy_potential(uv_index):
    if uv_index > 7:
        return f"{Fore.GREEN}Great solar energy potential today!"
    elif uv_index > 4:
        return f"{Fore.YELLOW}Moderate solar energy potential."
    else:
        return f"{Fore.RED}Low solar energy potential."


def sunscreen_suggestion(uv_index):
    if uv_index < 3:
        return f"{Fore.BLUE}Low UV: No sunscreen necessary unless you have sensitive skin."
    elif 3 <= uv_index < 6:
        return f"{Fore.YELLOW}Moderate UV: Apply broad-spectrum sunscreen with at least SPF 30. Reapply every 2 hours, especially if sweating or swimming."
    elif 6 <= uv_index < 8:
        return f"{Fore.YELLOW}High UV: Use broad-spectrum sunscreen with SPF 50+. Apply 15 minutes before going outdoors. Wear SPF-rated lip balm."
    else:
        return f"{Fore.RED}Very High UV: Use water-resistant SPF 50+ sunscreen. Apply every 2 hours, and more frequently if swimming or sweating. Consider zinc-based sunscreens for sensitive areas."


def skin_cancer_risk(uv_exposure_days, skin_type):
    risk_factor = uv_exposure_days * (1.5 if skin_type == "fair" else 1)
    
    if risk_factor > 100: 
        return f"{Fore.RED}High risk of skin cancer. Please consult a dermatologist."
    elif risk_factor > 50:
        return f"{Fore.YELLOW}Moderate risk. Consider reducing sun exposure."
    else:
        return f"{Fore.GREEN}Low risk, keep monitoring your sun exposure."


def best_time_for_outdoor(uv_forecast):
    best_time = min(uv_forecast, key=uv_forecast.get)
    return f"{Fore.GREEN}The best time for outdoor activities is {best_time}, with a UV index of {uv_forecast[best_time]}"


def vitamin_d_cal(uv_index, skin_type):
    if skin_type == "fair":
        exposure_time = 10 / uv_index
    elif skin_type == "medium":
        exposure_time = 20 / uv_index
    else:
        exposure_time = 30 / uv_index
    
    return f"{Fore.CYAN}To get enough Vitamin D, stay in the sun for {exposure_time:.2f} minutes."


def sunburn_recovery_tips(uv_exposure_days):
    if uv_exposure_days > 3:
        return f"{Fore.RED}Consider aloe vera and moisturizers to soothe your skin. Drink plenty of water."
    else:
        return f"{Fore.GREEN}Your skin seems fine, just maintain good hydration."



if __name__ == "__main__":
    latitude = input("Enter your latitude: ")
    longitude = input("Enter your longitude: ")
    
    # Fetch UV data and skincare tips
    uv_index = fetch_uv_data(latitude, longitude, API_KEY)
    print(skincare_tips(uv_index))
    
    # Send email notification
    send_notification(
        subject="UV Alert - Protect Your Skin!",
        message=f"Today's UV index is {uv_index}, which is high. Please apply SPF 50+ and avoid prolonged sun exposure.",
        to_email="YOUR_EMAIL"  # Replace with the recipient's email
    )

    # Track sun exposure
    user_id = "user567"
    skin_health = track_sun_exposure(user_id, latitude, longitude, uv_index)
    print(f"Skin health tracked: {skin_health}")

    # Check solar energy potential
    print(solar_energy_potential(uv_index))

    # Sunscreen suggestion
    print(sunscreen_suggestion(uv_index))

    # Risk of skin cancer
    print(skin_cancer_risk(skin_health['total_exposure'], "fair"))

    # Best time for outdoor activities
    uv_forecast = {'8:00 AM': 2, '12:00 PM': 8, '4:00 PM': 5}
    print(best_time_for_outdoor(uv_forecast))

    # Vitamin D calculation
    print(vitamin_d_cal(uv_index, "medium"))

    # Sunburn recovery tips
    print(sunburn_recovery_tips(skin_health['days']))

    # Fetch solar eclipse data
    eclipse_info = fetch_nasa_solar_eclipse_data()
    for info in eclipse_info:
        print(f"Date: {info[0]}, Type: {info[1]}, Location: {info[2]}")

    # Example UV trend data for plotting
    uv_trend_data = {
        'Day 1': 2,
        'Day 2': 5,
        'Day 3': 6,
        'Day 4': 8,
    }
    plot_uv_trends(uv_trend_data)

