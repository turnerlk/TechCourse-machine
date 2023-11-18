# JWT COURSE

Criei este desafio com o intuito de ajudar a comunidade de hacking e colocar meus conhecimentos em programação em prática.

Esta aplicação contém três tipos comuns de vulnerabilidades web, frequentemente encontradas no dia a dia: broken access control, SQL Injection e Command Injection.

Deixarei abaixo os comandos de como baixar o projeto e executar em sua maquina.

Baixar o projeto:

```jsx
git clone https://github.com/turnerlk/TechCourse-machine
```

Acesse o diretório:

```jsx
cd TechCourse-machine
```

Utilizando o comando abaixo a aplicação estará executando [localhost](http://localhost) (http://127.0.0.1) na porta 80:

```jsx
sudo docker-compose up --build
```

Caso você não tenha o docker, utilize o seguinte comando para instalar em sua maquina.

```jsx
sudo apt update
sudo apt install -y docker.io
```

E aí? Tudo pronto? Vamos explorar?

Vambora……

Quando acessamos a aplicação em 127.0.0.1, observamos que a página inicial contém algumas informações sobre o que é a plataforma, etc.

Então, iniciamos nossa exploração, clicamos em "Log In" e somos redirecionados para a tela de login da aplicação.

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled.png)

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%201.png)

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%202.png)

Após a tentativa malsucedida de utilizar credenciais padrão, decidimos realizar uma varredura de diretórios visando identificar possíveis rotas ou arquivos que pudessem conter informações sensíveis ou apresentar vulnerabilidades.

Com a ferramenta WFUZZ, realizamos o fuzzing de diretórios e encontramos as seguintes rotas:

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%203.png)

```jsx
wfuzz -z file,big.txt --hc 404 http://127.0.0.1/FUZZ/
```

Podemos observar que a rota "course" retornou o código 200 e o valor de "chars" foi bastante elevado.

Tentamos acessar a rota e fomos direcionados para a rota "login". Então, abrimos o Burp Suite e interceptamos a requisição para "/course/".

Ao analisar o acesso à rota com a ferramenta Burp, notamos que o HTML da página do curso foi retornado com sucesso. Além disso, foi possível visualizar o conteúdo de um curso específico diretamente da rota explorada.

  

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%204.png)

Primeira vulnerabilidade encontrada!

“A vulnerabilidade de broken access control é **um tipo de falha de segurança que permite que um usuário não autorizado acesse recursos restritos** . Ao explorar esta vulnerabilidade, os invasores podem contornar os procedimentos de segurança padrão e obter acesso não autorizado a informações ou sistemas confidenciais”

Analisando o HTML, podemos observar que existe um campo de pesquisa na página. Utilizando esse campo para pesquisar um curso dentro da plataforma, notamos que o campo de pesquisa está funcionando perfeitamente. Pesquisamos pelo curso "Python" e retornou apenas o curso pesquisado.

```jsx
/course/?q=python
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%205.png)

 

Utilizamos uma payload de SQLI neste campo e observamos que todos os cursos foram retornados sem nenhum erro.

```jsx
/course/?q=a'or+1+%3d+1+--+-
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%206.png)

Após alguns testes de SQLI, conseguimos pegar o número de colunas que existe no banco de dados, nesse caso existem 4 colunas.

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%207.png)

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%208.png)

Conseguimos encontrar a segunda vulnerabilidade.

“A injeção de SQL, também conhecida como SQLI, é **um vetor de ataque comum que usa código SQL malicioso para manipulação de banco de dados de back-end para acessar informações que não deveriam ser exibidas** . Essas informações podem incluir qualquer número de itens, incluindo dados confidenciais da empresa, listas de usuários ou detalhes particulares de clientes.”

Como podemos observar acima, o banco possui 4 colunas.

Após alguns testes, conseguimos ver a versão do banco de dados e qual tecnologia está rodando, que nesse caso é o sqlite 3.40.1.

Deixaremos o link abaixo de artigos para explorar esse tipo de vulnerabilidade nesta tecnologia.

