import asyncio
import os
from dotenv import load_dotenv
import semantic_kernel as sk

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelFunction, KernelArguments

# Load secrets from .env
load_dotenv()

# Get Azure OpenAI config from environment
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model = os.getenv("AZURE_OPENAI_MODEL")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize kernel and chat completion service
kernel = Kernel()
chat_service = AzureChatCompletion(
    deployment_name=deployment,
    endpoint=endpoint,
    api_key=api_key,
    api_version=api_version,
)
kernel.add_service(chat_service)

# Define prompt templates
writer_prompt = """
You are a book writer. Continue the story or write a new section based on the previous context.
Context:
{{$history}}
---
Your response:
"""

editor_prompt = """
You are a book editor. Review the latest book section and give your opinion.
If you think the book is ready to publish, say exactly: "The book is ready."
Context:
{{$history}}
---
Your response:
"""

selector_prompt = """
Given the chat history, decide who should go next: 'Writer' or 'Editor'.
Only respond with 'Writer' or 'Editor'.
Chat history:
{{$history}}
---
Next agent:
"""

# Create kernel functions
writer_fn = KernelFunction.from_prompt(
    plugin_name="WriterPlugin", function_name="Writer", prompt=writer_prompt
)
editor_fn = KernelFunction.from_prompt(
    plugin_name="EditorPlugin", function_name="Editor", prompt=editor_prompt
)
selector_fn = KernelFunction.from_prompt(
    plugin_name="SelectorPlugin", function_name="Selector", prompt=selector_prompt
)

# Create and register plugins
from semantic_kernel.functions import KernelPlugin

writer_plugin = KernelPlugin(name="WriterPlugin", functions=[writer_fn])
editor_plugin = KernelPlugin(name="EditorPlugin", functions=[editor_fn]) 
selector_plugin = KernelPlugin(name="SelectorPlugin", functions=[selector_fn])

kernel.plugins[writer_plugin.name] = writer_plugin
kernel.plugins[editor_plugin.name] = editor_plugin
kernel.plugins[selector_plugin.name] = selector_plugin


# Load seed input (book idea)
def load_seed():
    path = "book_seed.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return input("📘 Enter your book idea:\n> ").strip()


# Agent loop
async def run_loop():
    history = f"[User]: {load_seed()}"
    max_turns = 20

    for turn in range(max_turns):
        # Decide who goes next
        selector_result = await kernel.invoke(selector_fn, KernelArguments(history=history))
        agent = selector_result.value[0].content.strip()

        if agent not in ["Writer", "Editor"]:
            print("⚠️ Invalid selector output. Defaulting to Writer.")
            agent = "Writer"

        chosen_fn = writer_fn if agent == "Writer" else editor_fn
        print(f"\n🔁 [{agent}] is now responding...\n")

        # Get response
        response = await kernel.invoke(chosen_fn, KernelArguments(history=history))
        output = response.value[0].content.strip()

        history += f"\n[{agent}]: {output}"
        print(f"[{agent}]: {output}")

        if "The book is ready" in output:
            print("\n✅ Editor approved. Book is done!")
            break


# Run it
if __name__ == "__main__":
    asyncio.run(run_loop())
