from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.tools import RunContext


def keep_last_n_messages(
    ctx: RunContext[None], messages: list[ModelMessage]
) -> list[ModelMessage]:
    # Access current usage
    current_tokens = ctx.usage.total_tokens

    # Filter messages based on context
    if current_tokens > 1e6:
        return messages[-3:]  # Keep only recent messages when token usage is high
    return messages


async def summarize_old_messages(
    ctx: RunContext[None], messages: list[ModelMessage]
) -> list[ModelMessage]:
    current_tokens = ctx.usage.total_tokens

    if current_tokens > 1e6:
        summarize_agent = Agent(
            "openai:gpt-4.1-nano-2025-04-14",
            instructions="""
                Summarize this conversation, omitting small talk and unrelated topics.
                Focus on the technical discussion and next steps.
                """,
        )

        summary = await summarize_agent.run(message_history=messages)
        # Return the last message and the summary
        return summary.new_messages() + messages[-1:]

    return messages
