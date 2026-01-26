import os
import re

SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(SKILLS_DIR, 'README.md')

def parse_skill_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse Frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    metadata = {}
    if frontmatter_match:
        fm_content = frontmatter_match.group(1)
        for line in fm_content.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")
    
    # Parse Trigger (When to Use) from body
    # Look for "## When to Use" or similar
    trigger = "See details in file"
    when_match = re.search(r'##\s+(?:When to Use|Trigger|Usage)', content, re.IGNORECASE)
    if when_match:
        start = when_match.end()
        # Find next header
        next_header = re.search(r'\n##\s+', content[start:])
        end = start + next_header.start() if next_header else len(content)
        trigger_text = content[start:end].strip()
        # Clean up trigger text (take first few bullets or lines)
        lines = [l.strip() for l in trigger_text.splitlines() if l.strip()]
        # Take up to 3 meaningful lines/bullets
        preview = []
        for line in lines:
            if len(preview) >= 3:
                break
            preview.append(line)
        if preview:
            trigger = "<br>".join(preview)
            
    # Function (Description)
    # Use frontmatter description if available, else parsed text
    description = metadata.get('description', 'No description provided.')
    # If description contains "Invoke", we might want to split it? 
    # But user wants "Main Function". The frontmatter usually has it.
    
    name = metadata.get('name', os.path.basename(os.path.dirname(file_path)))
    
    return {
        'name': name,
        'trigger': trigger,
        'description': description,
        'path': os.path.relpath(file_path, SKILLS_DIR)
    }

def generate_readme():
    skills = []
    
    # Iterate over directories
    for item in sorted(os.listdir(SKILLS_DIR)):
        item_path = os.path.join(SKILLS_DIR, item)
        if os.path.isdir(item_path):
            skill_md = os.path.join(item_path, 'SKILL.md')
            if os.path.exists(skill_md):
                skills.append(parse_skill_file(skill_md))
    
    # Build Markdown
    lines = []
    lines.append("# Available Skills")
    lines.append("")
    lines.append("This directory contains the skills available to the AI agent. This file is **automatically updated** when skills are created or modified.")
    lines.append("")
    lines.append("| Skill Name | Main Function | Trigger / When to Use |")
    lines.append("|------------|---------------|-----------------------|")
    
    for skill in skills:
        # Link name to the folder
        name_link = f"[{skill['name']}](./{skill['name']}/SKILL.md)"
        lines.append(f"| {name_link} | {skill['description']} | {skill['trigger']} |")
    
    lines.append("")
    lines.append("> **Note**: To create a new skill, use the `skill-creator` tool. This README will be updated automatically.")
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Successfully updated {README_PATH} with {len(skills)} skills.")

if __name__ == "__main__":
    generate_readme()
