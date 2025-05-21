"""Publisher plugin: lay out title, content and illustration, output A4 PDF."""

import json
from semantic_kernel.functions import KernelPlugin, KernelFunction

def build_publisher_plugin() -> KernelPlugin:
    """Create and configure the publisher plugin.
    
    Returns:
        Configured KernelPlugin for the publisher role
    """

    extract_fn = KernelFunction.from_prompt(
    plugin_name="PublisherPlugin",
    function_name="extract_structured",
    prompt="""
Extract the following fields from the conversation history as JSON: title, content, image_paths.
If a field is missing, set title/content to empty string, image_paths to empty array.
Content is not the history, but the content of the book. Only the text itself, not the conversation between the agents.

Respond ONLY with a JSON object using **double quotes**, like this:
{
  "title": "string",
  "content": "string",
  "image_paths": ["string"]
}

Do NOT include any explanation or markdown formatting. Just return valid raw JSON.

History:
{{$input}}
"""
)

    return KernelPlugin(name="PublisherPlugin", functions=[extract_fn])
