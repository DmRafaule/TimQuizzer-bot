import json


async def update_user(user_id: str, key: str, value) -> None:
    with open(f"user_{user_id}.json", "r", encoding="utf-8") as file:
        user_values = json.load(file)
        user_values[key] = value
    with open(f"user_{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(user_values, file)


async def is_user_completed(user_id: str) -> bool:
    with open(f"user_{user_id}.json", "r", encoding="utf-8") as file:
        user_values = json.load(file)
        user_values["is_complete"] = True
        for key in user_values:
            if user_values[key] is None:
                user_values["is_complete"] = False
                return False
    return True
