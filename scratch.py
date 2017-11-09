from xml.etree import ElementTree as ET


file = "project_resources/LRG_5.xml"

tree = ET.parse(file)
root = tree.getroot()

mapping_list = (root.find("updatable_annotation")
                    .find("annotation_set[@type='lrg']")
                    .findall("mapping"))


