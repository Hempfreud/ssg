import os
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        content = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_content = (markdown_to_html_node(content)).to_html()
    title = extract_title(content)

    template = template.replace("{{ Content }}", html_content)
    template = template.replace("{{ Title }}", title)

    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(full_path):
            generate_pages_recursive(
                full_path,
                template_path,
                os.path.join(dest_dir_path, entry)
            )
        elif entry.endswith('.md') and os.path.isfile(full_path):
            dest_path = os.path.join(dest_dir_path, entry[:-3] + '.html')
            generate_page(full_path, template_path, dest_path)
