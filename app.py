import streamlit as st
import os
from crewai import Crew
from dotenv import load_dotenv
from TravelAgents import TravelAgents
from TravelTasks import TravelTasks
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

st.title("🌍 AI Travel Planner")
st.subheader("Plan your perfect trip with AI assistance")

# Sidebar for user inputs
with st.sidebar:
    st.header("OpenAI API Key")
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    
    # Check if API key is set
    if not openai_api_key and not os.getenv("OPENAI_API_KEY"):
        st.error("Please enter your OpenAI API key.")
    
    st.header("Trip Details")
    starting_point = st.text_input("Starting Point", placeholder="e.g., New York, USA")
    destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
    
    # Travel dates
    st.subheader("Travel Dates")
    today = datetime.now()
    start_date = st.date_input("Start Date", today + timedelta(days=30))
    end_date = st.date_input("End Date", today + timedelta(days=37))
    
    # Calculate duration from dates
    if start_date and end_date:
        duration = (end_date - start_date).days
        if duration < 1:
            st.error("End date must be after start date.")
            st.stop()
    else:
        duration = 7
    
    st.subheader("Trip Preferences")
    interests = st.multiselect(
        "Your Interests",
        options=["History", "Art", "Food", "Nature", "Adventure", "Culture", "Shopping", "Relaxation", "Nightlife", "Photography"],
        default=["Food", "Culture"]
    )
    
    budget_level = st.selectbox(
        "Budget Level",
        options=["Budget", "Moderate", "Luxury"],
        index=1
    )
    
    travel_style = st.selectbox(
        "Travel Style",
        options=["Relaxed", "Moderate", "Packed"],
        index=1
    )
    
    model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    model_name = st.selectbox(
        "AI Model",
        options=model_options,
        index=0
    )
    
    submit_button = st.button("Generate Travel Plan")

# Main content area
if not submit_button:
    st.info("Fill in your trip details and click 'Generate Travel Plan' to get started.")
    
    # Display example output
    with st.expander("See an example travel plan"):
        st.write("""
        # Tokyo, Japan - 7 Day Itinerary
        
        ## Trip Details:
        - **Starting Point**: New York, USA
        - **Destination**: Tokyo, Japan
        - **Travel Dates**: June 1-7, 2023
        
        ## Day 1: Arrival and Tokyo Essentials
        - **Morning**: Arrive at Narita Airport, transfer to hotel in Shinjuku
        - **Afternoon**: Visit Meiji Shrine and Harajuku
        - **Evening**: Welcome dinner at Omoide Yokocho (Memory Lane)
        
        ## Day 2: Historic Tokyo
        - **Morning**: Visit Senso-ji Temple in Asakusa
        - **Afternoon**: Explore Tokyo National Museum
        - **Evening**: Dinner cruise on the Sumida River
        
        *And so on...*
        """)
