import openai
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchResults
from io import StringIO
import sys


class MainAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
            )

        # Initialize ChatOpenAI with gpt-3.5-turbo and max_tokens set to 3000
        self.openai_llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.3,  # Lowered temperature for more consistent answers
            top_p=0.9,  # Added top_p for better control over response sampling
            openai_api_key=self.api_key,
            max_tokens=3000,  # Adjusted max_tokens
        )

        # Initialize specialized agents as tools for LangChain
        self.tools = [
            Tool(
                name="Problem Solver",
                func=self.problem_solver_agent,
                description="Handles problem-solving queries, generates code solutions, and provides explanations.",
            ),
            Tool(
                name="Topic Explorer",
                func=self.topic_explorer_agent,
                description="Provides detailed topic explanations and suggests related topics.",
            ),
            Tool(
                name="Code Debugger",
                func=self.code_debugger_agent,
                description="Analyzes code, finds errors, and provides correct solutions.",
            ),
            Tool(
                name="Web Search",
                func=DuckDuckGoSearchResults().run,
                description="Searches the web for relevant information.",
            ),
        ]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.openai_llm,
            agent="zero-shot-react-description",
            verbose=True,  # Set verbose to True to capture detailed reasoning steps
        )

    def dispatch_query(self, user_query):
        try:
            # Capture intermediate steps and response together
            log_stream = StringIO()
            original_stdout = sys.stdout
            sys.stdout = log_stream

            # Gather response using a more cohesive prompt
            full_query = (
                f"Identify the key topics and provide a summary of the problem: {user_query}\n"
                f"Provide a brute force solution, including Python code, explanation, and time complexity analysis.\n"
                f"Provide a better solution with Python code, explanation, and time complexity analysis, highlighting improvements over brute force.\n"
                f"Provide the optimal solution, including Python code, a detailed explanation of its time complexity, and why it is the best approach.\n"
                f"Make sure each solution includes a detailed step-by-step explanation, and highlight the differences between each approach."
            )

            response = self.agent.run(full_query)
            sys.stdout = original_stdout

            # Combine intermediate steps and the final response
            intermediate_steps = log_stream.getvalue()
            full_response = (
                "## Intermediate Steps:\n"
                + intermediate_steps
                + "\n\n## Final Answer:\n"
                + response
            )
            return full_response
        except Exception as e:
            sys.stdout = original_stdout  # Ensure stdout is reset
            return f"An error occurred while processing your request: {str(e)}"

    def problem_solver_agent(self, user_query):
        problem_solver = ProblemSolverAgent(self.openai_llm)
        return problem_solver.handle_query(user_query)

    def topic_explorer_agent(self, user_query):
        topic_explorer = TopicExplorerAgent(self.openai_llm)
        return topic_explorer.handle_query(user_query)

    def code_debugger_agent(self, user_query):
        code_debugger = CodeDebuggerAgent(self.openai_llm)
        return code_debugger.handle_query(user_query)


class ProblemSolverAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are an expert programming assistant."
                ),
                HumanMessagePromptTemplate.from_template(
                    "Problem: {user_query}\nProvide the following details:\n1. Identify the key topics involved and provide a summary of these topics.\n2. Clearly explain the problem statement with context and examples.\n3. Provide a brute force solution, including full Python code, a detailed explanation of its time complexity, limitations, and a step-by-step explanation of how the code works.\n4. Provide a better solution, including full Python code, a detailed explanation of its time complexity, improvements over the brute force solution, and a step-by-step explanation of the code.\n5. Provide the optimal solution, including full Python code, a detailed explanation of its time complexity, why it is the most efficient approach, and a step-by-step explanation of how the code works.\nMake sure that all code is properly formatted, and provide step-by-step reasoning for each solution, including real-world analogies if possible to make the concepts clearer."
                ),
            ]
        )

    def handle_query(self, user_query):
        response = self.llm(self.prompt.format_messages(user_query=user_query))
        return response.content.strip()


class TopicExplorerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful assistant for exploring technical topics."
                ),
                HumanMessagePromptTemplate.from_template(
                    "Explain the following topic in detail and suggest related topics: {user_query}. Provide a thorough explanation and examples where possible."
                ),
            ]
        )

    def handle_query(self, user_query):
        response = self.llm(self.prompt.format_messages(user_query=user_query))
        return response.content.strip()


class CodeDebuggerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful assistant for debugging and correcting code."
                ),
                HumanMessagePromptTemplate.from_template(
                    "Analyze the following code for errors, provide detailed corrections, and suggest solutions. Include full corrected code and explanations for each change. Explain the reasons behind each correction and provide best practices. {user_query}"
                ),
            ]
        )

    def handle_query(self, user_query):
        response = self.llm(self.prompt.format_messages(user_query=user_query))
        return response.content.strip()


# Streamlit Frontend for Chatbot Interface
st.title("Chat with AI Agent")
st.write("This is a chatbot interface for interacting with the AI agent.")

if "main_agent" not in st.session_state:
    st.session_state["main_agent"] = MainAgent()

user_query = st.text_area("Enter your query:", height=100)
if st.button("Submit"):
    if user_query:
        response = st.session_state["main_agent"].dispatch_query(user_query)
        st.markdown(
            response
        )  # Use st.markdown for better visibility of formatted text and code
    else:
        st.write("Please enter a query.")
