import os
import sys
import random
import json
from decouple import config
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

def create():

    restList = []

    # Load JSON data
    with open("restoration.json") as f:

        data = json.load(f)
        
        for restoration in data:

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

    return standard_response


    