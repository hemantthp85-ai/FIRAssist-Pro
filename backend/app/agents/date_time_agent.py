import re
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
from app.utils.performance import timed_agent


# Month mapping for various formats
MONTH_MAP = {
    'january': 1, 'jan': 1,
    'february': 2, 'feb': 2,
    'march': 3, 'mar': 3,
    'april': 4, 'apr': 4,
    'may': 5,
    'june': 6, 'jun': 6,
    'july': 7, 'jul': 7,
    'august': 8, 'aug': 8,
    'september': 9, 'sep': 9, 'sept': 9,
    'october': 10, 'oct': 10,
    'november': 11, 'nov': 11,
    'december': 12, 'dec': 12,
}

# Time patterns
TIME_PATTERNS = [
    r'(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)',  # 9:30 PM
    r'(\d{1,2})\s*:\s*(\d{2})\s*(?:o\'clock|o\'clock)',  # 9:30 o'clock
    r'around\s+(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)',  # around 9:30 PM
    r'about\s+(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)',  # about 9:30 PM
]

# Date patterns
DATE_PATTERNS = [
    r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\s+(\d{4})',  # 14 January 2026
    r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)(?:\s+(\d{4}))?',  # 14 January or 14 January 2026
    r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2026-06-14
    r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 14/06/2026
    r'(\d{1,2})-(\d{1,2})-(\d{4})',  # 14-06-2026
]

# Relative date patterns
RELATIVE_PATTERNS = [
    (r'\byesterday\b', -1),
    (r'\btoday\b', 0),
    (r'\btomorrow\b', 1),
]


def extract_time(text: str) -> str:
    """Extract time from text in HH:MM AM/PM format."""
    
    if not text:
        return ""
    
    # Search for time patterns
    for pattern in TIME_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = match.group(2)
            period = match.group(3).upper()
            
            # Convert to 24-hour format for validation
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            
            # Format back to 12-hour format
            if hour == 0:
                hour_12 = 12
                period = 'AM'
            elif hour < 12:
                hour_12 = hour
                period = 'AM'
            elif hour == 12:
                hour_12 = 12
                period = 'PM'
            else:
                hour_12 = hour - 12
                period = 'PM'
            
            return f"{hour_12}:{minute} {period}"
    
    return ""


def parse_date_with_month_name(text: str) -> datetime:
    """Parse date with month name like '14 January 2026'."""
    
    # Pattern: day month [year]
    pattern = r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)(?:\s+(\d{4}))?'
    
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year = int(match.group(3)) if match.group(3) else datetime.now().year
        
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                return datetime(year, month, day)
            except ValueError:
                return None
    
    return None


def parse_numeric_date(text: str) -> datetime:
    """Parse numeric dates like 2026-06-14, 14/06/2026, 14-06-2026."""
    
    # Try YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
    if match:
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return datetime(year, month, day)
        except ValueError:
            pass
    
    # Try DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return datetime(year, month, day)
        except ValueError:
            pass
    
    # Try DD-MM-YYYY
    match = re.search(r'(\d{1,2})-(\d{1,2})-(\d{4})', text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        try:
            return datetime(year, month, day)
        except ValueError:
            pass
    
    return None


def parse_relative_date(text: str) -> datetime:
    """Parse relative dates like 'today', 'yesterday', 'tomorrow'."""
    
    now = datetime.now()
    
    for pattern, offset in RELATIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return now + timedelta(days=offset)
    
    return None


def extract_dates_from_text(text: str) -> list:
    """Extract all dates from text and return as list."""
    
    dates = []
    seen_dates = set()
    
    # Try month name patterns first (more reliable)
    # Find all occurrences of date patterns like "14 January 2026"
    pattern = r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)(?:\s+(\d{4}))?'
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year = int(match.group(3)) if match.group(3) else datetime.now().year
        
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                date_obj = datetime(year, month, day)
                date_str = date_obj.strftime("%Y-%m-%d")
                if date_str not in seen_dates:
                    dates.append(date_obj)
                    seen_dates.add(date_str)
            except ValueError:
                pass
    
    # Try numeric patterns
    for pattern_str in [r'(\d{4})-(\d{1,2})-(\d{1,2})', r'(\d{1,2})/(\d{1,2})/(\d{4})', r'(\d{1,2})-(\d{1,2})-(\d{4})']:
        for match in re.finditer(pattern_str, text):
            if pattern_str == r'(\d{4})-(\d{1,2})-(\d{1,2})':
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            elif pattern_str == r'(\d{1,2})/(\d{1,2})/(\d{4})':
                day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
            else:  # DD-MM-YYYY
                day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
            
            try:
                date_obj = datetime(year, month, day)
                date_str = date_obj.strftime("%Y-%m-%d")
                if date_str not in seen_dates:
                    dates.append(date_obj)
                    seen_dates.add(date_str)
            except ValueError:
                pass
    
    # Try relative patterns
    for pattern_str, offset in RELATIVE_PATTERNS:
        if re.search(pattern_str, text, re.IGNORECASE):
            now = datetime.now()
            date_obj = now + timedelta(days=offset)
            date_str = date_obj.strftime("%Y-%m-%d")
            if date_str not in seen_dates:
                dates.append(date_obj)
                seen_dates.add(date_str)
    
    # Try parsing with dateutil as fallback for any missed dates
    try:
        parsed = dateutil_parser.search_dates(text, fuzzy=True)
        if parsed:
            for date_str, date_obj in parsed:
                # Only accept dates not in the future (unless very close)
                if date_obj.year <= datetime.now().year + 1:
                    date_str_key = date_obj.strftime("%Y-%m-%d")
                    if date_str_key not in seen_dates:
                        dates.append(date_obj)
                        seen_dates.add(date_str_key)
    except:
        pass
    
    # Sort by date descending (most recent first)
    return sorted(dates, reverse=True)


