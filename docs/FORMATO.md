# O formato dos textos do Resident Evil Remake (GameCube)

Anotações técnicas do que descobrimos ao traduzir o jogo. Não existiam ferramentas abertas para esses arquivos, então tudo abaixo foi descoberto analisando os discos e testando no Dolphin. Os números valem para a versão americana (GBIE08), a menos que esteja escrito PAL.

## Onde ficam os textos

| Arquivo | Conteúdo |
|---|---|
| `st1/` a `st5/rXXX.dat` | Mensagens de cada sala (`st5` é o laboratório, só no disco 2). |
| `subscr/subscr.dat` | Nomes e descrições dos itens, títulos e texto dos documentos, texturas da tela de status e capas dos documentos. |
| `etc/core.dat` | Mensagens comuns: portas trancadas, ervas, máquina de escrever, memory card, mapa. Também guarda a textura da fonte. |
| `subscr/subsel.dat` | Imagem do questionário de dificuldade. |
| `etc/title.dat` | Imagens do menu da tela de título. |
| `main.dol` (PAL) | Menu de idioma e legendas do vídeo de abertura. |

No disco 1 americano são 1167 mensagens em 93 arquivos.

## Caracteres

Cada caractere ocupa **2 bytes** (big-endian). O código é `0x80` + a posição da letra na textura da fonte (32 letras por linha). A tabela completa está em [`scripts/tabela.py`](../scripts/tabela.py). Alguns exemplos:

| Caractere | Código |
|---|---|
| espaço | `0x0080` |
| `0` | `0x0083` |
| `A` | `0x00A7` |
| `a` | `0x00C1` |

A fonte (textura em `etc/core.dat`, posição `0x24EC60`) **já tem todos os acentos do português**: á à â ã é ê í ó ô õ ú ç e as maiúsculas. Não foi preciso editar a fonte. Ela não tem `º`, por isso o mapa usa "Andar 1" em vez de "1º andar".

Códigos abaixo de `0x80` são códigos de controle.

## Blocos de mensagens

Os textos ficam em blocos com este formato (tudo big-endian):

```
u32  valor desconhecido (mantido como está)
u32  N = quantidade de mensagens
u32  deslocamento[N]   (relativo ao início do bloco; vários podem apontar para a mesma mensagem)
...  mensagens (sequências de u16)
```

Cada mensagem vai do seu deslocamento até o começo da próxima (em ordem de posição) e normalmente termina em `0x0001`. O `0x0001` também aparece no meio, como parâmetro dos comandos `0x0000`, `0x0009` e `0x000B`, então não dá para usar só ele como marca de fim.

Nos `.txt` de `textos/ptbr/`, cada mensagem aparece assim:

```
### bloco 0 (0x28960) mensagem 2
{0000}Há vários tipos de soro aqui.{0006}
Muitos deles têm uma cor{0005}{0007}doentia.
```

O número entre parênteses é a posição do bloco no arquivo original.

## Códigos de controle

Os significados foram deduzidos observando o jogo; os marcados com (?) ainda não foram confirmados.

| Código | Significado |
|---|---|
| `{0000}` | Início da mensagem. |
| `{0006}` | Quebra de linha (no `.txt` a linha também quebra logo depois). |
| `{0005}{0007}` | Espera o botão e abre uma nova caixa de texto. |
| `{0007}` | Nos documentos: nova página. |
| `{0003}{0002}...{0003}{0000}` | Muda a cor (nome de item destacado) e volta à cor normal. |
| `{000B}{0001}{00XX}` | Comando com parâmetro (aparece no começo das mensagens de porta) (?). |
| `{0011}{0046}` | Recuo/posição horizontal (?). |
| `{0016}` | Título (documentos e menus) (?). |
| `{0008}{00XX}` | Pausa/tempo, muito usado nas legendas do PAL (?). |
| `{FFFF}` | Fim de um comando especial (?). |
| `{NOFIM}` | Marcação dos scripts: a mensagem não tem código de fim. Não apagar. |

O script [`conferir_traducao.py`](../scripts/conferir_traducao.py) confere se cada mensagem traduzida tem os mesmos códigos, na mesma ordem, que a original (só `{0006}` e `{0005}{0007}` podem mudar de lugar) e se nenhuma linha ficou mais larga que a maior linha do original naquele bloco + 3 letras.

## Quando o texto em português é maior

### Salas e `core.dat`

Esses arquivos começam com 16 ponteiros (`u32`) em `0x00` e uma lista ordenada de inícios de seção em `0x40`, terminada em 0. Quando o texto não cabe, [`inserir_textos.py`](../scripts/inserir_textos.py) aumenta a seção de texto **no próprio lugar** (alinhada a `0x20`), empurra as seções seguintes para frente e corrige o cabeçalho e a lista. Mover o texto para o fim do arquivo fez o jogo travar.

