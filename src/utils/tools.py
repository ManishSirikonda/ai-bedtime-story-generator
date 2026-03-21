import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core._api import LangChainDeprecationWarning

# Suppress the LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

load_dotenv()

# Global instances of the models and tools
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
tavily_tool = TavilySearchResults(max_results=3)
