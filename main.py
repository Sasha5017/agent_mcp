import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3:1.7b")

async def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    async with MultiServerMCPClient({
        "search": {
            "command": "python",
            "args": ["./mcp_server/search_sever_duckduck_go.py"],
            "transport": "stdio",
            "env": {"PYTHONPATH": project_root}
        },
        "files": {
            "command": "python",
            "args": ["./mcp_server/server_2.py"],
            "transport": "stdio",
            "env": {"PYTHONPATH": project_root}
        }
    }) as client:
        search_session = client.sessions["search"]
        files_session = client.sessions["files"]

        search_tools = await load_mcp_tools(search_session)
        files_tools = await load_mcp_tools(files_session)

        agent = create_react_agent(model, search_tools + files_tools)

        print("Интерактивный чат запущен. Напишите 'exit' для выхода.\n")

        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Выход из чата.")
                break

            try:
                res = await agent.ainvoke({"messages": user_input})
                for m in res['messages']:
                    print("Агент:", m.content)
            except Exception as e:
                print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
