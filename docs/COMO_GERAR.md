# Como gerar as ISOs traduzidas

Este guia é para quem quer refazer a tradução a partir do código (por exemplo, para corrigir um texto). Para só jogar, use os patches da página de Releases (veja o [README](../README.md)).

Os comandos abaixo são para Windows, rodando na pasta raiz do repositório. Nada aqui altera os discos originais: tudo é gravado em cópias, dentro de `build/`.

## O que você precisa

- Python 3 com o [Pillow](https://pypi.org/project/pillow/) (`pip install pillow`), usado pelos scripts de imagem.
- [Dolphin](https://dolphin-emu.org/) (o `DolphinTool.exe` que vem com ele extrai e converte os discos). Nos exemplos ele está em `ferramentas\Dolphin-x64\`.
- As fontes do Windows usadas nas imagens: Courier New, Garamond, Georgia e Times New Roman, em `C:\Windows\Fonts`.
- Os seus próprios discos do jogo, em `originais\` (americano) e `originais (PAL)\` (europeu). Essas pastas estão no `.gitignore` e nunca vão para o GitHub.

## Versão americana (NTSC-U, GBIE08)

### 1. Extrair os discos (uma vez só)

```
ferramentas\Dolphin-x64\DolphinTool.exe extract -i "originais\Resident Evil (USA) (Disc 1).rvz" -o extraido\disco1 -q
ferramentas\Dolphin-x64\DolphinTool.exe convert -i "originais\Resident Evil (USA) (Disc 1).rvz" -o build\disco1_base.iso -f iso
```

Repita com o disco 2 (`extraido\disco2`, `build\disco2_base.iso`).

### 2. Extrair os textos originais em inglês (uma vez só)

```
python -I scripts\extrair_textos.py extraido\disco1\files textos\en\disco1
python -I scripts\extrair_textos.py extraido\disco2\files textos\en\disco2
```

A pasta `textos\en` não vai para o GitHub (é o texto da Capcom), mas é usada pelo conferidor e pelo PAL como referência.

### 3. Editar a tradução

Os textos traduzidos estão em `textos\ptbr\discoN\`, um `.txt` por arquivo do jogo. Edite só o texto entre os cabeçalhos `### bloco ... mensagem ...` e mantenha todos os códigos entre chaves (`{0006}`, `{0005}{0007}` etc.). Veja o que cada código faz em [FORMATO.md](FORMATO.md).

Partes maiores (documentos, itens, `core.dat`, laboratório) foram escritas como dicionários Python em `scripts\traducoes\` e aplicadas com:

```
python -I scripts\aplicar_traducao.py scripts\traducoes\docs_disco1.py textos\en\disco1\subscr\subscr.dat.txt textos\ptbr\disco1\subscr\subscr.dat.txt
```

Para levar ao disco 2 o que já foi traduzido no disco 1 (os textos se repetem quase todos):

```
python -I scripts\reaproveitar_traducao.py textos\en\disco1 textos\ptbr\disco1 textos\en\disco2 textos\ptbr\disco2
```

### 4. Gerar a ISO

Dê dois cliques em `gerar_disco1.bat` (ou `gerar_disco2.bat`). Ele:

1. confere a tradução (`conferir_traducao.py`: mesmos códigos de controle e linhas que cabem na caixa);
2. traduz as imagens (capas dos documentos, tela de status, questionário de dificuldade, menu do título);
3. reinsere os textos (`inserir_textos.py`), gravando só os arquivos que mudaram em `build\alterados_discoN`;
4. grava esses arquivos numa cópia da ISO base (`aplicar_na_iso.py`) → `build\discoN_ptbr.iso`.

## Versão europeia (PAL, GBIP08)

A versão PAL tem cinco idiomas (inglês, alemão, francês, espanhol, italiano) e legendas nas cenas. O português entra no lugar do espanhol. Os textos normais vêm da tradução americana; as legendas das cenas estão em `pal\scripts\traducoes\legendas_discoN.py`.

### 1. Extrair os discos e os textos (uma vez só)

```
ferramentas\Dolphin-x64\DolphinTool.exe extract -i "originais (PAL)\Resident Evil (Europe) (Disc 1).rvz" -o pal\extraido\disco1 -q
ferramentas\Dolphin-x64\DolphinTool.exe convert -i "originais (PAL)\Resident Evil (Europe) (Disc 1).rvz" -o pal\build\disco1_pal_base.iso -f iso
python -I pal\scripts\pal_texto.py extrair pal\extraido\disco1\files pal\textos\en_pal2\disco1
python -I pal\scripts\pal_texto.py extrair pal\extraido\disco1\sys pal\textos\en_pal2\disco1_sys
```

Repita com o disco 2. A tradução americana (`textos\en` e `textos\ptbr`) também precisa estar pronta, porque o PAL usa os dois como dicionário inglês → português.

### 2. Gerar as ISOs

Dê dois cliques em `pal\gerar_pal.bat`. Para cada disco ele:

1. monta os textos em português (`montar_pal.py`) em `pal\textos\ptbr\` e lista o que ficou sem tradução;
2. reinsere os textos (`pal_texto.py inserir`), inclusive no `main.dol` (legendas do vídeo de abertura e menu de idioma);
3. confere as salas (`verificar_salas.py`): o bloco espanhol precisa ter exatamente o português, e o italiano precisa continuar válido;
4. grava os arquivos numa cópia da ISO base (`aplicar_na_iso_pal.py`) → `pal\build\discoN_pal_ptbr.iso`.

## Criar os patches xdelta

Com a ISO original e a traduzida:

```
xdelta3 -e -9 -S djw -s build\disco1_base.iso build\disco1_ptbr.iso disco1_ptbr.xdelta
```

Os patches são publicados na página de Releases, nunca no repositório.
