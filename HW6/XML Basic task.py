import xml.etree.ElementTree as ET

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


# define empty list where governments will be written
distinct_governments = []
countries = parse_and_remove('mondial-3.0.xml', 'country')
for country in countries:
    # find goverment of every country into xml and remove extra whitespaces
    government = country.attrib['government'].strip()
    # when extra whitespaces have removed we need check list on none objects
    if government not in distinct_governments and government != 'none':
        distinct_governments.append(government)
print(distinct_governments)
