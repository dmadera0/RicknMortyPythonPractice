# === IMPORTS ===
import requests       # For making HTTP requests to the Rick and Morty API
import sqlite3        # To store and query local database using SQLite
import time           # To pause between requests (so we don't overload the API)
import warnings       # Used to suppress SSL warnings specific to macOS

# === SUPPRESS MAC SSL WARNINGS (Optional) ===
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# === DATABASE CONNECTION ===
# This connects to a local SQLite database file. If it doesn't exist, it will be created.
conn = sqlite3.connect("rick_and_morty.db")
cursor = conn.cursor()  # Cursor is used to execute SQL commands

# === CREATE THE CHARACTERS TABLE IF IT DOESN'T EXIST ===
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    type TEXT,
    gender TEXT,
    origin TEXT,
    location TEXT,
    image TEXT
)
''')
conn.commit()

# === FUNCTION 1: Fetch Characters from the API and Store in DB ===
def fetch_and_store_characters():
    """
    Retrieves all character data from the Rick and Morty API (paginated),
    and stores them in the local SQLite database.
    """
    base_url = "https://rickandmortyapi.com/api/character"
    page = 1  # API is paginated, we start with page 1

    while True:
        url = f"{base_url}?page={page}"
        print(f"Requesting {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print("❌ Request failed or no more pages.")
            break

        try:
            data = response.json()
            characters = data.get("results", [])
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
            break

        if not characters:
            print("⚠️ No characters returned.")
            break

        for char in characters:
            print(f"Saving character: {char['name']}")
            cursor.execute('''
                INSERT OR REPLACE INTO characters (
                    id, name, status, species, type, gender, origin, location, image
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                char['id'],
                char['name'],
                char['status'],
                char['species'],
                char['type'],
                char['gender'],
                char['origin']['name'],
                char['location']['name'],
                char['image']
            ))

        conn.commit()
        print(f"✅ Page {page} stored.")
        page += 1
        time.sleep(0.2)  # Be respectful to the API server

