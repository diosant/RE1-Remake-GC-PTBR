@echo off
rem Gera a ISO FINAL traduzida de um disco: textos + imagens + legendas das cenas.
rem Uso: scripts\gerar_disco.bat 1   (ou 2). Resultado: build\discoN_ptbr.iso
rem Nao altera os originais. Pode rodar quantas vezes quiser.
cd /d "%~dp0.."
set N=%1
if "%N%"=="" set N=1
echo [1/5] Conferindo a traducao...
python -I scripts\conferir_traducao.py textos\en\disco%N% textos\ptbr\disco%N%
echo [2/5] Traduzindo as imagens (capas, telas, menus)...
if exist build\imagens_disco%N% rmdir /s /q build\imagens_disco%N%
mkdir build\imagens_disco%N%\subscr
mkdir build\imagens_disco%N%\etc
python -I scripts\capas.py extraido\disco%N%\files\subscr\subscr.dat build\imagens_disco%N%\subscr\subscr.dat || goto erro
python -I scripts\interface.py build\imagens_disco%N%\subscr\subscr.dat build\imagens_disco%N%\subscr\subscr.dat || goto erro
python -I scripts\questionario.py extraido\disco%N%\files\subscr\subsel.dat build\imagens_disco%N%\subscr\subsel.dat || goto erro
python -I scripts\titulo.py extraido\disco%N%\files\etc\title.dat build\imagens_disco%N%\etc\title.dat || goto erro
for %%L in (opcoes final selecao) do python -I scripts\textos_imagem.py extraido\disco%N%\files build\imagens_disco%N% scripts\imagens\%%L.py || goto erro
echo [3/5] Reinserindo os textos...
if exist build\alterados_disco%N% rmdir /s /q build\alterados_disco%N%
if exist build\alterados_disco%N%_sys rmdir /s /q build\alterados_disco%N%_sys
python -I scripts\inserir_textos.py extraido\disco%N%\files textos\ptbr\disco%N% build\alterados_disco%N% build\imagens_disco%N% || goto erro
echo [4/5] Colocando as legendas das cenas...
python -I pal\scripts\legendas_us.py %N% || goto erro
xcopy /e /y /q pal\build\us_legendas_disco%N%\* build\alterados_disco%N%\ >nul || goto erro
echo [5/5] Gerando a ISO...
python -I scripts\aplicar_na_iso.py build\disco%N%_base.iso build\alterados_disco%N% build\disco%N%_ptbr.iso || goto erro
echo.
echo Pronto: build\disco%N%_ptbr.iso
exit /b 0
:erro
echo.
echo Deu erro. Leia a mensagem acima.
exit /b 1
