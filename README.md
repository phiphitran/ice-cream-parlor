# The Menti Ice Cream Parlor Project

## About
This is an AI agent that can interact with customers through an API. Users can see and choose available ice cream flavors, provide feedback and get a report of the customer satisfaction.

> [!NOTE]
> The project is currently in an early development stage. Further testing and formatting and can be done to improve the answers of the agent.

## Installation
Start with cloning the project and install the packages.
```
pip install -r requirements.txt
```
## How to interact with the agent
Open a terminal, locate the main.py and run
```
uvicorn main:app --reload
```
Keep the window open and in a second terminal, locate the streamlit.py and run it using
```
streamlit run streamlit.py
```
A browser tab will open where you can chat with the agent.

Example flow of user input:
- Hi!
- Can I see the menu please?
- How does the inventory looks like?
- I want to have 5 scoops of cheesecake
- How many scoops of each flavor do you have left?
- Im here to restock the hazelnut flavor. I have 5 scoops to give
- I had the chocolate ice cream and it was delicious! I will give this as feedback and a rating of 5!
- Can you give me the list of all feedback?
- I want the feedback report.

> [!NOTE]
> If an error occurs, the app needs to be restarted to perform well again.

## Design rationale
Below are the tools used and a short description of why they were chosen
- FastAPI
    - Minimalistic framework that uses python with security and authorization features that can easily be implemented
- Sqlite3
    - Lightweight database engine that already is built into the Python's standard library.
- Streamlit
    - Easy to use open source Python library to quickly create and share web apps.
- Transformers (huggingface)
    - Used to perform sentiment analysis on feedback for feedback report
- MistralAI
    - To ensure data privacy, open-source models are preferred and OpenAI models was thus excluded. 
    - Another important aspect to consider was the possibility to connect to external tools, such as APIs, and perform a so called function calling. Limited chat models has this functionality today and one of the models with clear documentations was Mistral.

## Challenges
- One of the time consuming part was to find relevant tools and modules to use, for example the function calling. 
    - Material related to OpenAI is easier to find. This was in the beginning used as inspiration to replicate, using open-source tools instead. Was quickly abandoned due to the time consumption.
    - Modules from LangChain was tested, for example the SQL Database to construct SQL statements for the database. The limitation here is that it only generates the code, without acting on it.
    - The challenge was that I did from the beginning not know what tools to use or how to implement the solution. Even if the goal was clear, the plan was not. I knew that I needed a database and make API calls, and after that it was learning by doing. The structure was put together piece by piece.