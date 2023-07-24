import os
import json
import sys
from decouple import config
from langchain.agents import (
    create_json_agent,
    AgentExecutor
)
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
from langchain.prompts import PromptTemplate

import section

print(section())

sys.exit()

#Set env variables
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

with open("data.json") as f:
    data = json.load(f)
json_spec = JsonSpec(dict_=data, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)

json_agent_executor = create_json_agent(
    llm=OpenAI(temperature=0),
    toolkit=json_toolkit,
    verbose=True
)

response = json_agent_executor.run('write a detailed description about the property and incident using the property type, listed status, Incident Category, Site Survey Count Of Rooms Affected, Site Survey Count Of Floors Affected and occupier status')

print(response)