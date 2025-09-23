import json
import random

def generate_nickname(json_file_path="words.json"):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            adjectives = data.get("adjectives")
            nouns = data.get("nouns")

            if adjectives and nouns:
                adjective = random.choice(adjectives)
                noun = random.choice(nouns)
                number = random.randint(0, 99)

                nickname = f"{adjective}{noun}{number}"
                return nickname
            else:
                return "Fehler: Adjektive oder Nomen in der JSON-Datei fehlen."

    except FileNotFoundError:
        return "Fehler: JSON-Datei nicht gefunden."
    except json.JSONDecodeError:
        return "Fehler: JSON-Datei ist ungültig."
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}"