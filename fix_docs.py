import os
import glob
import re

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # teaql-maven-plugin
    content = content.replace('1.0.1', '1.1.0')
    content = content.replace('teaql-maven-plugin:1.1.0:gen-lib', 'teaql-maven-plugin:1.1.0:generate -Dservice=java-lib')
    content = content.replace('teaql-maven-plugin:1.1.0:gen-workspace', 'teaql-maven-plugin:1.1.0:generate -Dservice=java-workspace')
    content = content.replace('teaql-maven-plugin:1.1.0:gen-doc', 'teaql-maven-plugin:1.1.0:generate -Dservice=markdown-doc')
    content = content.replace('teaql-maven-plugin:1.1.0:gen-model', 'teaql-maven-plugin:1.1.0:generate -Dservice=frontend-model')
    content = content.replace('mvn teaql:gen-lib', 'mvn teaql:generate -Dservice=java-lib')
    content = content.replace('mvn teaql:gen-workspace', 'mvn teaql:generate -Dservice=java-workspace')

    # cargo-teaql
    content = content.replace('version `0.2.2`', 'version `1.1.0`')
    content = content.replace('cargo-teaql >= 0.2.2', 'cargo-teaql >= 1.1.0')
    content = content.replace('cargo-teaql gen-lib', 'cargo-teaql rust-lib-core')
    content = content.replace('cargo-teaql gen-workspace', 'cargo-teaql rust-workspace')
    content = content.replace('cargo-teaql gen-doc', 'cargo-teaql markdown-doc')
    content = content.replace('cargo-teaql gen-model', 'cargo-teaql frontend-model')

    # General text mentions
    content = content.replace('fully qualified gen-lib', 'fully qualified generate -Dservice=java-lib')
    content = content.replace('fully qualified gen-workspace', 'fully qualified generate -Dservice=java-workspace')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for md_file in glob.glob('playbooks/*.md') + ['TECH-INTRODUCTION.md']:
    update_file(md_file)
    print(f"Updated {md_file}")

