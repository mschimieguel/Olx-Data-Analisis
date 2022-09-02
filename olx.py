
import requests
from bs4 import BeautifulSoup
import pandas as pd



def getAnuncios(url,headers):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.select('a[data-lurker_list_position]')
    anuncios = []
    for i in a_tags:
        anuncios.append(i['href'])

    return anuncios


def getDescricaoAnuncio(url,headers):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #exemplo da tag que contem a descricao do anuncio
    #<span class="sc-1sj3nln-1 eOSweo sc-ifAKCX cmFKIN" color="dark" font-weight="400">
    span_tags = soup.select('span[font-weight][color="dark"]')


    descricao = span_tags[1].text
    if(descricao == "Calcule o frete" ):
        descricao = span_tags[2].text
    if(descricao == "Descrição" ):
        descricao = span_tags[3].text
    if(descricao == "Detalhes"):
        #print("DETALHES_DEBUG")
        descricao = span_tags[0].text
    return descricao
   

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}


url =  "https://mg.olx.com.br/eletronicos-e-celulares?o=1"
descricoes = []
anuncios = []
for i in range(1,5):
    #trocando de paginas
    url = url[:-1] + str(i)
    print("Coletando Pagina: \n",url)

    anuncios.extend(getAnuncios(url,headers))

   
count = 1
print(len(anuncios))


for anuncio in anuncios:
    print("Coletando Anuncio: ",count)
    count = count + 1
    descricoes.append(getDescricaoAnuncio(anuncio,headers))

    #    print ("--------------------------------------------------------")

df = pd.DataFrame(data = zip(anuncios,descricoes,),  columns = ['Anuncio','Descricao'])
df.to_csv("Amostra.csv")


