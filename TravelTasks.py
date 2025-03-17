from crewai import Task
from typing import List
from TravelAgents import TravelAgents

class TravelTasks:
    def __init__(self, agents: TravelAgents):
        self.agents = agents
    
    def destination_research_task(self, destination: str, starting_point: str, interests: List[str], duration: int, travel_date_info: str = "") -> Task:
        """
        Create a task for researching a travel destination.
        
        Args:
            destination: The destination to research.
            starting_point: The starting point of the journey.
            interests: List of traveler interests.
            duration: Trip duration in days.
            travel_date_info: Information about travel dates.
            
        Returns:
            A Task for destination research.
        """
        return Task(
            description=f"""Research comprehensive information about {destination} as a travel destination.
            Starting point: {starting_point}
            {travel_date_info}

            Focus on the following areas:
            - Main attractions and points of interest
            - Local customs and cultural norms
            - Typical weather conditions during the travel dates
            - Transportation options within the destination
            - Transportation from {starting_point} to {destination}
            - Safety considerations
            - Language considerations
            - Visa and entry requirements
            
            The traveler is interested in: {', '.join(interests)}
            Trip duration: {duration} days
            
            Provide a detailed report with all relevant information organized by category.
            """,
            agent=self.agents.create_research_agent(),
            expected_output="A comprehensive report on the destination with all relevant travel information",
            output_file="destination_research_report.txt"  # Optional: Save output to a file
        )
    
    def itinerary_creation_task(self, destination: str, starting_point: str, interests: List[str], duration: int, 
                                budget_level: str, travel_style: str, travel_date_info: str, research_report: str) -> Task:
        """
        Create a task for developing a travel itinerary.
        
        Args:
            destination: The destination for the itinerary.
            starting_point: The starting point of the journey.
            interests: List of traveler interests.
            duration: Trip duration in days.
            budget_level: Budget level (e.g., "budget", "moderate", "luxury").
            travel_style: Travel style preference (e.g., "relaxed", "packed").
            travel_date_info: Information about travel dates.
            research_report: The research report from the previous task.
            
        Returns:
            A Task for itinerary creation.
        """
        return Task(
            description=f"""Create a detailed day-by-day itinerary for a {duration}-day trip to {destination}.
            
            Starting from: {starting_point}
            {travel_date_info}
            Traveler interests: {', '.join(interests)}
            Budget level: {budget_level}
            Travel style: {travel_style}
            
            Use the following research as a basis for your itinerary:
            {research_report}
            
            For each day, include:
            - Morning activities
            - Afternoon activities
            - Evening activities
            - Recommended dining options
            - Estimated costs for activities and meals
            - Transportation between locations
            
            Begin with travel details from {starting_point} to {destination}.
            Ensure the itinerary is realistic in terms of travel times and distances.
            Balance the itinerary according to the traveler's preferred style.
            Include the return journey to {starting_point} at the end of the trip.
            """,
            agent=self.agents.create_planning_agent(),
            expected_output="A detailed day-by-day itinerary for the entire trip",
            output_file="detailed_itinerary.txt"  # Optional: Save output to a file
        )
    
    def local_recommendations_task(self, destination: str, interests: List[str], research_report: str) -> Task:
        """
        Create a task for gathering local recommendations.
        
        Args:
            destination: The destination for recommendations.
            interests: List of traveler interests.
            research_report: The research report from the previous task.
            
        Returns:
            A Task for local recommendations.
        """
        return Task(
            description=f"""Provide authentic local recommendations for {destination} based on 
            the traveler's interests: {', '.join(interests)}.
            
            Use the following research as additional context:
            {research_report}
            
            Include recommendations for:
            - Hidden gems and off-the-beaten-path attractions
            - Local restaurants and street food
            - Cultural experiences and interactions with locals
            - Local markets and shopping opportunities
            - Authentic local experiences
            - Ways to avoid tourist traps
            
            Explain why each recommendation is special and how it provides an authentic experience.
            """,
            agent=self.agents.create_local_expert_agent(),
            expected_output="A curated list of authentic local recommendations",
            output_file="local_recommendations.txt"  # Optional: Save output to a file
        )
    
    def budget_optimization_task(self, destination: str, duration: int, budget_level: str, 
                                itinerary: str) -> Task:
        """
        Create a task for optimizing the travel budget.
        
        Args:
            destination: The destination for budget optimization.
            duration: Trip duration in days.
            budget_level: Budget level (e.g., "budget", "moderate", "luxury").
            itinerary: The itinerary from the previous task.
            
        Returns:
            A Task for budget optimization.
        """
        return Task(
            description=f"""Optimize the travel budget for a {duration}-day trip to {destination}
            with a {budget_level} budget level.
            
            Use the following itinerary as a reference:
            {itinerary}
            
            Provide specific recommendations for:
            - Accommodation options at different price points
            - Transportation cost-saving strategies
            - Meal planning to save money
            - Free or low-cost attractions and activities
            - Local discount cards or passes
            - Best times to visit paid attractions for discounts
            - Money-saving tips specific to the destination
            
            Create a detailed budget breakdown by category (accommodation, food, transportation, activities, etc.)
            and provide a total estimated cost for the trip.
            """,
            agent=self.agents.create_budget_optimization_agent(),
            expected_output="A detailed budget optimization plan with specific recommendations and cost estimates",
            output_file="budget_optimization_plan.txt"  # Optional: Save output to a file
        )