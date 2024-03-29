import requests
import json
import sys
import subprocess

def get_outdated_list(brewtype='all'):
    if brewtype == 'cask':
        output = subprocess.run(['brew', 'outdated', '--cask', '--json'], capture_output=True, text=True)
    elif brewtype == 'formula':
        output = subprocess.run(['brew', 'outdated', '--formula', '--json'], capture_output=True, text=True)
    else:
        output = subprocess.run(['brew', 'outdated', '--json'], capture_output=True, text=True)

    outdated_list = json.loads(output.stdout)
    result = {"items": []}
    if 'formulae' in outdated_list:
        for package in outdated_list['formulae']:
            name = package['name']
            installed_version = package['installed_versions'][0]
            current_version = package['current_version']

            result["items"].append({
                "title": f'{name} ({installed_version}) < {current_version}',
                "subtitle": f'⏎ to run "brew upgrade {name}"',
                "icon": {
                    "path": "icons/formula_outdated.png" 
                },
                "arg": 'brew upgrade ' + name,
                "autocomplete": name,
                "quicklookurl": f'https://formulae.brew.sh/formula/{name}'
            })

    if 'casks' in outdated_list:
        for package in outdated_list['casks']:
            name = package['name']
            installed_version = package['installed_versions'][0]
            current_version = package['current_version']

            result["items"].append({
                "title": f'{name} ({installed_version}) < {current_version}',
                "subtitle": f'⏎ to run "brew upgrade --cask {name}"',
                "icon": {
                    "path": "icons/cask_outdated.png" 
                },
                "arg": 'brew upgrade --cask ' + name,
                "autocomplete": name,
                "quicklookurl": f'https://formulae.brew.sh/cask/{name}'
            })
    if not result["items"]:
        result["items"].append({
            "title": "Everything is up to date",
            "icon": {
                "path": "icons/uptodate.png"
            },
            "valid": False
        })
    else:
        result["items"].append({
            "title": "Upgrade all",
            "icon": {
                "path": "icons/update_all.png"
            },
            "arg": "brew update && brew upgrade",
            "autocomplete": "Upgrade all",
            "valid": True
        })
    return result

def get_brew_leaves():
    output = subprocess.run(['brew', 'leaves'], capture_output=True, text=True)
    lines = output.stdout.split('\n')
    result = {"items": []}
    for line in lines:
        if not line:
            continue
        result["items"].append({
            "title": line,
            "icon": {
                "path": "icons/leaves.png"
            },
            "arg": line,
            "autocomplete": line,
            "quicklookurl": f'https://formulae.brew.sh/formula/{line}',
            "mods": {
                "cmd": {
                    "valid": True,
                    "subtitle": 'brew uninstall ' + line,
                    "arg": 'brew uninstall ' + line,
                },
            },
        })
    return result

def get_brew_list(brewtype='all'):
    if brewtype == 'cask':
        output = subprocess.run(['brew', 'list', '--versions', '--cask'], capture_output=True, text=True)
        uninstall_command = 'brew uninstall --cask '
        force_uninstall_command = 'brew uninstall --cask --force --zap '
        icon_path = {"path": "icons/cask_check.png"}
    elif brewtype == 'formula':
        output = subprocess.run(['brew', 'list', '--versions', '--formula'], capture_output=True, text=True)
        uninstall_command = 'brew uninstall '
        force_uninstall_command = 'brew uninstall '
        icon_path = {"path": "icons/formula_check.png"}
    else:
        output = subprocess.run(['brew', 'list', '--versions'], capture_output=True, text=True)
        uninstall_command = 'brew uninstall '
        force_uninstall_command = 'brew uninstall --force '
        icon_path = {"path": "icons/check.png"}
    lines = output.stdout.split('\n')
    result = {"items": []}
    for line in lines:
        if not line:
            continue
        name, version = line.split(' ', 1)

        result["items"].append({
            "title": f'{name} - {version}',
            "icon": icon_path,
            "arg": name,
            "autocomplete": name,
            "mods": {
                "alt": {
                    "valid": True,
                    "subtitle": uninstall_command + name,
                    "arg": uninstall_command + name,
                },
                "cmd": {
                    "valid": True,
                    "subtitle": force_uninstall_command + name,
                    "arg": force_uninstall_command + name,
                },
            },
        })
    return result

