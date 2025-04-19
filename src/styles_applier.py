""" 

Author: Omar Muhammad (OmarMGaber) 
Date: 19/4/2025

"""

from bs4 import BeautifulSoup
import css_parser
import css_to_html
import os
from dotenv import load_dotenv

load_dotenv()

MAPPER = css_to_html.CSSToHTMLMapper()
IGNORE_STYLE_ATTR = os.getenv("IGNORE_STYLE_ATTR") == "true"
IGNORE_HTML_LEGACY_ATTR = os.getenv("IGNORE_HTML_LEGACY_ATTR") == "true"

def _map(styles):
    idx = styles.find(':')
    return {styles[:idx].strip(): styles[idx+1:].strip()}

def _apply(elements, styles, key):
    
    for element in elements:
        for style in styles[key]:
            if not IGNORE_HTML_LEGACY_ATTR: 
                attr = MAPPER.css_to_html_attributes(_map(style))
                
                if attr:
                    for attr_name, attr_value in attr.items():
                        element[attr_name] = attr_value
                    
                    continue
            
            if not IGNORE_STYLE_ATTR:
                element_styles = element.get('style', '')
                if element_styles:
                    element['style'] = element_styles + ';' + style
                else:
                    element['style'] = style


def add_styles(content: str, styles_path : str) -> str:
        """
        Reads the tags, class, and id of HTML content and applies the styles to the matching elements.

        Parameters:
        - content: str
            A string containing the HTML content that will be parsed and modified.
        - styles_path: dict
            Path to the styles file.
            
        Returns:
        - str: 
            The modified HTML content as a string with the applied styles.
        """
        soup = BeautifulSoup(content, 'html.parser')
        styles = css_parser.parse_css_all_selectors(open(styles_path).read())
        
        for key in styles:
            if key.startswith('.'):  # Class selector
                elements = soup.find_all(class_=key[1:])
                if elements:
                    _apply(elements, styles, key)

            elif key.startswith('#'):  # ID selector
                element = soup.find(id=key[1:])
                if element:
                    _apply([element], styles, key)

            else:
                elements = soup.find_all(key)
                if elements:
                    _apply(elements, styles, key)

        return str(soup)
    