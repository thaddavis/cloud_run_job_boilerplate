import json
import os
import sys
from datetime import datetime  # Add this line
from helpers.format_news_for_email import format_news_for_email
from helpers.is_valid_email import is_valid_email
from helpers.send_email_ses import send_email_ses
from crewai import Agent, Crew, Task, Process
from crewai_tools import ScrapeWebsiteTool
import yaml
from helpers.replace_yaml_variables import replace_yaml_variables
from pydantic_types.NewsResults import NewsResults
import agentops
from dotenv import load_dotenv
load_dotenv()

agentops.init(os.getenv("AGENTOPS_API_KEY"))

# YAML Configuration
current_date = datetime.now().strftime("%Y-%m-%d")  # Add current date
replacements = {
    "current_date": current_date
}
tasks_yaml = None
with open("config/tasks.yaml", 'r') as file:
    tasks_yaml = yaml.safe_load(file)
    tasks_yaml = replace_yaml_variables(tasks_yaml, replacements)
agents_yaml = None
with open("config/agents.yaml", 'r') as file:
    agents_yaml = yaml.safe_load(file)

emails=(os.getenv("COMMA_SEPARATED_EMAILS") or "")

# Retrieve Job-defined env vars # ie: TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0) # ie: TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars # ie: FAIL_RATE = os.getenv("FAIL_RATE", 0)

scrape_web_tool = ScrapeWebsiteTool()

# Define main script
def main():
    print('--- Hierarchical !!! News !!! Crew ---')

    manager = Agent(
        role=agents_yaml["manager"]["role"],
        goal=agents_yaml["manager"]["goal"],
        backstory=agents_yaml["manager"]["backstory"],
        verbose=True,
    )

    workers = []
    
    for worker in agents_yaml["workers"]:
        workers.append(
            Agent(
                role=agents_yaml["workers"][worker]["role"],
                goal=agents_yaml["workers"][worker]["goal"],
                backstory=agents_yaml["workers"][worker]["backstory"],
                verbose=True,
                tools=[scrape_web_tool],
            )
        )

    research_task = Task(
        description=tasks_yaml["research_task"]["description"],
        expected_output=tasks_yaml["research_task"]["expected_output"],
        output_pydantic=NewsResults
    )

    crew = Crew(
        agents=workers,
        manager_agent=manager,
        tasks=[research_task],
        process=Process.hierarchical,
        # verbose=True,
    )

    crew_output = crew.kickoff()

    # print()
    # print('FINAL OUTPUT')
    # print()
    # print(crew_output.raw)
    # print()

    email_list = emails.split(',')
    for email in email_list:
        if bool(email) and is_valid_email(email):
            send_email_ses([email.strip()], format_news_for_email(crew_output.pydantic, current_date))

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        message = (
            f"Attempt failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process