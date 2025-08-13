import os
import asyncio
import google.generativeai as genai
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import CreateResult, AssistantMessage, RequestUsage, UserMessage

class GeminiClient:
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
        self.model_info = {"vision": False}
        genai.configure(api_key=self.api_key)

    async def create(self, messages, **kwargs):
        # Extract the prompt from the last message.
        prompt = messages[-1].content

        model = genai.GenerativeModel(self.model)
        response = await model.generate_content_async(prompt)

        response_text = response.text

        # Extract token usage
        prompt_tokens = response.usage_metadata.prompt_token_count
        completion_tokens = response.usage_metadata.candidates_token_count

        return CreateResult(
            finish_reason="stop",
            content=response_text,
            usage=RequestUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
            cached=False,
            messages=[AssistantMessage(content=response_text, source="assistant")]
        )

    async def cost(self, response):
        return 0

async def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    model_client = GeminiClient(model="gemini-1.5-flash-latest", api_key=gemini_api_key)

    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
    )

    result = await assistant.run(task="Explain how AI works in a few words.")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
