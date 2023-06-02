import sys
import requests
import json
from brewinfo import get_brew_list
from brewinfo import get_info

def compare_versions(formula_name, version):
    brew_list = get_brew_list()
    for item in brew_list["items"]:
        if item["arg"] == formula_name:
            installed_version = item["title"].split(' ')[2]
            if installed_version == version:
                return "Installed and version matches.", installed_version
            else:
                return "Installed but version does not match.", installed_version
    return "Not installed.", None

def get_commands(brewtype,formula_name):
    token = formula_name.lower()
    info_command = 'brew info '+ token
    response = requests.get('https://formulae.brew.sh/api/'+brewtype+'/'+token+'.json')
    data = response.json()
    icon_path = {"path": f"icons/{brewtype}.png"}

    if brewtype == 'cask':
        install_command = 'brew install --cask '+ token
        uninstall_command = 'brew uninstall --cask '+ token
        force_uninstall_command = 'brew uninstall --force --zap --cask '+ token
        upgrade_command = 'brew upgrade --cask '+ token
        name = data['name'][0]
        version = data['version']
        try:
            subtitle = name + '  ℹ️ '+ data['desc']
        except:
            subtitle = name

    elif brewtype == 'formula':
        install_command = 'brew install '+ token
        uninstall_command = 'brew uninstall '+ token
        upgrade_command = 'brew upgrade '+ token
        name = data['name']
        subtitle =  data['desc']
        version = data['versions']['stable']
    
    information = {
            "valid": False,
            "title": token,
            "subtitle": subtitle,
            "icon": icon_path,
            "autocomplete": token,
            "quicklookurl": f'https://formulae.brew.sh/{brewtype}/{token}',
            "match": brewtype + ' ' + token
        }
    back_button = {
        "title": "Back to list",
        "arg": 1,
        "icon": {"path": "icons/back.png"},
        "valid": True
    }
    output_data = {"items": []}
    if description_toggle == 'description-on':
        output_data["items"].append(information)
    if button_toggle == 'button-on':
        output_data["items"].append(back_button)
    
    status, installed_version = compare_versions(token, version)
    if status == "Not installed.":
        output_data["items"].extend([
        {
            "valid": True,
            "title": f'Not installed. ⏎ to install {name}.',
            "arg": install_command,
            "subtitle": install_command,
            "icon": {"path": "icons/install.png"},
        },
        {
            "valid": True,
            "subtitle": info_command,
            "title": "Run info command of "+ name,
            "arg": info_command,
            "icon": {"path": "icons/info.png"},
        },
        ])
    elif status == "Installed and version matches.":
        output_data["items"].append(
        {
            "valid": False,
            "title": 'Great! You are up to date.',
            "icon": {"path": "icons/uptodate.png"},
        })
        if brewtype == 'cask':  #  force clean uninstall for casks
            output_data["items"].append(
            {   
                "valid": True,
                "subtitle": uninstall_command,
                "title": f"Uninstall cask {name}, ⌘ + ⏎ to force clean uninstall.",
                "arg": uninstall_command,
                "icon": {"path": "icons/uninstall.png"},
                "mods": {
                    "cmd": {
                        "valid": True,
                        "subtitle": force_uninstall_command,
                        "arg": force_uninstall_command,
                    },
            },
            },
            )
        elif brewtype == 'formula':  # No force clean uninstall for formulas
            output_data["items"].append(
            {   
                "valid": True,
                "subtitle": uninstall_command,
                "title": f"Uninstall formula {name}",
                "arg": uninstall_command,
                "icon": {"path": "icons/uninstall.png"},
            },
            )
    elif status == "Installed but version does not match." and brewtype == 'cask':
        output_data["items"].extend([
        {
            "valid": True,
            "title": 'Version mismatch, installed '+ installed_version+ ' < '+ version,
            "subtitle": f"⏎ to force upgrade cask {name}, regardless of in-app auto updates.",
            "icon": {"path": "icons/outdated.png"},
            "arg": upgrade_command
        },
        {   
            "valid": True,
            "subtitle": uninstall_command,
            "title": f"Uninstall cask {name}, ⌘ + ⏎ to force clean uninstall.",
            "arg": uninstall_command,
            "icon": {"path": "icons/uninstall.png"},
            "mods": {
                "cmd": {
                    "valid": True,
                    "subtitle": force_uninstall_command,
                    "arg": force_uninstall_command,
                },
            },  
        },])
    elif status == "Installed but version does not match." and brewtype == 'formula':
        output_data["items"].extend([
        {
            "valid": True,
            "title": 'Version mismatch, installed '+ installed_version+ ' < '+ version,
            "subtitle": f"⏎ to upgrade formula {name}.",
            "icon": {"path": "icons/outdated.png"},
            "arg": upgrade_command
        },
        {   
            "valid": True,
            "subtitle": uninstall_command,
            "title": f"Uninstall formula {name}",
            "arg": uninstall_command,
            "icon": {"path": "icons/uninstall.png"},
        },])
    return output_data

if __name__ == '__main__':
    button_toggle = sys.argv[2]
    description_toggle = sys.argv[3]
    button = {
        "title": "Back to list",
        "arg": 1,
        "icon": {"path": "icons/back.png"},
        "valid": True
    }
    output_data = {"items": []}
    try:
        output_data = get_commands('cask',sys.argv[1])
        output_data['items'].extend(get_info('cask',sys.argv[1])['items'])
    except:
        try:
            output_data = get_commands('formula',sys.argv[1])
            output_data['items'].extend(get_info('formula',sys.argv[1])['items'])
        except:
            if button_toggle == 'button-on':
                output_data["items"].append(button)
    print(json.dumps(output_data))