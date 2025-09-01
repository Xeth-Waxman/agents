import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../../.env", override=True)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )
    
    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=240,
            max_retry_limit=5,
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            
        )
    
    @agent
    def unit_test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['unit_test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=240,
            max_retry_limit=5,
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
        )
    
    @task
    def backend_coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_coding_task'],
        )
    
    @task
    def frontend_coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_coding_task'],
        )
    
    @task
    def unit_test_coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['unit_test_coding_task'],
        )


    @crew
    # create the engineering team
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
