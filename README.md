# Ambiente-Docker-para-desnvolvidmento-django-react-postgres

<img src="https://imagens.tiespecialistas.com.br/2016/02/django.png"/> <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"/> <img src="https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node-dot-js&logoColor=white"/> 


*******
<h3>Sobre:</h3>


O Wiki.js é um software de documentação que segue o estilo wiki rodando no Node.js e escrito em JavaScript.
Você pode optar por fazer o download dos arquivos e buildar a imagens apartir dos arquivos, isso está na sesção de [Configuração Dockerfile](#dockerfile) ou seguido todos os passos e fazer manualmente todo o processo.


<div id='requerimentos'/>

*******
<h3>Requisitos:</h3>


<ul>
  <li>Sistema operacional Linux. No projeto foi usado um ambiente controlado, uma VM criada no Virtual Box e usando o SO <a href="https://docs.docker.com/compose/install/">CentOS 7.</a></li>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/centos/">Docker</a> e também o <a href="https://docs.docker.com/engine/install/centos/">Docker-compose</a> para a segunda parte do projeto
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
<h2>Configurando o Dockerfile:</h2>

para esse projeto foi usado 2 Dockerfiles que estão em diretórios diferentes, eles foram criados com as configurações básicas para buildar as imagens que serão executadas no ambiente para subir o serviço, sendo que o Dockerfile da imagem do postgres contém um arquivo .sql que vai executar no entrypoint do serviço um script que cria o banco de dados da apilicação e o usuário e senha.

   Crie  a estrutura de diretórios:
            
       mkdir bd-setup && mkdir wiki-setup
    
   Dentro do bd-setup crie o arqui init.sql e o Dockerfile:
      
       vi init.sql
       
   Conteúdo do arquivo init.sql:
       
       CREATE USER wikiuser WITH password 'wiki1234';

       ALTER USER wikiuser WITH SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN REPLICATION;

       CREATE DATABASE wikijs WITH OWNER wikiuser;
       
   Criando o Dockerfile:
  
       vi init.sql
       
   Conteúdo do arquivo Dockerfile:
  
       FROM postgres:11-alpine
       COPY init.sql /docker-entrypoint-initdb.d/
       LABEL CUSTON_BY="seunome"
       
       

  
   Acesse o diretório do wiki-setup para criar o Dockerfile da do serviço:
   
       cd ../wiki-setup
      
       vi Dockerfile
      
   
   Conteúdo do Dockerfile da wiki:
   
       FROM requarks/wiki:2
       ENV WIKI_ADMIN_EMAIL=seuemail@dominio.com
       ENV DB_HOST=postgres-db
       ENV DB_TYPE=postgres
       ENV DB_PORT=5432
       ENV DB_USER=wikiuser
       ENV DB_PASS=wiki1234
       ENV DB_NAME=wikijs

 
 
  OBS: o arquivo Dockerfile deve ser criado exatamente com essa nomenclatura.
 
 *******
 <h3>Build das imagens  a partir dos Dockerfiles:</h3>
     
   acesse os respectivos diretórios para buildar as imagens:
        
      cd /db-setup
      Docker build -t postgres-wiki .
      
      cd /wiki-setup
      Docker build -t my-wiki-js .
    
   Você pode checar se as imagens foram criadas com o seguinte comando:
     
      docker image ls -a
      
   Exemplo de saida do comando:
    <img src="https://github.com/Gileno29/wiki-js-docker/blob/main/img/dockerimagels.jpg"/>
   
   
      
 *******    
 <h3>Criando os containers Docker:</h3>
 
   Com a build das imagens prontas pode ser criado os containers, os crie exatamente nessa ordem:
    
      docker run -d -p 5432:5432 --name postgres-db -p 5432:5432 -e POSTGRES_PASSWORD=123456  postgres-wiki:latest
      
      docker run -d -p 8080:3000  --link postgres-db:db --name wiki --restart unless-stopped  my-wiki-js:latest
   
   pode ser conferido se os containers estão criados com o comando:
      
      docker container ls -a 
      
      
   Exemplo de saída do comando:
   
   <img src="https://github.com/Gileno29/wiki-js-docker/blob/main/img/dockercontainerls.jpg"/>
   
   <a name="verificar"><a/>
   Ao final do processo você validar se a aplicação funcinou pelos logs:
      
        docker logs -f my-wiki-js
       
   A saída do log com a aplicação funcionando será a seguinte:
   
   <img src="https://github.com/Gileno29/wiki-js-docker/blob/main/img/servicoup.jpg"/>
   
  O serviço pode ser acessado, nesse caso, através do ip da máquina virtual mais a porta que definimos na hora da criação do container. Para uma máquina em uma plataforma de cloud como a azure, por exemplo, pode ser acessado atráves do ip da instância que a azure fornece ou atráves do serviço de dns que os mesmos também possuem.

Exemplo de acesso em uma VM local:
<img src="https://github.com/Gileno29/wiki-js-docker/blob/main/img/pagina_wiki_js.jpg"/>

<a name="composer"></a>
 *******   
 <h3>instalação utilizando Docker-compose:</h3>
 
caso deseje a intalação pode ser feita via docker-compose para facilitar na hora de subir os containers e não ter que usar tantos parâmetros em um comando Docker. Os passos a seguir descrevem como subir os containers apartir do docker-compose, o cenário e organização dos diretórios é mesma esse método serve apenas para substituir a inicialização dos containers pelo modo tradicional do docker.
 
 
 *******
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
 
      version: "3"
        services:
          postgres-db:
            image: postgres-wiki:latest

            container_name: postgres-db

            restart: unless-stopped

            volumes:
              - /home/centos/wiki-js-docker/db-setup/init.sql:/docker-entrypoint-initdb.d/init.sql

            environment:
              - POSTGRES_USER=postgres
              - POSTGRES_PASSWORD=1234

            ports:
              - "5353:5432"

            networks: 
              - wiki-network

          wiki:
            image: my-wiki-js:latest
            depends_on:
              - postgres-db

            networks: 
              - wiki-network

            restart: unless-stopped

            ports:
              - "8080:3000"


        networks:
          wiki-network:
            driver: bridge
  
 
 
No docker compose.yml são declaradas as imagens que vão utilizas para o container e também pode ser criado  váriaveis de ambiente, no caso  do service wiki, não precisa declarar as variáveis do BD pois as mesmas já foram associadas no Dockerfile e está sendo usado a build da imagem criada apartir do Dockerfile.
 
      version: "3"
        services:
          postgres-db:
            image: postgres-wiki:latest

            container_name: postgres-db

            restart: unless-stopped

            volumes:
              - /home/centos/wiki-js-docker/db-setup/init.sql:/docker-entrypoint-initdb.d/init.sql

            environment:
              - POSTGRES_USER=postgres
              - POSTGRES_PASSWORD=1234

            ports:
              - "5353:5432"

            networks: 
              - wiki-network
 
 
 nessa primeira parte do arquivo foi declarado a versão do docker-compose utilizada e o primeiro service(Container a ser contruido), foi dado um  nome a ele, foi informado qual imagem vai ser usada para a contrução docontainer e foi passado o parâmetro ` restart: unless-stopped ` para que, se o container parar, o mesmo seja reiniciado. Construimos um volume apontando para o nosso script `init.sql` para que quando o banco inicie crie o BD da aplicação e seu usuário e senha, aqui deixo uma observação, mesmo com script apontado dentro do Dockerfile do BD como o composer gerenciando o banco burla esse script no `docker-entrypoint-initdb.d`, por a necessidade da criação desse volume, passamos o usuário e senha padrão que desejamos para o usuário padrão do BD (Use senha mais seguras em aplicações em produção), estabelecemos o mapeamento entre aporta externa e do container e por último criamos atribuimos uma network ao container.
 
 

       wiki:
            image: my-wiki-js:latest
            depends_on:
              - postgres-db

            networks: 
              - wiki-network

            restart: unless-stopped

            ports:
              - "8080:3000"


        networks:
          wiki-network:
            driver: bridge
  
  Nessa útima parte do `docker-compose.yml` criamos o segundo service com nome de `wiki` infomamos que ele vai ser dependente de um outro serviço que precisa está funcional para ele poder iniciar, no caso o banco de dados, especificamos isso com o parâmentro `depends_on:- postgres-db` também definimos o parâmetro `restart: unless-stopped` e colocamos o serviço na mesma network que o outro fazemos o mapeamento de portas em  `ports:- "8080:3000"`, por fim criamos a network que atribuimos a ambos os containers em ` networks: wiki-network: driver: bridge`.
  
  após o arquivo está devidamente criado, podemos executar o comando `docker-compose up` e os nossos containers estarão criados.

para checar podemos usar os comando da seção [acima](#verificar) 

