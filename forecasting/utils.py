import datetime

def date_to_day(date_str):
    """Convert YYYY-MM-DD string to day of year"""
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date.timetuple().tm_yday
