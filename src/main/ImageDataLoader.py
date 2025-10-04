import os
import json
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv 

load_dotenv() 
IMAGE_PATH = "image.png"

class ImageDataLoader:
    def __init__(self, image_path: str):
        self.prompt =  """
            Analise esta imagem que é um placar de final de jogo de Counter-Strike 2.
            Extraia o placar geral, o status da partida, e as estatísticas detalhadas de CADA UM dos cinco jogadores exibidos na parte inferior.
            Seja preciso com a transcrição dos nomes e dos números.
        """
        self.img_path = image_path
        self.img = self.load_image()
        self.schema = self.define_schema()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def define_schema(self):
        return types.Schema(
            type=types.Type.OBJECT,
            properties={
                "score": types.Schema(type=types.Type.STRING, description="Placar final (ex: '13-9')."),
                "status": types.Schema(type=types.Type.STRING, description="Status do jogo (ex: 'VITÓRIA' ou 'DERROTA' ou 'EMPATE')."),
                "players": types.Schema(
                    type=types.Type.ARRAY,
                    description="Lista de estatísticas dos jogadores.",
                    items=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "nick": types.Schema(type=types.Type.STRING, description="Nome de usuário do jogador."),
                            "kda": types.Schema(type=types.Type.STRING, description="O número grande de Kills na carta do jogador."),
                            "tag": types.Schema(type=types.Type.STRING, description="A primeira estatística descritiva (ex: 'Matador quádruplo')."),
                            "hs": types.Schema(type=types.Type.STRING, description="A porcentagem que aparece (ex: '57%')."),
                            "damage": types.Schema(type=types.Type.STRING, description="O número em destaque no canto superior do card (ex: 103 ou 56)."),
                        },
                        required=["nick", "kda"]
                    )
                )
            },
            required=["score", "status", "players"]
        )

    def load_image(self) -> Image.Image:
        try:
            img = Image.open(self.img_path)
            return img
        except FileNotFoundError:
            return None
    
    def analyse_scoreboard(self):
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[self.prompt, self.img],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=self.schema,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            return None