from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
import os

# --- Custom Tool Definition ---
class SearchTools:
    @tool("Search the internet")
    def search_internet(query: str):
        """Useful to search the internet about a a given topic and return relevant news."""
        # MOCK IMPLEMENTATION TO FIX CRASH
        # Once we have an API Key (Perplexity/Serper), we replace this logic.
        return f"""
        [SIMULATED SEARCH RESULT for: {query}]
        Title: High Turnover Costs Companies Billions
        Source: Business Insider (Simulated)
        Summary: A new report shows that replacing an employee costs 2x their annual salary. Companies are investing more in retention.
        Link: https://www.businessinsider.com/turnover-costs-2024
        """

class SalesCrew:
    def __init__(self, client_name, pain_points, meeting_date, company_name):
        self.client_name = client_name
        self.pain_points = pain_points
        self.meeting_date = meeting_date
        self.company_name = company_name

    def run(self):
        # 1. Tools
        search_tool = SearchTools.search_internet

        # 2. Agents
        researcher = Agent(
            role='Market Trends Analyst',
            goal=f'Find 1 recent and impactful news article related to: {self.pain_points}',
            backstory="""You are an expert market analyst. You do not care about gossip or superficial news. 
            You look for hard data, economic trends, and business news that validate a specific business problem.
            Your job is to find ammunition for the sales team to show the client that their problem is real and urgent.""",
            verbose=True,
            allow_delegation=False,
            tools=[search_tool]
        )

        writer = Agent(
            role='Senior SDR & Copywriter',
            goal='Draft a short, personalized WhatsApp message connecting the news to the client.',
            backstory="""You are a top-performing SDR. You write like a human, not a robot. 
            You use short sentences. You never use hashtags. You rarely use emojis (maybe 1 max).
            You are helpful and consultative. You want to nurture the lead for the upcoming meeting.""",
            verbose=True,
            allow_delegation=False
        )

        # 3. Tasks
        task_search = Task(
            description=f"""
            Search for recent news (last 30 days preferably) regarding '{self.pain_points}' in the business world (Brazil context if applicable).
            If the pain point is specific (e.g. 'Turnover'), find stats or news about why this is damaging companies.
            
            OUTPUT REQUIRED: A short summary of the news and the URL.
            """,
            agent=researcher,
            expected_output="A summary of a relevant news article and its URL."
        )

        task_draft = Task(
            description=f"""
            Write a WhatsApp message for the lead named '{self.client_name}'.
            
            Context:
            - They have a meeting scheduled for: {self.meeting_date}
            - Their main pain point is: {self.pain_points}
            - We found this news: [Use the result from the researcher]
            
            Instructions:
            1. Start with a casual greeting ("Oi {self.client_name}").
            2. Mention you saw this news and it reminded you of their challenge ({self.pain_points}).
            3. Paste the Link.
            4. End by reinforcing that this will be a key topic for the meeting on {self.meeting_date}.
            
            CRITICAL: The output must be JUST the message text, ready to copy-paste. No quotes, no intro text like "Here is the message:".
            Language: Portuguese (Brazil).
            """,
            agent=writer,
            expected_output="The final WhatsApp message text in Portuguese."
        )

        # 4. Crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task_search, task_draft],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
