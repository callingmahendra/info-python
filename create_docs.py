#write a code to read the xml file and 
# create a markdown file with the workflow name and the workflow description
# find all the occurrences of the element <SORUCE> and print the NAME attribute and TYPE attribute
# find all the occurrences of the element <TARGET> and print the NAME attribute and TYPE attribute

import xml.etree.ElementTree as ET
import os

def extract_xml_to_markdown_source(root):
    """
    Extracts specific attributes from SOURCE and SOURCEFIELD tags and formats them in markdown.
    
    Args:
        xml_content (str): XML content as string
    
    Returns:
        str: Markdown formatted string
    """
    

    # Initialize markdown content
    markdown = []

    # Extract SOURCE attributes
    source = root
    markdown.append(f"## Source name: {source.get('NAME')}")
    markdown.append(f"- **Database Type:** {source.get('DATABASETYPE')}")
    markdown.append(f"- **Database Name:** {source.get('DBDNAME')}")
    markdown.append(f"- **Table Name:** {source.get('NAME')}")
    markdown.append(f"- **Owner:** {source.get('OWNERNAME')}")
    markdown.append("")

    # Extract SOURCEFIELD attributes
    markdown.append("### Fields")
    markdown.append("| Field Name | Data Type | Length | Precision | Scale | Nullable |")
    markdown.append("|------------|-----------|---------|-----------|--------|----------|")

    for field in source.findall('SOURCEFIELD'):
        name = field.get('NAME')
        datatype = field.get('DATATYPE')
        length = field.get('LENGTH')
        precision = field.get('PRECISION')
        scale = field.get('SCALE')
        nullable = field.get('NULLABLE')

        markdown.append(f"| {name} | {datatype} | {length} | {precision} | {scale} | {nullable} |")

    return "\n".join(markdown)

def xml_to_markdown_table_target(root):
    """
    Extracts specific attributes from TARGET and TARGETFIELD tags and formats them in markdown.
    
    Args:
        root: ElementTree root element containing TARGET elements
    
    Returns:
        str: Markdown formatted string
    """
    # Initialize markdown content
    markdown = []

    # Find all TARGET elements
    targets = root.findall('.//TARGET')
    
    for target in targets:
        markdown.append(f"## Target name: {target.get('NAME')}")
        markdown.append(f"- **Database Type:** {target.get('DATABASETYPE')}")
        markdown.append(f"- **Database Name:** {target.get('DBDNAME')}")
        markdown.append(f"- **Table Name:** {target.get('NAME')}")
        markdown.append(f"- **Owner:** {target.get('OWNERNAME')}")
        markdown.append("")

        # Add fields table
        markdown.append("### Fields")
        markdown.append("| Field Number | Name | Data Type | Precision | Scale | Nullable | Key Type |")
        markdown.append("|--------------|------|-----------|-----------|--------|----------|-----------|")

        for field in target.findall('TARGETFIELD'):
            field_num = field.get('FIELDNUMBER')
            name = field.get('NAME')
            datatype = field.get('DATATYPE')
            precision = field.get('PRECISION')
            scale = field.get('SCALE')
            nullable = field.get('NULLABLE')
            keytype = field.get('KEYTYPE')

            markdown.append(f"| {field_num} | {name} | {datatype} | {precision} | {scale} | {nullable} | {keytype} |")
        
        markdown.append("\n")  # Add space between targets

    return "\n".join(markdown)

def extract_mapping_details(root, mapping_name):
    """
    Extracts mapping details including source to target field mappings and transformations.
    
    Args:
        root: ElementTree root element containing mapping information
        
    Returns:
        str: Markdown formatted string with mapping details
    """
    markdown = []
    markdown.append('---')
    # Initialize markdown content
    markdown.append(f"- **Mapping Name:** {root.get('NAME')}")
    markdown.append(f"- **Description:** {root.get('DESCRIPTION') or 'N/A'}")
    #find all MAPPINGVARIABLE     
    mapping_variables = root.findall('.//MAPPINGVARIABLE')

    markdown.append("\n** Mapping Variables **")
    for mapping_variable in mapping_variables:
        markdown.append(f"- **{mapping_variable.get('NAME')}**: {mapping_variable.get('VALUE')}")
    # Get all connectors
    connectors = root.findall('.//CONNECTOR')
    transformations = root.findall('.//TRANSFORMATION')
    instances = root.findall('.//INSTANCE')
    
    # Create a mapping table
    markdown.append("### Field Mappings")
    markdown.append("")
    markdown.append("| Source | Target | Transformation | Default Value | Data Type | Precision | Scale |")
    markdown.append("|--------|---------|----------------|----------------|-----------|-----------|---------|")
    
    # Track source to target mappings
    mapping_details = {}
    
    # First pass - collect all mappings
    for connector in connectors:
        from_instance = connector.get('FROMINSTANCE')
        from_field = connector.get('FROMFIELD')
        to_instance = connector.get('TOINSTANCE')
        to_field = connector.get('TOFIELD')
        # Skip if target instance is not the final target
        if connector.get('TOINSTANCETYPE') != 'Target Definition':
            continue
        
        transformation = None

        for instance in instances:
            if instance.get('TRANSFORMATION_NAME') == from_instance:
                for i in transformations:
                    if i.get('NAME') == from_instance:
                        transformation = i
                        break
                
        #find the from field in the transformation
        from_field_transformation = transformation.find(f'.//TRANSFORMFIELD[@NAME="{from_field}"]')

        default_value = from_field_transformation.get('DEFAULTVALUE')
        data_type = from_field_transformation.get('DATATYPE')
        precision = from_field_transformation.get('PRECISION')
        scale = from_field_transformation.get('SCALE')
        
        key = f"{to_instance}.{to_field}"
        if key not in mapping_details:
            mapping_details[key] = {
                'source': f"{from_field}",
                'target': f"{to_field}",
                'transformation': from_instance,
                'default_value': default_value,
                'data_type': data_type,
                'precision': precision,
                'scale': scale
                
            }
    
    
    # Add mappings to markdown
    for key, mapping in mapping_details.items():
        source = mapping['source']
        target = mapping['target']
        transformation = mapping['transformation']
        default_value = mapping['default_value']
        data_type = mapping['data_type']
        precision = mapping['precision']
        scale = mapping['scale']
                
        markdown.append(f"| {source} | {target} | {transformation} | {default_value} | {data_type} | {precision} | {scale} |")
    
    
    return "\n".join(markdown)

