import os
from datetime import date, timedelta
import requests

COUNTRY_CODE = "MX"

DAYS_OF_WEEK_SPANISH = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes"
}

PARKING_WEEKDAYS = [0, 1, 2, 3]

MONTHS_IN_SPANISH = {
    "1": "Enero",
    "2": "Febrero",
    "3": "Marzo",
    "4": "Abril",
    "5": "Mayo",
    "6": "Junio",
    "7": "Julio",
    "8": "Agosto",
    "9": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
}

def get_next_weekdays():
    today = date.today()
    days_until_monday = (7 - today.weekday()) % 7
    next_monday = today + timedelta(days=days_until_monday)

    return [
        next_monday + timedelta(days=i)
        for i in PARKING_WEEKDAYS  # Monday-Thursday
    ]

def get_mexico_holidays(year: int):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{COUNTRY_CODE}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    holidays = response.json()

    return {
        date.fromisoformat(holiday["date"])
        for holiday in holidays
        if holiday.get("global") is True
    }

def get_parking_days():
    weekdays = get_next_weekdays()

    holiday_years = {day.year for day in weekdays}
    holidays = set()

    for year in holiday_years:
        holidays |= get_mexico_holidays(year)

    return [
        day
        for day in weekdays
        if day not in holidays
    ]

def format_email_subject(parking_days: list[date]):
    first_day = parking_days[0].strftime("%-d")
    first_month = MONTHS_IN_SPANISH[parking_days[0].strftime("%-m")]
    last_day = parking_days[-1].strftime("%-d")
    last_month = MONTHS_IN_SPANISH[parking_days[-1].strftime("%-m")]

    subject = f"Estacionamiento de {first_month} {first_day} a {last_month} {last_day} - Daniel González Cervantes"
    return subject

def get_vehicle_details():
    vehicle_model = os.getenv("VEHICLE_MODEL")
    vehicle_color = os.getenv("VEHICLE_COLOR")
    vehicle_plates = os.getenv("VEHICLE_PLATES")

    if not vehicle_model:
        raise ValueError("VEHICLE_MODEL is not set")

    if not vehicle_color:
        raise ValueError("VEHICLE_COLOR is not set")

    if not vehicle_plates:
        raise ValueError("VEHICLE_PLATES is not set")

    return vehicle_model, vehicle_color, vehicle_plates

def format_email_body(parking_days: list[date]):
    vehicle_model, vehicle_color, vehicle_plates = get_vehicle_details()

    lines = ["Hola! buenas tardes, estos son los días de la siguiente semana en los que necesitaré el estacionamiento en Tokio 12:", ""]

    for day in parking_days:
        day_of_week_in_spanish = DAYS_OF_WEEK_SPANISH[day.strftime("%A")]
        day_number = day.strftime("%-d")
        month_in_spanish = MONTHS_IN_SPANISH[day.strftime("%-m")]

        lines.append(f"\t\u2022 {day_of_week_in_spanish} {day_number} de {month_in_spanish}" )
    
    lines.append(f"\nDatos de mi vehículo:\n\t\u2022 {vehicle_model}\n\t\u2022 Color: {vehicle_color}\n\t\u2022 Placas: {vehicle_plates}")

    lines.append("\nDaniel González Cervantes")

    return "\n".join(lines)

def get_email_body():
    parking_days = get_parking_days()
    subject = format_email_subject(parking_days)
    body = format_email_body(parking_days)

    print(subject)
    print(body)
    return body, subject

if __name__ == "__main__":
    get_email_body()
