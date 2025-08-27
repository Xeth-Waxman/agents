from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool

class TrendingCompanies(BaseModel):
    """ A company that is in the news and trending"""
    name: str = Field(..., description="The name of the company")
    ticker: str = Field(..., description="The stock ticker of the company")
    reason: str = Field(..., description="The reason the company is trending")

class TrendingCompaniesList(BaseModel):
    """ A list of trending companies that are in the news"""
    trending_companies: List[TrendingCompanies] = Field(..., description="The list of trending companies")

class InvestmentProspectus(BaseModel):
    """ A detailed investment prospectus for a company"""
    name: str = Field(..., description="The name of the company")
    ticker: str = Field(..., description="The stock ticker of the company")
    reason: str = Field(..., description="The reason the company is or is not a good investment")
    summary: str = Field(..., description="A summary of the company")
    market_position: str = Field(..., description="The market position of the company and relative competition")
    future_outlook: str = Field(..., description="The future outlook for the company")
    full_report: str = Field(..., description="A full report of the company")

class InvestmentProspectusList(BaseModel):
    """ A list of investment prospectuses for a list of companies"""
    investment_prospectuses: List[InvestmentProspectus] = Field(..., description="The list of investment prospectuses")

class BestInvestment(BaseModel):
    """ The best investment from a list of investment prospectuses"""
    name: str = Field(..., description="The name of the company")
    ticker: str = Field(..., description="The stock ticker of the company")
    reason: str = Field(..., description="The reason the company is the best investment")
    summary: str = Field(..., description="A summary of the company")
    investment_forecast: str = Field(..., description="The anticipated annual return on investment for the company over a five-year period.")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    serper_tool = SerperDevTool()

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[self.serper_tool] )
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[self.serper_tool])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'])
    
    @agent
    def manager(self) -> Agent:
        return Agent(config=self.agents_config['manager'])
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'], output_pydantic=TrendingCompaniesList)

    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'], output_pydantic=InvestmentProspectusList)

    @task
    def pick_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'], expected_output=BestInvestment)

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(config=self.agents_config['manager'], allow_delegation=True)

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager
        )

if __name__ == "__main__":
    crew = StockPicker().crew()
    crew.kickoff()
