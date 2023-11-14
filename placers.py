from config import ages, countries, sexes, works, cars


def place_age(template: str, users: list, formater: callable) -> str:
    for age in ages:
        age_num = 0
        for user in users:
            if age in user['age']:
                age_num += 1
        pos_to_insert = template.find("\n", template.find(age))
        template = template[:pos_to_insert] + formater(age_num, len(users)) + template[pos_to_insert:]
    return template


def place_country(template: str, users: list, formater: callable) -> str:
    for country in countries:
        country_num = 0
        for user in users:
            if country["name"] in user['country']:
                country_num += 1
        if country_num > 0:
            pos_to_insert = template.find('\n', template.find("Страна"))
            template = template[:pos_to_insert] + formater(country_num, len(users), prefix="\n\t• " + country["emoji"] + " " + country["name"] + "\t") + template[pos_to_insert:]
    return template


def place_sex(template: str, users: list, formater: callable) -> str:
    for sex in sexes:
        sex_num = 0
        for user in users:
            if sex in user['sex']:
                sex_num += 1
        pos_to_insert = template.find('\n', template.find(sex[:5]))
        template = template[:pos_to_insert] + formater(sex_num, len(users)) + template[pos_to_insert:]
    return template


def place_work(template: str, users: list, formater: callable) -> str:
    for work in works:
        profession_num = 0
        for user in users:
            if work in user['work']:
                profession_num += 1
        pos_to_insert = template.find('\n', template.find(work))
        template = template[: pos_to_insert] + formater(profession_num, len(users)) + template[pos_to_insert:]
    return template


def place_car(template: str, users: list, formater: callable) -> str:
    for car in cars:
        has_car_num = 0
        for user in users:
            if car in user['car']:
                has_car_num += 1
        pos_to_insert = template.find('\n', template.find(car))
        template = template[: pos_to_insert] + formater(has_car_num, len(users)) + template[pos_to_insert:]
    return template
