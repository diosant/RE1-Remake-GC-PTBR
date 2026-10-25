"""Traducao dos documentos (subscr.dat, bloco 1). Chave (1, numero do documento).
Nestes textos cada quebra de linha real vira {0006}; {0007} = nova pagina.
Linhas de no maximo ~40 letras (a largura das paginas do original)."""

def doc(texto):
    # a primeira linha do texto (logo apos as aspas) e ignorada; o resto vira {0006}
    return texto[1:].replace('\n', '{0006}')

T = {}

T[(1, 0)] = doc("""
{0000}
{0016}Manual da S.T.A.R.S.

Se você mudou o controle para o
TIPO-B ou o TIPO-C, lembre-se de que
as instruções daqui valem para o
controle TIPO-A. {0007}
{0016}—Como ver a TELA DE STATUS—

Aperte o botão Y durante o jogo.
(Não é possível ver a TELA DE STATUS
durante as cenas ou enquanto você
estiver sendo atacado.) {0007}
Na TELA DE STATUS você pode fazer
o seguinte:
{0011}N•Equipar armas
{0011}N•Usar itens
{0011}N•Ver mapas
{0011}N•Ler arquivos
{0007}
{0016}—Como VER O MAPA—

Na TELA DE STATUS escolha MAPA na
barra de menu, ou aperte o botão Z
durante o jogo. Se você não tiver o
mapa, só os lugares já explorados
vão aparecer. {0007}
{0016}—Como LER OS MAPAS—

sala sem cor:{0011}ÿSala inexplorada.
sala laranja:{0011}ÿSala que ainda
{0011}ÿtem itens.
sala verde:{0011}ÿSala explorada
{0011}ÿe sem itens.
{0007}



{0011}{0046}porta vermelha:{0011}hTrancada.
{0011}{0046}porta branca:{0011}hDestrancada.
{0011}{0046}porta azul:{0011}hPorta por onde
{0011}hvocê já passou.
{0007}{000E}{0007}{0001}{0009}{0002}{001E}{FFFF}
{0016}—SOBREVIVÊNCIA REAL, dicas extras—

Você pode ver os itens que estão
dentro dos baús.
{0007}



Na TELA DO MAPA, aperte o botão A,
escolha o baú que quer olhar e
aperte o botão A de novo para
confirmar. (O conteúdo do baú
vai aparecer.) {0007}{NOFIM}""")

T[(1, 1)] = doc("""
{0000}



É o filme que pertencia ao
Kenneth. Preciso de um aparelho para
ver o que foi gravado nele. """)

T[(1, 2)] = doc("""
{0000}



{0016}Livro da Maldição
{0007}
{0016}As quatro máscaras,
{0016}uma máscara que não fala o mal…
{0016}uma máscara que não cheira o mal…
{0016}uma máscara que não vê o mal…
{0016}uma máscara que não fala, não
{0016}cheira nem vê o mal…

{0016}Quando as quatro estiverem no lugar,
{0016}o mal despertará. """)

T[(1, 4)] = doc("""
{0000}



{0016}Bilhete amassado {0007}


Hoje, o Sr. Spencer me mandou
esconder uma coisa num lugar onde
ninguém pudesse encontrar. {0007}


Bom, eu tive uma ideia. Pensei que,
se ela ficasse protegida por um
animal perigoso, como o cão feroz
que vive aqui, ninguém conseguiria
chegar perto dela!  {0007}


Pelo que sei, o vira-lata está
sempre rondando a sacada do segundo
andar, no lado oeste do terraço, e
deve vir correndo quando ouvir
um apito de cachorro. {0007}


É aí que você entra. Acontece que,
pelo que eu vejo, você é a única
pessoa capaz de chegar perto daquele
maldito cão sem ser estraçalhada. {0007}


Ou seja, só você pode pôr esta
coleira nele. O objeto que o Sr.
Spencer quer esconder está escondido
dentro dela. {0007}


Você é a única pessoa em quem posso
confiar isto. É claro que você também
vai ganhar algo com isso. Lembra
daquele item que você sempre quis
conseguir? {0007}


Pois bem, em troca dos seus serviços,
talvez eu consiga arranjá-lo para
você. Isso pode ser bom para nós
dois…

{0011}{012C}Jon Toleman""")

