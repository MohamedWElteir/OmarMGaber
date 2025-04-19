import json

class Project:
    def __init__(self, name: str, description: str, url: str, tags: list, tech: list):
        self.name = name
        self.description = description
        self.url = url
        self.tags = tags
        self.tech = tech

    def __hash__(self):
        return hash((self.name, self.description, self.url, tuple(self.tags), tuple(self.tech)))

def _read_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

# should be handled better
def _make_names_table(projects : list[Project]):
    headers = ["Name", "Description", "Tags", "Technologies"]
    width_p = ["15%", "45%", "25%", "15%"]
    
    html = "<div class='table-container'>\n"
    html += "<table>\n"
    
    html += "<thead>\n"
    html += "<tr>\n"
    for i in range(len(headers)):
        html += f"  <th style='width: {width_p[i]};'>{headers[i]}</th>\n"
    html += "</tr>\n"
    html += "</thead>\n"
    
    html += "<tbody>\n"
    tag_span = '<span class="tag tag">'
    tech_span = '<span class="tag tech">'
    for project in projects:
        html += "  <tr>\n"
        html += f"    <td style='font-weight: bold;'><a href='{project.url}' target='_blank' class='name-link'>{project.name}</a></td>\n"
        html += f"    <td>{project.description}</td>\n"
        html += f"    <td>{'<br>'.join([tag_span + tag + '</span>' for tag in project.tags])}</td>\n"
        html += f"    <td>{'<br>'.join([tech_span + tech + '</span>' for tech in project.tech])}</td>\n"
        html += "  </tr>\n"

    html += "</tbody>\n"
    
    html += "</table>\n"
    html += "</div>\n"
    return html

def _parse_project_data(project_json : list) -> list[Project]:
    projects = []
    for item in project_json:
        project = Project(
            name=item.get("name", ""),
            description=item.get("description", ""),
            url=item.get("src-url", "#"),
            tags=item.get("tags", []),
            tech=item.get("technologies", [])
        )
        projects.append(project)
        
    return projects

def generate_names_table(projects_file_path : str) -> str:
    projects = _parse_project_data(_read_json(projects_file_path))    
    projects.sort(key=lambda x: x.name.lower())
    
    return _make_names_table(projects)