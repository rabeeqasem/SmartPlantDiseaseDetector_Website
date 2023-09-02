import openai

openai.api_key = ""


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def get_response(context_):
    gptresponse = get_completion_from_messages(context_)
    context_.append({'role': 'assistant', 'content': gptresponse})
    return context_, gptresponse     