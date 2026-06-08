import json
import re

def loadProjects():
    with open("projects.json", "r") as f:
        projects = json.load(f)
    with open("README.md", "r") as f:
        readme = f.read()
    spaces = " " * 4

    projectNames = "\n".join(f'{spaces}<td><a href="{p["url"]}">{p["name"]}</a></td>' for p in projects)
    projectDescriptions = "\n".join(f'{spaces}<td>{p["description"]}</td>' for p in projects)
    projectImages = "\n".join(f'{spaces}<td><img src="{p["imageURL"]}" alt="{p["name"]}"></td>' for p in projects)

    def replaceSection(section, content):
        return re.sub(
            rf"<!--START OF PROJECTS {section}-->.*?<!--END OF PROJECTS {section}-->",
            f"<!--START OF PROJECTS {section}-->\n{content}\n{spaces}<!--END OF PROJECTS {section}-->",
            readme,
            flags=re.DOTALL,
        )

    readme = replaceSection("NAMES", projectNames)
    readme = replaceSection("DESCRIPTIONS", projectDescriptions)
    readme = replaceSection("IMAGE", projectImages)

    with open("README.md", "w") as f:
        f.write(readme)

loadProjects()