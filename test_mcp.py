import asyncio

from agent.agent import toolbox


async def main():
    print("Connecting to MCP Toolbox...")
    
    tools = await toolbox.get_tools()

    print()
    print("DISCOVERED TOOLS")
    print("================")

    for tool in tools:
        print("-", tool.name)


asyncio.run(main())
