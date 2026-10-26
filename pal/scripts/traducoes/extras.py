"""Textos que so existem (ou mudaram) no disco PAL: ingles do PAL -> portugues.
Usado por montar_pal.py junto com a traducao do disco US."""
D = {}

for s in 'AB':
    D["{0000}{0002}{0000}Memory Card in the Slot %s{0006}contains corrupted data and{0006}needs to be formatted.{0005}{0007}Do you want to format?{0008}{0001}{0006}{0004}Format{0006}{0004}Retry{0006}{0004}Continue Without Saving{0005}" % s] = \
        "{0000}{0002}{0000}O Memory Card da entrada %s{0006}tem dados corrompidos e{0006}precisa ser formatado.{0005}{0007}Deseja formatar?{0008}{0001}{0006}{0004}Formatar{0006}{0004}Tentar de novo{0006}{0004}Continuar sem salvar{0005}" % s
    D["{0000}{0002}{0000}Another device in the Slot %s.{0006}Please insert Memory Card.{0005}" % s] = \
        "{0000}{0002}{0000}Há outro aparelho na entrada %s.{0006}Insira um Memory Card.{0005}" % s

for n in '12':
    D["{0000}{0002}{0000}Please insert the Resident Evil™{0006}Game Disc %s. {0006}{0006}" % n] = \
        "{0000}{0002}{0000}Insira o disco %s de{0006}Resident Evil™. {0006}{0006}" % n
    D["{0000}{0002}{0000}This disc is not the Resident{0006}Evil™{0006}Game Disc %s.{0006}Please insert the Resident{0006}Evil™ Game Disc %s. " % (n, n)] = \
        "{0000}{0002}{0000}Este não é o disco %s de{0006}Resident Evil™.{0006}Insira o disco %s de{0006}Resident Evil™. " % (n, n)

for hz in ('60', '50'):
    D["{0000}{0002}{0000}Screen display has been set to {0006}%sHz mode. " % hz] = \
        "{0000}{0002}{0000}A imagem foi ajustada para o {0006}modo %sHz. " % hz

D.update({
    "{0000}“Use these to protect yourself{0006}{0011}{0046}from that bullet-proof{0005}{0007}monster in chains. I also fixed{0006}the doorknob to make sure you{0005}{0007}can get away.”                       {0006}       -Wesker-":
        "{0000}“Use isto para se proteger{0006}{0011}{0046}daquele monstro acorrentado{0005}{0007}à prova de balas. Também{0006}consertei a maçaneta para que{0005}{0007}você possa fugir.”                     {0006}       -Wesker-",
    "{0000}{0002}{0000}{0016}Memory Card": "{0000}{0002}{0000}{0016}Memory Card",
    "{0000}{0002}{0000}An error has occurred.{0006}Turn the power off and refer{0006}to the Nintendo GameCube™{0006}Instruction Booklet for{0006}more information.":
        "{0000}{0002}{0000}Ocorreu um erro.{0006}Desligue o console e consulte{0006}o manual de instruções do{0006}Nintendo GameCube™ para{0006}mais informações.",
    "{0000}{0002}{0000}The Disc Cover is open.{0006}If you want to continue the{0006}game, please close{0006}the Disc Cover. {0006}{0006}{0006}":
        "{0000}{0002}{0000}A tampa do disco está aberta.{0006}Para continuar o jogo,{0006}feche a tampa{0006}do disco. {0006}{0006}{0006}",
    "{0000}It's an old typewriter.{0005}{0007}You cannot save your progress{0006}in this version. ":
        "{0000}É uma máquina de escrever antiga.{0005}{0007}Não dá para salvar o progresso{0006}nesta versão. ",
    "{0000}{0002}{0000}{0011}{0064}Would you like to display{0006}{0011}{0064}in 60Hz mode?{0006}{0011}{0180}{0004}Yes {0004}No{0005}":
        "{0000}{0002}{0000}{0011}{0064}Deseja usar a imagem{0006}{0011}{0064}no modo 60Hz?{0006}{0011}{0180}{0004}Sim {0004}Não{0005}",
    "{0000}{0002}{0000}{0016}Select Language{0006}{0006}{0011}Â{0004}ENGLISH{0006}{0011}Â{0004}GERMAN{0006}{0011}Â{0004}FRENCH{0006}{0011}Â{0004}SPANISH{0006}{0011}Â{0004}ITALIAN{0005}":
        "{0000}{0002}{0000}{0016}Escolha o idioma{0006}{0006}{0011}Â{0004}INGLÊS{0006}{0011}Â{0004}ALEMÃO{0006}{0011}Â{0004}FRANCÊS{0006}{0011}Â{0004}PORTUGUÊS{0006}{0011}Â{0004}ITALIANO{0005}",
    "{0000}{0002}{0000}Previously saved data will{0006}be lost. Would you like to{0006}continue formatting?{0006}{0012}":
        "{0000}{0002}{0000}Os dados salvos antes serão{0006}perdidos. Deseja continuar{0006}a formatação?{0006}{0012}",
})

# Menu de idioma em ingles: troca SPANISH por PORTUGUESE (bloco ingles do main.dol)
MENU_INGLES = ("{0000}{0002}{0000}{0016}Select Language{0006}{0006}{0011}Â{0004}ENGLISH{0006}{0011}Â{0004}GERMAN{0006}{0011}Â{0004}FRENCH{0006}{0011}Â{0004}SPANISH{0006}{0011}Â{0004}ITALIAN{0005}",
               "{0000}{0002}{0000}{0016}Select Language{0006}{0006}{0011}Â{0004}ENGLISH{0006}{0011}Â{0004}GERMAN{0006}{0011}Â{0004}FRENCH{0006}{0011}Â{0004}PORTUGUESE{0006}{0011}Â{0004}ITALIAN{0005}")
