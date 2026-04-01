from app.weather_service import get_weather_data
from app.llm_service import explain_weather
from app.utils import parse_query


def run():
    query = input("Ask your question: ")

    city, compare_type, custom_date = parse_query(query)

    weather_data = get_weather_data(
        city=city,
        compare_type=compare_type,
        custom_date=custom_date
    )

    result = explain_weather(query, weather_data)

    print("\n🌤️ Result:\n")
    print(result)
    print("Parsed:", city, compare_type, custom_date)


if __name__ == "__main__":
    run()