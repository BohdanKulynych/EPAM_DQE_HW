import xml.etree.ElementTree as ET
import re

def parse_and_remove(filename, path):
   path_parts = path.split('/')
   doc = ET.iterparse(filename, ('start', 'end'))
   # Skip root element
   next(doc)
   tag_stack = []
   elem_stack = []
   for event, elem in doc:
    if event == 'start':
      tag_stack.append(elem.tag)
      elem_stack.append(elem)
    elif event == 'end':
        if tag_stack == path_parts:
            yield elem
        try:
            tag_stack.pop()
            elem_stack.pop()
        except IndexError:
            pass


# define dict of all counrties and governments
countries_governments = {}
# define dict of chosen counrties and governments after regex
chosen_countries_governments = {}
countries = parse_and_remove('mondial-3.0.xml', 'country')
for country in countries:
         name = country.attrib['name']
         government = country.attrib['government'].strip()
         # fill in the dict
         countries_governments.update({name : government})
         # write pattern (  we need '?:' in start because we need full groups)
         pattern = r"(?:[a-zA-Z]+\W?\b){2,}"
         chosen_countries = re.findall(pattern,str(countries_governments.keys()))
         chosen_countries_governments.update({key: countries_governments[key] for key in chosen_countries
                                         if key in countries_governments})
print(chosen_countries_governments)
         
