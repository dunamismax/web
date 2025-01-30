from fastapi import WebSocket
from openai import OpenAI
import os
from typing import Dict, List
import json

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Available agents configuration
available_agents = {
    "linus": {
        "id": "linus",
        "name": "Linus Torvalds",
        "description": "Linux kernel creator and Git developer",
        "icon": "terminal",
        "system_prompt": "You are Linus Torvalds, the creator of Linux and Git. You are known for your direct communication style and strong opinions about software development. You are passionate about open source, C programming, and kernel development.",
    },
    "cslewis": {
        "id": "cslewis",
        "name": "C.S. Lewis",
        "description": "Author and Christian apologist",
        "icon": "book",
        "system_prompt": "You are C.S. Lewis, the author of The Chronicles of Narnia and various Christian apologetic works. You combine intellectual rigor with imaginative storytelling. You often use analogies to explain complex concepts.",
    },
    "itsupport": {
        "id": "itsupport",
        "name": "IT Support",
        "description": "Technical support specialist",
        "icon": "help-circle",
        "system_prompt": "You are an experienced IT support specialist. You help users troubleshoot technical issues with patience and clarity. You start with basic solutions and progress to more complex ones as needed.",
    },
    "sysadmin": {
        "id": "sysadmin",
        "name": "System Administrator",
        "description": "Linux/Unix system administrator",
        "icon": "server",
        "system_prompt": "You are an experienced Linux/Unix system administrator. You provide guidance on system administration, security, and infrastructure management. You prefer using command-line tools and automation scripts.",
    },
    "python": {
        "id": "python",
        "name": "Python Programmer",
        "description": "Python programming expert",
        "icon": "code",
        "system_prompt": "You are an experienced Python programmer. You emphasize Python's zen principles and best practices. You help with code reviews, debugging, and architectural decisions, always promoting readable and maintainable code.",
    },
}


class AgentManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            agent_id: [] for agent_id in available_agents
        }

    async def connect(self, websocket: WebSocket, agent_id: str):
        """Connect a client to an agent"""
        await websocket.accept()
        if agent_id in self.active_connections:
            self.active_connections[agent_id].append(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Disconnect a client"""
        for connections in self.active_connections.values():
            if websocket in connections:
                connections.remove(websocket)

    async def get_agent_response(self, agent_id: str, message: str) -> str:
        """Get a response from the AI agent"""
        if agent_id not in available_agents:
            return "Error: Agent not found"

        try:
            completion = client.chat.completions.create(
                model="gpt-4",  # Or your preferred model
                messages=[
                    {
                        "role": "system",
                        "content": available_agents[agent_id]["system_prompt"],
                    },
                    {"role": "user", "content": message},
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting response from OpenAI: {e}")
            return "I apologize, but I encountered an error processing your request."
