"""Writer plugin for generating story content."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

WRITER_PROMPT = """
You are a book writer. Continue the story or write a new section based on the previous context.
Context:
{{$history}}
---
Your response:
"""

def build_writer_plugin() -> KernelPlugin:
    """Create and configure the writer plugin.
    
    Returns:
        Configured KernelPlugin for the writer role
    """
    writer_fn = KernelFunction.from_prompt(
        plugin_name="WriterPlugin",
        function_name="Writer",
        prompt=WRITER_PROMPT
    )
    
    return KernelPlugin(name="WriterPlugin", functions=[writer_fn])
