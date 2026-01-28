import logging 
import time 
from pydantic import BaseModel , Field 
import requests
from typing import Dict , Optional , Any 
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMStool:
    """
    This is a tool to send a static SMS via API to the given phone number 
    where if we face any error , we retry for 3 times leaving a 1 second gap 
    """
    def __init__(self):
        self.url = ""   # some URL we can paste it here 
        self.Default_Phone_Number = "1234567891"
        bank="ABC"
        self.Default_Message = f"Hey welcome to {bank} bank , if you want to proceed with our services please contact out customer care"
        self.Retry = 3
        self.Timeout = 5
        self.Delay = 1

    
    def call_sms_api(self , Phone_Number:str , Message:str) -> Dict[str,Any]:

        logger.info("Now the api is being called ")

        payload = {
            "phone_number" :Phone_Number ,
            "message" : Message
        }

        response = requests.post(
            self.url,
            json=payload,
            headers={"Content-Type":"application/json"},
            timeout = self.Timeout
        )

        response.raise_for_status() # if there any error it'll detect using the status code and try us as an error 
        return response.json()
    
    def create_sms_tool(self):

        class Schema(BaseModel):
            phone_number : Optional[str] = Field(None,description="This is the phone number where we have to send the message" )
            message: Optional[str] = Field(None, description = "This is the message that we have to send the mentioned number")

        @tool("sms_tool" , description = "use this tool if you want to send SMS" , args_schema = Schema)
        def sms_tool(phone_number:Optional[str]=None, message:Optional[str]=None)-> Dict[str,Any]:
            """
            This is the function where our logic , retry and all other things comes 
            """

            phone_number = phone_number or self.Default_Phone_Number
            message = message or self.Default_Message

            for i in range(1,self.Retry+1):
                try: 
                    logger.info("Sending the message via the help of API ")

                    response = self.call_sms_api(phone_number,message)


                    return {
                        "status": "success",
                        "attempts": i,
                        "phone_number": phone_number,
                        "response":response
                    }
                except Exception as e:
                    logger.error(f"Facing some error , Try to fix it and the error is {e}")
                    
                    if i<self.Retry:
                        time.sleep(self.Delay)
                
            return {
                "status":"failed", 
                "attempts":self.Retry,
                "phone_number":phone_number,
                "error": "SMS trigger failed after retries"
            }
        
        return sms_tool
    

if __name__=="__main__":
    sms=SMStool()
    sms.url="https://example.com/sms"
    sms_tool= sms.create_sms_tool()

    result = sms_tool.invoke({
        "phone_number" : "2635726352",
        "message" :"Hello from Pragadish"
        }
    )
    print(result)










    

        
    