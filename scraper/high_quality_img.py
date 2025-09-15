import urllib.parse

def parse_alt_img_link(link):
    original_string = link
    stripped_string = ''.join(e for e in original_string if e.isalnum() or e == " ")
    parsed_string = ""
    for char in original_string:
        if char.isalnum():
            match char:
                case "ä":
                    parsed_string += "ae"
                case "ö":
                    parsed_string += "oe"
                case "ü":
                    parsed_string += "ue"
                case _:
                    parsed_string += char
        else:
            parsed_string += " "
    parsed_string = " ". join(parsed_string. split())

    url_encoded_string = urllib.parse.quote_plus(parsed_string.lower())
    url_encoded_string = url_encoded_string.replace("+", "-")

    return url_encoded_string

def strip_original_link(original_link:str):
    stripped_link = ""
    for char in original_link:
        if char == "?":
            break
        stripped_link += char
    return stripped_link

def get_high_quality_link(original_link:str, alt_img_link:str):
    url_encoded_string = parse_alt_img_link(alt_img_link)
    stripped_link = strip_original_link(original_link)

    final_link = ""
    final_link += stripped_link + "/"
    final_link += url_encoded_string +".jpg"
    final_link += "?$formatz$"

    return final_link