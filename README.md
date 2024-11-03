AI-Powered Multi-Agent Query Processor

A multi-agent system built with Python, LangChain, and the OpenAI API to efficiently handle a range of user queries, from problem-solving to code debugging. Each agent specializes in a unique task, providing focused, context-aware responses, all accessible through an interactive Streamlit interface.

Features

Multi-Agent Design: Multiple agents handle different query types, including problem-solving, topic exploration, code debugging, and web search.
Specialized Query Handling: Each agent is tailored for a specific purpose, utilizing OpenAI's GPT-3.5-turbo to generate high-quality, contextual responses.
User-Friendly Interface: A clean Streamlit interface lets users interact seamlessly with each agent.
Modular and Extensible: The system is designed to easily support additional agents and tools, enhancing its functionality over time.

Technology Stack

LangChain: Manages the creation and orchestration of specialized agents.
OpenAI API: Powers the agents with GPT-3.5-turbo for natural language understanding and response generation.
Streamlit: Provides a user-friendly web interface for interacting with the multi-agent system.
DuckDuckGo API (via LangChain tools): Adds real-time web search capabilities for information retrieval.

Installation

Clone the repository
git clone (https://github.com/Nikhilesh-915/AI-Powered-Multi-Agent-Query-Processor.git)
Navigate to the project directory
cd multi-agent-query-system
Install dependencies
pip install -r requirements.txt
Set up your API keys
Add your OpenAI API key and any other required keys (e.g., for DuckDuckGo search) to your environment variables.

Usage

To start the application, run:

streamlit run main.py

Query Types Supported

Problem Solver: Solves complex questions, provides solutions with explanations, and offers code where needed.
Topic Explorer: Delivers in-depth explanations of technical topics and suggests related areas of interest.
Code Debugger: Analyzes code for errors, suggests corrections, and provides best practices.
Web Search: Retrieves relevant information from the web using DuckDuckGo.

Project Structure

main.py: Initializes the Streamlit application and connects user inputs to the agents.
agents/: Contains agent-specific code and configurations for handling distinct query types.
utils/: Utility functions for managing API calls, caching, and other background processes.
requirements.txt: Lists all required packages for easy setup.

How It Works

The system uses LangChain to organize specialized agents as tools.
The Main Agent acts as a dispatcher, routing queries to the appropriate specialized agent.
Problem Solver, Topic Explorer, Code Debugger: Each agent is configured to respond to a specific type of query by leveraging the OpenAI API.
Web Search Tool: Uses DuckDuckGo for external information retrieval when needed.

Future Enhancements

Additional Agents: Plan to add more agents for data analysis, NLP processing, or user-defined tasks.
Direct Agent Communication: Enable agents to share insights or collaboratively solve complex queries.
Enhanced User Metrics: Track agent performance and accuracy to continuously improve responses.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

OpenAI for providing advanced language models.
LangChain for enabling the creation of multi-agent workflows.
Streamlit for simplifying the development of interactive web applications.

This AI-Powered Multi-Agent Query Processor is designed to make complex query processing easier and more accessible. Feel free to fork, experiment, and contribute!

