import streamlit as st
import os 

from openai import OpenAI


client = OpenAI( api_key=st.secrets["API_key"], 
                )

async def gen_response(message):
# generates a response with openai
    res = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = message
    )

    return res.choices[0].message.content

async def app():
  # To initialize the app
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1

    if st.session_state["current_form"] == 1:
        await intro_page()
    elif st.session_state["current_form"] == 2:
        await form_1_page()


async def intro_page():
   # Presents an intro page
    st.header("Fitness Plan Maker")
    intro_text = """by Isaiah Louis Emmanuel Yee\n
    This is Plan Maker, an openAI powered tool used to generate a fitness plan. Select options below to start
    """
    st.write(intro_text)

    form_1 = st.form("Intro")
    
    user_sex = form_1.selectbox("What is your sex?", ("Male", "Female"))
    fitness_goal = form_1.text_input("What is your fitness goal?")

    submit_1 = form_1.form_submit_button("Start planning")

    if submit_1:
        if user_sex and fitness_goal:
            st.session_state["user_sex"] = user_sex
            st.session_state["fitness_goal"] = fitness_goal
            messages = []
            messages.append({"role": "user", "content": f"You will generate choices of types of fitness plans based on {fitness_goal}. Create a list of comma separated values. Use 1 word each item in list. Don't add additional text"})
            messages.append({"role": "system", "content": "You are a fitness pal AI."})
            messages.append({"role": "system", "content": f"The user is {user_sex} so detail the type of program to think of based on the user's sex"})
            response = await gen_response(messages)
            choices = response.split(", ")
            st.session_state["response"] = response
            st.session_state["choices"] = choices
            st.session_state["current_form"] = 2
            await form_1_page()

        else:
            if not user_sex:
                form_1.error("No Sex")
            if not fitness_goal:
                form_1.error("No Goal")


async def form_1_page():
  # Second form to handle choices
    response = st.session_state["response"]
    choices = st.session_state["choices"]
    st.header("Choice of Plan")
    st.text(response)
    form_2 = st.form("Pick the Choice")
    choice = form_2.selectbox("Choose a plan", choices)
    submit_2 = form_2.form_submit_button("Submit")
    messages = []
    user_sex = st.session_state["user_sex"]
    fitness_goal = st.session_state["fitness_goal"]

    if submit_2:
        messages.append({"role": "user", "content": f"Generate a full weekly fitness and meal plan based on {choice}"})
        messages.append({"role": "system", "content": f"The user is {user_sex} so detail the type of program to think of based on the user's sex"})
        messages.append({"role": "system", "content": f"The user also aims to {fitness_goal} so design around that"})
        response = await gen_response(messages)
        st.session_state["open_ai_response"] = response
        st.write(response)
    else:
        form_2.error("Missing Choice")
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
