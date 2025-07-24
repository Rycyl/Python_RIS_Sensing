from pathlib import Path

#directory = Path("C:\\Users\\cyryl\\Documents\\GitHub\\Python_RIS_Sensing")

# #folders = [f.name for f in directory.iterdir() if f.is_dir() and not (f.name.startswith(".") or f.name == "Dokumentacja" or f.name == "venv")]

# for folder in directory.iterdir():
#     if folder.is_dir() and not (folder.name.startswith(".") or folder.name == "Dokumentacja" or folder.name == "venv"):
#         print(f"Files in folder: {folder.name}")
#         for sub_folder in folder.iterdir():
#             if sub_folder.is_dir():
#                 print(f"Files in sub-folder: {sub_folder.name}")
#         # for file in folder.rglob("*"):
#         #     if file.is_file() and not (file.name.endswith(".csv") or file.name.endswith(".png") or file.name.endswith(".jpg") or file.name.endswith(".pkl")):
#         #         print(f" {file.relative_to(folder)}")
from pathlib import Path
import json

def find_description(name, docs):
    x = 0
    for item in docs:
        if item.name.split(".")[0] == name:
            return x
        else:
            x += 1
    return -1

def get_docs(path: Path):
    docs = []
    for item in path.iterdir():
        if item.is_dir() and item.name == "Dokumentacja":
            for element in item.iterdir():
                docs.append(element)
    return docs


def build_structure(path: Path, docs: list):
    structure = {}
    for item in path.iterdir():
        if item.is_dir() and not (item.name.startswith(".") or item.name == "Dokumentacja" or item.name == "venv"):
            structure[item.name] = build_structure(item, docs)
        elif item.is_file():
            ind = find_description(item.name.split(".")[0], docs)
            if ind >= 0:
                try:
                    description = docs[ind].read_text(encoding='utf-8').strip()
                except Exception as e:
                    description = f"[Error reading file: {e}]"
                file_entry = {"name": item.name, 'description': description}
            else:
                file_entry = item.name
            structure.setdefault('files', []).append(file_entry)
    return structure

 

# Set your base directory here
base_dir = Path("C:\\Users\\cyryl\\Documents\\GitHub\\Python_RIS_Sensing")

#
docs = get_docs(base_dir)
print(type(docs[0]))
# Build the folder structure
folder_structure = build_structure(base_dir, docs)

# Save it to a JSON file
output_file = 'directory_structure.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(folder_structure, f, indent=4, ensure_ascii=False)

print(f"Directory structure saved to {output_file}")