T[(1, 5)] = doc("""
{0000}



{0016}BOTÂNICA
{0016}—Usos das Ervas Medicinais— {0007}

É bem sabido que existem muitas
plantas às quais se atribuem poderes
de cura. Desde a antiguidade, a
humanidade trata ferimentos e
doenças usando várias plantas. {0007}

Neste livro, vamos apresentar três
ervas nativas das Montanhas Arklay
e resumir as propriedades medicinais
de cada uma. Cada erva tem uma cor
e uma propriedade medicinal
própria. {0007}

A erva verde recupera as forças.
A erva azul neutraliza venenos
naturais. Já a erva vermelha não tem
efeito sozinha. Descobrimos que
misturar ervas verdes e vermelhas
aumenta muito o efeito. {0007}

Vamos descrever os efeitos da erva
vermelha misturada a outras ervas
quando tivermos mais dados. Enquanto
isso, fique à vontade para fazer
seus próprios testes, pois o melhor
saber vem da própria experiência. """)

T[(1, 6)] = doc("""
{0000}



{0016}Instruções especiais para o descarte
de cadáveres {0007}


Temos novas informações sobre
aqueles “seres”. Eles podem parecer
mortos, mas na verdade são capazes
de voltar à vida. Porém, há formas
de impedir que voltem a se
mexer. {0007}


Hoje se conhecem duas formas de
impedir que eles ressuscitem.

1.  INCINERAÇÃO
2.  DESTRUIÇÃO DA CABEÇA
{0007}


Se outros métodos forem descobertos,
todos serão avisados imediatamente. {0007}


Enquanto isso, para quem ainda tem
vontade de viver, deixamos óleo no
primeiro andar da mansão. Peguem
quanto for preciso. {0007}


Vocês vão precisar de algo para
acendê-lo, e isso terão de achar
sozinhos. """)

T[(1, 7)] = doc("""
{0000}



{0016}Diário do Zelador {0007}
9 de maio de 1998

Joguei pôquer hoje à noite com o Scott
e o Alias, da Segurança, e com o Steve,
da Pesquisa. O Steve ganhou tudo, mas
acho que ele roubou. Canalha. {0007}
10 de maio de 1998

Um dos chefões me mandou cuidar
de uma criatura nova. Parece um
gorila sem pele. As instruções eram
alimentá-la com animais vivos. {0007}


Quando joguei um porco lá dentro,
a criatura pareceu brincar com ele…
arrancou as pernas do porco e puxou
as tripas para fora antes de
começar a comer. {0007}
11 de maio de 1998

Lá pelas 5 da manhã, o Scott me
acordou. Quase morri de susto. Ele
estava com uma roupa de proteção.
Me deu outra e mandou eu vestir.
Disse que houve um acidente no
laboratório do subsolo. {0007}


Eu sabia que algo assim ia acontecer.
Aqueles desgraçados da Pesquisa
nunca dormem, nem nos feriados. {0007}
12 de maio de 1998

Estou com essa maldita roupa espacial
desde ontem. Minha pele está imunda e
coçando inteira. Os malditos cães
estão me olhando de um jeito
estranho, então resolvi não dar
comida para eles hoje. Que se danem. {0007}
13 de maio de 1998

Fui à enfermaria porque minhas costas
estão inchadas e coçando. Puseram um
curativo enorme e disseram que eu
não precisava mais usar a roupa.
Só quero dormir. {0007}
14 de maio de 1998

Achei outra bolha grande no meu pé
hoje de manhã. Acabei arrastando o pé
até o canil. Os cães ficaram quietos
o dia inteiro, o que é estranho. {0007}


Aí percebi que alguns tinham fugido.
Talvez seja a vingança deles por eu
não ter dado comida nos últimos três
dias. Se alguém descobrir, vou ter
a cabeça arrancada. {0007}
16 de maio de 1998

Dizem por aí que um pesquisador que
tentou fugir da propriedade ontem à
noite levou um tiro. Meu corpo inteiro
está quente e coçando, e eu suo o
tempo todo. {0007}


Cocei o inchaço no braço e um pedaço
de carne podre simplesmente caiu.
Que diabos está acontecendo comigo? {0007}
19 de maio de 1998

Febre passou mas coça. Hoje fome
e como comida de cachorro. {0007}
21 de maio de 1998

Coça coça Scott veio cara feia então
matei ele. Gostoso. {0007}
4 / /  Coça.  Gostoso. """)

