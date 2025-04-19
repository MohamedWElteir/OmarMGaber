"""

Author: Omar Muhammad (OmarMGaber) 
Date: 19/4/2025

CSS to HTML Legacy Attribute Mapper

This script maps CSS rules to their equivalent HTML attributes.
Used as a workaround for my github readme file, since github doesn't allow 'style' attr or css in readme files.
"""

class CSSToHTMLMapper:
    def __init__(self):
        self.MAPPING = {
            'text-align': ('align', None),
            'align-items': ('align', None),
            'align-self': ('align', None),
            'align-content': ('align', None),
            
            'width': ('width', self._convert_dimension),
            'height': ('height', self._convert_dimension),
            'max-width': ('width', self._convert_dimension),
            'max-height': ('height', self._convert_dimension),
            
            'background-color': ('bgcolor', self._convert_color),
            'color': ('color', self._convert_color),
            
            'border': ('border', self._convert_border),
                        
            'padding': ('cellpadding', self._convert_dimension_to_integer),
            'padding-top': ('cellpadding', self._convert_dimension_to_integer),
            'padding-right': ('cellpadding', self._convert_dimension_to_integer),
            'padding-bottom': ('cellpadding', self._convert_dimension_to_integer),
            'padding-left': ('cellpadding', self._convert_dimension_to_integer),
            'border-spacing': ('cellspacing', self._convert_dimension_to_integer),
            
            'vertical-align': ('valign', None),
            
            'background-image': ('background', self._convert_background_image),
            
            'font-family': ('face', self._convert_font_family),
            'font-size': ('size', self._convert_font_size),
        }
        
    def _convert_dimension(self, value):
        if value.endswith('%'):
            return value
        
        try:
            if value.endswith('px'):
                return value[:-2]
            elif value.isdigit():
                return value
            else:
                return value
        except:
            return value
    
    def _convert_dimension_to_integer(self, value):
        try:
            if value.endswith('px'):
                return str(int(float(value[:-2])))
            elif value.isdigit():
                return value
            else:
                return str(int(float(value)))
        except:
            return '0'
    
    def _convert_color(self, value):
        # Hex colors
        if value.startswith('#'):
            return value
        
        return value
    
    def _convert_border(self, value):
        if value.lower() == 'none':
            return '0'
            
        parts = value.split()
        if len(parts) >= 1:
            try:
                width = parts[0]
                if width.endswith('px'):
                    return width[:-2]
                else:
                    return width
            except:
                pass
        
        return '1'
    
    def _convert_background_image(self, value):
        if value.startswith('url(') and value.endswith(')'):
            url = value[4:-1].strip('\'"')
            return url
        return value
    
    def _convert_font_family(self, value):
        families = value.split(',')
        if families:
            return families[0].strip().strip('\'"')
        return value
    
    def _convert_font_size(self, value):
        size_mapping = {
            'xx-small': '1',
            'x-small': '2',
            'small': '2',
            'medium': '3',
            'large': '4',
            'x-large': '5',
            'xx-large': '6',
            'xxx-large': '7',
        }
        
        if value.lower() in size_mapping:
            return size_mapping[value.lower()]
        
        if value.endswith('em'):
            try:
                em_size = float(value[:-2])
                if em_size <= 0.8:
                    return '1'
                elif em_size <= 1.0:
                    return '2'
                elif em_size <= 1.1:
                    return '3'
                elif em_size <= 1.5:
                    return '4'
                elif em_size <= 2.0:
                    return '5'
                elif em_size <= 3.0:
                    return '6'
                else:
                    return '7'
            except:
                pass
        
        if value.endswith('px'):
            try:
                px_size = float(value[:-2])
                if px_size <= 10:
                    return '1'
                elif px_size <= 13:
                    return '2'
                elif px_size <= 16:
                    return '3'
                elif px_size <= 18:
                    return '4'
                elif px_size <= 24:
                    return '5'
                elif px_size <= 32:
                    return '6'
                else:
                    return '7'
            except:
                pass
        
        return '3'

    def css_to_html_attributes(self, css_rules, tag_name):
        """
        Convert CSS rules to HTML attributes for a specific tag.
        
        Args:
            css_rules (dict): Dictionary of CSS properties and values
            tag_name (str): HTML tag name to check attribute compatibility
            
        Returns:
            dict: Dictionary of HTML attributes and values
        """
        html_attr = {}
        
        for css_prop, css_value in css_rules.items():
            
            if css_prop in self.MAPPING:
                attr_name, transform_func = self.MAPPING[css_prop]
                
                if transform_func:
                    html_attr[attr_name] = transform_func(css_value)
                else:
                    html_attr[attr_name] = css_value
        
        return html_attr

    def generate_html_attributes_string(self, attributes):
        """
        Generate HTML attribute string from a dictionary of attributes.
        
        Args:
            attributes (dict): Dictionary of HTML attributes and values
            
        Returns:
            str: HTML attribute string
        """
        result = []
        for attr, value in attributes.items():
            result.append(f'{attr}="{value}"')
        return ' '.join(result)
