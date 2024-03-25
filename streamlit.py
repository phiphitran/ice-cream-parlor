import streamlit as st
from streamlit_helper import check_menu, check_inventory, purchase_ice_cream, restock_ice_cream, give_user_feedback, get_all_feedback, feedback_report
from tools import tools
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
import functools
import json

api_key = <mistral-api-key>
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

# Functions used for agent to perform function calling
names_to_functions = {
    'check_menu': functools.partial(check_menu),
    'check_inventory': functools.partial(check_inventory),
    'purchase_ice_cream': functools.partial(purchase_ice_cream),
    'restock_ice_cream': functools.partial(restock_ice_cream),
    'give_user_feedback': functools.partial(give_user_feedback),
    'get_all_feedback': functools.partial(get_all_feedback),
    'feedback_report': functools.partial(feedback_report)
}

# Initilizing message history
MESSAGES = "messages"
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [ChatMessage(role="assistant", content="Hi and welcome to the ice cream shop!")]

# Printing message history
for msg in st.session_state[MESSAGES]:
    if msg.role != "tool":
        st.chat_message(msg.role).write(msg.content)

# Creates a chat window for user to interact with agent.
user_input: str = st.chat_input("Enter a prompt here")
if user_input:
    # Adding user input to history and checking if function calling is needed
    st.session_state[MESSAGES].append(ChatMessage(role="user", content=user_input))
    st.chat_message("user").write(user_input)
    response = client.chat(model=model, messages=st.session_state[MESSAGES], tools=tools, tool_choice="auto")
    st.session_state[MESSAGES].append(response.choices[0].message)
    perform_function_call = response.choices[0].message.tool_calls
    if perform_function_call is not None:
        # Extracting function name and its parameters
        tool_call = perform_function_call[0]
        function_name = tool_call.function.name
        function_params = json.loads(tool_call.function.arguments)
        print(function_name, function_params)
        # Performing function calling and saving output for agent to use
        function_result = names_to_functions[function_name](**function_params)
        st.session_state[MESSAGES].append(ChatMessage(role="tool", name=function_name, content=function_result))
        response = client.chat(model=model, messages=st.session_state[MESSAGES])
        st.session_state[MESSAGES].append(response.choices[0].message)
    st.chat_message(st.session_state[MESSAGES][-1].role).write(st.session_state[MESSAGES][-1].content)