T[(1, 9)] = doc("""
{0000}



{0016}Mensagem do chefe de segurança {0007}{0016}CONFIDENCIAL
A/C: Chefe de Segurança
Data: 22 de julho de 1998  2:13

O Dia X está chegando. Execute os
procedimentos abaixo em até uma
semana. Exige-se ação imediata. {0007}

{0011}{0046}1.{0011}{005A}Atrair a S.T.A.R.S. para a propriedade
{0011}{005A}e obter dados de combate reais das
{0011}{005A}B.O.W. contra a S.T.A.R.S. {0007}

{0011}{0046}2.{0011}{005A}Coletar dois embriões de cada espécime
{0011}{005A}mutante como amostra, exceto o
{0011}{005A}Tyrant. Descartar o Tyrant. {0007}

{0011}{0046}3.{0011}{005A}Garantir a eliminação total do
{0011}{005A}Laboratório Arklay, incluindo todo o
{0011}{005A}pessoal e as cobaias. Disfarçar as
{0011}{005A}mortes como um acidente.
{0011}{005A}Concluídos os procedimentos acima,
{0011}{005A}informe a sede para receber
{0011}{005A}novas instruções. {0007}

Se por algum motivo não for possível
cumprir o procedimento no prazo,
informe imediatamente. Em caso de
emergência, ligue direto para o
ramal 5691. {0007}


Boa sorte.
Sede da Umbrella,
Umbrella Inc. """)

T[(1, 10)] = doc("""
{0000}



{0016}Bilhete de suicídio 





{0007}
22 de junho de 1998

Eu tive que fazer isso. Fugimos
daquelas coisas, um ajudando o outro
a sobreviver. Mas o Robert começou
a mostrar os sintomas. Eu tive que
fazer. Aquelas coisas são o mal puro. {0007}


Não havia outro jeito. Ele teria feito
o mesmo se fosse o contrário. Depois
de acabar com o sofrimento dele, tive
que deixá-lo no banheiro. Agora devo
ser o último.... {0007}


Como isso pôde acontecer? Nunca vou
me perdoar por ter feito parte deste
projeto. Mas um dia vou pagar pelo
que fiz. Não há como escapar deste
hospício. Agora é só questão de
tempo. {0007}


Está tudo pronto. Só preciso de um
pouco de coragem para ir até o fim.
Saber que vou deixar tanta coisa por
fazer é um arrependimento que não
cabe em palavras. {0007}


Mas é melhor do que esperar para
virar uma daquelas coisas. Por favor,
entenda, e me deixe ao menos acabar
com a minha vida como uma pessoa. {0007}



{0016}Há uma mensagem no verso. {0007}



{0016}Linda, por favor, me perdoe... """)

T[(1, 11)] = doc("""
{0000}



{0016}RELATÓRIO DA PLANTA 42 {0007}

Quatro dias se passaram desde o
acidente. A planta do Ponto 42 está
crescendo num ritmo espantoso. {0007}

Embora haja muito de desconhecido
nesta planta, sabemos que, comparado
ao outro grupo de plantas, o Vírus-T
teve um efeito bem mais forte
sobre ela. {0007}

O Vírus-T mudou drasticamente a
anatomia e o tamanho do hospedeiro.
Olhando o estado atual, é difícil
imaginar como ela era. Não existe
nada parecido em nenhum lugar
da Terra. {0007}

Também descobrimos que a PLANTA 42
tem duas fontes principais de
nutrientes. Uma delas é a raiz. De
algum jeito, ela criou raízes até
o subsolo. {0007}

Logo depois do acidente, um cientista
enlouqueceu e destruiu o Anel
Aquático. Desde então, o subsolo virou
uma piscina. É bem provável que um
dos produtos químicos da água esteja
acelerando o crescimento da PLANTA 42. {0007}


Porém, ainda não identificamos qual
é esse produto químico. {0007}

Um corpo em forma de bulbo da
PLANTA 42 foi visto pendurado no teto
do primeiro andar. Temos certeza de que
ela usou os dutos de ar para chegar
lá. Muitos cipós longos, parecidos com
tentáculos, saem do bulbo. {0007}

Acreditamos que os cipós são a segunda
forma de conseguir nutrientes. Quando
a PLANTA 42 sente uma presa, usa os
cipós como tentáculos para pegá-la.
Depois disso, ventosas nos cipós
sugam todo o sangue da presa. {0007}

Também notamos que ela tem certa
inteligência. Quando captura uma presa
ou está inativa, os cipós se enroscam
na porta para barrar possíveis
invasores. {0007}

Infelizmente, vários dos nossos
cientistas já foram vítimas da
PLANTA 42. Ao ouvir os relatos dos
sobreviventes, todos notaram uma
coisa em comum: {0007}

Quando as abas em forma de pétala se
abrem e mostram as partes vitais,
ela tende a ficar mais
agressiva. {0007}

Uma testemunha disse que era como se
ela tentasse se proteger. Ainda não se
sabe por que ela age desse jeito.

{0011}{012C}21 de maio de 1998
{0011}{012C}Henry Sarton """)

