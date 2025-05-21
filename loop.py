"""Main orchestration loop for the story creation process."""

from agents import WriterAgent, EditorAgent, SelectorAgent, IllustratorAgent, PublisherAgent

class RunLoop:
    """Orchestrates the interaction between writer and editor agents."""

    def __init__(
        self,
        writer: WriterAgent,
        editor: EditorAgent,
        selector: SelectorAgent,
        illustrator: IllustratorAgent,
        publisher: PublisherAgent,
        seed: str,
        max_turns: int
    ):
        """Initialize the run loop.
        
        Args:
            writer: Agent that writes story content
            editor: Agent that reviews content
            selector: Agent that chooses next responder
            illustrator: Agent that generates image descriptions
            publisher: Agent that creates PDF layout
            seed: Initial book idea
            max_turns: Maximum number of turns before stopping
        """
        self.writer = writer
        self.editor = editor
        self.selector = selector
        self.illustrator = illustrator
        self.publisher = publisher
        self.seed = seed
        self.max_turns = max_turns
        # Track whether an illustration has already been generated
        self.has_image = False

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
            if agent_name == "Writer":
                agent = self.writer
            elif agent_name == "Editor":
                agent = self.editor
            else:
                agent = self.illustrator
            
            print(f"\n🔁 [{agent_name}] is now responding...\n")

            # Get response
            response = await agent.respond(history)
            output = response.strip()

            history += f"\n[{agent_name}]: {output}"
            print(f"[{agent_name}]: {output}")

            # Update illustration flag if the current response contains an image
            if "![Generated illustration]" in output:
                self.has_image = True

            # Check if editor thinks we're done
            if agent_name == "Editor" and self.editor.is_ready(output):
                if self.has_image:
                    print("\n✅ Editor approved. Creating PDF...")
                    response = await self.publisher.respond(history)
                    print(response)
                    print("\n✅ Book is done!")
                    break
                else:
                    print("\n❌ Editor attempted to approve but no illustration exists yet.")