# === FUNCTION 2: Find Characters by Name with Selection ===
def find_character_by_name():
    """
    Prompts the user to input a partial or full character name.
    Shows a list of matches and allows the user to select one
    to view full details.
    """
    name = input("Enter partial or full character name: ").strip()
    cursor.execute("SELECT * FROM characters WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()

    if not results:
        print("❌ No characters found.")
        return

    print("\n🔎 Matching Characters:")
    for idx, r in enumerate(results, 1):
        print(f"{idx}. {r[1]} (ID: {r[0]}, Species: {r[3]})")

    try:
        choice = int(input("Select a number to view full profile: ").strip())
        selected = results[choice - 1]
    except (IndexError, ValueError):
        print("⚠️ Invalid selection.")
        return

    print("\n📄 Character Profile:")
    print(f"ID: {selected[0]}")
    print(f"Name: {selected[1]}")
    print(f"Status: {selected[2]}")
    print(f"Species: {selected[3]}")
    print(f"Type: {selected[4]}")
    print(f"Gender: {selected[5]}")
    print(f"Origin: {selected[6]}")
    print(f"Location: {selected[7]}")
    print(f"Image: {selected[8]}")

# === FUNCTION 3: Find Characters by Species ===
def find_characters_by_species():
    """
    Displays all available species, allows the user to select one,
    and then lists all characters matching that species.
    """
    cursor.execute("SELECT DISTINCT species FROM characters WHERE species != '' ORDER BY species")
    species_list = [row[0] for row in cursor.fetchall()]

    print("\n🧬 Available Species:")
    for idx, sp in enumerate(species_list, 1):
        print(f"{idx}. {sp}")

    try:
        choice = int(input("Select a species by number: ").strip())
        selected_species = species_list[choice - 1]
    except (IndexError, ValueError):
        print("⚠️ Invalid selection.")
        return

    cursor.execute("SELECT * FROM characters WHERE species = ?", (selected_species,))
    characters = cursor.fetchall()

    print(f"\n👽 Characters with Species '{selected_species}':")
    for r in characters:
        print(f"- {r[1]} (ID: {r[0]}, Status: {r[2]}, Gender: {r[5]})")

# === FUNCTION 4: List Characters by Location ===
def list_characters_by_location():
    """
    Displays a dropdown of all character locations.
    Prompts the user to select one and shows all characters at that location.
    """
    cursor.execute("SELECT DISTINCT location FROM characters WHERE location != '' ORDER BY location")
    locations = [row[0] for row in cursor.fetchall()]

    print("\n📍 Available Locations:")
    for idx, loc in enumerate(locations, 1):
        print(f"{idx}. {loc}")

    try:
        choice = int(input("Select a location by number: ").strip())
        selected_location = locations[choice - 1]
    except (IndexError, ValueError):
        print("⚠️ Invalid selection.")
        return

    cursor.execute("SELECT * FROM characters WHERE location = ?", (selected_location,))
    characters = cursor.fetchall()

    print(f"\n🌍 Characters located at '{selected_location}':")
    for r in characters:
        print(f"- {r[1]} (ID: {r[0]}, Species: {r[3]}, Gender: {r[5]})")

# === FUNCTION 5: Print All Characters ===
def print_all_characters():
    """
    Lists all characters in the database with basic information.
    """
    cursor.execute("SELECT * FROM characters")
    results = cursor.fetchall()

    if not results:
        print("⚠️ No characters found. Try option 1 to fetch them first.")
        return

    print("\n📋 All Characters:")
    for r in results:
        print(f"ID: {r[0]}, Name: {r[1]}, Status: {r[2]}, Species: {r[3]}, Gender: {r[5]}, Origin: {r[6]}, Location: {r[7]}")

# === FUNCTION 6: Filter Characters by Status or Gender ===
def filter_characters_by_status_or_gender():
    """
    Allows the user to filter characters using status and/or gender.
    Both filters are optional.
    """
    # Get available status options
    cursor.execute("SELECT DISTINCT status FROM characters WHERE status != '' ORDER BY status")
    statuses = [row[0] for row in cursor.fetchall()]
    
    print("\n🧠 Available Statuses:")
    for i, s in enumerate(statuses, 1):
        print(f"{i}. {s}")
    
    try:
        status_choice = input("Select status number or press Enter to skip: ").strip()
        selected_status = statuses[int(status_choice)-1] if status_choice else None
    except (ValueError, IndexError):
        selected_status = None

    # Get available gender options
    cursor.execute("SELECT DISTINCT gender FROM characters WHERE gender != '' ORDER BY gender")
    genders = [row[0] for row in cursor.fetchall()]

    print("\n🧠 Available Genders:")
    for i, g in enumerate(genders, 1):
        print(f"{i}. {g}")

    try:
        gender_choice = input("Select gender number or press Enter to skip: ").strip()
        selected_gender = genders[int(gender_choice)-1] if gender_choice else None
    except (ValueError, IndexError):
        selected_gender = None

    # Build query dynamically
    query = "SELECT * FROM characters WHERE 1=1"
    params = []

    if selected_status:
        query += " AND status = ?"
        params.append(selected_status)
    if selected_gender:
        query += " AND gender = ?"
        params.append(selected_gender)

    cursor.execute(query, params)
    characters = cursor.fetchall()

    print("\n🎯 Filtered Characters:")
    if not characters:
        print("No characters matched your filters.")
    else:
        for r in characters:
            print(f"- {r[1]} (ID: {r[0]}, Status: {r[2]}, Gender: {r[5]}, Species: {r[3]}, Location: {r[7]})")

# === MAIN MENU LOOP ===
def main():
    """
    The CLI interface loop that displays menu options and handles user input.
    """
    print("\n🎓 Welcome to the Rick and Morty Database CLI")

    while True:
        # Print the menu options
        print("\n📘 Choose an option:")
        print("1. Fetch & Store Characters from API")
        print("2. Find Character by Name (with match list)")
        print("3. Find Characters by Species (choose from list)")
        print("4. List Characters by Location (choose from list)")
        print("5. Print All Characters in Database")
        print("6. Exit")
        print("7. Filter Characters by Status or Gender")

        # Take user input
        choice = input("\nEnter a choice (1-7): ").strip()

        # Match user input to function calls
        if choice == '1':
            fetch_and_store_characters()
        elif choice == '2':
            find_character_by_name()
        elif choice == '3':
            find_characters_by_species()
        elif choice == '4':
            list_characters_by_location()
        elif choice == '5':
            print_all_characters()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        elif choice == '7':
            filter_characters_by_status_or_gender()
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 7.")

# === RUN THE PROGRAM ===
if __name__ == '__main__':
    main()