T[(1, 12)] = doc("""
{0000}



{0016}Experimento de química orgânica {0007}

As semelhanças nas características
celulares da planta de crescimento
rápido infectada pelo Vírus Tyrant já
foram relatadas em estudos anteriores.
Porém, ao repetir os experimentos,
um fato novo e curioso apareceu. {0007}

Descobrimos que um produto da família
UMB, o UMB No. 20, contém um composto
que é tóxico para as células
da planta. {0007}

Demos ao UMB No. 20 um novo nome:
V-JOLT. Se os cálculos estiverem certos,
aplicando o V-JOLT direto na raiz da
planta, ela inteira deve morrer em
5 segundos. {0007}

O V-JOLT pode ser feito apenas
misturando os produtos VP e UMB numa
proporção certa. Mas é preciso muito
cuidado ao lidar com os produtos UMB.
Eles podem soltar gases tóxicos se
forem mal manuseados. {0007}

As características de cada produto
UMB são as seguintes:

UMB No. 3{0011}{012C}vermelho
Yellow-6{0011}{012C}amarelo
UMB No. 7{0011}{012C}verde
UMB No. 10{0011}{012C}laranja
VP-017{0011}{012C}azul
V-JOLT{0011}{012C}marrom-escuro """)

T[(1, 14)] = doc("""
{0000}



{0016}Fotografia do Barry {0007}{0007}

Esta é a foto que caiu da camisa do
Barry pouco antes de ele cair no
buraco. Há algo escrito no
verso. {0007}

Nós te amamos, papai.
Das suas filhas queridas,

{0011}{012C}Moira e Polly""")

T[(1, 15)] = doc("""
{0000}



{0016}Carta de um pesquisador {0007}
8 de junho de 1998
Minha querida Ada,

Quando você ler esta carta, eu já não
serei a pessoa que você conheceu.
O resultado do meu exame saiu hoje,
e, como eu suspeitava, deu positivo.
 {0007}


Sinto que estou à beira da loucura
só de pensar no fim que me espera.
Eu daria tudo para não ter que virar
uma daquelas coisas. {0007}


Pelo que sei, você não está infectada.
Espero de verdade que as coisas não
cheguem a esse ponto, mas, se você for
a última pessoa viva, quero que pegue
o material da Sala de Dados
Visuais. {0007}


Depois, ative o Sistema de
Autodestruição na Sala de Energia e
fuja daqui. Por favor, faça tudo o que
puder para tornar público todo esse
acidente. {0007}


Se tudo ainda estiver funcionando,
você deve conseguir liberar todas as
travas pelo Sistema de Segurança. {0007}


Configurei o terminal da pequena sala
de segurança para que você entre no
sistema usando o meu nome e, como
senha, o seu nome. {0007}


Você vai precisar de outra senha para
liberar a trava da porta do Subsolo 2,
onde fica a Sala de Dados
Visuais. {0007}


Por segurança, codifiquei essa senha
numa radiografia, um raio X. Eu
conheço você e sei que vai conseguir
decifrá-la sem dificuldade. {0007}


Só mais uma coisa… é o meu último
pedido. Espero que você nunca precise
me ver nesse estado, mas, se cruzar
comigo nessa forma horrenda, eu
imploro: acabe com o meu sofrimento.
Espero que você entenda. {0007}


{0011}{0064}Obrigado, Ada.
{0011}{0064}Com todo o carinho,

{0011}{0064}John """)

T[(1, 16)] = doc("""
{0000}



{0016}V-ACT
{0016}Nota do pesquisador {0007}

Agora há provas de que, quando o
hospedeiro perde a consciência, o
corpo entra num estado dormente.
Nesse período, o vírus fica ativo e
transforma e reconstrói rapidamente
a composição básica do corpo. {0007}

O hospedeiro acabou se transformando
numa criatura humanoide. (Nós os
chamamos de V-ACT) {0007}

A velocidade e o incrível
desenvolvimento muscular chamam
atenção. Depois da transformação, ele
fica mais ágil e agressivo. {0007}

Quatro dos nossos pesquisadores já
morreram tentando alimentá-lo, e o
lugar virou um banho de sangue.
(Desde esse acidente trágico e
bárbaro, decidimos chamar esse tipo
de “Crimson Heads”) {0007}

Aquele protótipo perigoso e precioso
não pode ficar lá. Precisamos achar
um jeito de lidar com ele. Eliminá-lo
está totalmente fora de questão.
{0007}

Por fim, decidimos congelar o
espécime e trancar o corpo no subsolo
do cemitério nos fundos.""")

