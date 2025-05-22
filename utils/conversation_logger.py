"""Utility for persisting agent conversations to disk."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

class ConversationLogger:
    """Logs agent conversations to disk in JSON and Markdown formats."""

    def __init__(self, base_dir: str = "conversations"):
        """Initialize a new conversation logger.
        
        Args:
            base_dir: Base directory for storing conversation logs
        """
        self.base_dir = Path(base_dir)
        self.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_dir = self.base_dir / self.session_id
        self.messages: List[Dict[str, Any]] = []
        
        # Ensure directories exist
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
    def append(self, role: str, content: str) -> None:
        """Append a new message to the conversation log.
        
        Args:
            role: The speaker (e.g. "User", "Writer", "Editor")
            content: The message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        
        # Write JSON after every message for real-time access
        self._write_json()
        
    def finalize(self) -> None:
        """Finalize the conversation by writing both JSON and Markdown versions."""
        self._write_json()
        self._write_markdown()
        
    def _write_json(self) -> None:
        """Write the current message list to log.json."""
        json_path = self.session_dir / "log.json"
        # Write to temp file first for atomic update
        temp_path = json_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "messages": self.messages
            }, f, indent=2)
        temp_path.replace(json_path)  # Atomic replace
        
    def _write_markdown(self) -> None:
        """Write a human-readable Markdown version of the conversation."""
        md_path = self.session_dir / "log.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Conversation {self.session_id}\n\n")
            for msg in self.messages:
                timestamp = datetime.fromisoformat(msg['timestamp'])
                time_str = timestamp.strftime("%H:%M:%S")
                f.write(f"## [{time_str}] {msg['role']}\n\n")
                f.write(f"{msg['content']}\n\n")
