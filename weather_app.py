import tkinter as tk
import requests
import time
import logging


class WeatherApp(tk.Tk):
    """
    A simple weather application using Tkinter.
    """

    def __init__(self):
        """
        Initialize the WeatherApp class.
        """
        super().__init__()
        self.geometry("500x500")
        self.title("Weather App")
        self.font_large = ("Arial", 30)
        self.font_small = ("Arial", 12)
        self.weather_emojis = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Smoke': '🌫️',
            'Haze': '🌫️',
            'Dust': '🌫️',
            'Fog': '🌫️',
        }

        self.create_widgets()
        self.eval('tk::PlaceWindow . center')

        # Configure logging
        logging.basicConfig(filename='weather_app.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def create_widgets(self):
        """
        Create the user interface.
        """
        # Create label for city name input
        question_label = tk.Label(self, text="Enter the city name:", font=(self.font_large[0], self.font_large[1]))
        question_label.pack()

        # Create text field for city name input
        self.text_field = tk.Entry(self, justify='center', width=20, font=self.font_large)
        self.text_field.pack(pady=10)
        self.text_field.focus()
        self.text_field.bind('<Return>', self.get_weather)

        # Create button to fetch weather information
        enter_button = tk.Button(self, text="Get Weather", font=self.font_small, command=self.get_weather)
        enter_button.pack()

        # Create clear button
        clear_button = tk.Button(self, text="Clear", font=self.font_small, command=self.clear_weather)
        clear_button.pack()

        # Create labels to display weather information
        self.label1 = tk.Label(self, font=self.font_large)
        self.label1.pack()
        self.label2 = tk.Label(self, font=self.font_small)
        self.label2.pack()

        # Create label for guidance
        guidance_label = tk.Label(self, text="Press Enter or click 'Get Weather' to fetch weather information.\n"
                                             "Use 'Clear' to clear the displayed weather information.", font=self.font_small)
        guidance_label.pack(pady=10)

    def get_weather(self, event=None):
        """
        Fetch weather information from the API and update the labels.
        """
        try:
            city = self.text_field.get()
            api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid='enter_your_generated_app_id'"

            # Fetch weather data from the API
            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise_timestamp = json_data['sys']['sunrise']
            sunset_timestamp = json_data['sys']['sunset']

            # Format sunrise and sunset times
            sunrise = time.strftime('%I:%M:%S %p', time.gmtime(sunrise_timestamp - 21600))
            sunset = time.strftime('%I:%M:%S %p', time.gmtime(sunset_timestamp - 21600))

            # Prepare the final weather information strings
            final_info = f"{self.weather_emojis.get(condition, '')} {condition}\n{temp}°C"
            final_data = (
                f"\nMin Temp: {min_temp}°C\n"
                f"Max Temp: {max_temp}°C\n"
                f"Pressure: {pressure}\n"
                f"Humidity: {humidity}\n"
                f"Wind Speed: {wind}\n"
                f"Sunrise: {sunrise}\n"
                f"Sunset: {sunset}"
            )

            # Update the labels with weather information
            self.label1.config(text=final_info)
            self.label2.config(text=final_data)

            # Log weather retrieval success
            logging.info(f"Weather retrieved successfully for {city}")

        except requests.exceptions.ConnectionError:
            # Handle connection error
            error_message = "⚠️ Connection Error: Please check your internet connection."
            self.label1.config(text=error_message, font=self.font_small)
            self.label2.config(text="")

            # Log connection error
            logging.error(f"Connection Error occurred: {error_message}")

        except KeyError:
            # Handle invalid city or missing weather data
            error_message = "⚠️ City not found. Please enter a valid city name."
            self.label1.config(text=error_message, font=self.font_small)
            self.label2.config(text="")

            # Log invalid city error
            logging.error(f"Invalid city or missing weather data: {error_message}")

    def clear_weather(self):
        """
        Clear the displayed weather information.
        """
        self.text_field.delete(0, tk.END)
        self.label1.config(text="")
        self.label2.config(text="")


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