T[(1, 17)] = doc("""
{0000}



{0016}FAX{0007}


Para:{0011}•Divisão de Saneamento
A/C:{0011}•Gerente de Saneamento
De:{0011}•Comitê de Contingência de
{0011}•Desastres de Raccoon {0007}

O conteúdo deste fax é confidencial
e destinado só ao destinatário
indicado. Qualquer cópia ou divulgação
do conteúdo deste fax a terceiros
é terminantemente proibida pelo
remetente. {0007}

Depois de lido, este fax deve ser
destruído imediatamente. {0007}

Esperamos que os danos do recente
surto do Vírus-T sejam bem maiores
do que o estimado no início.
Há várias preocupações. {0007}

Primeira preocupação
Mais da metade dos pesquisadores foi
infectada pelo Vírus-T e morreu.
Também foi informado que quase todos
os sobreviventes do acidente estão
começando a mostrar sintomas da
infecção pelo Vírus-T. {0007}

Segunda preocupação
Nossa Equipe Secreta de Patrulha de
Segurança também foi totalmente
eliminada. Por isso, nossa pesquisa
mais secreta corre risco de vir a
público. Exige-se ação rápida para
impedir a cobertura da imprensa. {0007}

Terceira preocupação
É muito provável que a maioria dos
espécimes esteja à solta dentro do
complexo. Esperamos muitas vítimas
em seguida. {0007}

Ainda que lamentáveis, essas vítimas
comprovam o sucesso dos resultados da
nossa pesquisa. É preciso agir para
impedir que esses resultados se
tornem públicos. {0007}

Suspeitamos que a primeira intervenção
oficial virá da Polícia Estadual e da
S.T.A.R.S. Recomendamos fortemente
tomar medidas contra eles
primeiro. """)

T[(1, 18)] = doc("""
{0000}



{0016}PROTOCOLOS DE SEGURANÇA {0007}
{0016}NÍVEL UM

Heliporto/ Só para uso de executivos.
Esta restrição não vale em caso de
emergência. {0007}
{0016}SUBSOLO 1

Passagem para o heliporto/ Entrada
proibida, a não ser acompanhado por um
Pesquisador Consultor ou pelo Chefe de
Segurança. Pessoas não autorizadas
que entrarem no heliporto serão
baleadas na hora. {0007}


Elevador/ O elevador para em casos
de emergência. {0007}
{0016}SUBSOLO 2

Sala de Dados Visuais/ Uso exclusivo da
Divisão de Pesquisas Especiais. Qualquer
outro acesso à Sala de Dados Visuais
deve ser liberado por Keith Arving,
responsável pela sala. {0007}
{0016}SUBSOLO 3

Prisão/ A Divisão de Saneamento
controla o uso da prisão. Pelo menos um
Pesquisador Consultor (E. Smith, S.
Ross, A. Wesker) deve estar presente se
o uso de vírus for autorizado. {0007}


Porta de Tranca Tripla/ A entrada na
sala é limitada à única pessoa que
desativar a tranca com todas as Senhas.
O acesso aos Terminais de Saída
exclusivos de cada seção dos
Pesquisadores Seniores desativa a tranca.
{0007}


Sala de Energia/ Nesta sala, um
composto nitro é usado como principal
combustível de energia. Acesso limitado
aos Supervisores da Sede. A restrição
pode não valer para Pesquisadores
Consultores com autorização especial. {0007}


Terminais de Saída de Senha/ O uso e
o acesso aos Terminais de Saída são
limitados aos Pesquisadores Seniores
autorizados. {0007}
{0016}SUBSOLO 4

Sobre o progresso do “Tyrant”
após a aplicação do Vírus-T…
{0011}Ý(Ilegível daqui em diante…) """)

