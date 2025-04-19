""" 

Author: Omar Muhammad (OmarMGaber) 
Date: 19/4/2025

"""

import json
import styles_applier 
import table_generator

class MDGenerator:
    def __init__(self, template_path, dist_path):
        self.dist_path = dist_path
        self.content = open(template_path, 'r').read()

    def add_content(self, content : str, start : str, end : str) -> bool:
        start_index = self.content.find(start)
        end_index = self.content.find(end)
        
        if start_index != -1 and end_index != -1:
            self.content = self.content[:start_index + len(start)] + "\n" + content + self.content[end_index:]
            return True
        else: return False        

    def add_styles(self, styles):
        self.content = styles_applier.add_styles(self.content, styles)
    
    def dump(self):
        with open(self.dist_path, 'w') as file: file.write(self.content)
        print(f"{self.dist_path} updated successfully.")
        
if __name__ == "__main__":
    config = json.load(open('config.json'))
    
    md_gen = MDGenerator(config['template_file_path'], config['output_file_path'])
    
    for file in config['projects_file_paths']:
        table = table_generator.generate_names_table(file['file_path'])
        md_gen.add_content(table, file['start'], file['end'])
    
    for css_file in config['css_file_paths']:
        md_gen.add_styles(css_file)
    
    md_gen.dump()
