import ollama
from openai import OpenAI
from financial_reports.config.deepseek import DEEPSEEK_CODE, DEEPSEEK_URL


class LLMRequester:
    def __init__(self):
        self.ollama_client = ollama
        self.deepseek_client = OpenAI(api_key=DEEPSEEK_CODE, base_url=DEEPSEEK_URL)
        
    
    def request_qianwen05b(self, prompt):
        # 小组件
        response = self.ollama_client.chat('qwen2:0.5b', 
                                    messages=[
                                        {"role": "user", "content": prompt}
                                    ],
                                    stream=False)
        return response
    
    def request_deepseekreasoner(self, prompt):
        response = self.deepseek_client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    
    def request_deepseekchat(self, prompt):
        response = self.deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    

if __name__ == "__main__":
    llm_requester = LLMRequester()
    prompt = "What is the capital of France?"
    print("ChatGLM-6B Response:", llm_requester.request_chatglm6b(prompt))