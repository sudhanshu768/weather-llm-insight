# 🌤️ Weather LLM Insight

A smart weather analysis system using:

* 🌦️ WeatherAPI (data source)
* 🤖 Google Gemini (LLM for explanation)

## 🚀 Flow

User → Backend → Weather API → Backend → Gemini → Output

⚠️ LLM does NOT call APIs (clean architecture)

## 🔧 Features

* Current weather
* Historical weather (date-based)
* Temperature comparison
* Natural language queries

## 🛠️ Tech Stack

* Python
* WeatherAPI
* Gemini API
* dotenv

## ▶️ Run

```bash
python -m app.main
```

## 🔐 Setup

Create `.env`:

```
WEATHER_API_KEY=your_key
GEMINI_API_KEY=your_key
```

## 📌 Example Queries

* temperature today in pune
* did it rain yesterday in mumbai
* what was the temperature on 30 march 2026
* compare today and yesterday temperature in delhi
