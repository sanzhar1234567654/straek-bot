from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime
import calendar

app = FastAPI()

class DateRequest(BaseModel):
    dates: List[str]

def format_calendar(dates: List[str]) -> str:
    # Преобразуем строки в объекты datetime
    target_dates = [datetime.strptime(d, "%d-%m-%Y").date() for d in dates]
    if not target_dates:
        return "Нет дат для отображения."

    year = target_dates[0].year
    month = target_dates[0].month

    # Календарная структура месяца
    cal = calendar.Calendar(firstweekday=0)  # неделя с понедельника
    month_days = cal.monthdayscalendar(year, month)

    # Даты с галочками
    day_set = {d.day for d in target_dates if d.month == month and d.year == year}

    # Заголовок
    output = f"Календарь активностей для {year}-{month:02}:\n"
    output += "Пн Вт Ср Чт Пт Сб Вс\n"

    for week in month_days:
        for day in week:
            if day == 0:
                output += "   "
            elif day in day_set:
                output += "✅ "
            else:
                output += f"{day:2} "
        output += "\n"

    return output.strip()

@app.post("/calendar")
async def get_calendar(data: DateRequest):
    try:
        calendar_output = format_calendar(data.dates)
        return {"calendar": calendar_output}
    except ValueError as e:
        return {"error": f"Неверный формат даты: {e}"}
