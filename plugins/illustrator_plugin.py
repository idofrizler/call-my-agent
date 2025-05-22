"""Illustrator plugin for generating image descriptions."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

ILLUSTRATOR_PROMPT = """
You are a children-book illustrator using DALL·E 3.
Below is a scene description to illustrate. If needed, enhance it to be more specific and vivid,
while keeping true to the original intent. Keep it appropriate for a children's book.

Scene:
{{$input}}
---
Write only your enhanced prompt text (one line):
"""

def build_illustrator_plugin() -> KernelPlugin:
    """Create and configure the illustrator plugin.
    
    Returns:
        Configured KernelPlugin for the illustrator role
    """
    illustrator_fn = KernelFunction.from_prompt(
        plugin_name="IllustratorPlugin",
        function_name="Illustrator",
        prompt=ILLUSTRATOR_PROMPT
    )
    
    return KernelPlugin(name="IllustratorPlugin", functions=[illustrator_fn])
