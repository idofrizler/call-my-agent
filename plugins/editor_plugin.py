"""Editor plugin for reviewing story content."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

EDITOR_PROMPT = """
You are a book editor. Review the latest book section and give your opinion.
If you think the book is ready to publish, say exactly: "The book is ready."
Context:
{{$history}}
---
Your response:
"""

def build_editor_plugin() -> KernelPlugin:
    """Create and configure the editor plugin.
    
    Returns:
        Configured KernelPlugin for the editor role
    """
    editor_fn = KernelFunction.from_prompt(
        plugin_name="EditorPlugin",
        function_name="Editor",
        prompt=EDITOR_PROMPT
    )
    
    return KernelPlugin(name="EditorPlugin", functions=[editor_fn])
