import requests

# Replace 'your_api_key_here' with your actual API key
api_key ="78f5ce31-1838-48d1-be5a-8e373dedb9c6"
country = 'IN'  # Example: United States
year = 2024  # Example: Year 2024

response = requests.get(
    f"https://holidayapi.com/v1/holidays?pretty&key={api_key}&country={country}&year={year}"
)

holidays = response.json()
print(holidays)
