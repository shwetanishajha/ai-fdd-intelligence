from src.agents.registry import get_agent


def execute_plan(selected_agents: list[str]) -> list[dict]:
    results = []

    for agent_name in selected_agents:
        agent = get_agent(agent_name)
        result = agent()
        results.append(result)

    return results