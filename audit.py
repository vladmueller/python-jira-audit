from labels import fetch_all_labels, search, extract_project_labels
from collections import Counter

def find_duplicates(label_list):
    lower_counts = Counter(label.lower() for label in label_list)
    duplicates = {label.lower() for label, count in lower_counts.items() if count > 1}
    return [label for label in label_list if label.lower() in duplicates]

def is_kebab_case(item):
    # Check if the string is all lowercase and has a hyphen, or is just lowercase with no hyphen
    return (all(c.islower() or c == '-' for c in item) and '-' in item) or item.islower()

all_labels = fetch_all_labels()

print(f"Duplicates: {find_duplicates(all_labels)}")

#print(extract_project_labels(search()))

not_kebab_case = [item for item in all_labels if not is_kebab_case(item)]

print(f"Not in kebab case: {not_kebab_case}")
