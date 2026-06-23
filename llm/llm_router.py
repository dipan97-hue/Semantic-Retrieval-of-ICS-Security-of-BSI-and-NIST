from llm.gemini_llm import generate_gemini 
from llm.gpt_llm import  generate_gpt_5
from llm.mistral_llm import generate_mistral
from llm.anthropic_llm import claude


def generate_answer(model_name, prompt):

    # if model_name == 'gpt-4o-mini':
    #     return generate_gpt(prompt)
    #print(f"MODEL SELECTED: {model_name}")
    if model_name == 'gemini-3.1-flash-lite':
        return generate_gemini(prompt)
    
    if model_name == 'Mistral':
        return generate_mistral(prompt)
    
    if model_name == 'gpt-5.4-nano':
        return generate_gpt_5(prompt)

    if model_name == 'claude-haiku-4-5':
        return claude(prompt)

    else:
        return "Invalid Model"
