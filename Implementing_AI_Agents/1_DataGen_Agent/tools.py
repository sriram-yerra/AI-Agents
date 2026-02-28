from langchain_core.tools import tool
import random, json, string
from datetime import datetime, timedelta
from typing import List
from tabulate import tabulate


@tool
def write_json(filepath: str, data: dict) -> str:
    """
    Save a list of users into a JSON file.
    Use this ONLY when the user explicitly asks to save users to a file.
    The file_path must be a valid file name like 'users.json'.
    """                                                                      
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"Successfully wrote JSON data to '{filepath}' ({len(json.dumps(data))} characters)."
    except Exception as e:
        return f"Error writing JSON: {str(e)}"


@tool
def read_json(filepath: str) -> str:
    """
    Read a JSON file from disk.
    Use this ONLY when the user asks to read an existing JSON file.
    Do NOT use this for generating users.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found."
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON in file - {str(e)}"
    except Exception as e:
        return f"Error reading JSON: {str(e)}"


@tool
def generate_sample_users(
        first_names: List[str],
        last_names: List[str],
        domains: List[str],
        min_age: int,
        max_age: int
) -> dict:
    """
    Generate random sample users.

    Use this for ANY request related to:
    - generating users
    - creating fake data
    - sample data
    """
    # Validation
    if not first_names:
        return {"error": "first_names list cannot be empty"}
    if not last_names:
        return {"error": "last_names list cannot be empty"}
    if not domains:
        return {"error": "domains list cannot be empty"}
    if min_age > max_age:
        return {"error": f"min_age ({min_age}) cannot be greater than max_age ({max_age})"}
    if min_age < 0 or max_age < 0:
        return {"error": "ages must be non-negative"}

    users = []
    count = len(first_names)

    for i in range(count):
        first = first_names[i]
        last = last_names[i % len(last_names)]
        domain = domains[i % len(domains)]
        email = f"{first.lower()}.{last.lower()}@{domain}"

        user = {
            "id": i + 1,
            "firstName": first,
            "lastName": last,
            "email": email,
            "username": f"{first.lower()}{random.randint(100, 999)}",
            "age": random.randint(min_age, max_age),
            "registeredAt": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        }
        users.append(user)

    return {"users": users, "count": len(users)}

DEFAULT_PATH = "/home/sriram/Documents/OnGoing Github Repos/AI-Agents/Implementing AI Agents/Basic AI Agent/users.json"

@tool
def show_users_table():
    """
    Display users in table format from the default users.json file.
    Use this when the user asks to show, display, list, or view users.
    """
    try:
        with open(DEFAULT_PATH, "r") as f:
            users = json.load(f)

        if not users:
            return "No users found."

        headers = users[0].keys()
        rows = [user.values() for user in users]

        table = tabulate(rows, headers=headers, tablefmt="grid")
        return table, len(table)

    except Exception as e:
        return f"Error reading users: {str(e)}"
    

@tool
def update_user_by_name(file_path: str, user_name: str, field: str, new_value: str) -> str:
    """
    Updates a specific field of a user by name.
    """

    try:
        with open(file_path, "r") as f:
            users = json.load(f)

        updated = False

        for user in users:
            full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()

            if user_name.lower() == full_name.lower():
                user[field] = new_value
                updated = True
                break

        if not updated:
            return f"User '{user_name}' not found."

        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)

        return f"User '{user_name}' updated successfully."

    except Exception as e:
        return f"Error updating user: {str(e)}"
