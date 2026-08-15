import logging
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from backend.app.config import settings

logger = logging.getLogger(__name__)


def build_checkpointer() -> SqliteSaver:
    """Return a SQLite-backed LangGraph checkpointer so conversation threads survive restarts."""
    db_path = Path(settings.SESSIONS_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return SqliteSaver(conn)


# Global checkpointer instance for thread persistence, shared by the compiled agent graph.
memory_checkpointer = build_checkpointer()


def get_conversation_history(graph_app: Any, thread_id: str) -> List[Dict[str, str]]:
    """
    Retrieve and format the existing conversation history for a given thread_id.
    
    Args:

        graph_app: Compiled LangGraph application instance.
        thread_id: Unique session identifier for the conversation.
        
    Returns:
        List of formatted message dictionaries: [{"role": "user/assistant", "content": "..."}]
    """
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Get state history from LangGraph checkpointer
        state = graph_app.get_state(config)
        
        if not state or "messages" not in state.values:
            return []
        
        formatted_history = []
        for message in state.values["messages"]:
            if isinstance(message, HumanMessage):
                formatted_history.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                formatted_history.append({"role": "assistant", "content": message.content})
                
        return formatted_history

    except Exception as e:
        logger.error("Error retrieving conversation history for thread %s: %s", thread_id, e)
        return []


def clear_conversation_history(thread_id: str) -> bool:
    """
    Reset or wipe state checkpointer memory for a specific thread_id.
    
    Args:
        thread_id: Unique session identifier to clear.
    """
    try:
        config = {"configurable": {"thread_id": thread_id}}
        # Overwrite state with empty messages list
        memory_checkpointer.put(config, checkpoint={"channel_values": {"messages": []}}, metadata={})
        logger.info("Successfully cleared conversation memory for thread: %s", thread_id)
        return True
    except Exception as e:
        logger.error("Failed to clear conversation history for thread %s: %s", thread_id, e)
        return False