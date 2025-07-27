import os, json, copy


        
def find(obj, path, current_pos, final):
    
    if [] == path:
        final.append(current_pos)
        return
    
    element = path.pop(0)

    if '*' != element:
        if not isinstance(obj, dict):
            return 
        new_obj = obj.get(element)
        if new_obj is None:
            current_pos = []
            return 
        current_pos.append(element)
        find(new_obj, path, current_pos, final)
        return final
    else:
        if not isinstance(obj, dict):
            return 
        for key,value in obj.items():
            res = find(value, copy.deepcopy(path), current_pos+[key], final)
        return final




path = os.path.join('examples','example1.json')
with open(path, mode='r', encoding='utf-8') as f:
    json_obj = json.load(f)


r = find(json_obj,['*','*','*','t6', '*'], [], [])
print(r)


