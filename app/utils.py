import re
from dateutil import parser


def extract_date_from_text(text):
    # Match patterns like "30 march 2026"
    pattern = r"\b\d{1,2}\s+\w+\s+\d{4}\b"
    match = re.search(pattern, text)

    if match:
        try:
            return parser.parse(match.group())
        except:
            return None

    return None


def parse_query(query: str):
    query_lower = query.lower()

    # city detection
    city = "pune"
    if "mumbai" in query_lower:
        city = "mumbai"
    elif "delhi" in query_lower:
        city = "delhi"

    compare = None
    custom_date = None

    # relative keywords
    if "yesterday" in query_lower:
        compare = "yesterday"
    elif "last month" in query_lower:
        compare = "last_month"
    elif "last year" in query_lower:
        compare = "last_year"

    # 🔥 NEW: robust date extraction
    custom_date = extract_date_from_text(query_lower)

    print("[DEBUG] Parsed:", city, compare, custom_date)

    return city, compare, custom_date