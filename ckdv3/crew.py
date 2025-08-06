from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from ckd_v3.tools.custom_tool import DoclingTool
from ckd_v3.tools.custom_tool import Find_Next_Text_Node

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

llm = LLM(
    model="watsonx/meta-llama/llama-3-1-70b-instruct",
    base_url="<your-watsonx-base-url>",
    api_key="<your-watsonx-api-key>"
)


@CrewBase
class CkdV3():
	"""CkdV3 crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def docling_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['docling_agent'],
			verbose=True,
			tools=[DoclingTool()],
			llm=llm,
		)

	@agent
	def JSON_data_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['JSON_data_extractor'],
			verbose=True,
			tools=[Find_Next_Text_Node()],
			llm=llm,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def parse_pdf(self) -> Task:
		return Task(
			config=self.tasks_config['parse_pdf'],
		)

	@task
	def parse_json(self) -> Task:
		return Task(
			config=self.tasks_config['parse_json'],
			context=[self.parse_pdf()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CkdV3 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
