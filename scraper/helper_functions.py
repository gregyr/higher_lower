import json

def clean_price(pricetag:str):
    """
    Säubert den Preis zu einem Floatformat
    """
    remove_letters = "ab€."
    new_string = ""
    for i in pricetag:
        if i not in remove_letters:
            if i == ",":
                new_string += "."
            else:
                new_string += i
    
    return float(new_string.strip())
            
def remove_duplicates(list):
    """
    Entfernt doppelte Produkte
    """
    new_list = []

    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

def export_to_json(data, filename="data.json"):
    """
    Exportiert das Dictionary an Artikeln in eine JSON
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported data to {filename}")

    except Exception as e:
        print(f"Error exporting to JSON: {e}")