# Define the Ollama LLM function
def ollama_llm(question, context, chat_history=None):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    messages = [{'role': 'user', 'content': formatted_prompt}]
    
    if chat_history:
        messages.extend(chat_history)
    
    response = ollama.chat(model='llama2:chat', messages=messages)
    return response['message']['content']
