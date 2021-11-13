import json

accounts_oname = "output/accounts.txt"
groups_oname = "output/groups.txt"
vkconfig_iname = "temp/vk_config.txt"

def save_as_json(obj, filename):
    with open(filename, 'w') as f:
        print(json.dumps(obj, ensure_ascii=False, indent=4), file=f)
