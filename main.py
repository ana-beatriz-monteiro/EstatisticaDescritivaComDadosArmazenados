import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

class Tabela:
    def __init__(self, nome):
        self.nome = nome

    def listarConteudo(self):
        response = (
            supabase.table(self.nome)
            .select("*")
            .execute()
        )

        return response

    def criarDataframe(self):
        return pd.DataFrame(self.listarConteudo().data)

    def mediaSegmento(self, segmento):
        df = self.criarDataframe()
        return df[df["segmento"] == segmento]["total_venda"].mean()

@app.route('/')
def index():
    vendasInformatica = Tabela("vendas_informatica")
    df = vendasInformatica.criarDataframe()

    media_educacao = vendasInformatica.mediaSegmento("educacao")
    media_corporativo = vendasInformatica.mediaSegmento("corporativo")
    media_gamer = vendasInformatica.mediaSegmento("gamer")

    segmentos = ["Educação", "Corporativo", "Gamer"]
    medias = [media_educacao, media_corporativo, media_gamer]
    plt.figure(figsize=(8,5))
    plt.bar(segmentos, medias, color="pink")
    plt.title("Média de Vendas por Segmento")
    plt.xlabel("Segmento")
    plt.ylabel("Média")
    plt.savefig("static/medias_segmento.png")
    plt.close()
    
    return (
        df.to_html(index=False, border=1)
        + f"<h3>Média do segmento Educação R$ {media_educacao:.2f}</h3>"
        + f"<h3>Média do segmento Corporativo R$ {media_corporativo:.2f}</h3>"
        + f"<h3>Média do segmento Gamer R$ {media_gamer:.2f}</h3>"
        + f"<img src='/static/medias_segmento.png'></img>"
    )

if __name__ == '__main__':
    app.run(debug=True)