# write a python script to extract the FOLDER element from the xml file
import xml.etree.ElementTree as ET
import os

tree = ET.parse('CPM_AFPS.xml')
root = tree.getroot()
base_folder = 'CPM_AFPS'
os.makedirs(f'{base_folder}', exist_ok=True)
folder = root.find('.//FOLDER')

for child in folder:
    #Create separate file for each child
    if child.tag == 'MAPPING':
        with open(f'{base_folder}/mapping-{child.attrib["NAME"]}.xml', 'w') as file:
            file.write(ET.tostring(child, encoding='utf-8').decode('utf-8'))
    elif child.tag == 'SESSION':
        with open(f'{base_folder}/session-{child.attrib["NAME"]}.xml', 'w') as file:
            file.write(ET.tostring(child, encoding='utf-8').decode('utf-8'))
    
