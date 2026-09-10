import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import (
    McpToolset,
    StreamableHTTPConnectionParams,
)

from agent.prompts import SYSTEM_PROMPT


TOOLBOX_URL = os.getenv(
    "TOOLBOX_URL",
    "http://127.0.0.1:5000/mcp",
)


toolbox = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=TOOLBOX_URL,
    ),
)


root_agent = Agent(
    name="dataops_copilot",
    model="gemini-3.5-flash-lite",
    description=(
        "A DataOps incident investigation agent that "
        "uses MCP Toolbox and BigQuery to investigate "
        "and remediate customer data quality incidents."
    ),
    instruction=SYSTEM_PROMPT,
    tools=[toolbox],
)


if __name__ == "__main__":
    print("=" * 70)
    print("DATAOPS COPILOT - ADK + MCP TOOLBOX")
    print("=" * 70)
    print()
    print("Agent:", root_agent.name)
    print("Model:", root_agent.model)
    print("Toolbox:", TOOLBOX_URL)
    print("Toolsets:", len(root_agent.tools))
    print()
    print("Agent configuration loaded successfully.")