T[(1, 19)] = doc("""
{0000}



{0016}Nota de observação {0007}

A descoberta do Vírus-G aconteceu, na
verdade, 21 anos depois da aplicação
do vírus primordial. {0007}

O “Parasita Protótipo”, que recebemos
de um laboratório na França, foi
aplicado no espécime de amostra. O
espécime aceitou o parasita sem
mostrar nenhum sinal de reação
adversa. {0007}

A falta de qualquer reação era um
mistério sem solução. Mas agora está
tudo claro para mim. {0007}

O “Parasita Protótipo” ficou incubado
no corpo do espécime por 21 anos.
Então, desse estado de incubação, o
protótipo sofreu uma mutação súbita.
(“Evoluiu” talvez seja a palavra mais
adequada para descrever isso.) {0007}

Essa observação ampliou minha visão
da pesquisa. Com mais modificações e
testes, consegui chegar a um método
para criar o “G”, que supera o
desempenho do “T”. {0007}


Foi essa a descoberta que mudaria o
futuro da história das B.O.W. {0007}
Mal posso esperar para ver a cara
irritante da Alexia quando eu enfim
anunciar a minha pesquisa. Mas, pena,
vou ter de esperar mais alguns anos
para confirmar tudo por completo.

{0011}{012C}William Birkin """)

T[(1, 20)] = doc("""
{0000}
{0016}-EXAMINAR UM ITEM-

Na TELA DE STATUS, escolha um ITEM
e depois o comando EXAMINAR.
(Os detalhes do item vão
aparecer.) """)

T[(1, 21)] = doc("""
{0000}
{0016}—Fuga de Emergência— 

Usar ITENS DE DEFESA, como as
adagas, permite escapar por um
instante quando um inimigo agarra
você. (Mas não é possível escapar
quando o inimigo agarra você
por trás.) {0007}


Para equipar um ITEM DE DEFESA, vá
à TELA DE STATUS e escolha um ITEM
no menu ITENS DE DEFESA. Depois,
escolha o comando EQUIPAR. {0007}


Se o modo de ITEM DE DEFESA estiver
em MANUAL nas opções do controle,
você precisa apertar o botão L para
usar o ITEM DE DEFESA.""")

T[(1, 23)] = doc("""
{0000}



{0016}Foto de família e anotações {0007}{0007}



{0016}Há algo escrito no verso.
{0007}10 de nov. de 1967
-Vírus Progenitor aplicado

•Jessica
  Vírus aplicado: Tipo-A
      Plasmólise do tecido durante a
      ativação celular.

  Fusão do vírus: Negativa

  Ação: Descartada {0007}
•Lisa

  Vírus aplicado: Tipo-B
      Plasmólise do tecido durante a
      ativação celular.

  Fusão do vírus:
      Positiva, mas com fusão tardia.
{0007}


  Modificação corporal:
      Resultados constantes observados.

  Situação:
      Manter observação protegida. {0007}
•George
  Ação: Eliminado (30 de nov. de 1967) {0007}



{0016}Há um diário deixado por alguém. {0007}
14 de nov. de 1967

Fiquei tonta depois da injeção que me
deram. Não vejo a mamãe. Para onde
levaram ela?
Ela prometeu que a gente ia fugir
juntas. Será que fugiu sozinha e me
deixou para trás? {0007}
15 de nov. de 1967

Achei a mamãe. A gente comeu junto.
Fiquei muito feliz. {0007}


Mas ela era falsa. Não minha mamãe.
Mesmo rosto mas diferente por dentro. {0007}


Tenho que achar mamãe. Tenho que
devolver rosto para mamãe. {0007}


Peguei de volta o rosto da mamãe.
Ninguém pode ter minha mamãe só eu.
Prendo o rosto dela em mim para ela
não ir embora.
Porque mamãe triste quando encontro
ela sem o rosto. {0007}
17 de nov. de 19 7

dentro da caixa, cheiro da mamãe.
talvez mamãe de verdade lá.
caixa de pedra dura. Doeu. corda de
aço no caminho.
não vejo mamãe porque 4 pedras. """)

T[(1, 24)] = doc("""
{0000}



{0016}Foto de família {0007}{0007}{NOFIM}""")

