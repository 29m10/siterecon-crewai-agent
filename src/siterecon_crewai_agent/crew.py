import os, sys

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from pathlib import Path

file_dir = Path(sys.argv[0]).resolve().parents[2] / "knowledge" / "siterecon-knowledge.pdf"
tool = PDFSearchTool(pdf=str(file_dir))

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SitereconCrewaiAgent():
	"""SitereconCrewaiAgent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def persona_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['persona_extractor'],
			tools=[tool],
			verbose=True
		)

	@agent
	def persona_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['persona_generator'],
			verbose=True
		)
	
	# @agent
	# def persona_validator(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['persona_validator'],
	# 		verbose=True
	# 	)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def persona_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['persona_extraction_task'],
		)

	@task
	def persona_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['persona_generation_task'],
			output_file='siterecon-user-personas.md'
		)
	
	# @task
	# def persona_validation_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['persona_validation_task'],
	# 		output_file='validation.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the SitereconCrewaiAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
