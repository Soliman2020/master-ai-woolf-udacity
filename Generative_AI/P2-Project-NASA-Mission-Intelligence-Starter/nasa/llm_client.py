from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, conversation_history: List[Dict],   
                      model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    SYSTEM_PROMPT = """You are an expert assistant specializing in NASA space missions, particularly Apollo 11, Apollo 13, and the Challenger mission.
You have deep knowledge of space exploration history, mission details, technical specifications, and astronaut experiences.

## GROUNDING REQUIREMENTS
1. You MUST base your answers primarily on the provided context from NASA mission documents.
2. You MUST cite your sources using [Source X] notation (e.g., [Source 1], [Source 2]) when referencing information from the context.
3. If the context does not contain sufficient information to fully answer the question, clearly state: "The provided context does not contain information about [specific topic]."
4. Only supplement with general knowledge when the context is clearly insufficient, and always explicitly note when you are doing so.
5. Never make claims that are not supported by the provided context without clearly indicating uncertainty.

Be concise but thorough. Prioritize accuracy over completeness."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if context:
        context_message = f"Here is relevant context from NASA mission documents:\n\n{context}\n\nAnswer the user's question using ONLY information from this context. Cite sources using [Source X] notation."
        messages.append({"role": "user", "content": context_message})

    if conversation_history:
        for msg in conversation_history:
            messages.append(msg)
            
    # Add current user message to messages
    messages.append({"role": "user", "content": user_message})
    # TODO: Creaet OpenAI Client
    client = OpenAI(
        api_key= openai_key,
        base_url= "https://openai.vocareum.com/v1"
    )
    # TODO: Send request to OpenAI
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    # TODO: Return response
    return response.choices[0].message.content

# print(generate_response(context="NASA Mission Documents part I", conversation_history=[]))
