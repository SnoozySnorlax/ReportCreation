import os
import sys
import json
from pyjsonq import JsonQ
from decouple import config
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

def create():

    #Set env variables
    os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

    with open("rooms.json") as f:
        roomsData = json.load(f)
        for room in roomsData:
            
            readingsCount = JsonQ('rm.json').at('').where('location', '=', room['Room Name']).count()

            if(readingsCount > 1):
                
                reading = JsonQ('rm.json').at('').where('location', '=', room['Room Name']).get()

                print(reading)

                sys.exit()
                    
                roomList = list(room.items())

                roomList.append(reading)

                
                print(roomList)

            print(readingsCount)

        sys.exit()
            
    #Prompt templates
    standard_template = PromptTemplate(
        input_variables = ['facts'],
        template='Write me a description using all of the facts from the json provided {facts}, keep it factual and based off the information I have provided'
    )
    non_standard_template = PromptTemplate(
        input_variables = ['bigfacts'],
        template='Write me a description using all of the facts from the json provided {bigfacts}, keep it factual and based off the information I have provided'
    )
    full_description_template = PromptTemplate(
        input_variables = ['standard_desc','non_standard_desc'],
        template='Combine these two descriptions: {standard_desc}, {non_standard_desc}. Keep it factual.'
    )

    #Llms
    llm = OpenAIChat(temperature=0.2, model='gpt-3.5-turbo-16k')
    standard_chain = LLMChain(llm=llm, prompt=standard_template, verbose=True, output_key='standard_desc')
    non_standard_chain = LLMChain(llm=llm, prompt=non_standard_template, verbose=True, output_key='non_standard_desc')
    full_description_chain = LLMChain(llm=llm, prompt=full_description_template, verbose=True, output_key='full_desc')

    standard_response = standard_chain.run(json.dumps(roomsData))
    non_standard_response = non_standard_chain.run(json.dumps(rmData))
    full_description_response = full_description_chain.run(standard_desc=standard_response, non_standard_desc=non_standard_response)

    return full_description_response