def get_all_formula_names(brewtype):
    response = requests.get('https://formulae.brew.sh/api/'+brewtype+'.json')
    icon_path = {"path": f"icons/{brewtype}.png"}
    data = response.json()
    items = []
    for item in data:
        if brewtype == 'cask':
            name = item['name'][0]
            token = item['token']
            install_command = 'brew install --cask ' + token
            try:
                subtitle = name + '  ℹ️ '+ item['desc']
            except:
                subtitle = name
        elif brewtype == 'formula':
            token = item['name']
            subtitle =  item['desc']
            install_command = 'brew install ' + token
        formula = {
            "valid": True,
            "title": token,
            "subtitle": subtitle,
            "arg": token, 
            "icon": icon_path,
            "autocomplete": token,
            "quicklookurl": f'https://formulae.brew.sh/{brewtype}/{token}',
            "match": brewtype + ' ' + token,
            "mods": {
                "cmd": {
                    "valid": True,
                    "subtitle": "Run install commmand: " +install_command,
                    "arg": install_command,
                },
            },
        }
        items.append(formula)
    return items


def get_info(brewtype,formula_name):
    output_data = {"items": []}
    token = formula_name.lower().strip()
    response = requests.get(f'https://formulae.brew.sh/api/{brewtype}/{token}.json')
    info_page = f'https://formulae.brew.sh/{brewtype}/{token}'
    data = response.json()
    if brewtype == 'cask':
        version = data['version']
        auto_update = '\t🔄 Auto updates = ✅' if data['auto_updates'] == True else '\t🔄 Auto updates = ❌'
        version_info = f'Newest version: {version}, {auto_update}'
    elif brewtype == 'formula':
        if data['versions']['bottle'] == True:
            version = data['versions']['stable'] + ' (bottle)'
        else:  
            version = data['versions']['stable']
        version_info = f'Newest version: {version}'
    output_data['items'].extend([
        {
            "valid": True,
            "title": data['homepage'],
            "subtitle": "Open homepage",
            "arg": data['homepage'],
            "icon": {"path": "icons/homepage.png"},
        },
        {
            "valid": True,
            "title": info_page,
            "subtitle": "Open brew.sh info page",
            "arg": info_page,
        },
        {
            "valid": False,
            "title": f"Installs (30 days): {data['analytics']['install']['30d'][token]}\t(90 days): {data['analytics']['install']['90d'][token]}\t (365 days): {data['analytics']['install']['365d'][token]}",
            "icon": {"path": "icons/hot.png"},
        },
        {
            "valid": False,
            'title': version_info,
            "icon": {"path": "icons/version.png"},
        }
    ])
    return output_data


if  __name__ == '__main__':
    output_data = {"items": []}
    if sys.argv[1] == 'all':
        output_data['items'].extend(get_all_formula_names(brewtype='cask'))
        output_data['items'].extend(get_all_formula_names(brewtype='formula'))
    elif sys.argv[1] == 'list':
#        output_data = get_brew_list()
        output_data['items'].extend(get_brew_list(brewtype='cask')['items'])
        output_data['items'].extend(get_brew_list(brewtype='formula')['items'])
    elif sys.argv[1] == 'leaves':
        output_data = get_brew_leaves()
    elif sys.argv[1] == 'get_info':
        try:
            output_data = get_info('cask',sys.argv[2])
        except:
            output_data = get_info('formula',sys.argv[2])
    if sys.argv[1] == 'outdated':
        output_data = get_outdated_list()
        
    print(json.dumps(output_data))