else:
    if not os.getenv("OPENAI_API_KEY") and not openai_api_key:
        st.error("Please enter your OpenAI API key.")
        st.stop()
        
    if not destination or not interests or not starting_point:
        st.error("Please fill in all required fields (Starting Point, Destination, and Interests).")
        st.stop()
    
    # Display progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create agents, tasks and crew
    try:
        status_text.text("Initializing AI agents...")
        progress_bar.progress(10)
        
        agents = TravelAgents(model_name=model_name)
        tasks = TravelTasks(agents)
        
        status_text.text("Researching destination...")
        progress_bar.progress(20)
        
        # Format travel dates for task description
        travel_date_info = f"Travel dates: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')} ({duration} days)"
        
        # Create research task
        research_task = tasks.destination_research_task(
            destination=destination,
            starting_point=starting_point,
            interests=interests,
            duration=duration,
            travel_date_info=travel_date_info
        )
        
        # Execute research task
        travel_crew = Crew(
            agents=[agents.create_research_agent()],
            tasks=[research_task],
            verbose=True
        )
        try:
            crew_output = travel_crew.kickoff()
            research_results = str(crew_output) if not isinstance(crew_output, str) else crew_output
        except Exception as e:
            st.error(f"Error in research task: {str(e)}")
            research_results = "Error occurred during research. Please try again."
        
        status_text.text("Creating itinerary...")
        progress_bar.progress(50)
        
        # Create itinerary task
        itinerary_task = tasks.itinerary_creation_task(
            destination=destination,
            starting_point=starting_point,
            interests=interests,
            duration=duration,
            budget_level=budget_level,
            travel_style=travel_style,
            travel_date_info=travel_date_info,
            research_report=research_results
        )
        
        # Execute itinerary task
        travel_crew = Crew(
            agents=[agents.create_planning_agent()],
            tasks=[itinerary_task],
            verbose=True
        )
        try:
            crew_output = travel_crew.kickoff()
            itinerary_results = str(crew_output) if not isinstance(crew_output, str) else crew_output
        except Exception as e:
            st.error(f"Error in itinerary task: {str(e)}")
            itinerary_results = "Error occurred during itinerary creation. Please try again."
        
        status_text.text("Finding local recommendations...")
        progress_bar.progress(70)
        
        # Create local recommendations task
        local_recommendations_task = tasks.local_recommendations_task(
            destination=destination,
            interests=interests,
            research_report=research_results
        )
        
        # Execute local recommendations task
        travel_crew = Crew(
            agents=[agents.create_local_expert_agent()],
            tasks=[local_recommendations_task],
            verbose=True
        )
        try:
            crew_output = travel_crew.kickoff()
            recommendations_results = str(crew_output) if not isinstance(crew_output, str) else crew_output
        except Exception as e:
            st.error(f"Error in recommendations task: {str(e)}")
            recommendations_results = "Error occurred during recommendations. Please try again."
        
        status_text.text("Optimizing budget...")
        progress_bar.progress(90)
        
        # Create budget optimization task
        budget_task = tasks.budget_optimization_task(
            destination=destination,
            duration=duration,
            budget_level=budget_level,
            itinerary=itinerary_results
        )
        
        # Execute budget optimization task
        travel_crew = Crew(
            agents=[agents.create_budget_optimization_agent()],
            tasks=[budget_task],
            verbose=True
        )
        try:
            crew_output = travel_crew.kickoff()
            budget_results = str(crew_output) if not isinstance(crew_output, str) else crew_output
        except Exception as e:
            st.error(f"Error in budget task: {str(e)}")
            budget_results = "Error occurred during budget optimization. Please try again."
        
        status_text.text("Finalizing your travel plan...")
        progress_bar.progress(100)
        
        # Display results
        st.success("Your travel plan is ready!")
        
        # Display trip summary at the top
        st.markdown(f"""
        ## Trip Summary:
        - **Starting Point**: {starting_point}
        - **Destination**: {destination}
        - **Travel Dates**: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')} ({duration} days)
        - **Budget Level**: {budget_level}
        - **Travel Style**: {travel_style}
        """)
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["Destination Overview", "Itinerary", "Local Recommendations", "Budget"])
        
        with tab1:
            st.header(f"Destination Overview: {destination}")
            st.write(research_results)
        
        with tab2:
            st.header(f"Your {duration}-Day Itinerary")
            st.write(itinerary_results)
        
        with tab3:
            st.header("Local Recommendations")
            st.write(recommendations_results)
        
        with tab4:
            st.header("Budget Optimization")
            st.write(budget_results)
        
        # Add download buttons for each section
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.download_button(
                label="Download Overview",
                data=research_results,
                file_name="destination_overview.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="Download Itinerary",
                data=itinerary_results,
                file_name="travel_itinerary.txt",
                mime="text/plain"
            )
        
        with col3:
            st.download_button(
                label="Download Recommendations",
                data=recommendations_results,
                file_name="local_recommendations.txt",
                mime="text/plain"
            )
        
        with col4:
            st.download_button(
                label="Download Budget Plan",
                data=budget_results,
                file_name="budget_plan.txt",
                mime="text/plain"
            )
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

if __name__ == "__main__":
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **About**
        
        This AI Travel Planner uses CrewAI framework to generate comprehensive travel plans.
        
        It leverages multiple AI agents with different specializations to create a complete
        travel experience tailored to your preferences.
        """
    )