import json
import re
import urllib.request

WAKATIME_URL = "https://wakatime.com/share/@Daveberry/05adfbd0-c7d1-4460-9124-9cc326d50862.json"
WAKATIME_SPACES = " " * 8

PROJECTS_FORMAT = "list" # "table", "list"
PROJECTS_SPACES = " " * 4

def replaceSection(something, section, content, readme, spaces):
    return re.sub(
        rf"<!--START OF {something} {section}-->.*?<!--END OF {something} {section}-->",
        f"<!--START OF {something} {section}-->\n{content}\n{spaces[:-2]}<!--END OF {something} {section}-->",
        readme,
        flags=re.DOTALL,
    )

def loadProjects():
    with open("projects.json", "r") as f:
        projects = json.load(f)
    with open("README.md", "r") as f:
        readme = f.read()

    if PROJECTS_FORMAT == "table":
        projectNames = "\n".join(f'{PROJECTS_SPACES}<td><a href="{p["url"]}">{p["name"]}</a></td>' for p in projects)
        projectDescriptions = "\n".join(f'{PROJECTS_SPACES}<td>{p["description"]}</td>' for p in projects)
        projectImages = "\n".join(f'{PROJECTS_SPACES}<td><img src="{p["imageURL"]}" alt="{p["name"]}"></td>' for p in projects)

        readme = replaceSection("PROJECTS", "NAMES", projectNames, readme, PROJECTS_SPACES)
        readme = replaceSection("PROJECTS", "DESCRIPTIONS", projectDescriptions, readme, PROJECTS_SPACES)
        readme = replaceSection("PROJECTS", "IMAGE", projectImages, readme, PROJECTS_SPACES)
    elif PROJECTS_FORMAT == "list":
        projectFormat = "\n".join(f'{PROJECTS_SPACES}<li> <img src="{p["imageURL"]}" alt="{p["name"]}" width="24" height="24"> <a href="{p["url"]}">{p["name"]}</a>: <span>{p["description"]}</span> </li>' for p in projects)
        readme = replaceSection("PROJECTS", "NAMES", projectFormat, readme, PROJECTS_SPACES)

    with open("README.md", "w") as f:
        f.write(readme)

def loadWakatime():
    with urllib.request.urlopen(WAKATIME_URL) as f:
        data = json.load(f)
        limitedData = data["data"][:6]
    with open("README.md", "r") as f:
        readme = f.read()

    wakatimeLanguages = "\n".join(f'{WAKATIME_SPACES}<td>{d["name"]}</td>' for d in limitedData)
    wakatimeTime = "\n".join(f'{WAKATIME_SPACES}<td>{d["text"]}</td>' for d in limitedData)
    readme = replaceSection("WAKATIME", "LANGUAGES", wakatimeLanguages, readme, WAKATIME_SPACES)
    readme = replaceSection("WAKATIME", "TIME", wakatimeTime, readme, WAKATIME_SPACES)

    with open("README.md", "w") as f:
        f.write(readme)

try:
    loadProjects()
    # loadWakatime()
except Exception as e:
    print(e)
