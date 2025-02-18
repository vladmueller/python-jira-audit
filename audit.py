from labels import fetch_all_labels, search, extract_project_labels
from collections import Counter


def find_duplicates(label_list):
    lower_counts = Counter(label.lower() for label in label_list)
    duplicates = {label.lower() for label, count in lower_counts.items() if count > 1}
    return [label for label in label_list if label.lower() in duplicates]


def is_kebab_case(item):
    # Check if the string is all lowercase and has a hyphen, or is just lowercase with no hyphen
    return (all(c.islower() or c == '-' for c in item) and '-' in item) or item.islower()


def print_markdown_table(labels_by_projects):
    # Header of the table
    print("| Project Key | Labels |")
    print("|-------------|--------|")

    # Iterate over the dictionary and print each row
    for project_key, labels in labels_by_projects.items():
        labels_str = ", ".join(labels)
        print(f"| {project_key} | {labels_str} |")


all_labels = fetch_all_labels()

print(f"Duplicates: {find_duplicates(all_labels)}")


not_kebab_case = [item for item in all_labels if not is_kebab_case(item)]

print(f"Not in kebab case: {not_kebab_case}")

labels_by_projects = extract_project_labels(search())

print_markdown_table(labels_by_projects)
