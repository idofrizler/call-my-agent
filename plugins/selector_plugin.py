"""Selector plugin for choosing the next agent."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

SELECTOR_PROMPT = """
Given the chat history, decide who should go next: 'Writer', 'Editor' or 'Publisher'.
* Writer is responsible for writing the story, they should be called after initial user prompt.
They can also be called if prompted by the Editor to either make some edits to the text, or to provide a missing title.
* Editor has three roles: (1) to review the story, deciding if it's ready for publishing, or if it needs some edits. (2) to review the titles, and (3) to request illustrations for the story.
* Publisher is responsible for laying out the book, and generating the PDF. They should be called only after Editor has approved the content, and suggested illustrations to be created.

Only respond with one of those exact words.

Chat history:
{{$history}}
---
Next agent:
"""

def build_selector_plugin() -> KernelPlugin:
    """Create and configure the selector plugin.
    
    Returns:
        Configured KernelPlugin for the selector role
    """
    selector_fn = KernelFunction.from_prompt(
        plugin_name="SelectorPlugin",
        function_name="Selector",
        prompt=SELECTOR_PROMPT
    )
    
    return KernelPlugin(name="SelectorPlugin", functions=[selector_fn])