[https://book.hacktricks.xyz/pentesting-web/sql-injection](https://book.hacktricks.xyz/pentesting-web/sql-injection)

[https://www.exploit-db.com/docs/english/41397-injecting-sqlite-database-based-applications.pdf](https://www.exploit-db.com/docs/english/41397-injecting-sqlite-database-based-applications.pdf)

Testando algumas payloads e conseguimos trazer algumas tabelas do branco de dados e o nome das tabelas.

```jsx
a'union SELECT 1,sql,3,4 FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name NOT LIKE 'sqlite_%' AND name ='auth_user' -- -
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%209.png)

```jsx
a'union+SELECT+1,tbl_name,3,4+FROM+sqlite_master+where+type%3d'table'+and+tbl_name+NOT+like+'sqlite_%25''+--+-
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2010.png)

```jsx
a' union SELECT 1,GROUP_CONCAT(name),3,4 AS column_names FROM pragma_table_info('auth_user'); -- -
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2011.png)

Como podemos analisar acima, a nossa payload retornou os nomes das tabelas e as colunas de cada tabela, então vamos ler a coluna username e  password, da tabela  auth_user.

```jsx
a' union select 1,password,username,4 from auth_user -- -
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2012.png)

Como podemos notar, conseguimos obter acesso às informações do usuário administrador, incluindo o seu nome de usuário e a hash da senha.

Copiamos a hash do usuário admin e, em seguida, no nosso terminal (no meu caso, estou usando um Kali Linux), criamos um arquivo e colamos a hash dentro desse arquivo.

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2013.png)

Utilizando a ferramenta Hashcat, uma aplicação projetada para realizar quebra de senhas, empregamos a mesma para identificar o tipo específico da hash.

 

```jsx
hashcat --identify hash
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2014.png)

Com o comando que vamos disponibilizar abaixo, podemos tentar quebrar a hash do usuário admn e trazer a senha tem texto claro.

```jsx
sudo hashcat -a0 -m 10000 senha /usr/share/wordlists/rockyou.txt
```

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2015.png)

Como podemos perceber, conseguimos capturar a senha do administrador. Agora, procederemos com o acesso à aplicação.

Neste ponto, destacamos a importância de utilizar senhas complexas. Caso o administrador tivesse adotado uma senha mais robusta, a quebra da mesma seria consideravelmente mais desafiadora.

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2016.png)

Quando acessamos a rota /monitor_logs/, podemos observar que se trata de um painel onde o administrador utiliza comandos para bloquear alunos, realizar reload, entre outras ações. O painel exibe alguns comandos que podem ser utilizados.

Ao testar alguns desses comandos, conseguimos identificar nossa terceira vulnerabilidade conhecida como command injection.

Command injection: é **um ataque cibernético que envolve a execução de comandos arbitrários em um sistema operacional (SO) host** . Normalmente, o agente da ameaça injeta os comandos explorando uma vulnerabilidade do aplicativo, como validação de entrada insuficiente.

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2017.png)

Feito isso agora é só explorar.

Com essa vulnerabilidade é possível um RCE (remote command execution).

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2018.png)

![Untitled](JWT%20COURSE%20a2a0c08bb0a64e9395505e4795de5f87/Untitled%2019.png)

E assim concluímos nossa jornada! Este laboratório proporcionou a aprendizagem de três vulnerabilidades presentes em aplicações que podem ser encontradas mundo real.

Agradeço sinceramente a você, leitor, por baixar e testar o meu projeto. Espero que tenha contribuído para o seu conhecimento. Se possível, compartilhe com amigos, ajudando na disseminação do aprendizado.

Estou disponível para trocar ideias, criticas e sugestões. Deixo aqui meu LinkedIn e Instagram. Obrigado mais uma vez pela sua participação!

Linkedin: [https://www.linkedin.com/in/lucas-dantas-625007131/](https://www.linkedin.com/in/lucas-dantas-625007131/)

Instagram: [https://www.instagram.com/llucas.dantass/](https://www.instagram.com/llucas.dantass/)
