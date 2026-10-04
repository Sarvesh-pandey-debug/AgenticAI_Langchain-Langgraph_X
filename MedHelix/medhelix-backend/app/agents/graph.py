from langgraph.graph import StateGraph, START, END
from app.agents.state import CodingState
from app.agents.ccea_agent import ccea_node
from app.agents.ica_agent import ica_node
from app.agents.cqaa_agent import cqaa_node
from app.agents.crla_agent import crla_node

# Initialize the state graph
workflow = StateGraph(CodingState)

# Add nodes
workflow.add_node("ccea", ccea_node)
workflow.add_node("ica", ica_node)
workflow.add_node("cqaa", cqaa_node)
workflow.add_node("crla", crla_node)

# Define the edges
workflow.add_edge(START, "ccea")
workflow.add_edge("ccea", "ica")
workflow.add_edge("ica", "cqaa")
workflow.add_edge("cqaa", "crla")
workflow.add_edge("crla", END)

# Compile the graph
coding_graph = workflow.compile()
