"""Writer plugin for generating story content and titles."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

CONTENT_PROMPT = """
You are a book writer. Write a story based on the provided context.
Context:
{{$history}}
---
Your response:
"""

TITLE_PROMPT = """
You are a creative book-title generator. Output a concise, engaging title (≤ 10 words) that captures the essence of this section.
Context:
{{$history}}
---
Your response should contain ONLY the title, nothing else:
"""

def build_writer_plugin() -> KernelPlugin:
    """Create and configure the writer plugin with content and title functions.
    
    Returns:
        Configured KernelPlugin for the writer role
    """
    content_fn = KernelFunction.from_prompt(
        plugin_name="WriterPlugin",
        function_name="WriteContent",
        prompt=CONTENT_PROMPT
    )
    
    title_fn = KernelFunction.from_prompt(
        plugin_name="WriterPlugin",
        function_name="SuggestTitle", 
        prompt=TITLE_PROMPT
    )
    
    return KernelPlugin(name="WriterPlugin", functions=[content_fn, title_fn])
