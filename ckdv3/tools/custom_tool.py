import subprocess

from crewai.tools import BaseTool
from typing import Type

from pydantic import BaseModel, Field

import os
import json

class DoclingToolInput(BaseModel):
    """Input schema for DoclingTool."""
    pdf_file_name: str = Field(..., description="path of the PDF file")

class DoclingTool(BaseTool):
    name: str = "Docling"
    description: str = (
        "Tool used to parse input PDF file and convert it into JSON file"
    )
    args_schema: Type[BaseModel] = DoclingToolInput

    def _run(self, pdf_file_name: str) -> str:
        # Implementation goes here
        """Uses Docling tool to process a PDF file and convert it to a JSON file."""
        try:
            # Running Docling as a command-line tool
            cmd = f"docling --to json --force-ocr {pdf_file_name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
            # result = 0
            # if result == 0:
                json_file = os.path.splitext(pdf_file_name)[0] + ".json"
                print("Document processed successfully! Output saved to file:", json_file)
                return json_file
            else:
                return f"Error processing document: {result.stderr}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"



class Find_Next_Text_NodeInput(BaseModel):
    """Input schema for find_next_text_node."""
    file_name_json: str = Field(..., description="Name of the JSON file to parse")
    value: str = Field(..., description="The field to search for in the JSON file")


class Find_Next_Text_Node(BaseTool):
    name: str = "find_next_text_node"
    description: str = (
        "Recursively searches for a key-value pair in JSON and returns the next node with key 'text'"
    )
    args_schema: Type[BaseModel] = Find_Next_Text_NodeInput

    # def _run(self, input_pdf: str, value: str) -> str:
    def _run(self, file_name_json: str, value: str) -> str:
        # Implementation goes here
        print("file name json: ", file_name_json)

        with open(file_name_json, "r") as file:
            data = json.load(file)

        next_text_node = self.find_next_text_node_func(data, 'text', value)

        return f"The value of {value} is {next_text_node['text']}"

    def find_next_text_node_func(self, json_data, target_key, target_value):
        """
        Recursively searches for a key-value pair in JSON and returns the next node with key 'text'.

        :param json_data: The JSON object (dict or list).
        :param target_key: The key to search for (e.g., "text").
        :param target_value: The value to match (e.g., "CO2 Total").
        :return: The next node with key "text" after the matched node, or None if not found.
        """
        found_target = False  # Flag to track if we've found the target node

        def recursive_search(node):
            nonlocal found_target  # Allow modifying the flag inside the nested function

            if isinstance(node, dict):
                for key, value in node.items():
                    if key == target_key and value == target_value:
                        found_target = True  # Mark that we found the target

                    elif key == "text" and found_target:  # Return the first "text" node found after target
                        return node

                    elif isinstance(value, (dict, list)):
                        result = recursive_search(value)
                        if result:
                            return result

            elif isinstance(node, list):
                for item in node:
                    result = recursive_search(item)
                    if result:
                        return result

            return None  # Return None if no match is found

        return recursive_search(json_data)
