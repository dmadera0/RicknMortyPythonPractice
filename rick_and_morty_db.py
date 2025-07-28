import requests
import sqlite3
import time

# === Part 1: Setup Database === #

# Establish connection to SQLite (file-based) database.
# If the file does not exist, it will be created.
conn = sqlite3.connect('rick_and_morty.db')
cursor = conn.cursor()

# Create a table to store character data.
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

# === Part 2: Fetch Data from API === #

def fetch_and_store_characters():
    """
    This function fetches character data from the Rick and Morty API and stores it in the SQLite database.
    """

    base_url = "https://rickandmortyapi.com/api/character"
    page = 1

    while True:
        response = requests.get(f"{base_url}?page={page}")

        if response.status_code != 200:
            print("Finished fetching all characters.")
            break

        data = response.json()
        characters = data['results']

        for char in characters:
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
        page += 1
        time.sleep(0.25)  # be respectful to the API server

# === Part 3: Query Functions === #

def find_character_by_name(name):
    """
    Find a single character by name.
    """
    cursor.execute("SELECT * FROM characters WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    return results


def list_similar_characters(character_name):
    """
    Given a character name, find other characters with similar traits (species, origin).
    """
    cursor.execute("SELECT species, origin FROM characters WHERE name = ?", (character_name,))
    match = cursor.fetchone()

    if not match:
        return []

    species, origin = match

    cursor.execute(
        "SELECT * FROM characters WHERE (species = ? OR origin = ?) AND name != ?",
        (species, origin, character_name)
    )
    return cursor.fetchall()


def list_character_traits(name):
    """
    Display the traits of a character.
    """
    cursor.execute("SELECT * FROM characters WHERE name LIKE ?", ('%' + name + '%',))
    return cursor.fetchall()


# === Part 4: CLI Interaction for Learning Purposes === #

def main():
    print("Welcome to the Rick and Morty DB Interface!")
    print("1. Fetch & Store Characters")
    print("2. Find Character by Name")
    print("3. Find Similar Characters")
    print("4. List Character Traits")
    print("5. Exit")

    while True:
        choice = input("\nEnter a choice: ")

        if choice == '1':
            fetch_and_store_characters()
            print("Characters fetched and stored!")
        elif choice == '2':
            name = input("Enter character name: ")
            results = find_character_by_name(name)
            for r in results:
                print(r)
        elif choice == '3':
            name = input("Enter base character name: ")
            results = list_similar_characters(name)
            for r in results:
                print(r)
        elif choice == '4':
            name = input("Enter character name: ")
            results = list_character_traits(name)
            for r in results:
                print(f"ID: {r[0]}, Name: {r[1]}, Status: {r[2]}, Species: {r[3]}, Type: {r[4]}, Gender: {r[5]}, Origin: {r[6]}, Location: {r[7]}")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# This block ensures that if the script is run directly, it will start the CLI.
if __name__ == '__main__':
    main()
