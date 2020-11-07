# Integrantes do grupo
* Lucas Ramalho Luiz da Silva
* Gabriel Ferreira Gomes da Silva
* Alisson Alex Weiss
* Daianny Santana de Oliveira
* Bruno bellisi

# Requisitos
Para executar este projeto é necessário ter instalado o python 3.

# Sobre o projeto
O trabalho se baseia em um script em python que utiliza como base a lib nativa sockets. Foram criadas duas classes:
* Response (usada para fazer a conexão do socket e fazer todo o tratamento de envio e recebimento de mensagens)
* Response (classe utilizada para guardar os headers, o status code e o conteúdo da resposta)

Além disso foi utilizada a lib re do python para usar regular expression para detectar as tags img's do código do site.
# Como executar
A url a ser visitada deve ser passada como argumento ao executar o arquivo trab.py da seguinte forma:
```
python trab.py [URL]
```
Se a url a ser visitada é www.google.com.br, por exemplo, o comando seria:
```
python trab.py www.google.com.br
```