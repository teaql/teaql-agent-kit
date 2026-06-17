import os
import glob
import re

def update_file(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update cargo-teaql versions
    content = re.sub(r'cargo-teaql` version `[0-9\.]+`', r'cargo-teaql` version `2.0.1`', content)
    content = re.sub(r'cargo-teaql >= [0-9\.]+', r'cargo-teaql >= 2.0.1', content)
    content = re.sub(r'cargo-teaql 0\.2\.0', r'cargo-teaql 2.0.1', content)
    content = re.sub(r'cargo-teaql` `[0-9\.]+`', r'cargo-teaql` `2.0.1`', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

files_to_update = glob.glob('playbooks/*.md') + glob.glob('*.md') + glob.glob('agents/*.md')
for md_file in files_to_update:
    update_file(md_file)
    print(f"Updated {md_file}")
