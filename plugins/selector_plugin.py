"""Selector plugin for choosing the next agent."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

SELECTOR_PROMPT = """
Given the chat history, decide who should go next: 'Writer', 'Editor', or 'Illustrator'.
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
