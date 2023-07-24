import os
import sys
import random
import json
from decouple import config
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain



restList = []

    # Load JSON data
with open("restoration.json") as f:

        restoration_data = json.load(f)
        
        for restoration in restoration_data:

            for item in restoration['Items']:
              
                restList.append(item['Name'])


restList = list(dict.fromkeys(restList))
   

    # Do all of your open AI stuff below
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

    #Prompt templates
standard_template = PromptTemplate(
        input_variables = ['facts'],
        template='Write me a description, not a list, of work to be carried out using all of the facts from the array provided {facts}, keep it factual and based off the information I have provided'
    )

    #Llms
llm = OpenAIChat(temperature=0.2, model='gpt-3.5-turbo-16k')
standard_chain = LLMChain(llm=llm, prompt=standard_template, verbose=True, output_key='standard_desc')

standard_response = standard_chain.run(restList)


    #Set env variables
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

with open("data.json") as f:
        data = json.load(f)

    #Prompt templates

description_template = PromptTemplate(
        input_variables = ['bigfacts'],
        template='Write me a description using all of the facts from the json provided {bigfacts}, keep it factual and based off the information I have provided'
    )

report_template = PromptTemplate(
        input_variables = ['full_description_response','standard_response'],
        template='Using the data in {full_description_response} and {standard_response} write a report with the following headings: Property description and use, Purpose of our work, Investigation carried out, Restoration plan, Further comments. Keep it factual. Include number of affected rooms and floors under the investigation carried out heading. Avoid using lists apart from under the restoration plan heading.'
    )

    #Llms
llm = OpenAIChat(temperature=0.2, model='gpt-3.5-turbo-16k')
full_description_chain = LLMChain(llm=llm, prompt=description_template, verbose=True, output_key='full_desc')
report_chain = LLMChain(llm=llm, prompt=report_template, verbose=True, output_key='report_desc')

description_response = full_description_chain.run(json.dumps(data))
report_response = report_chain.run(full_description_response=description_response, standard_response=standard_response)

print(report_response)
