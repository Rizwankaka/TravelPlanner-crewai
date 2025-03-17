from crewai import Agent
from TravelTools import SearchTools
from langchain_openai import ChatOpenAI
import os

class TravelAgents:
    def __init__(self, model_name="gpt-4o-mini"):
        self.model_name = model_name
        self.search_tools = SearchTools()
        
        # Configure OpenAI LLM
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=model_name
        )
    
    def create_research_agent(self):
        """Creates a research agent focused on gathering travel data."""
        return Agent(
            role="Travel Data Researcher",
            goal="Gather comprehensive and up-to-date information about travel destinations",
            backstory="""You are an expert travel researcher with extensive knowledge of
            global destinations. You excel at finding detailed information about
            attractions, accommodations, local customs, and travel requirements.""",
            tools=[self.search_tools.duckduckgo_search],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def create_planning_agent(self):
        """Creates a planning agent focused on creating itineraries."""
        return Agent(
            role="Travel Itinerary Planner",
            goal="Create detailed, personalized travel itineraries based on research",
            backstory="""You are a highly organized travel planner who specializes in
            creating optimal itineraries. You have a talent for balancing sightseeing,
            relaxation, and local experiences while considering budget and time constraints.""",
            tools=[self.search_tools.duckduckgo_search],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def create_local_expert_agent(self):
        """Creates a local expert agent with deep knowledge of local attractions."""
        return Agent(
            role="Local Travel Guide Expert",
            goal="Provide authentic local insights and recommendations for destinations",
            backstory="""You are a worldly travel guide with deep knowledge of local
            cultures, hidden gems, and authentic experiences. You know how to help
            travelers experience destinations like a local rather than a tourist.""",
            tools=[self.search_tools.duckduckgo_search],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def create_budget_optimization_agent(self):
        """Creates an agent focused on optimizing travel costs."""
        return Agent(
            role="Travel Budget Optimizer",
            goal="Find the best deals and optimize travel expenses",
            backstory="""You are a savvy budget travel expert who knows how to
            maximize value while minimizing costs. You excel at finding deals on
            flights, accommodations, and activities without sacrificing quality.""",
            tools=[self.search_tools.duckduckgo_search],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )