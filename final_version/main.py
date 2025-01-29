from xml_splitter import XMLSplitter
from file_handler import FileHandler
import xml.etree.ElementTree as ET
from openai_analyzer import OpenAIAnalyzer
import os

def main(root: ET.Element, output_directory: str):
    sources = XMLSplitter.extract_sources_xml_and_qualifier_and_target(root)
    sample_code = FileHandler.read_file(os.path.join(output_directory, "sample_code.py"))
    source_code = FileHandler.read_file(os.path.join(output_directory, "source_code.py"))
    openai_analyzer = OpenAIAnalyzer()

    
    output_file = os.path.join(output_directory, "source_information.xml")
    FileHandler.save_file(output_file, sources)

    source_information = openai_analyzer.generate_source_information(sources)
    output_file = os.path.join(output_directory, "source_information.md")
    FileHandler.save_file(output_file, source_information)

    
    source_code = openai_analyzer.generate_source_code(sources, source_information, sample_code)
    output_file = os.path.join(output_directory, "source_code.py")
    FileHandler.save_file(output_file, source_code)
 
    
    mapping_xml = XMLSplitter.extract_mapping_xml(root)
    output_file = os.path.join(output_directory, "mapping_xml.xml")
    FileHandler.save_file(output_file, mapping_xml)
    mapping_codes = []
    mapping_summaries = []
    # split the mapping_xml str to chunks of str
    for i in range(0, len(mapping_xml), 1000):
        mapping_xml_chunk = mapping_xml[i:i+1000]
        mapping_summary = openai_analyzer.generate_mapping_summary(mapping_xml_chunk)
        mapping_codes.append(openai_analyzer.generate_mapping_code(mapping_xml_chunk, mapping_summary,sample_code))

    output_file = os.path.join(output_directory, "mapping_summary.md")
    FileHandler.save_file(output_file, mapping_summaries)

    output_file = os.path.join(output_directory, "mapping_code.py")
    FileHandler.save_file(output_file, "".join(mapping_codes))

    mapping_code = FileHandler.read_file(os.path.join(output_directory, "mapping_code.py"))
    final_code = openai_analyzer.generate_final_code(mapping_code, source_code)
    output_file = os.path.join(output_directory, "final_code.py")
    FileHandler.save_file(output_file, final_code)

if __name__ == "__main__":
    file_name = "pay.xml"
    directory = "./resources"
    output_directory = "./output2"
    os.makedirs(output_directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)
    output_file = os.path.join(output_directory, "source_information.xml")
    root = XMLSplitter.read_workflow_xml(file_path)
    main(root, output_directory) 