import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env", override=True)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class XDebate():
    """XDebate crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def debater(self) -> Agent:
        return Agent(config=self.agents_config['debater'], verbose=True)

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config['judge'], verbose=True)

    @task
    def propose_motion(self) -> Task:
        return Task(config=self.tasks_config['propose_motion'])

    @task
    def oppose_motion(self) -> Task:
        return Task(config=self.tasks_config['oppose_motion'])
    
    @task
    def decide_winner(self) -> Task:
        return Task(config=self.tasks_config['decide_winner'])

    @crew
    def crew(self) -> Crew:
        """Creates the XDebate crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
