from typing import Dict, Any  # This is to just define the types explicitly
from langchain_core.tools import tool #We use this bcoz when there is some AI in a langchain flow, it has to automatically call the tool so allow that we use this tool 
from pydantic import BaseModel, Field #This is to structure the data like datatypes and etc and also validate it whether it is correct or not 

class ToolName:
    def __init__(self, dynamic_variables: Dict[Any, Any], logger): # this is like a special function , where we initialize configuration and also log 
        self.logger = logger
        #here the logging library will be in the file which is calling and we are importing it directly here 
        # Add your configuration here
        # self.config_value = dynamic_variables.get("config_key", "default_value")
        
    def create_tool_name(self):  # This is the function to create our tool 
        #self keyword - lets say we create a class and then for instance/object which we will call but we shld mention it is this object we need to do all the things so we use the word self , 
        # it is not a keyword but it is the standard one most of the people use 
        # Define parameter schema
        class ToolRequest(BaseModel):     # This is class to define the schema of the input or the data
            #BaseModel - it is where we define the datatypes and also the structure 
            #Field - it is like we add more information like - description , default values 
            param1: float = Field(description="Description of param1")
            param2: str = Field(description="Description of param2")
        
        @tool("tool_name", description="Tool description", args_schema=ToolRequest) # This is the special thing we use so that ai can automatically use/call this tool
        #which includes the tool name , description , args_schema - description is so important so that AI will know the exact usecase of this tool 
        def tool_name(param1: float, param2: str) -> Dict[str, Any]: # here starts our tool creation
            try:
                # Add your tool logic
                result = param1 * 2  # Example calculation
                
                self.logger.info("Tool executed")
                
                return {
                    "param1": param1,
                    "param2": param2,
                    "result": result,
                    "status": "success"
                }
            except Exception as e:
                self.logger.error(f"Tool error: {e}")
                return {"error": str(e), "status": "failed"}
        
        return tool_name

    def get_tools(self):  # This is like a middlemen between out above tool creation and other files who needs tools access or to create it ,
        #the other files dont know the function name to create the tool so they call this function and this function does everything to them , 
        #it is returned in list but there can be many tools , so it is return as a list 
        return [self.create_tool_name()]