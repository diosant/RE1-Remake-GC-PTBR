# Como extrair os textos (disco 1)

1. Extrair o disco (só lê o .rvz original):
   ```
   ferramentas\Dolphin-x64\DolphinTool.exe extract -i "originais\Resident Evil (USA) (Disc 1).rvz" -o extraido\disco1 -q
   ```
2. Extrair os textos para .txt:
   ```
   python -I scripts\extrair_textos.py extraido\disco1\files textos\en\disco1
   ```

## Como colocar a tradução de volta (gerar ISO de teste)

1. Converter o disco original para ISO (uma vez só; não altera o .rvz):
   ```
   ferramentas\Dolphin-x64\DolphinTool.exe convert -i "originais\Resident Evil (USA) (Disc 1).rvz" -o build\disco1_base.iso -f iso
   ```
2. Traduzir os .txt em `textos\ptbr\disco1` (copiados de `textos\en\disco1`).
3. Reinserir (grava só os arquivos que mudaram em `build\alterados_disco1`):
   ```
   python -I scripts\inserir_textos.py extraido\disco1\files textos\ptbr\disco1 build\alterados_disco1
   ```
4. Gerar a ISO traduzida (a ISO base não é alterada):
   ```
   python -I scripts\aplicar_na_iso.py build\disco1_base.iso build\alterados_disco1 build\disco1_teste_ptbr.iso
   ```

Espaço: nas salas (`stN/rXXX.dat`) e no `core.dat`, se o texto não couber, o script aumenta a seção de texto
e empurra o resto do arquivo (testado no jogo). Arquivos que crescem vão para o espaço livre no fim da ISO.
No `subscr.dat` (itens) o texto ainda precisa caber no espaço original. Caracteres fora da tabela dão erro.

## O que descobrimos sobre o formato

- Cada caractere ocupa 2 bytes (big-endian). A tabela está em `scripts/tabela.py`
  (ex.: `A` = 0x00A7, `a` = 0x00C1, espaço = 0x0080, `0` = 0x0083).
- A fonte (textura em `etc/core.dat`, posição 0x24EC60) já tem todos os acentos do português:
  á à â ã é ê í ó ô õ ú ç (e maiúsculas). Imagem em `fontes/analise/core_0_1024x1024.png`.
- Os textos ficam em blocos: `u32 ?` + `u32 quantidade` + lista de deslocamentos `u32`.
- Onde estão: `st1..st4/rXXX.dat` (mensagens de cada sala), `subscr/subscr.dat`
  (nomes e descrições de itens, títulos de documentos), `etc/core.dat` (sistema, mapa, memory card).
- 1167 mensagens em 93 arquivos no disco 1.

## Códigos de controle (não apagar nem mudar!)

| Código | Significado (provável) |
|---|---|
| `{0006}` | quebra de linha (o .txt também pula linha logo depois) |
| `{0005}{0007}` | espera o botão e abre uma nova caixa |
| `{0000}` | início da mensagem |
| `{0003}{0002}...{0003}{0000}` | cor / nome de item inserido |
| `{FFFF}` | fim de comando especial |
| `{NOFIM}` | marcação do script: a mensagem não tem código de fim (não apagar) |

## Ainda não confirmado

- Legendas das cenas: nada encontrado em `event/`. Provavelmente a versão americana
  não tem legendas nas cenas (a confirmar no jogo).
- O conteúdo dos documentos (diários, cartas) não aparece como texto; deve ser imagem.
