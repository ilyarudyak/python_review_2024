import datetime, zoneinfo

def get_datetime_from_string(datetime_str):
    """
    Extracts the date and time from a string includime the timezone
    using datetime module. Example string:
    Wed, Sep 4, 2024 11:59 AM UTC
    """
        # Define the format string
    format_str = '%a, %b %d, %Y %I:%M %p %Z'
    
    # Parse the string into a datetime object
    dt_naive = datetime.datetime.strptime(datetime_str, format_str)

    # Attach the UTC timezone to the naive datetime object
    dt_aware = dt_naive.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
    
    return dt_aware


if __name__ == "__main__":
    datetime_str = "Wed, Sep 4, 2024 11:59 AM UTC"
    dt = get_datetime_from_string(datetime_str)
    print(dt)
    print(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.tzinfo)



