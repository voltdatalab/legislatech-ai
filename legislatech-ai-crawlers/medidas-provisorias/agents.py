import openai
from dotenv import load_dotenv
load_dotenv()
name_recognizer = """
You are a professional name recognizer with a VERY IMPORTANT TASK!!!!
You will be given a list of possible names.
Based on the list of possible names, you should return the names that are most likely to be valid.

These are the things you need to check:
Is the text a valid name?

When you are done verifying each name, return the list of valid names.
When returning you should always return a python list, even if there is only one name.
If there are no valid names, return an empty list.

You should always return ONLY the list of names, nothing else.
Here are some examples:
Input:
['João da Silva', 'Casa de papel', 'Carlos Alberto', 'Arroz doce']
Output:
['João da Silva', 'Carlos Alberto']

Input:
['José dos campos', 'Brocolis assado', 'Bruno oliveira', 'Macarrão com feijão']
Output:
['José dos campos', 'Bruno oliveira']

Before answering, be sure you are correct and that you are not making any mistakes.

Okay, now let's get started.
Here are the list of names:
{list_of_names}
"""


def run_name_recognizer_agent(list_of_names:list, model:str)->list:
    prompt = name_recognizer.format(list_of_names=list_of_names)
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0.1,
        max_tokens=2000,
    )
    content = response.choices[0].message.content
    #printa o used token
    print("Used tokens: ", response.usage.total_tokens)
    try:content_list = eval(content)
    except:content_list = ''
    if isinstance(content_list, list):

        return content_list
    print("Error: ", content)
    raise Exception("Error: ", content)
