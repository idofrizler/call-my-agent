"""Editor plugin for reviewing story content and ensuring titles exist."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

EDITOR_PROMPT = """
You are a book editor. Review the latest book section and give your opinion.
Before approving, verify that:
1. Each chapter/section has a title
2. The overall book has a title
3. The content is complete and polished

If ANY title is missing, mention it specifically and request it.
If all titles exist and content is ready, say exactly: "The book is ready."

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
