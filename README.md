# Ambiente com React+Django+Postegres provisonado com Docker-compose. 

<img src="https://quintagroup.com/cms/technology/Images/docker-compose-button.jpg"/>



*******
<h3>Sobre:</h3>


Esse repositorio tem como objetivo documentar o provisionamento de ambiente com Django, React e Postgres utilizando o docker-compose.
Você pode optar por fazer o download dos arquivos e buildar a imagens apartir dos arquivos, isso está na sesção de [Configuração Dockerfile](#dockerfile) ou seguido todos os passos e fazer manualmente todo o processo.


<div id='requerimentos'/>

*******
<h3>Requisitos:</h3>


<ul>
  <li>Sistema operacional Linux. Para esse exemplo está sendo usado o SO <a href="https://www.centos.org/centos-linux/">CentOS 7.</a></li>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/centos/">Docker</a> e também o <a href="https://docs.docker.com/compose/install/">Docker-compose</a> para a segunda parte do projeto
  <li>Node</li>
  <li>Python 3</li>
</ul>


*******
<h3>Documentação:</h3>

[Instalação Docker](#docker)

[Configuração Dockerfile](#dockerfile)

[Configuração Docker Composer](#composer)



Todos os comandos aqui podem ser consultados  na <a href="https://docs.requarks.io/">documentção oficial</a> do software

<a name="docker"></a>
*******
<h2>Instalação Docker Centos 7 via respositório:</h2>
  Caso possua uma instalação antiga, remova:
 
  
    sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

  Após remover qualquer versão antiga do Docker será nessário a instalação de alguns utilitários para adicionar o source-list do Docker ao Centos e em seguida 
  a adicionar o source-list:
  
     sudo yum install -y yum-utils

     sudo yum-config-manager \
           --add-repo \
           https://download.docker.com/linux/centos/docker-ce.repo
    
   
  
  Agora basta apenas fazer a instalação:
  
      sudo yum install docker-ce docker-ce-cli containerd.io
    
 <a name="dockerfile"></a>
 *******
 <h2>Instalando Node JS:</h2>
     
    wget http://nodejs.org/dist/v10.19.0/node-v10.19.0.tar.gz
 
    tar xzvf node-v* && cd node-v*
    
 Instale os pacotes necessários para copilar o código:
 
    sudo yum install gcc gcc-c++
 
 Copile o código:
  
    ./configure
    make
    
    sudo make install
 
 se você digitar:
  
    node --version
    
 devera ter a seguite resposta:
 
    v10.19.0

 ******
<h2>Configurando o Dockerfile:</h2>

para esse projeto foi usado 2 Dockerfiles que estão em diretórios diferentes, eles foram criados com as configurações básicas para buildar as imagens que serão executadas no ambiente para subir o serviço.

   Crie  o diretório:
            
       mkdir react-front 
    
   Dentro do react-front use o seguinte comando para instalar o utilitário para criar o projeto:
      
       npm install -g create-react-app 
       
   crie o projeto:
   
       create-react-app front-client

   Criando o Dockerfile:
   
   OBS: o arquivo Dockerfile deve ser criado exatamente com essa nomenclatura.
  
       vi Dockerfille
       
       
   Conteúdo do arquivo Dockerfile:
  
      FROM node:14-slim

      WORKDIR /user/src/app

      COPY ./package.json ./

      COPY ./package-lock.json ./

      RUN npm install

      COPY . .

      EXPOSE 3000

      ENTRYPOINT [ "npm" ]

      CMD ["start"]

   Volte ao diretório principal e crie o projeto Django para o Backed:
        
       cd ../../
       django-admin startproject desafio .
       
  crie o Dockerfile:
        
        vi Dockerfile
      
   
   Conteúdo do Dockerfile da do python:
   
      FROM python:3.10
      WORKDIR /app
      COPY requirements.txt .
      RUN pip install -r requirements.txt

      COPY . .







 
 

 
 
      
 
 <h3>Instalação:</h3>
 
 execute o curl para download da versão mais recente do docker-compose:
 
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
 dê permissão de execução ao arquivo:
    
    sudo chmod +x /usr/local/bin/docker-compose

  crie um link simbolíco para que o docker-copose fique vísivel na variável PATH (opcional, porém recomendo):
  
     sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
     
  agora pode checar se o compose está instalado com o comando:
    
      docker-compose --version
      
  Exemplo de saída do comando:
  
 <img src="https://github.com/Gileno29/wiki-js-docker/blob/main/img/dockercomposeversion.jpg"/>
 
 ******* 
 <h3>configuração do docker-compose.yml:</h3>
 
 na raiz do projeto crie um arquivo chamado docker-compose.yml e faça as configurações do ambiente nele:
 
    vi docker-compose.yml
    
 conteúdo do docker-compose.yml:
 
      version: "3.3"

      services:
        backend:
          build: .
          command: python manage.py runserver 0.0.0.0:8000
          volumes:
            - .:/app
          ports:
            - 8000:8000
          depends_on:
            - db
        db:
          image: postgres:14
          environment:
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=postgres
          volumes:
            - postgres_data:/var/lib/postgresql/data/

        frontend:
          build: ./react-front/front-client
          ports:
            - 3000:3000
          depends_on:
            - backend

          volumes:
            - ./react-front/front-client:/user/src/app

      volumes:
        postgres_data:
  
 
 
No docker compose.yml são declaradas as imagens que vão utilizas para o container no caso para a build do serviço de Backend é passado o "." que referencia o Dockerfile que está no mesmo nivel do composer.yml o serviço do db e passado é buildado apartir da imagem do postgres baixada do dockerhub e por ultimo o serviço do front-end que é buildado apartir da imagem que está em outro diretório com seu caminho referenciado.
 
para checar podemos usar os comando da seção [acima](#verificar) 

