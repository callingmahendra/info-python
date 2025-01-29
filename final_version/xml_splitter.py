import xml.etree.ElementTree as ET

class XMLSplitter:

    @staticmethod
    def read_workflow_xml(file_path: str) -> ET.Element:
        """Read and parse the Powercenter workflow XML file."""
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            raise Exception(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        
    @staticmethod
    def extract_sources_xml_and_qualifier_and_target(root: ET.Element) -> str:
        sources = root.findall(".//SOURCE")
        source_information = []
        for source in sources:
            source_information.append(ET.tostring(source, encoding='utf-8').decode('utf-8'))
        
        source_qualifier = root.findall(".//TRANSFORMATION[@TYPE='Source Qualifier']")
        for source_qualifier in source_qualifier:
            source_information.append(ET.tostring(source_qualifier, encoding='utf-8').decode('utf-8'))
        target = root.findall(".//TARGET")
        for child in target:
            source_information.append(ET.tostring(child, encoding='utf-8').decode('utf-8'))
        
        return "\n".join(source_information)

    
    @staticmethod
    def extract_mapping_xml(root: ET.Element) -> str:
        mapping = root.findall(".//MAPPING")
        mapping_information = []
        for mapping in mapping:
            mapping_information.append(ET.tostring(mapping, encoding='utf-8').decode('utf-8'))
        return "\n".join(mapping_information)

    