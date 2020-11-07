import socket
import re
import sys

class Response(object):
    def __init__(self, data):
        data_split = data.split(b'\r\n\r\n')
        self._headers = data_split[0]
        self._status_code = int(self.headers.split(b"\r\n")[0].split()[1])

        self._content = data[len(self._headers)+4:]
    
    @property
    def headers(self):
        return self._headers
    
    @property
    def content(self):
        return self._content
    

    @property
    def status_code(self):
        return self._status_code
    

    def __str__(self):
        return (
            "_________Headers_________\n"
            +self.headers
            +"\n"
            +"_________Content_________\n"
            +self.content
        )


class Socket(object):
    def __init__(self, host, port, main_path):
        self._host = host
        self._port = port
        self._main_path = main_path
        self._socket = socket.socket()
    
    def connect(self, timeout=10):
        self._socket.settimeout(timeout) #define timeout para acusar erro em caso de demora ao receber mensagens
        self._socket.connect((self._host, self._port))
    
    def send_headers(self, path=None):
        if not path:
            path = self._main_path
        else:
            path = self._main_path+path
        print(f"Acessando caminho: {path}")
        headers = (
            f"GET {path} HTTP/1.1\r\n" #indica o path dentro do domínio que vai ser visitado
            f"Host: {self._host}\r\n" 
            f"Accept-Encoding: identity\r\n"
            "\r\n"
        )
        self._socket.sendall(bytes(headers, "utf-8"))
    
    def receive_response(self):
        data = b""

        while True:
            try:
                part = self._socket.recv(2048) #recebe dados
            except: #caso o timeout ocorra sai do loop
                break
            data += part
            if part == b"": #caso a mensagem seja vazia sai do loop 
                break
        if data == b"":
            print("Não foi possível receber qualquer tipo de resposta do servidor!")
            exit()
        return Response(data)
    
    def close(self):
        self._socket.close()
    


url = sys.argv[-1] # Recupera url passada como argumento


if "http" in url:
    url_arr = url.split("/")
    url_arr = url_arr[2:]
else:
    url_arr = url.split("/")


host = url_arr[0] #Extrai o host da url dada


#Recupera caminho dentro do host da url dada
main_path = "/".join(url_arr[1:])
main_path = "/"+main_path
if main_path[-1] != "/":
    main_path = main_path+"/"


s = Socket(host, 80, main_path) # Instancia a classe Socket passando o host, a porta 80 e o caminho principal do site
s.connect() # Cria a conexão

s.send_headers() # Envia os headers da requisição
response = s.receive_response() # Recebe o corpo do site
f = open("index.html", 'wb') #Salva em um arquivo chamado index.html
f.write(response.content)
f.close()

if response.status_code == 200:
    images = re.findall(r'<[iI][mM][gG].+?[sS][rR][cC]="(.+?)"', response.content.decode("utf-8", "ignore")) # Utiliza regular expression para recuperar os links das imagens presentes no site

    print("Imagens encontradas na página:")
    print(
        "\n".join(images)
    )
    print("Começando o download...")

    for image in images:
        if ("http" in image or "www" in image) and host not in image: # Verifica se a imagem reside em outro host
            print(f"Imagem presente em outro hosst, portanto não será baixada: {image}")
        else:
            img_url_arr = image.split("/") # Cria uma lista pelo split por '/' da url
            url_filter = lambda element : False if ("http" in element or "www" in element or element.strip()=="") else True # Função que exclui da lista posições que contém www ou http ou https ou strings vazias
            img_url = "/".join(list(filter(url_filter, img_url_arr))) # Utiliza a função acima e um join com '/' para obter apenas o caminho da imagem no servidor

            s.send_headers(img_url) # Envia os header da requisição passando o caminho da imagem
            image_response = s.receive_response() # Recebe o conteúdo da imagem
            if image_response.status_code == 200:
                f = open(image.split("/")[-1], 'wb') # Salva a imagem localmente com o nome dela no servidor
                f.write(image_response.content)
                f.close()
                print("Imagem baixada com sucesso!")
            else:
                print(
                    f"Infelizmente não foi possível fazer o download da imagem de url {image}! Esta requisição recebeu um status {image_response.status_code}"
                )
else:
    print(
        f"Infelizmente não foi possível realizar a operação! Esta requisição recebeu um status {response.status_code}"
    )

s.close() #fecha o socket







