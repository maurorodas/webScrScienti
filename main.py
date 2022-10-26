import mechanicalsoup
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

browser = mechanicalsoup.Browser()
browser.keep_alive = False

url = "https://scienti.minciencias.gov.co/ciencia-war/busquedaAvanzadaGrupos.do?integrantes=&proyectos=&annoCreacion=&depInst=&status=&progNacional=&nmeLider=&codIdGrupo=&progNacionalSec=&buscar=buscar&nmeGrupo=&areaConocimiento=&ciuInst=&productos=&genLider=&nmeInstitucion=%22Universidad%20de%20Caldas%22&filtrar=&maxRows=100&gruposAvanzada_tr_=true&gruposAvanzada_p_=1&gruposAvanzada_mr_=100"

page = browser.get(url, verify=False)
soup = BeautifulSoup(page.text, 'lxml')
table = soup.find('table', id='gruposAvanzada')
rows = []
data = []

for group_data in table.find_all('tbody', {'class': 'tbody'}):
  rows = group_data.find_all('tr')
  for row in rows:
    groupCode = row.find_all('td')[1].text
    groupName = row.find_all('td')[2].text
    groupURL = row.find_all('td')[2].a["href"]
    
    browserGroup= mechanicalsoup.Browser()
    browserGroup.keep_alive = False
    pageGroup = browserGroup.get(groupURL, verify=False)
    soupGroup = BeautifulSoup(pageGroup.text, 'lxml')
    filename = groupCode + ".html"
    f = open(filename, "w")
    f.write(soupGroup.prettify( formatter="html" ))
    f.close()
    
    groupLider = row.find_all('td')[3].text
    groupLiderURL = row.find_all('td')[3].a["href"]
    groupCat_temp = row.find_all('td')[6].text
    groupConv_temp = row.find_all('td')[7].text
    
    if "CATEGORIA" in groupCat_temp:
      cat = groupCat_temp.split()
      groupCat = cat[1]
    else:
      groupCat = groupCat_temp
    
    if "CONVOCATORIA" in groupConv_temp:
      conv = groupConv_temp.split()
      groupConv = conv[3]
    else:
      groupConv = "NA"
    
    data.append(
        {
            'Código': groupCode,
            'Nombre': groupName,
            'grupo_URL': groupURL,
            'Lider': groupLider,
            'lider_URL': groupLiderURL,
            'Categoría': groupCat,
            'Año_Convocatoria': groupConv
        }
    )
df = pd.DataFrame(data)
print(df)