### `subscr.dat` (itens e documentos)

O `subscr.dat` não tem cabeçalho próprio. Quem sabe onde fica cada parte dele é o **`main.dol`**: uma tabela de pares `(posição, tamanho)` entre `0x178AC0` e `0x178C38` (posição dentro do arquivo `main.dol`).

- Textos dos itens: fim da parte que começa em `0x806A0` (termina em `0x10C620`). Esse fim também está no código, em `0x700A0` do `main.dol` (`lis r3,0x11` / `addi r30,r3,-0x39E0`).
- Textos dos documentos: parte que começa em `0x1CCD00` (termina em `0x1DA540`).

Para aumentar um texto, [`espaco_subscr.py`](../scripts/espaco_subscr.py) aumenta a parte dele, empurra as seguintes e corrige a tabela e a constante no `main.dol`.

### Na ISO

[`aplicar_na_iso.py`](../scripts/aplicar_na_iso.py) lê a FST do disco (posição em `0x424`). Arquivos do mesmo tamanho são gravados por cima; arquivos que cresceram vão para o espaço livre no fim da ISO e a FST é corrigida. No PAL o disco está quase cheio, então [`aplicar_na_iso_pal.py`](../pal/scripts/aplicar_na_iso_pal.py) primeiro tenta manter o arquivo no lugar, usando a sobra antes do próximo arquivo.

## Versão PAL e legendas

A versão americana **não tem legendas** nas cenas. A europeia (GBIP08) tem cinco idiomas e legendas.

- Nas salas, cada seção de texto começa com uma tabela de 5 deslocamentos (`0x14` no primeiro `u32`), na ordem **inglês, alemão, francês, espanhol, italiano**. O português é gravado no bloco **espanhol** (4º). Algumas salas fazem o italiano apontar para o mesmo bloco.
- As legendas das cenas ficam em blocos separados nos mesmos arquivos (grupos de 4 ou 5 blocos com a mesma quantidade de mensagens; o inglês às vezes vem vazio). Cada fala é dividida em trechos separados por códigos de pausa/tempo. Nas traduções em [`pal/scripts/traducoes/`](../pal/scripts/traducoes/) os trechos são separados por `|`, e [`montar_pal.py`](../pal/scripts/montar_pal.py) encaixa o texto novo entre os códigos originais, sem mudar os tempos.
- `subscr.dat` no PAL: itens EN, documentos EN, itens DE FR ES IT, documentos DE FR ES IT.
- `main.dol`: bloco 3 = espanhol (legendas do vídeo de abertura e textos de sistema). O menu de idioma em inglês também foi alterado para mostrar `PORTUGUESE` no lugar de `SPANISH`.
- [`verificar_salas.py`](../pal/scripts/verificar_salas.py) confere, depois de inserir, que o bloco espanhol de cada sala tem exatamente o português e que o italiano continua válido.

## Textos em imagem

Alguns textos são desenhados em texturas **TPL** (formato de imagem do GameCube):

| Arquivo | Textura | O que é |
|---|---|---|
| `subscr/subscr.dat` | TPL em `0x0`, CMPR 1024×1024 | Botões e rótulos da tela de status |
| `subscr/subscr.dat` | CMPR 512×448 | Capas dos documentos (título na faixa das linhas 284–300) |
| `subscr/subsel.dat` | TPL em `0x0`, imagem 0, CMPR 512×448 | Questionário de dificuldade |
| `etc/title.dat` | TPL em `0x76700`, 9 imagens RGBA8 170×22 | Menu da tela de título |
| `subscr/subopt.dat` | TPL em `0x0` | Menu de opções (em andamento) |
| `etc/ending.dat` | — | Telas do final e extras (em andamento) |

- [`tpl.py`](../scripts/tpl.py) lê as texturas e salva como PNG, sem bibliotecas externas.
- [`cmpr.py`](../scripts/cmpr.py) recodifica CMPR (parecido com DXT1) só nos sub-blocos 4×4 que mudaram; o resto da imagem fica idêntico ao original.
- [`textos_imagem.py`](../scripts/textos_imagem.py) é a ferramenta geral: apaga o texto antigo de uma área e escreve o novo, a partir de listas em [`scripts/imagens/`](../scripts/imagens/).
- [`grade.py`](../scripts/grade.py) gera uma imagem ampliada com grade de coordenadas para achar a posição dos textos.

## Ferramentas de investigação

- [`busca_relativa.py`](../scripts/busca_relativa.py): acha uma palavra mesmo sem conhecer a codificação, comparando a diferença entre letras vizinhas (foi assim que a tabela de caracteres foi descoberta).
- [`mapear_textos.py`](../scripts/mapear_textos.py): procura em todos os arquivos trechos que parecem texto.
