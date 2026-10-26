# Resident Evil Remake (GameCube) em Português do Brasil

Tradução de fã dos **textos** e das **legendas** de *Resident Evil* (Remake de 2002, GameCube) para o português do Brasil, feita para jogar no **Wii U pelo Nintendont** (e também no Dolphin ou num Wii).

> Projeto de fã, sem fins lucrativos e sem ligação com a Capcom. Este repositório **não contém o jogo** nem arquivos dele: só os scripts, os textos traduzidos e a documentação. Para jogar, você precisa da sua própria cópia do jogo.

## O que está traduzido

Tudo o que tem texto no jogo:

- mensagens das salas, itens, documentos e textos de sistema (memory card, máquina de escrever, mapa);
- **legendas de todas as cenas**, inclusive do vídeo de abertura;
- telas em imagem: menu do título, questionário de dificuldade, seleção de personagem, tela de status, capas dos documentos, menu de opções e telas do final e dos extras.

A tradução foi jogada do começo ao fim no **Wii U pelo Nintendont**.

Os nomes dos locais na tela de save ficam em inglês de propósito, para não quebrar essa tela.

## Qual versão usar

- **Americana (NTSC-U, GBIE08)**: a recomendada. O disco americano já tem o sistema de legendas (com as falas vazias); a tradução preenche essas falas, então o jogo fica com **textos e legendas em português**.
- **Europeia (PAL, GBIP08)**: também traduzida, com textos e legendas. O português entra no lugar do **espanhol**: no menu de idioma do jogo, escolha **PORTUGUESE** (é a opção que antes era o espanhol).

## Como aplicar o patch

> Os patches (`.xdelta`) são publicados na aba **[Releases](../../releases)**. Se ainda não houver nenhum lá, eles ainda não foram publicados.

1. Tenha o jogo original (os dois discos) da versão que você escolheu. Se ele estiver em `.rvz`, `.gcz` ou `.nkit`, converta para `.iso` no Dolphin: clique com o botão direito no jogo → **Converter arquivo...** → formato **ISO**.
2. Baixe o patch de cada disco na página de Releases.
3. Aplique o patch com o **[Delta Patcher](https://github.com/marco-calautti/DeltaPatcher)** (Windows, com janela) ou com o `xdelta3` na linha de comando:
   ```
   xdelta3 -d -s "Resident Evil (Disc 1).iso" disco1_ptbr.xdelta "Resident Evil (Disc 1) PT-BR.iso"
   ```
   O patch só funciona com a ISO exatamente igual à usada para criá-lo (o Release vai informar o CRC32/SHA-1 esperado).

## Como jogar no Wii U (Nintendont)

1. No cartão SD, crie uma pasta para o jogo dentro de `games`, com o ID do disco entre colchetes:
   - Americana: `sd:/games/Resident Evil [GBIE08]/`
   - Europeia: `sd:/games/Resident Evil [GBIP08]/`
2. Coloque o disco 1 com o nome `game.iso` e o disco 2 com o nome `disc2.iso` nessa pasta.
3. Abra o Nintendont pelo Homebrew Launcher (modo vWii) e escolha o jogo. A troca de disco é automática quando o jogo pedir o disco 2.

No **Dolphin**, abra a ISO por **Arquivo → Abrir**. Use só uma janela do Dolphin por vez, senão o save no memory card pode falhar.

## Para quem quer mexer na tradução

Tudo aqui foi feito com scripts próprios em Python.

- [`docs/COMO_GERAR.md`](docs/COMO_GERAR.md): passo a passo para extrair os discos, editar os textos e gerar as ISOs traduzidas.
- [`docs/FORMATO.md`](docs/FORMATO.md): o que descobrimos sobre os arquivos do jogo (tabela de caracteres, blocos de texto, códigos de controle, tabela do `subscr.dat` no `main.dol`, legendas do PAL, texturas).
- [`textos/glossario.md`](textos/glossario.md): glossário de termos usados na tradução.

### Estrutura do repositório

```
scripts/              scripts do disco americano (extrair, inserir, gerar ISO, imagens)
scripts/traducoes/    traduções de partes maiores (documentos, itens, core.dat, laboratório)
scripts/imagens/      listas de textos de imagem a trocar (menu de opções, final)
textos/ptbr/          textos traduzidos, um .txt por arquivo do jogo (disco 1 e 2)
pal/scripts/          scripts da versão europeia (PAL) e as legendas traduzidas
gerar_disco1.bat      gera a ISO americana final do disco 1: textos, imagens e legendas (Windows)
gerar_disco2.bat      idem, disco 2
pal/gerar_pal.bat     gera as duas ISOs PAL traduzidas
scripts/imagens_wiiu.py, som_wiiu.py   imagens e som de abertura para instalar o jogo no menu do Wii U (UWUVCI)
```

Encontrou um erro de tradução, texto cortado ou letra estranha? Abra uma [issue](../../issues) dizendo o disco, a versão (US ou PAL), o lugar no jogo e, se puder, uma captura de tela.

## Créditos

- Tradução, scripts e testes no Wii U: **Mah** ([@diosant](https://github.com/diosant)), com a ajuda do Claude (Anthropic).
- *Resident Evil* é marca registrada da Capcom. Todos os direitos do jogo pertencem à Capcom.
