from xml.etree import ElementTree as ET


file = "project_resources/LRG_5.xml"

tree = ET.parse(file)
root = tree.getroot()

annotation_set = root.find('updatable_annotation').findall('annotation_set')

annotations = []

for item in annotation_set:
    if "lrg" in item.attrib['type']:
        annotations.extend(item.findall('mapping'))


print(GRCh37)
print(GRCh38)
