from typing import Union
import json
import os
import logging




class JSON_modulator:
    def __init__(self, json_obj):
        self._json = json_obj

    @staticmethod
    def _get_path(position, delimiter='^'):
        return position.split(delimiter)

    def _find_position(self, position: str):
        obj = self._json
        for key in JSON_modulator._get_path(position):
            if not isinstance(obj, dict):
                logging.warning(f"Expected dict at '{key}' in path '{position}', found {type(obj)}.")
                return None
            obj = obj.get(key)
            if obj is None:
                logging.warning(f"Key '{key}' not found in path '{position}'.")
                return None
        return obj

    def key_remove(self, position: str, key: str) -> bool:
        res = self._find_position(position)
        if res is None:
            logging.error("Couldn't perform key removal.")
            return False
        try:
            res.pop(key)
            logging.info(f"Removed key '{key}' from '{position}'.")
            return True
        except KeyError:
            logging.warning(f"Key '{key}' not found at '{position}'.")
            return False

    def subjson_append(self, position: str, subjson: dict) -> bool:
        res = self._find_position(position)
        if res is None:
            logging.error("Couldn't append subjson.")
            return False
        if not isinstance(res, dict):
            logging.error(f"Target at '{position}' is not a dict.")
            return False
        res.update(subjson)
        logging.info(f"Appended subjson to '{position}'.")
        return True

    def listitem_append(self, position: str, item: Union[str, int, float]) -> bool:
        res = self._find_position(position)
        if res is None:
            logging.error("Couldn't append list item.")
            return False
        if not isinstance(res, list):
            logging.error(f"Target at '{position}' is not a list.")
            return False
        res.append(item)
        logging.info(f"Appended item '{item}' to list at '{position}'.")
        return True

    def listitem_delete(self, position: str, item) -> bool:
        res = self._find_position(position)
        if res is None:
            logging.error("Couldn't delete list item.")
            return False
        if not isinstance(res, list):
            logging.error(f"Target at '{position}' is not a list.")
            return False
        original_len = len(res)
        res[:] = [x for x in res if x != item]
        deleted_count = original_len - len(res)
        if deleted_count:
            logging.info(f"Deleted {deleted_count} occurrences of '{item}' from '{position}'.")
        else:
            logging.warning(f"No occurrences of '{item}' found in '{position}'.")
        return True

    def key_rename(self, position: str, new_key: str) -> bool:
        temp = JSON_modulator._get_path(position)
        old_key = temp[-1]
        parent_pos = "^".join(temp[:-1])
        parent = self._find_position(parent_pos)
        if parent is None or old_key not in parent:
            logging.error(f"Cannot rename key '{old_key}' at '{parent_pos}'.")
            return False
        parent[new_key] = parent.pop(old_key)
        logging.info(f"Renamed key '{old_key}' to '{new_key}' at '{parent_pos}'.")
        return True

    def value_rename(self, position: str, new_value: Union[str, int, float]) -> bool:
        temp = JSON_modulator._get_path(position)
        target_key = temp[-1]
        parent_pos = "^".join(temp[:-1])
        parent = self._find_position(parent_pos)
        if parent is None or target_key not in parent:
            logging.error(f"Cannot rename value at '{position}'.")
            return False
        parent[target_key] = new_value
        logging.info(f"Replaced value at '{position}' with '{new_value}'.")
        return True





if '__main__' == __name__:
    path = os.path.join('examples','example1.json')
    with open(path, mode='r', encoding='utf-8') as f:
        json_obj = json.load(f)
    mymod=JSON_modulator(json_obj)
    # mymod.key_remove('glossary^GlossDiv^GlossList^GlossEntry', 'ID')

    my_dict = {
        'my_key1':'value1',
        'my_key2': {
            'my_key3': [2,3,2]
        }
    }
    mymod.subjson_append('glossary^GlossDiv^GlossList', my_dict)
    mymod.listitem_append('glossary^GlossDiv^GlossList^GlossEntry^GlossDef', "ABC")
    mymod.listitem_delete('glossary^GlossDiv^GlossList^GlossEntry^GlossDef^GlossSeeAlso', "GML")
    mymod.key_rename('glossary^GlossDiv^GlossList', 'new_GlossList')
    mymod.value_rename('glossary^GlossDiv^new_GlossList', 'new_value')


    path = os.path.join('examples','example2.json')
    with open(path, mode='r', encoding='utf-8') as f:
        json_obj = json.load(f)
    mymod=JSON_modulator(json_obj)

    mymod.key_remove('shipTo', 'name')
    print(json.dumps(mymod._json, indent=4))
    

