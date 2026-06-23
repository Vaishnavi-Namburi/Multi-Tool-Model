from dotenv import load_dotenv

from openai import OpenAI

import json

import requests

import os

import yfinance as yf



load_dotenv()

client = OpenAI(

    base_url='http://localhost:11434/v1/',

    api_key='ollama',  # required but ignored

)





def get_weather(city: str): #weather api calling logic

    url = f"https://wttr.in/{city}?format=%C+%t" #open source weather api, we don't need to create apis for weather

    response = requests.get(url)



    if response.status_code == 200:

        return f"The weather in {city} is {response.text}."

    

    return "Something went wrong"



def run_command(cmd: str): #executing system commands logic

    result = os.system(cmd)

    return result





def stock_price(company:str): #stock market api calling logic

    stock = yf.Ticker(company)

    data = stock.history(period="1d")

    if data.empty:

        return "No stock data found"

    price = data["Close"].iloc[-1]

    return f"The current stock price of {company} is {price}"



available_tools = {

    "get_weather": get_weather, #using get_weather function where we designed our weather api calling logic

    "run_command": run_command, #using run_commad function where we designed our running system commands logic.

    "stock_price": stock_price  #using stock_price function where we designed our stock market api calling logic.

}



SYSTEM_PROMPT = f"""

    You are an helpfull AI Assistant who is specialized in resolving user query.

    You work on start, plan, action, observe mode.



    For the given user query and available tools, plan the step by step execution, based on the planning,

    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.



    Wait for the observation and based on the observation from the tool call resolve the user query.



    Rules:

    - Follow the Output JSON Format.

    - Always perform one step at a time and wait for next input

    - Carefully analyse the user query

    - Don't do all steps one at a time, go one by one, step by step response



    Output JSON Format:

    {{

        "step": "string",

        "content": "string",

        "function": "The name of function if the step is action",

        "input": "The input parameter for the function",

    }}



    Available Tools:

    - "get_weather": Takes a city name as an input and returns the current weather for the city

    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.

    - "stock_price": Takes a stock symbol as an input and returns the current stock market data

    - If the user specifies a company name instead of a ticker symbol, infer the ticker symbol first.

    Examples:

    Google -> GOOG

    Apple -> AAPL

    Microsoft -> MSFT

    Tesla -> TSLA

    Amazon -> AMZN

    IBM -> IBM

    



    Example:

    User Query: What is the weather of new york?

    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}

    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}

    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}

    Output: {{ "step": "observe", "output": "12 Degree Cel" }}

    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}



"""



#automating the agent (llm+tools(get_weather,run_command))



messages = [
  { "role": "system", "content": SYSTEM_PROMPT }
]

def agent_response(query):

    messages.append({ "role": "user", "content": query })

    while True:

        response = client.chat.completions.create(

            model="qwen2.5-coder:3b",

            response_format={"type": "json_object"},

            messages=messages

        )



        messages.append({ "role": "assistant", "content": response.choices[0].message.content })

        parsed_response = json.loads(response.choices[0].message.content)



        if parsed_response.get("step") == "plan":#output will be of modes:plan,plan, action

            print(f"🧠: {parsed_response.get('content')}")

            continue



        if parsed_response.get("step") == "action":#once i hit action mode

            tool_name = parsed_response.get("function") #will get the respective function 

            tool_input = parsed_response.get("input")



            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")



            if available_tools.get(tool_name) != False: #if that function is in available tools

                output = available_tools[tool_name](tool_input) #func() calling

                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) }) #adding that action response in messages

                continue #go to the next mode

        

        if parsed_response.get("step") == "output":
            return parsed_response.get('content')