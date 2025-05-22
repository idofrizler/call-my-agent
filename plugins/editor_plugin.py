"""Editor plugin for reviewing story content and ensuring titles exist."""

from semantic_kernel.functions import KernelFunction, KernelPlugin

EDITOR_PROMPT = """
You are a book editor. Review the latest book section and give your opinion on two aspects:

1. TEXT QUALITY
Review the content and verify:
- Each chapter/section has a title
- The overall book has a title
- The content is complete and polished

If ANY title is missing, mention it specifically and request it.
If all titles exist and content is ready, say exactly: "The book is ready."

2. ILLUSTRATION NEEDS
List 2-3 scenes/moments that need illustrations, prefixed with "IMG:" (no leading characters, start with IMG:). For example:
IMG: A young boy playing with his dog in a sunny park
IMG: The magical forest at night with glowing fireflies

Each IMG: line should be a clear, specific scene description that can be turned into an illustration.
Only request illustrations for key story moments. Not every page needs an image.

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
        description="Reviews the book content and titles, ensuring quality and completeness.",
        prompt=EDITOR_PROMPT
    )
    
    return KernelPlugin(name="EditorPlugin", functions=[editor_fn])
