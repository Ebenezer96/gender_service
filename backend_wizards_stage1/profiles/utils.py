def get_age_group(age: int) -> str:
    if 0 <= age <= 12:
        return "child"
    elif 13 <= age <= 19:
        return "teenager"
    elif 20 <= age <= 59:
        return "adult"
    else:
        return "senior"


def get_top_country(countries: list):
    if not countries:
        return None

    return max(countries, key=lambda c: c["probability"])