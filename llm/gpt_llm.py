from config.config  import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# def generate_gpt(prompt):
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a cybersecurity expert in industrial control systems (ICS)."},
#             {"role": "user", "content": prompt}
#         ]
    
#     )

    # return response.choices[0].message.content

def generate_gpt_5(prompt):
    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert in industrial control systems (ICS)."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
