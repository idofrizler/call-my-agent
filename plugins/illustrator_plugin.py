"""Illustrator plugin for generating image descriptions."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

ILLUSTRATOR_PROMPT = """
You are a children-book illustrator using DALL·E 3.
From the story context below, craft a vivid and specific 1-sentence image prompt in English.
Return only the prompt text, nothing else.

Note: Keep the prompt appropriate for a children's book and imagine a scene
that best represents what's happening in the story at this moment.

Context:
{{$history}}
---
Write only your prompt text (one line):
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
