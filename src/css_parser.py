""" 

Author: Omar Muhammad (OmarMGaber) 
Date: 19/4/2025

"""

import re
from collections import defaultdict

def parse_css_all_selectors(css: str) -> dict[str, list[str]]:
    """ Parse a given css file and returns a map of class, id, tag -> list of strings (css rules)
    
    Args:
        css (str): css file content

    Returns:
        dict[str, list[str]]: A map of class, id, tag -> list of strings (css rules)
    """
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

    # Match selectors and their style blocks
    # ([^{]+) -> match any character except { one or more times
    # \{ -> match { 
    # ([^}]+) -> match any character except } one or more times
    # \} -> match }
    # The above regex will match the following pattern: selectors { style }
    rules = re.findall(r'([^{]+)\{([^}]+)\}', css)

    selector_styles = defaultdict(list)

    for selector_group, body in rules:
        styles = [s.strip() for s in body.strip().split(';') if s.strip()]
        selectors = [sel.strip() for sel in selector_group.split(',')]

        for sel in selectors:
            parts = re.findall(r'([.#]?[a-zA-Z0-9_-]+)', sel)
            for part in parts:
                selector_styles[part].extend(styles)

    return dict(selector_styles)
