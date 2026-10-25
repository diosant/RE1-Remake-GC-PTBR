@echo off
rem Gera as ISOs PAL traduzidas (portugues no lugar do espanhol, com legendas nas cenas):
rem   pal\build\disco1_pal_ptbr.iso e pal\build\disco2_pal_ptbr.iso
rem Nao altera os originais. Pode rodar quantas vezes quiser.
rem Traducoes: pal\scripts\traducoes (legendas) + traducao do disco US (textos\ptbr).
cd /d "%~dp0.."
for %%N in (1 2) do (
  echo === Disco %%N ===
  echo [1/4] Montando os textos em portugues...
  python -I pal\scripts\montar_pal.py %%N || goto erro
  echo [2/4] Reinserindo os textos...
  if exist pal\build\alterados_disco%%N rmdir /s /q pal\build\alterados_disco%%N
  if exist pal\build\alterados_disco%%N_sys rmdir /s /q pal\build\alterados_disco%%N_sys
  python -I pal\scripts\pal_texto.py inserir pal\extraido\disco%%N\files pal\textos\ptbr\disco%%N pal\build\alterados_disco%%N || goto erro
  python -I pal\scripts\pal_texto.py inserir pal\extraido\disco%%N\sys pal\textos\ptbr\disco%%N_sys pal\build\alterados_disco%%N_sys || goto erro
  echo [3/4] Conferindo as salas...
  python -I pal\scripts\verificar_salas.py pal\build\alterados_disco%%N pal\textos\ptbr\disco%%N || goto erro
  echo [4/4] Gerando a ISO...
  python -I pal\scripts\aplicar_na_iso_pal.py pal\build\disco%%N_pal_base.iso pal\build\alterados_disco%%N pal\build\disco%%N_pal_ptbr.iso || goto erro
)
echo.
echo Pronto: pal\build\disco1_pal_ptbr.iso e pal\build\disco2_pal_ptbr.iso
pause
exit /b 0
:erro
echo.
echo Deu erro. Leia a mensagem acima.
pause
exit /b 1
