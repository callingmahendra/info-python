from openai import OpenAI
from typing import Dict
from config import Config

config = Config()
api_key = config.openai_api_key
api_base = config.api_base
api_model = config.api_model

class OpenAIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=api_key,base_url=api_base)

    def generate_source_information(self, source_information: str) -> Dict:
        """
        Generate source information from the source information.
        """
        prompt = f"""
        Analyze this Informatica PowerCenter Source and extract the source information.
        Source: {source_information}
        Return the following information only: Dont return anything else. 
        *   **Source:**
        *   System: [e.g., Oracle Database, Flat File, etc.]
        *   Tables/Files: [List of source tables/files]
        *   Data Fields: [List of source data fields with data types]

        *   **Target:**
        *   System: [e.g., Snowflake, AWS S3, etc.]
        *   Tables/Files: [List of target tables/files]
        *   Data Fields: [List of target data fields with data types]
        """
        try:
            response = self.client.chat.completions.create(model=api_model,
            messages=[{"role": "user", "content": prompt}])

            print("Response received")
            return response.choices[0].message.content
        except Exception as e:
            return {
                'summary': f"Error analyzing transformation: {str(e)}"
            } 
    
    def generate_source_code(self, source_information: str, summary: str, sample_code: str) -> str:
        prompt = f"""
        You are an expert in python and ETL. You are given a source information and summary. 
        You need to generate the python ETL code for the given source information and summary.
        You need to generate code for load_source_data and load_target_data function only.
        Use comments to explain the code.
        dont return anything else just the code. and code should be explainable with comments.
        Source Information: {source_information}
        Summary: {summary}
        Sample Code: {sample_code}
        """
        try:
            response = self.client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return {
                'summary': f"Error analyzing transformation: {str(e)}"
            }

    def generate_mapping_summary(self, mapping_xml: str) -> str:
        prompt = f"""
        You are an expert in python and ETL. You are given a mapping xml.
        You need to generate the summary for the given mapping xml.
        Mapping XML: {mapping_xml}
                Return the following information only: Dont return anything else. 
        **3. Mapping Details:**

        | Source Field | Target Field | Transformation Logic |
        |---|---|---|
        | Source_Field1 | Target_Field1 | Direct Map |
        | Source_Field2 | Target_Field2 | Data Type Conversion (e.g., String to Date) |
        | Source_Field3 | Target_Field3 | Expression Transformation (e.g., Calculate Age) |
        | Source_Field4 | Target_Field4 | Lookup Transformation (e.g., Enrich data from a lookup table) |
        | ... | ... | ... |

        **4. SQL Queries and Stored Procedures:**

        *   [List of SQL queries used in the workflow, including:
            *   Source Qualifier queries
            *   Expression Transformation logic
            *   Filter Transformation conditions]
        *   [List of stored procedures used in the workflow, including:
            *   Name of the stored procedure
            *   Input parameters
            *   Output parameters
            *   Brief description of the procedure's functionality]

        **5. Business Rules and Logic:**

        *   [Describe any specific business rules or logic implemented in the workflow, such as:
            *   Data validation rules
            *   Data quality checks
            *   Conditional logic for data routing
            *   Error handling mechanisms]
        """
        try:
            response = self.client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return {
                'summary': f"Error analyzing transformation: {str(e)}"
            }
    def generate_mapping_code(self, mapping_xml: str, mapping_summary: str, sample_code: str) -> str:
        prompt = f"""
        You are an expert in python and ETL. You are given a mapping xml and source code.
        You need to generate the python ETL code for the given mapping xml and source code.
        dont return anything else just the code. and code should be explainable with comments.
        Mapping XML: {mapping_xml}
        mapping summary: {mapping_summary}
        Sample Code: {sample_code}
        """
        try:
            response = self.client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return {
                'summary': f"Error analyzing transformation: {str(e)}"
            }
        
    def generate_final_code(self, mapping_code: str, source_code: str) -> str:
        prompt = f"""
        You are an expert in python and ETL. You are given a mapping code and source code.
        You need to generate the final python ETL code for the given mapping code and source code.
        Mapping Code: {mapping_code}
        Source Code: {source_code}

        Dont return anything else just the code. and final code should be explainable with comments.

        """
        try:
            response = self.client.chat.completions.create(model=api_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return {
                'summary': f"Error analyzing transformation: {str(e)}"
            }   