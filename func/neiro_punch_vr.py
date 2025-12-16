import re
import requests
import json
def neiro_punch(text):
                        # First API call with reasoning
            response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-v3.2",
                "messages": [
                    {
                    "role": "user",
                    "content": f"Ты вписан в код моего личного автоответчика для друзей. В случае их опечатки я хочу чтобы им автоматически приходил ответ. Напиши нудное гневное сообщение-упрек из-за опечатки в слове. Ошибочно написанное слово {text}, по возможности обыграй это в ответе. Напиши только само сообщение-упрек и ничего больше"
                    }
                ],
                "reasoning": {"enabled": True}
            })
            )

            # Extract the assistant message with reasoning_details
            response = response.json()
            response = response['choices'][0]['message']

            for i, item in enumerate(response.get('reasoning_details', [])):
                text = item.get('text')
                return text