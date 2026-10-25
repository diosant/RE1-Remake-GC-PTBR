@echo off
rem Gera a ISO traduzida do disco 1 (build\disco1_ptbr.iso) a partir de textos\ptbr\disco1.
rem Nao altera os originais. Pode rodar quantas vezes quiser.
cd /d "%~dp0"
set N=1
echo [1/4] Conferindo a traducao...
python -I scripts\conferir_traducao.py textos\en\disco%N% textos\ptbr\disco%N%
echo [2/4] Traduzindo as imagens (capas dos documentos)...
if not exist build\imagens_disco%N%\subscr mkdir build\imagens_disco%N%\subscr
python -I scripts\capas.py extraido\disco%N%\files\subscr\subscr.dat build\imagens_disco%N%\subscr\subscr.dat || goto erro
python -I scripts\interface.py build\imagens_disco%N%\subscr\subscr.dat build\imagens_disco%N%\subscr\subscr.dat || goto erro
python -I scripts\questionario.py extraido\disco%N%\files\subscr\subsel.dat build\imagens_disco%N%\subscr\subsel.dat || goto erro
if not exist build\imagens_disco%N%\etc mkdir build\imagens_disco%N%\etc
python -I scripts\titulo.py extraido\disco%N%\files\etc\title.dat build\imagens_disco%N%\etc\title.dat || goto erro
echo [3/4] Reinserindo os textos...
if exist build\alterados_disco%N% rmdir /s /q build\alterados_disco%N%
if exist build\alterados_disco%N%_sys rmdir /s /q build\alterados_disco%N%_sys
python -I scripts\inserir_textos.py extraido\disco%N%\files textos\ptbr\disco%N% build\alterados_disco%N% build\imagens_disco%N% || goto erro
echo [4/4] Gerando a ISO...
python -I scripts\aplicar_na_iso.py build\disco%N%_base.iso build\alterados_disco%N% build\disco%N%_ptbr.iso || goto erro
echo.
echo Pronto: build\disco%N%_ptbr.iso
pause
exit /b 0
:erro
echo.
echo Deu erro. Leia a mensagem acima.
pause
exit /b 1
