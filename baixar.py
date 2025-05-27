import requests
import os
import re

# Jovem, informe aqui o token de acesso da página que foi copiado do Graph API Explorer
ACCESS_TOKEN = 'Access token'
PAGE_ID = 'Vai o ID da FanPage'

# Aqui vai limpar os nomes dos albuns para evitar erros ao criar as pastas no nosso pc
def limpar_nome(nome):
    return re.sub(r'[\\/*?:"<>|]', "_", nome)

def pegar_albuns():
    url = f'https://graph.facebook.com/v18.0/{PAGE_ID}/albums?access_token={ACCESS_TOKEN}'
    resposta = requests.get(url)
    dados = resposta.json()
    return dados.get('data', [])

def pegar_fotos_do_album(album_id):
    url = f'https://graph.facebook.com/v18.0/{album_id}/photos?fields=images&access_token={ACCESS_TOKEN}'
    resposta = requests.get(url)
    dados = resposta.json()
    return [foto['images'][0]['source'] for foto in dados.get('data', [])]

def baixar_fotos(urls, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)
    for i, url in enumerate(urls):
        try:
            img = requests.get(url)
            with open(f"{pasta_destino}/foto_{i}.jpg", "wb") as f:
                f.write(img.content)
        except Exception as e:
            print(f"Erro ao baixar a imagem {i}: {e}")
    print(f"{len(urls)} fotos baixadas para a pasta: {pasta_destino}")

albuns = pegar_albuns()

if not albuns:
    print("Nenhum álbum encontrado ou erro ao acessar a API.")
else:
    for album in albuns:
        nome_album = limpar_nome(album['name'])
        print(f"Baixando álbum: {nome_album}")
        fotos = pegar_fotos_do_album(album['id'])
        if fotos:
            baixar_fotos(fotos, f"albuns/{nome_album}")
        else:
            print(f"Nenhuma foto encontrada no álbum: {nome_album}")