def extract_most_recent_date(text: str) -> str:
    """Extract the most recent date from text and return formatted as 'DD Month YYYY'."""
    
    if not text:
        return ""
    
    dates = extract_dates_from_text(text)
    
    if dates:
        # Return the most recent date
        date_obj = dates[0]
        # Format: "14 January 2026"
        return date_obj.strftime("%d %B %Y").lstrip("0") if date_obj.day < 10 else date_obj.strftime("%d %B %Y")
    
    return ""


def clean_date_string(date_str: str) -> str:
    """Clean and normalize date strings."""
    
    if not date_str:
        return ""
    
    # Remove phrases that are not dates
    invalid_phrases = [
        'stalked', 'abused', 'theft', 'fraud', 'robbery',
        'harassment', 'assault', 'incident', 'complaint',
        'on', 'at', 'around', 'about', 'and', 'or'
    ]
    
    lower_text = date_str.lower()
    for phrase in invalid_phrases:
        if lower_text == phrase or (len(invalid_phrases) == 1 and lower_text.startswith(phrase)):
            return ""
    
    return date_str.strip()


@timed_agent("date_time_agent.extract")
def extract_date_and_time(text: str) -> dict:
    """
    Main function to extract date and time from complaint text.
    
    Returns:
        {
            "date": "14 January 2026",  # or empty string
            "time": "9:30 PM",  # or empty string
            "all_dates": ["14 January 2026", "12 January 2026"],  # all found dates
        }
    """
    
    if not text:
        return {
            "date": "",
            "time": "",
            "all_dates": []
        }
    
    # Extract time first
    time = extract_time(text)
    
    # Extract most recent date
    date = extract_most_recent_date(text)
    
    # Extract all dates
    all_dates = extract_dates_from_text(text)
    all_dates_formatted = [
        (d.strftime("%d %B %Y").lstrip("0") if d.day < 10 else d.strftime("%d %B %Y"))
        for d in all_dates
    ]
    
    # Clean date string
    date = clean_date_string(date)
    
    return {
        "date": date,
        "time": time,
        "all_dates": all_dates_formatted
    }


@timed_agent("date_time_agent.timeline")
def parse_incident_timeline(text: str) -> dict:
    """
    Parse multiple incidents from text and return timeline.
    
    Returns:
        {
            "primary_incident": {
                "date": "14 January 2026",
                "time": "9:30 PM",
                "description": "abused"
            },
            "related_incidents": [
                {
                    "date": "12 January 2026",
                    "time": "",
                    "description": "stalked"
                }
            ]
        }
    """
    
    result = extract_date_and_time(text)
    
    primary_date = result['date']
    primary_time = result['time']
    all_dates = result['all_dates']
    
    # Extract incident descriptions
    incident_keywords = {
        'stalked': 'Stalking',
        'abused': 'Abuse',
        'theft': 'Theft',
        'stolen': 'Theft',
        'fraud': 'Fraud',
        'scam': 'Fraud',
        'harassment': 'Harassment',
        'assault': 'Assault',
        'kidnapped': 'Kidnapping',
        'abducted': 'Kidnapping',
    }
    
    description = ""
    for keyword, incident_type in incident_keywords.items():
        if keyword.lower() in text.lower():
            description = incident_type
            break
    
    related = []
    for date_str in all_dates[1:]:  # All except the first (primary)
        related.append({
            "date": date_str,
            "time": "",
            "description": ""
        })
    
    return {
        "primary_incident": {
            "date": primary_date,
            "time": primary_time,
            "description": description
        },
        "related_incidents": related,
        "total_incidents": len(all_dates)
    }


if __name__ == "__main__":
    
    # Test cases
    test_cases = [
        "Stalked on 12 Jan and abused on 14 Jan at 9:30 PM",
        "On 5 June 2026 at around 6:30 PM, my phone was stolen",
        "Yesterday at 3:45 PM someone stole my wallet",
        "Theft happened on 14/06/2026 at 2:00 AM",
        "Incident on 14-06-2026",
        "It happened today around 5:30 PM",
        "14 January 2026 at 9:30 PM near the market",
    ]
    
    for test in test_cases:
        print(f"\nInput: {test}")
        result = extract_date_and_time(test)
        print(f"Output: {result}")
        
        timeline = parse_incident_timeline(test)
        print(f"Timeline: {timeline}")
