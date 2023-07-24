import os
import json
from decouple import config
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

def create():

    #Set env variables
    os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

    with open("data.json") as f:
        data = json.load(f)

        #Seperate variable keys
        standard = {
            "incidentCategory" : data["Incident Category"],
            "typeOfProperty" : data["Type Of Property"],
            "occupierStatus" : data["Occupier Status"],
            "propertyAge" : data["Property Age"],
            "listedStatus" : data["Listed Status"],
            "complexLoss" : data["Complex Loss"],
            "emergencyElectricianRequired" : data["Emergency Electrician Required"],
            "electricianNote" : data["Electrician's Note"],
            "damageToCeilingOrWallPanelNoted" : data["Damage To Ceiling Or Wall Panel Noted"],
            "intakePhaseCountOfRoomsAffected" : data["Intake Phase Count Of Rooms Affected"],
            "intakePhaseCountOfFloorsAffected" : data["Intake Phase Count Of Floors Affected"],
            "intakePhaseFloorOfIncident" : data["Intake Phase Floor Of Incident"],
            "intakePhaseLowestFloor" : data["Intake Phase Lowest Floor"],
            "intakePhaseRoomOfIncident" : data["Intake Phase Room Of Incident"],
            "siteSurveyCountOfRoomsAffected" : data["Site Survey Count Of Rooms Affected"],
            "siteSurveyCountOfFloorsAffected" : data["Site Survey Count Of Floors Affected"]
        }
        non_standard = {
            "occupierOrLandlordConcernsAndDates" : data["Occupier Or Landlord's Concerns And Dates"],
            "initialRerrerInstructions" : data["Initial Referrer Instructions"],
            "incidentDescriptionByOccupier" : data["Incident Description By Occupier, Landlord, or Agent"]
            }

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

    standard_response = standard_chain.run(json.dumps(standard))
    non_standard_response = non_standard_chain.run(json.dumps(non_standard))
    full_description_response = full_description_chain.run(standard_desc=standard_response, non_standard_desc=non_standard_response)

    return full_description_response




