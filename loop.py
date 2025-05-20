"""Main orchestration loop for the story creation process."""

from agents import WriterAgent, EditorAgent, SelectorAgent

class RunLoop:
    """Orchestrates the interaction between writer and editor agents."""

    def __init__(
        self,
        writer: WriterAgent,
        editor: EditorAgent,
        selector: SelectorAgent,
        seed: str,
        max_turns: int
    ):
        """Initialize the run loop.
        
        Args:
            writer: Agent that writes story content
            editor: Agent that reviews content
            selector: Agent that chooses next responder
            seed: Initial book idea
            max_turns: Maximum number of turns before stopping
        """
        self.writer = writer
        self.editor = editor
        self.selector = selector
        self.seed = seed
        self.max_turns = max_turns

    async def run(self) -> None:
        """Execute the story creation loop.
        
        The loop continues until either:
        - The editor indicates the book is ready
        - The maximum number of turns is reached
        """
        history = f"[User]: {self.seed}"

        for turn in range(self.max_turns):
            # Decide who goes next
            agent_name = await self.selector.next(history)
            agent = self.writer if agent_name == "Writer" else self.editor
            
            print(f"\n🔁 [{agent_name}] is now responding...\n")

            # Get response
            response = await agent.respond(history)
            output = response.strip()

            history += f"\n[{agent_name}]: {output}"
            print(f"[{agent_name}]: {output}")

            # Check if editor thinks we're done
            if agent_name == "Editor" and self.editor.is_ready(output):
                print("\n✅ Editor approved. Book is done!")
                break
