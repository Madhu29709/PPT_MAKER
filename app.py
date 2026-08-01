# ===== step 1 load modules==========
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

st.set_page_config(layout ="wide")

# ======== step 2 LOAD ENV AND API - KEYS=======
st.title("your Agent PPT Generator")
st.header("""user can generate ,PPT,Images, and fetch Latest news""")

st.sidebar.title("Give API KEYS")
GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type ="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type ="password")

ALL_API =[GOOGLE_API_KEY,TAVILY_API_KEY]

if not all(ALL_API):
  st.sidebar.error("Must Pass ALL API-Keys")
  url ="https://aistudio.google.com/api-keys"
  st.markdown(f"Get Google API Keys-{url}")

  url ="https://app.tavily.com/playground"
  st.markdown(f"Get Tavily API Keys-{url}")

elif all(ALL_API):
  st.success("API KEYS LOADED")
  options = ["gemini-3.5-flash-lite","gemini-3.5-flash",
             "gemini-2.5-flash-lite","gemini-2.5-flash",]

  selected_model =st.selectbox("Select=model",options=options)

  model = ChatGoogleGenerativeAI(
    model = selected_model,
    google_api_key = GOOGLE_API_KEY)

else:
  st.sidebar.info("Try Valid API-keys")

# ================ step 3==========================
#  Search_latest info using tavily
def search_latest_info(query):
  """This function helps to give
  latest search using tavily
  based on the given user realted research os
  contents"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  responsev = client.search(query)
  return response


def generate_image(img_prompt,slide_no =1):
  """This function helps user to generate
  image using  free api , with given
  img_prompt, with slide no"""


  url =f"https://image.pollinations.ai/{img_prompt}"
  import requests as r
  content  = r.get(url).content
  with open(f"ai_image_{slide_no}.jpeg",'wb') as f:
    f.write(content)
  return url

def run_agent(leader_agent, query):

    prompt = f"""Based on Below given Query,
    your task is to call specific tool, first to
    promptify user prompt, than call image tool, or
    latest search if required. give slide dynamic, ui ux,
    with creative design, keep help of function to generate image
    based on given topic,
    Generate image using
    with number of slide asked, and use time sleep to hit image request on server
    and using file handling embed this in output html, use java script function
    give Final response output in HTML, no markdowns
    user query given below:
    """

    prompt = prompt + query

   
    response = leader_agent.invoke({
        'messages': [ {'role': 'user',
                       'content': prompt }]})

    code = response['messages'][-1].content[-1]['text']

    return code

#  leader-agent creation
if all(APP_API):
  leader_agent  = create_agent(
    model = model,
    tools =[search_latest_info,
            #generate_image
            ])
 # leader_agent

else:
  st.info("Give  API - keys frist to  load agent")


# ================ step 4 STREAMLIT NAVBARS==================


tab1, tab2, tab3, = st.tabs(["Generate Image",
                            "Fetch News"],
                           "Generate PPT")

user_input = st.text_area("Write Prompt & click Enter")

if (user_input):
  with tab1:
    if st.button("Click to Generate Image",key ="Image-Button"):
      with st.spinner("Running Agent"):
        try:
          url = generate_image(user_input)
          import request as r
          img_data = r.get(url)
          st.image(url)
        except Exception as error:
          st.error("Error Code:",err)

  with  tab2:
     if st.button("Fetch Latest News",key ="News-Button"):
       with st.spinner("Running Agent"):
        try:
          prompt = """Give Latest News Related to Given Query
          in   Dynamic  HTML .Output with cards Design Formate.
           strict HTML output,No Any markdown Response
           user Query:"""
          response = leader_agent.invoke({'messages': [ {'role': 'user',
                                                 'content': prompt }]})

          code = response['messages'][-1].content[-1]['text']
          st.html(code,widht ="stretch",unsafe_allow_javascript = True)
        except Exception as err:
          st.error("Error Code:",err)

  with tab3:
      if st.button("Click To Generate PPT",key ="PPT-Button"):
       with st.spinner("Running Agent"):
        try:
          code = run_agent(leader_agent,user_agent)
          st.html(code,widht ="stretch", unsafe_allow_javascript = True)
          if  st.download_buttion(label ="DOWNLOAD-PPT",
                                 data = code,
                                 file_name ='ppt.html',
                                 mime = 'text/html'):
              st.success("PPT DOWNLOAD Successfully!!")
        except Exception as err:
          st.error("Error Code : ",err)
                                   
          



    
  

      

      
          



       
       
    


 

 




  



