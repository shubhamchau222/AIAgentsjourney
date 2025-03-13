import asyncio
from pathlib import Path
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

env_path = r"D:\common_credentials\.env"
load_dotenv(dotenv_path=env_path)

async def create_filesystem_agent(session):
    """Create and configure a filesystem agent with MCP tools."""
    # Initialize the MCP toolkit
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()

    # Create an agent with the MCP toolkit
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[mcp_tools],
        instructions=dedent("""\
            You are a filesystem assistant. Help users explore files and directories.

            - Navigate the filesystem to answer questions
            - Use the list_allowed_directories tool to find directories that you can access
            - Provide clear context about files you examine
            - Use headings to organize your responses
            - Be concise and focus on relevant information\
        """),
        markdown=True,
        show_tool_calls=True,
    )


async def run_agent(message: str) -> None:
    """Run the filesystem agent with the given message."""
    # Initialize the MCP server
    server_params = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(Path(__file__).parent.parent.parent.parent),
        ],
    )

    # Create a client session to connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            agent = await create_filesystem_agent(session)

            # Run the agent
            await agent.aprint_response(message, stream=True)


# Example usage
if __name__ == "__main__":
    # Basic example - exploring project license
    asyncio.run(run_agent("What is the license for this project?"))