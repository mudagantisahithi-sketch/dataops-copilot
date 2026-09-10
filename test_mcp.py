import asyncio

from agent.agent import toolbox


async def main():
    print("Connecting to MCP Toolbox...")
    tools = await toolbox.get_tools()

    print(f"Found {len(tools)} MCP tools:")
    for tool in tools:
        print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())
