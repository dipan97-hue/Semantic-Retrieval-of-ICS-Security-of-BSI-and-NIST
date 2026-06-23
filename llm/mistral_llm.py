from mistralai import Mistral

from config.config import MISTRAL_API_KEY

client = Mistral(api_key= MISTRAL_API_KEY)

MODEL_NAME = "mistral-small-latest"

def generate_mistral(prompt):

    try:

        response = client.chat.complete(model=MODEL_NAME, messages=[{"role":"system",
                                                                     "content":"You are an OT cybersecurity expert."

                },

                {

                    "role":"user",

                    "content":prompt

                }

            ]

        )

        return response.choices[0].message.content

    except Exception as e:

        print("MISTRAL ERROR:",e)

        return "Mistral generation failed."