def extract_session_to_markdown(root):
    """
    Extracts session configuration details and formats them in markdown.
    
    Args:
        root: ElementTree root element containing SESSION element
    
    Returns:
        str: Markdown formatted string
    """
    # Initialize markdown content
    markdown = []

    # Session Basic Information
    markdown.append(f"# Session: {root.get('NAME')}")
    markdown.append(f"- **Mapping Name:** {root.get('MAPPINGNAME')}")
    markdown.append(f"- **Description:** {root.get('DESCRIPTION') or 'N/A'}")
    markdown.append(f"- **Version:** {root.get('VERSIONNUMBER')}")
    markdown.append("")

    # Transformation Components
    markdown.append("## Transformation Components")
    markdown.append("| Instance Name | Type | Stage | Pipeline | Repartition |")
    markdown.append("|---------------|------|-------|----------|-------------|")
    
    for trans in root.findall('.//SESSTRANSFORMATIONINST'):
        name = trans.get('SINSTANCENAME')
        type = trans.get('TRANSFORMATIONTYPE')
        stage = trans.get('STAGE')
        pipeline = trans.get('PIPELINE')
        repart = trans.get('ISREPARTITIONPOINT')
        
        markdown.append(f"| {name} | {type} | {stage} | {pipeline} | {repart} |")
    
    markdown.append("")

    # Connection Information
    markdown.append("## Connections")
    markdown.append("| Component | Connection Name | Type | Subtype |")
    markdown.append("|-----------|-----------------|------|---------|")
    
    for ext in root.findall('.//SESSIONEXTENSION'):
        if ext.find('.//CONNECTIONREFERENCE') is not None:
            conn = ext.find('.//CONNECTIONREFERENCE')
            name = ext.get('SINSTANCENAME')
            conn_name = conn.get('CONNECTIONNAME')
            conn_type = conn.get('CONNECTIONTYPE')
            conn_subtype = conn.get('CONNECTIONSUBTYPE')
            
            markdown.append(f"| {name} | {conn_name} | {conn_type} | {conn_subtype} |")
    
    markdown.append("")

    # Target Writer Settings
    markdown.append("## Target Load Settings")
    target_ext = root.find('.//SESSIONEXTENSION[@SUBTYPE="Relational Writer"]')
    if target_ext is not None:
        markdown.append("| Setting | Value |")
        markdown.append("|---------|-------|")
        for attr in target_ext.findall('ATTRIBUTE'):
            name = attr.get('NAME')
            value = attr.get('VALUE')
            markdown.append(f"| {name} | {value} |")
    
    markdown.append("")

    # Session Properties
    markdown.append("## Session Properties")
    markdown.append("| Property | Value |")
    markdown.append("|----------|-------|")
    
    important_attrs = [
        'Commit Type', 'Commit Interval', 'DTM buffer size',
        'Recovery Strategy', 'Pushdown Optimization',
        'Session Log File Name'
    ]
    
    for attr in root.findall('.//ATTRIBUTE'):
        if attr.get('NAME') in important_attrs:
            name = attr.get('NAME')
            value = attr.get('VALUE')
            markdown.append(f"| {name} | {value} |")

    return "\n".join(markdown)

def create_docs(file_name):

    # Parse XML
    
    tree = ET.parse(file_name)
    root = tree.getroot()
    base_folder = file_name.split(".")[0]
    os.makedirs(f'{base_folder}', exist_ok=True)

    with open(f'{base_folder}/workflow.md', 'w') as file:
        file.write(f'## Workflow name {file_name} \n')
        file.write("## Workflow description")
        file.write('\n')
        sources = root.findall('.//SOURCE')
        file.write('# Sources: \n')
        for source in sources:
            file.write(extract_xml_to_markdown_source(source))
        file.write('\n\n')
        file.write('# Targets')
        file.write('\n')
        file.write(xml_to_markdown_table_target(root))
        file.write('\n\n')
        file.write('## Mapping Details')
        file.write('\n')
        for mapping in root.findall('.//MAPPING'):
            file.write(extract_mapping_details(mapping, mapping.get('NAME')))
            file.write('\n\n')
        file.write('## Session')
        file.write('\n')
create_docs('sql_workflow.xml')
