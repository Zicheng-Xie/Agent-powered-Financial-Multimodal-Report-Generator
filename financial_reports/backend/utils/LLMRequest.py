import os
import sys
from openai import OpenAI
import json,os
from financial_reports.backend.config import config
import requests
import re

class LLMRequest:
    def __init__(self):
        
        apikey = config.data['deepseek_api_key']
        self.client = OpenAI(api_key=apikey, base_url="https://api.deepseek.com")
        self.ollama_url = "http://localhost:11434"  # Ollama server URL
        
    
    def chat_model(self, prompt: str, history: list = None):
        """
        Get the chat response for the given prompt by calling DeepSeek HTTP API.
        """
        answer = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        
        
        try:
            # 提取第一个 choice 的文本
            answer = answer.choices[0].message.content.strip()
            # 去除<think>和</think>标签里的内容
            answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
            return answer
        except (KeyError, IndexError):
            raise Exception(f"Unexpected response format: {answer}")

    def embedding_model(self, text: str):
        """
        Get the embedding for the given text by calling Ollama HTTP API.
        """
        payload = {
            "model": "bge-m3:latest",
            "input": text
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.ollama_url}/v1/embeddings",
            headers=headers,
            json=payload
        )
        try:
            # 提取第一个 choice 的文本
            return response.json()['data'][0]['embedding']
        except (KeyError, IndexError):
            raise Exception(f"Unexpected response format: {response}")
        
        
    def chat_prompt(self, prompt: str, data: dict):
        """
        Get the chat response for the given prompt by calling DeepSeek HTTP API.
        """
        keys = list(data.keys())
        values = list(data.values())
        prompt = prompt.format(**data)
        validation_prompt = '''
            This is my prompt: {prompt}
            This is the answer of this prompt: {answer}
            Please check if the answer can accurately answer the prompt. 
            If the answer is correct, return "yes", otherwise return "no".
            Please do not return any other text.
        '''
        while True:
            answer = self.chat_model(prompt)
            validation = self.chat_model(validation_prompt.format(prompt=prompt, answer=answer))
            if "yes" in validation.lower():
                break
        return answer

if __name__ == "__main__":
    llm_request = LLMRequest()
    # Example usage
    chat_response = llm_request.chat_model("Hello, how are you?")
    print("Chat Response:", chat_response)
    
    embedding_response = llm_request.embedding_model("This is a test text for embedding.")
    print("Embedding Response:", embedding_response)

    chat_prompt_response = llm_request.chat_prompt("The user ask a question {prompt} Here's some information: {da1}", {"prompt": "What is the capital of France?", "da1": "Paris is the capital of France."})
    print("Chat Prompt Response:", chat_prompt_response)