T[(1, 25)] = doc("""
{0000}



{0016}Diário de Trevor{0007}
24 de nov. de 1967

Onze dias se passaram desde que
cheguei a esta propriedade. Como vim
parar nesta situação? Um sujeito de
jaleco trouxe um prato com uma
refeição mirrada e me disse: {0007}


“Desculpe fazer o senhor passar por
isto, mas é por segurança.” Foi aí que
caiu a ficha. Agora tudo faz sentido. {0007}


Só duas pessoas sabem o segredo
desta mansão: o Sr. Spencer e eu.
Se me matarem, o Sr. Spencer será
o único a saber o segredo. {0007}


Mas com que objetivo? Isso já não
importa. É perigoso demais aqui.
Minha família… espero que esteja bem. {0007}


Decidi fugir…
Jessica, Lisa, rezo para que estejam
a salvo. {0007}
26 de nov. de 1967

Como pude ser tão descuidado? Perdi
meu isqueiro favorito, o que a Jessica
me deu de aniversário. Agora vai ser
bem mais difícil sair deste lugar
escuro. {0007}


13 de novembro, o dia em que meu
destino foi selado. Minha tia tinha
sido internada três dias antes. Jessica
e Lisa disseram que iam visitá-la.
Queria poder estar com elas. {0007}


Mas espere, enquanto escrevo, as
lembranças voltam com mais nitidez.
Pouco antes de desmaiar, lembro que
os homens de jaleco disseram algo como
“É provável que sua família já…”
Rezo para que estejam a salvo. {0007}
27 de nov. de 1967

De algum jeito consegui sair daquela
sala. Mas sair desta mansão não vai
ser tão fácil. Tenho que passar por
todas as armadilhas. Olhos de Tigre,
Emblema Dourado… Preciso tentar
lembrar, pelo meu próprio bem.... """)

T[(1, 26)] = doc("""
{0000}
29 de nov. de 1967

Não consigo sair. Tentei todas as
formas possíveis de fugir, mas só dei
de cara com a realidade: estou preso. {0007}


Já estive em todo lugar. O laboratório
com os grandes tubos de vidro cheios
de formol e aquelas cavernas escuras,
úmidas e sinistras… O que posso fazer? {0007}


No início, não quis acreditar no que
via. Mas aquele sapato de salto alto
conhecido no corredor... Foi como um
reflexo. Um nome me veio à cabeça:
Jessica! {0007}


Não quero acreditar que elas tiveram
o mesmo destino que eu.
Não! Não posso perder a esperança.
Tenho que acreditar que estão vivas. {0007}
30 de nov. de 1967

Não como nem bebo nada há dias.
Sinto que estou enlouquecendo. {0007}


Por que isso está acontecendo comigo?
Por que tenho que morrer assim?
Fiquei obcecado demais em projetar
esta mansão medonha. Eu devia ter
desconfiado. {0007}
31 de nov. de 1967

Era um túnel subterrâneo escuro e
úmido. E mais um beco sem saída. Mas,
mesmo na escuridão, algo chamou a
minha atenção. {0007}


Com cuidado, acendi o último fósforo
que tinha para ver o que era. {0007}


Um túmulo! E, gravado fundo na pedra,
estava o meu nome!

{0016}“George Trevor” {0007}


Naquele instante, tudo ficou claro.
Aqueles desgraçados sabiam desde o
começo que eu morreria aqui, e eu
caí direitinho na armadilha deles. {0007}


Mas agora é tarde. Estou perdendo
a razão. Tudo está ficando tão distante.
Jessica... Lisa... Me perdoem. {0007}


Por causa do meu orgulho, envolvi
vocês duas nessa maldita conspiração.
Me perdoem. Que Deus aceite a minha
morte em troca da segurança de vocês.

{0011}{012C}George Trevor """)

T[(1, 27)] = doc("""
{0000}


{0016}Há algo escrito à mão.
{0016}Não tem data. {0007}


Nada mudou.
Nunca pensei que esta sala que
projetei como experimento seria
tão útil. {0007}


Posso me esconder aqui em segurança
por um tempo, porque ninguém conhece
o segredo por trás deste quadro.
Nem mesmo o Sr. Spencer.

Quadro de uma mansão... No fundo da
sala de arte. """)

T[(1, 28)] = doc("""
{0000}



{0016}Testamento científico {0007}{000E}{0005}{01EA}{0009}{0002}{0025}{FFFF}


Há uma carta dentro.
A parte de cima da carta foi rasgada.
O resto da carta dá para ler. {0007}{0009}{0001}{0026}""")

T[(1, 29)] = doc("""
{0000}



{0016}Foto de família





{0007}{0007}



{0016}Há um diário deixado por alguém. {0007}{NOFIM}""")

