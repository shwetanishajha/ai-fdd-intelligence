from src.agents.registry import get_agent


def execute_plan(selected_agents: list[str]) -> list[dict]:
    # Validate the complete plan before executing any agent
    agents = [get_agent(agent_name) for agent_name in selected_agents]

    results = []

    for agent in agents:
        results.append(agent())

    return results