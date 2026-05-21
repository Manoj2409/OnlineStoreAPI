from datetime import datetime


def validate_cart_dates_within_range(cart_dates, start, end):
    fmt = "%Y-%m-%d"
    start_date = datetime.strptime(start, fmt)
    end_date = datetime.strptime(end, fmt)

    for cart_date in cart_dates:
        parsed_date = datetime.strptime(cart_date[:10], fmt)
        if not start_date <= parsed_date <= end_date:
            return False

    return True
