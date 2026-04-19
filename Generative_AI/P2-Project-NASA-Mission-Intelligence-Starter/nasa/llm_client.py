from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, conversation_history: List[Dict],   
                      model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    SYSTEM_PROMPT = """You are an expert assistant specializing in NASA space missions, particularly Apollo 11, Apollo 13, and the Challenger mission.
    You have deep knowledge of space exploration history, mission details, technical specifications, and astronaut experiences.
    Provide accurate, informative responses based on the context provided. If the context doesn't contain relevant information,
    acknowledge this and provide general knowledge while noting it may not be from the source documents.
    Be concise but thorough, and cite specific mission details when available in the context."""
    # TODO: Set context in messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    if context:
        context_message = f"Here is a relevant context: {context} from NASA mission documents. Use this context to answer the user's question."
        messages.append({"role": "user", "content": context_message})
    # TODO: Add chat history
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
