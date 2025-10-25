import os
import re
import json

# delete first all unused strings
# delete unused views
# delete again all unused strings

path = "/Users/poplorenzo/work/book-chat"
l10npattern = re.compile(r"L10n\.([A-Za-z0-9_.]+)")
viewpattern = re.compile(r"struct\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?:some\s+)?View")
l10nmatches = {}
allstrings = {}
views = {}
usageresults = {}
threeviews = {}

for subdir, _, files in os.walk(path):
    for file in files:
        if file.endswith(".swift") or file.endswith(".m") or file.endswith(".mm"):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in l10npattern.findall(content):
                    l10nmatches[match] = 1
                for view in viewpattern.findall(content):
                    views[view] = 1

        # if file.endswith(".strings"):
        #     file_path = os.path.join(subdir, file)
        #     with open(file_path, 'r', encoding='utf-8') as f:
        #         content = f.read()
        #         string_pattern = re.compile(r'["]?([\w\.]+)["]?\s*=\s*"([^"]+)"')
        #         for string_match in string_pattern.findall(content):
        #             key, value = string_match
        #             allstrings[key] = value 

matches = {key.lower(): value for key, value in l10nmatches.items()}

# print unused strings from strings file
# for key, value in allstrings.items():
#     if l10nmatches.get(key.lower()) is None:
#         print(f"{key} = {value}")


# see all the views
# for view in views.keys():
#     print(f"View: {view}")

# check all the views usage
print("Starting views usage analysis...")

for subdir, _, files in os.walk(path):
    for file in files: 
        if file.endswith(".swift") or file.endswith(".m") or file.endswith(".mm"):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for view in views:
                    structFinderPattern = re.compile(rf"(?<!struct\s){view}\b(?!\s*:\s*some\s*View)")
                    # match view name as whole word (not as part of another identifier)
                    for match in structFinderPattern.findall(content):
                        usageresults.setdefault(view, []).append(file_path)

views_file_usage = "views_usage.json"
# with open(views_file_usage, "w", encoding="utf-8") as f:
#     json.dump(usageresults, f, indent=2)
# print(f"✅ Saved {len(views)} views to {views_file_usage}")

with open(views_file_usage, "r", encoding="utf-8") as f:
    usageresults = json.load(f)

print(len(usageresults.keys()))

for view_name in views.keys():
    if usageresults.get(view_name) is None:
        print(f"View: {view_name} is unused")

# create a view subfile three
# from where all the views start