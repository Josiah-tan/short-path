'''
PHASE 1 🦆 Turning strings into a folder system
'''
sample = '''~/Desktop/josiah/
~/Documents/org/
~/Downloads/
~/Downloads/another_folder
~/.dotfiles/quick_projects_wsl/.config/.quick_projects/
~/.dotfiles/quick_projects_linux/.config/.quick_projects/
~/Desktop/josiah/neovim/quick_projects/assets/
~/Desktop/josiah/neovim/quick_projects/'''.split("\n")

# ~/De/josiah/
# ~/Doc/org/
# ~/Downloads/
# ~/Dow/another_folde/
# ~/./quick_projects_w/./.quick_projects/
# ~/./quick_projects_l/./.quick_projects/
# ~/De/j/n/q/assets/
# ~/De/j/n/quick_projects/
# We don't want duplicates in our folder system
def add_to_dict(key, val, dict):
    if val not in dict[key]:
        dict[key][val] = {"YEEEEET": None} # Yeet acts as a pointer to the soon to be truncated name :)

# This splits the root from the path
def strip_root(path):
    if "/" not in path:
        return (None, path)

    return path.replace("/", "\n", 1).split("\n")

def string_to_folder(parent, path, folder_sys):
    if "/" not in path:
        add_to_dict(parent, path, folder_sys)
        return

    child, rest_of_path = strip_root(path)
    add_to_dict(parent, child, folder_sys)
    string_to_folder(child, rest_of_path, folder_sys[parent])

folder_sys = {"~": {"YEEEEET": "~"}}

for string in sample:
    x, y = strip_root(string[:-1]) ## -1 is to get rid of final "/"
    string_to_folder(x, y, folder_sys)

import json


'''
PHASE 2 😎 Truncating
'''
def truncate(string, length):
    return string if length >= len(string) else string[:length]

def solve_folder_system(folder_sys):
    # Grab the things at the current level
    things = sorted(folder_sys.keys())
    things.remove("YEEEEET")

    # If its sorted, only the files directly in front and directly
    # behind are in contention for truncation
    benchmark = things[0][0]
    i = 0

    while i < len(things) - 1:
        length = 1
        left = truncate(things[i], length)
        right = truncate(things[i + 1], length)

        while left == right and length <= min(len(things[i]), len(things[i+1])):
            length += 1
            left = truncate(things[i], length)
            right = truncate(things[i + 1], length)

        folder_sys[things[i]]["YEEEEET"] = left if len(left) > len(benchmark) else benchmark
        benchmark = right
        i += 1

    folder_sys[things[i]]["YEEEEET"] = benchmark

    # Repeat for each level after
    for i in folder_sys:
        if i == "YEEEEET" or len(folder_sys[i]) <= 1:
            continue

        solve_folder_system(folder_sys[i])

solve_folder_system(folder_sys["~"])
print(json.dumps(folder_sys, indent=2))

'''
PHASE 3 🍞 Re-writing dem strings
'''
for string in sample:
    string = string[:-1] # again screw that final slash :P
    new_string = ""

    root, path = strip_root(string)
    my_folder = folder_sys

    while root != None:
        new_string += my_folder[root]["YEEEEET"] + "/"
        my_folder = my_folder[root]
        root, path = strip_root(path)

    new_string += path + "/"
    print(new_string)

