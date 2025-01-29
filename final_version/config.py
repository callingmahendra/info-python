from dataclasses import dataclass
import os
@dataclass
class Config:
    workflow_file: str = "./resources/sql_workflow.xml"
    output_file: str = "./output/analysis2.json"
    merged_file: str = "./output/analysis2.md"
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")
    api_base: str = "https://models.inference.ai.azure.com"
    #api_base:str = "http://localhost:11434/v1"
    #api_model: str = "llama3.1" #"llama3"
    api_model: str = "gpt-4o"
    code_file: str = "./output/code.py"
    summary_file: str = "./output/summary.md"
