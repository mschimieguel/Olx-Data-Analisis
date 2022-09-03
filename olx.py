
from turtle import numinput
import requests
from bs4 import BeautifulSoup
import pandas as pd



def getAnuncios(urlPagina,headers):
    response = requests.get(urlPagina,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.select('a[data-lurker_list_position]')
    anuncios = []
    for i in a_tags:
        anuncios.append(i['href'])

    return anuncios


def getDescricaoAnuncio(urlAnuncio,headers):
    response = requests.get(urlAnuncio,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #exemplo da tag que contem a descricao do anuncio
    #<span class="sc-1sj3nln-1 eOSweo sc-ifAKCX cmFKIN" color="dark" font-weight="400">
    span_tags = soup.select('span[font-weight][color="dark"][class="sc-1sj3nln-1 eOSweo sc-ifAKCX cmFKIN"]')
    
    if(len(span_tags) == 0):
        return "Erro Anuncio Vazio"
        
    descricao = span_tags[0].text

    return descricao
   

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


urlbase =  "https://mg.olx.com.br/eletronicos-e-celulares?o="
descricoes = []
anuncios = []
numPaginas = int(input("Digite o numero De Paginas para carrregar \n (Lembre-se que cada página tem 50 anuncios):\n"))
for i in range(1,numPaginas+1):
    #trocando de paginas
    urlPagina = urlbase + str(i)
    print("Coletando Pagina: \n",urlPagina)

    anuncios.extend(getAnuncios(urlPagina,headers))

   
count = 1
print(len(anuncios))


for anuncio in anuncios:
    print("Coletando Anuncio: ",count,"/",len(anuncios))
    count = count + 1
    descricoes.append(getDescricaoAnuncio(anuncio,headers))

    #    print ("--------------------------------------------------------")

df = pd.DataFrame(data = zip(anuncios,descricoes,),  columns = ['Anuncio','Descricao'])
df.to_csv("Amostra.csv")
