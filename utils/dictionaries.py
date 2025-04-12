import re
import json
from xml.sax import saxutils

from custom_logging import logger

# import demjson3
# raw_json = '{"key": "string with "internal" quotes"}'
# parsed_data = demjson3.decode(raw_json)


def extract_specific_key(json_string: str, key: str) -> str:
    """Search for a specific key in a json string, return the portion of the string containing the key and its value"""

    match_string = f'"{key}":'

    start = json_string.find(match_string)
    if start == -1:
        return ""

    start += len(match_string)
    end = start

    while json_string[end] not in ["}"]:
        end += 1

    return json_string[start : end + 1]


def pre_processing(dict_string: str) -> dict:
    """Pre-process a string to extract a json object"""

    new_string = saxutils.unescape(dict_string.replace("&quot;", ""))
    new_string = re.sub(
        "[^A-Za-z0-9 \\!\\@\\#\\$\\%\\&\\*\\:\\,\\.\\;\\:\\-\\_\\\"'\\]\\[\\}\\{\\+\\á\\à\\é\\è\\í\\ì\\ó\\ò\\ú\\ù\\ã\\õ\\â\\ê\\ô\\ç\\|]+",
        "",
        new_string,
    )

    try:
        new_dict = json.loads(new_string)
    except Exception:
        new_string = extract_specific_key(new_string, "reviewRating")

        try:
            new_dict = json.loads(new_string)
            return {"reviewRating": new_dict}
        except Exception as e:
            logger.error(f"Error while parsing json / pre_processing: {e}")
            return {}

    if (
        "@graph" in new_dict
        and isinstance(new_dict["@graph"], list)
        and len(new_dict["@graph"]) > 0
    ):
        new_dict = new_dict["@graph"][0]

    return new_dict