T[(1, 30)] = doc("""

{0016}—Como EMPURRAR COISAS—

Quando houver um objeto que se mexe,
fique de frente para ele, na direção
em que quer empurrar, e incline o
Control Stick (ou o + Control Pad)
para a frente. {0007}
{0016}—SUBIR E DESCER—

Vá até um objeto da altura da cintura
do personagem e aperte o botão A.
(Também dá para subir em objetos que
se mexem.) Para DESCER de um objeto,
aperte o botão A parado na beirada. {0007}
{0016}—Como EQUIPAR ARMAS— 

Na TELA DE STATUS, escolha a “arma”
que quer usar e depois o comando
“EQUIPAR”. (Mesmo tendo uma arma,
você precisa EQUIPÁ-LA para poder
atacar.) {0007}
{0016}—POSIÇÃO DE ATAQUE—

Segure o botão R. (O personagem
fica em posição de ataque, mirando
o inimigo mais próximo.) {0007}
{0016}—Como ATACAR—

Segurando o botão R, aperte o botão A.
(Você ataca o inimigo com a arma
equipada.) {0007}
{0016}—GIRO DE 180 GRAUS— 

Segurando o Control Stick (ou o
+ Control Pad) para trás, aperte o
botão B. (Também dá para fazer isso
só com o C Stick.)  {000E}{0005}{01ED}{0009}{0002}{001F}{FFFF}{0007}{000C}{0014}{NOFIM}""")

T[(1, 37)] = doc("""




{0016}Há uma carta. {0007}3 de junho de 1998
Minha querida Alma,

Antes de tudo, me desculpe por não
ter conseguido ligar. Um homem de
óculos escuros não permitiu nenhuma
ligação. Desculpe, Alma. {0007}


Estou aqui tentando pensar por onde
começar, como explicar em poucas
palavras tudo o que aconteceu desde
a última vez que nos falamos, e já
estou falhando. {0007}


Espero que esta carta encontre você
bem, e que você perdoe os rodeios da
minha caneta; isto não é fácil. {0007}


Enquanto escrevo, sinto as ideias mais
simples escaparem, perdidas em meio
ao desespero e à confusão, mas preciso
dizer o que está no meu coração antes
de descansar. Alma, por favor, acredite
que o que digo é verdade. {0007}


A história inteira levaria horas para
contar, e o tempo é curto, então aceite
estes fatos: mês passado houve um
acidente no laboratório, e o vírus que
estudávamos vazou. {0007}


Todos os colegas infectados estão
mortos ou morrendo, e a doença é tal
que os que ainda vivem perderam a
razão. Este vírus rouba a humanidade
das vítimas e as força, na doença, a
buscar e destruir a vida. {0007}


Enquanto escrevo estas palavras, ouço
eles forçando a minha porta como
animais famintos e sem mente. {0007}{NOFIM}""")

T[(1, 38)] = doc("""



Alma, tentei sobreviver só para ver
você de novo. Mas meus esforços só
adiaram o inevitável; estou infectado,
e não há cura para o que vem a seguir,
a não ser acabar com a minha vida antes
de perder a única coisa que me separa
deles. {0007}


O meu amor por você. {0007}


Em uma hora terei entrado no sono
eterno, onde há paz. Por favor, entenda.
Saiba que eu sinto muito.

{0011}{012C}Martin Crackhorn """)

T[(1, 42)] = doc("""




{0016}É uma carta. {0007}
Para a minha Lisa,

Dia após dia sinto minha consciência
se afastando cada vez mais.
As injeções que os homens de branco
me deram fizeram parte da coceira da
mamãe passar. Hoje me deram outra,
dizendo que era “nutrição”. {0007}


Quando me dão as injeções, a mamãe
consegue pensar direito, mas fica
chocada e triste por não conseguir
pensar em você o tempo todo. {0007}


A mamãe tem medo. Medo de esquecer
tudo, principalmente as lembranças de
você e do papai… Como são os seus
rostos, como a gente vivia junto…
Tudo está começando a sumir num
lugar escuro da minha mente.

{0007}


Ah, Lisa, queria poder tocar o seu rosto
e te abraçar agora mesmo, para não
perder as lindas lembranças de você
e do papai. {0007}


Lisa, não podemos mais ficar aqui.
Temos que fugir! {0007}


Me escute, Lisa. Nossa chance de fugir
é a próxima vez que formos juntas
àquele laboratório. Vamos fingir que
estamos desacordadas e, quando o homem
de branco se distrair, essa vai ser a
nossa chance. {0007}


Quando estivermos lá fora, vamos
procurar o papai juntas. Tá, querida?
Seja forte, Lisa.

{0011}{012C}13 de nov. de 1967
{0011}{012C}Jessica Trevor
""")

T[(1, 43)] = doc("""

19

papaii prendi primero
mamã prendi segumdo

dEntro vermeLho e gosmeNto
bRanco e dUro

não mãe De verdade oNde {0007}
sei não papaii
achei mamãe di novo

quando prendi mamãe
ela num mexe mais
ela gritando

por quê?
Só quero ficá com ela {0007}

4

mamãe
onde?

sdade di vc""")
