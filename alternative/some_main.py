import sys  
import json
from xml.dom.minidom import parse
from app.component import Component

if __name__ == "__main__":  
    folder_with_components = ""  
    try:  
        print(f"Name of the script : {sys.argv[0]=}")  
        print(f"Name of the folder : {sys.argv[1]=}")  
        folder_with_components = sys.argv[1] + "/json"  
        print(f"Arguments of the script : {sys.argv[1:]=}")  
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <string_to_reverse>")  
  
    only_files = [f for f in listdir(folder_with_components)]  # if isfile(join(folder_with_components, f))]
    for item in only_files:
        print(item)
  
    config_file = folder_with_components + "/components_config.json"  
    # print(config_file)
    with open(config_file, 'r') as f:  
        data = f.read().replace('\n', '').replace('\t', '')  
        components = json.loads(data)  
        for component in components:  
            comp = Component.from_json(component)  
            print(comp.name, comp.last_update)
