import os
from urllib import request
from datetime import date
import uteis

import requests

def cbk(a,b,c):  
    '''''Callback function 
    @a:Downloaded data block 
    @b:Block size 
    @c:Size of the remote file 
    '''  
    per=100.0*a*b/c  
    if per>100:  
        per=100
    #print('%.2f%%' % per)


def getArquivoMapBiomas(file_url):
    try:
        file = 'dashboard_alerts-shapefile.zip'
        dir= uteis.getPlataformaDownload()#os.path.abspath('.')+'\downloads\\'
        work_path=os.path.join(dir,file)          
        request.urlretrieve(file_url , work_path, cbk)
        return work_path
    except Exception as e:
        print(e)    
        return 'ERRO'    
    
def getArquivoDownload(file_url, file):
    try:
        dir= uteis.getPlataformaDownload()#os.path.abspath('.')+'\downloads\\'
        work_path=os.path.join(dir,file)          
        request.urlretrieve(file_url , work_path, cbk)
        return work_path
    except Exception as e:
        print(e)    
        return 'ERRO'    

def getArquivoOnline(file_url):
    try:
        print("Inciando o download, aguarde.")
        file = str(date.today())+'.tgz'
        dir= os.path.abspath('../../airflow/dags') + '\downloads\\'
        work_path=os.path.join(dir,file)          
        request.urlretrieve(file_url , work_path, cbk)
        print("Download Finalizado")
        return work_path
    except Exception as e:
        print(e)    
        return 'ERRO'    

def downloadImagem(urlImagem, nome):    
    response = requests.get(urlImagem)
    if response.status_code == 200:
        with open(nome, 'wb') as f:
            f.write(response.content)        
        return nome
    else:
        print('Failed to download image.')