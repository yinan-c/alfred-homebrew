import requests
import json
import sys

def get_all_formula_names():
    if sys.argv[1] == 'all_cask':
        response = requests.get('https://formulae.brew.sh/api/cask.json')
        icon_path = {"path": "icons/cask.png"}
    elif sys.argv[1] == 'all_formula':
        response = requests.get('https://formulae.brew.sh/api/formula.json')
        icon_path = {"path": "icons/brew.png"}
    data = response.json()

    items = []
    for item in data:
        if sys.argv[1] == 'all_cask':
            name = item['name'][0]
            token = item['token']
            try:
                subtitle = name + '  ℹ️ '+ item['desc']
            except:
                subtitle = name
            arg = f'https://formulae.brew.sh/cask/{token}#default'
        elif sys.argv[1] == 'all_formula':
            token = item['name']
            subtitle =  item['desc']
            arg = f'https://formulae.brew.sh/formula/{token}#default'
        formula = {
            "valid": True,
            "title": token,
            "subtitle": subtitle,
            "arg": arg,
            "icon": icon_path,
            "autocomplete": token,
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": item['homepage'],
                    "subtitle": item['homepage']
                },
            }
        }
        items.append(formula)

    output = {"items": items}
    
    return output


def get_info(formula_name):
    token = formula_name.lower()
    if sys.argv[2] == 'cask':
        response = requests.get('https://formulae.brew.sh/api/cask/'+token+'.json')
    elif sys.argv[2] == 'formula':
        response = requests.get('https://formulae.brew.sh/api/formula/'+token+'.json')
    data = response.json()
    if sys.argv[2] == 'cask':
        version = data['version']
    elif sys.argv[2] == 'formula':
        if data['versions']['bottle'] == True:
            version = data['versions']['stable'] + ' (bottle)'
        else:  
            version = data['versions']['stable']
    output_data = {
        "items": [
            {
                "valid": True,
                "title": data['homepage'],
                "subtitle": "Open homepage",
                "arg": data['homepage'],
                "icon": {"path": "icons/homepage.png"},
            },
            {
                "valid": False,
                "title": f"30 Days:\t{data['analytics']['install']['30d'][token]}",
                "icon": {"path": "icons/hot.png"},
            },
            {
                "valid": False,
                "title": f"90 Days:\t{data['analytics']['install']['90d'][token]}",
                "icon": {"path": "icons/hot.png"},
            },
            {
                "valid": False,
                "title": f"365 Days:\t{data['analytics']['install']['365d'][token]}",
                "icon": {"path": "icons/hot.png"},
            },
            {
                "valid": False,
                "title": version,
                "icon": {"path": "icons/uninstalled.png"},
            }
        ]
    }
    return output_data

def get_commands(formula_name):
    token = formula_name.lower()
    if sys.argv[2] == 'cask':
        response = requests.get('https://formulae.brew.sh/api/cask/'+token+'.json')
        install_command = 'brew install --cask '+ token
        info_command = 'brew info --cask '+ token
    elif sys.argv[2] == 'formula':
        response = requests.get('https://formulae.brew.sh/api/formula/'+token+'.json')
        install_command = 'brew install '+ token
        info_command = 'brew info '+ token
    data = response.json()
    if sys.argv[2] == 'cask':
        name = data['name'][0]
    elif sys.argv[2] == 'formula':
        name = data['name']
    ouput_data = {
        "items": [
            {
                "valid": True,
                "title": install_command,
                "subtitle": "Run install command of "+ name,
                "arg": install_command,
                "icon": {"path": "icons/install.png"},
            },
            {
                "valid": True,
                "title": info_command,
                "subtitle": "Run info command of "+ name,
                "arg": info_command,
                "icon": {"path": "icons/info.png"},
            },
        ]
    }
    return ouput_data

if sys.argv[1] == 'all_formula' or sys.argv[1] == 'all_cask':
    print(json.dumps(get_all_formula_names()))
elif sys.argv[1] == 'get_commands':
    print(json.dumps(get_commands(sys.argv[3])))
elif sys.argv[1] == 'get_info':
    print(json.dumps(get_info(sys.argv[3])))
