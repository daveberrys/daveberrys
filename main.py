import json
import re

FORMAT_PROJECTS = "list" # "table", "list"
SPACES = " " * 4

def loadProjects():
    with open("projects.json", "r") as f:
        projects = json.load(f)
    with open("README.md", "r") as f:
        readme = f.read()

    def replaceSection(section, content):
        return re.sub(
            rf"<!--START OF PROJECTS {section}-->.*?<!--END OF PROJECTS {section}-->",
            f"<!--START OF PROJECTS {section}-->\n{content}\n{SPACES[:-2]}<!--END OF PROJECTS {section}-->",
            readme,
            flags=re.DOTALL,
        )

    if FORMAT_PROJECTS == "table":
        projectNames = "\n".join(f'{SPACES}<td><a href="{p["url"]}">{p["name"]}</a></td>' for p in projects)
        projectDescriptions = "\n".join(f'{SPACES}<td>{p["description"]}</td>' for p in projects)
        projectImages = "\n".join(f'{SPACES}<td><img src="{p["imageURL"]}" alt="{p["name"]}"></td>' for p in projects)

        readme = replaceSection("NAMES", projectNames)
        readme = replaceSection("DESCRIPTIONS", projectDescriptions)
        readme = replaceSection("IMAGE", projectImages)
    elif FORMAT_PROJECTS == "list":
        projectFormat = "\n".join(f'{SPACES}<li> <img src="{p["imageURL"]}" alt="{p["name"]}" width="24" height="24"> <a href="{p["url"]}">{p["name"]}</a>: <span>{p["description"]}</span> </li>' for p in projects)
        readme = replaceSection("NAMES", projectFormat)

    with open("README.md", "w") as f:
        f.write(readme)

loadProjects()