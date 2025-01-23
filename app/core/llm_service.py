from openai import OpenAI
import os
import google.generativeai as genai
# from google.generativeai import configuration as config
# from google.generativeai import types
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from dotenv import load_dotenv
import json

load_dotenv()


class LLMService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.openai_client = None
        self.gemini_client = None
        self.chosen_llm = os.getenv("CHOSEN_LLM", "openai")

    def get_openai_client(self):
        if self.openai_client is None:
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return self.openai_client

    def get_gemini_client(self):
        if self.gemini_client is None:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_client = genai.GenerativeModel('gemini-pro')
        return self.gemini_client

    def generate_text(self, prompt_data: dict) -> str:
        """
        Gera texto usando a LLM escolhida (OpenAI ou Gemini).

        Args:
            prompt_data: Dicionário com os dados do prompt (system, user, assistant, etc.).

        Returns:
            O texto gerado pela LLM.
        """
        if self.chosen_llm == "openai":
            client = self.get_openai_client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # Substitua pelo modelo desejado
                messages=[
                    {"role": "system", "content": prompt_data.get("system", "")},
                    {"role": "user", "content": prompt_data.get("user", "")},
                    {"role": "assistant", "content": prompt_data.get("assistant", "")}
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=1
            )
            return response.choices[0].message.content
        elif self.chosen_llm == "gemini":
            client = self.get_gemini_client()

            # Inicia uma conversa
            # chat = client.start_chat()

            # Constrói a requisição
            request = json.loads(prompt_data["user"])
            request["generation_config"] = {
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            }
            request["safety_settings"] = {
                "HARASSMENT": "block_none",
                "HATE_SPEECH": "block_none",
                "SEXUALLY_EXPLICIT": "block_none",
                "DANGEROUS_CONTENT": "block_none",
            }

            # Converte a requisição para o formato esperado pelo Gemini
            request = json_format.ParseDict(request, Value())

            response = client.generate_content(request)

            return response.text
        else:
            raise ValueError(f"LLM desconhecida: {self.chosen_llm}")
