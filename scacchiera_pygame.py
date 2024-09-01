import pygame
import sys
from pezzi import Pedone, Torre, Cavallo, Alfiere, Donna, Re

# Inizializzazione di Pygame
pygame.init()

# Definizione dei colori
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
GRIGIO = (200, 200, 200)


# Dimensioni della finestra e dei quadrati
DIM_QUADRATO = 60
MARGINE = 50  # Spazio extra per le coordinate
LARGHEZZA = DIM_QUADRATO * 8 + 2 * MARGINE
ALTEZZA = DIM_QUADRATO * 8 + MARGINE

# Caricamento e ridimensionamento delle immagini dei pezzi
white_pawn = pygame.image.load("pieces-basic-png/white_pawn.png")
white_pawn = pygame.transform.scale(white_pawn, (DIM_QUADRATO, DIM_QUADRATO))
black_pawn = pygame.image.load("pieces-basic-png/black_pawn.png")
black_pawn = pygame.transform.scale(black_pawn, (DIM_QUADRATO, DIM_QUADRATO))
white_rook = pygame.image.load("pieces-basic-png/white_rook.png")
white_rook = pygame.transform.scale(white_rook, (DIM_QUADRATO, DIM_QUADRATO))
black_rook = pygame.image.load("pieces-basic-png/black_rook.png")
black_rook = pygame.transform.scale(black_rook, (DIM_QUADRATO, DIM_QUADRATO))
white_knight = pygame.image.load("pieces-basic-png/white_knight.png")
white_knight = pygame.transform.scale(white_knight, (DIM_QUADRATO, DIM_QUADRATO))
black_knight = pygame.image.load("pieces-basic-png/black_knight.png")
black_knight = pygame.transform.scale(black_knight, (DIM_QUADRATO, DIM_QUADRATO))
white_bishop = pygame.image.load("pieces-basic-png/white_bishop.png")
white_bishop = pygame.transform.scale(white_bishop, (DIM_QUADRATO, DIM_QUADRATO))
black_bishop = pygame.image.load("pieces-basic-png/black_bishop.png")
black_bishop = pygame.transform.scale(black_bishop, (DIM_QUADRATO, DIM_QUADRATO))
white_queen = pygame.image.load("pieces-basic-png/white_queen.png")
white_queen = pygame.transform.scale(white_queen, (DIM_QUADRATO, DIM_QUADRATO))
black_queen = pygame.image.load("pieces-basic-png/black_queen.png")
black_queen = pygame.transform.scale(black_queen, (DIM_QUADRATO, DIM_QUADRATO))
white_king = pygame.image.load("pieces-basic-png/white_king.png")
white_king = pygame.transform.scale(white_king, (DIM_QUADRATO, DIM_QUADRATO))
black_king = pygame.image.load("pieces-basic-png/black_king.png")
black_king = pygame.transform.scale(black_king, (DIM_QUADRATO, DIM_QUADRATO))

# Creazione della finestra
screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Scacchiera con Coordinate")

# Inizializzazione della scacchiera
scacchiera = [[None] * 8 for _ in range(8)]

# Posizionamento iniziale dei pedoni bianchi e neri
for colonna in range(8):
    scacchiera[6][colonna] = Pedone('bianco')
    scacchiera[1][colonna] = Pedone('nero')

# Posizionamento delle torri bianche
scacchiera[7][0] = Torre('bianco')  # Torre bianca in a1
scacchiera[7][7] = Torre('bianco')  # Torre bianca in h1

# Posizionamento delle torri nere
scacchiera[0][0] = Torre('nero')  # Torre nera in a8
scacchiera[0][7] = Torre('nero')  # Torre nera in h8

# Posizionamento dei cavalli bianchi
scacchiera[7][1] = Cavallo('bianco')  # Cavallo bianco in b1
scacchiera[7][6] = Cavallo('bianco')  # Cavallo bianco in g1

# Posizionamento dei cavalli neri
scacchiera[0][1] = Cavallo('nero')  # Cavallo nero in b8
scacchiera[0][6] = Cavallo('nero')  # Cavallo nero in g8

# Posizionamento degli alfieri bianchi
scacchiera[7][2] = Alfiere('bianco')  # Alfiere bianco in c1
scacchiera[7][5] = Alfiere('bianco')  # Alfiere bianco in f1

# Posizionamento degli alfieri neri
scacchiera[0][2] = Alfiere('nero')  # Alfiere nero in c8
scacchiera[0][5] = Alfiere('nero')  # Alfiere nero in f8

# Posizionamento della donna bianca
scacchiera[7][3] = Donna('bianco')  # Donna bianca in d1

# Posizionamento della regina nera
scacchiera[0][3] = Donna('nero')  # Regina nera in d8

# Posizionamento del re bianco
scacchiera[7][4] = Re('bianco')  # Re bianco in e1

# Posizionamento del re nero
scacchiera[0][4] = Re('nero')  # Re nero in e8

ultima_mossa = None  # Variabile per tracciare l'ultima mossa effettuata
font = pygame.font.SysFont(None, 24)

def re_sotto_scacco(scacchiera, colore_re, ultima_mossa):
    """Controlla se il re di un determinato colore è sotto scacco."""
    # Trova la posizione del re
    posizione_re = None
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if isinstance(pezzo, Re) and pezzo.colore == colore_re:
                posizione_re = (riga, colonna)
                break
        if posizione_re:
            break

    # Controlla se qualche pezzo avversario può attaccare il re
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if pezzo and pezzo.colore != colore_re:
                if pezzo.movimento_valido(scacchiera, (riga, colonna), posizione_re, ultima_mossa):
                    return True
    return False

def disegna_scacchiera(screen, DIM_QUADRATO, MARGINE, BIANCO, GRIGIO, NERO, font):
    """Disegna una scacchiera con le coordinate algebriche."""
    screen.fill(NERO)

    # Disegna la scacchiera
    for riga in range(8):
        for colonna in range(8):
            colore = BIANCO if (riga + colonna) % 2 == 0 else GRIGIO
            pygame.draw.rect(screen, colore, 
                             (colonna * DIM_QUADRATO + MARGINE, riga * DIM_QUADRATO, DIM_QUADRATO, DIM_QUADRATO))

    # Disegna le coordinate algebriche
    for i in range(8):
        # Colonne (A-H)
        lettera = chr(ord('A') + i)
        text_surface = font.render(lettera, True, BIANCO)
        screen.blit(text_surface, (i * DIM_QUADRATO + MARGINE + DIM_QUADRATO // 2 - text_surface.get_width() // 2, 8 * DIM_QUADRATO + MARGINE // 2))

        # Righe (1-8)
        numero = str(8 - i)
        text_surface = font.render(numero, True, BIANCO)
        screen.blit(text_surface, (MARGINE // 2 - text_surface.get_width() // 2, i * DIM_QUADRATO + DIM_QUADRATO // 2 - text_surface.get_height() // 2))


def disegna_alone_scacco(screen, posizione_re, DIM_QUADRATO):
    """Disegna un alone rosso attorno al re se è sotto scacco."""
    riga, colonna = posizione_re
    x = colonna * DIM_QUADRATO
    y = riga * DIM_QUADRATO

    # Creare un'ellisse sfumata intorno al re
    surface = pygame.Surface((DIM_QUADRATO, DIM_QUADRATO), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (255, 0, 0, 128), surface.get_rect().inflate(20, 20))
    screen.blit(surface, (x - 10, y - 10))

def disegna_pezzi(screen, scacchiera, DIM_QUADRATO, MARGINE, escluso=None):
    """Disegna tutti i pezzi sulla scacchiera, escludendo quello selezionato."""
    global posizione_re_bianco, posizione_re_nero
    posizione_re_bianco = None
    posizione_re_nero = None

    for riga in range(8):
        for colonna in range(8):
            if (riga, colonna) != escluso:
                pezzo = scacchiera[riga][colonna]
                if isinstance(pezzo, Re):
                    if pezzo.colore == 'bianco':
                        posizione_re_bianco = (riga, colonna)
                    else:
                        posizione_re_nero = (riga, colonna)

    # Ridisegna i pezzi sopra le caselle
    for riga in range(8):
        for colonna in range(8):
            if (riga, colonna) != escluso:
                pezzo = scacchiera[riga][colonna]
                x = colonna * DIM_QUADRATO + MARGINE
                y = riga * DIM_QUADRATO

                if isinstance(pezzo, Pedone):
                    screen.blit(white_pawn if pezzo.colore == 'bianco' else black_pawn, (x, y))
                elif isinstance(pezzo, Torre):
                    screen.blit(white_rook if pezzo.colore == 'bianco' else black_rook, (x, y))
                elif isinstance(pezzo, Cavallo):
                    screen.blit(white_knight if pezzo.colore == 'bianco' else black_knight, (x, y))
                elif isinstance(pezzo, Alfiere):
                    screen.blit(white_bishop if pezzo.colore == 'bianco' else black_bishop, (x, y))
                elif isinstance(pezzo, Donna):
                    screen.blit(white_queen if pezzo.colore == 'bianco' else black_queen, (x, y))
                elif isinstance(pezzo, Re):
                    screen.blit(white_king if pezzo.colore == 'bianco' else black_king, (x, y))

def scegli_promozione_grafica(colore):
    """Permette al giocatore di scegliere un pezzo di promozione con un'interfaccia grafica."""
    # Definisci le immagini per i pezzi
    pezzi_promozione = {
        "Q": Donna(colore),
        "R": Torre(colore),
        "B": Alfiere(colore),
        "N": Cavallo(colore)
    }

    # Crea una finestra per la selezione
    selezione_fatta = False
    pezzo_scelto = None

    # Dimensioni e posizioni per i pezzi di promozione
    larghezza_finestra = 240
    altezza_finestra = 60
    x_offset = (LARGHEZZA - larghezza_finestra) // 2
    y_offset = (ALTEZZA - altezza_finestra) // 2

    promozione_finestra = pygame.Surface((larghezza_finestra, altezza_finestra))
    promozione_finestra.fill(GRIGIO)

    while not selezione_fatta:
        promozione_finestra.fill(GRIGIO)

        # Disegna i pezzi per la promozione
        for i, (scelta, pezzo) in enumerate(pezzi_promozione.items()):
            immagine_pezzo = None
            if scelta == "Q":
                immagine_pezzo = white_queen if colore == 'bianco' else black_queen
            elif scelta == "R":
                immagine_pezzo = white_rook if colore == 'bianco' else black_rook
            elif scelta == "B":
                immagine_pezzo = white_bishop if colore == 'bianco' else black_bishop
            elif scelta == "N":
                immagine_pezzo = white_knight if colore == 'bianco' else black_knight

            # Posiziona i pezzi in fila
            x_pos = i * 60
            promozione_finestra.blit(immagine_pezzo, (x_pos, 0))

        screen.blit(promozione_finestra, (x_offset, y_offset))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x_rel = x - x_offset
                y_rel = y - y_offset

                if 0 <= y_rel < altezza_finestra:
                    scelta_idx = x_rel // 60
                    if 0 <= scelta_idx < 4:
                        pezzo_scelto = list(pezzi_promozione.values())[scelta_idx]
                        selezione_fatta = True

    return pezzo_scelto


import random

def cambia_pezzi_casualmente(scacchiera, colore, ultimo_pezzo_pos):
    """Cambia casualmente le posizioni dei pezzi di un giocatore sulla scacchiera, escluso l'ultimo pezzo mosso e il Re."""
    posizioni_pezzi = []

    # Raccogli tutte le posizioni dei pezzi che possono essere cambiati
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if pezzo is not None and pezzo.colore == colore and not isinstance(pezzo, Re):
                # Escludi l'ultimo pezzo mosso e il Re
                if (riga, colonna) != ultimo_pezzo_pos:
                    posizioni_pezzi.append((riga, colonna))

    # Mescola le posizioni raccolte
    nuove_posizioni = posizioni_pezzi[:]
    random.shuffle(nuove_posizioni)

    # Assegna i pezzi alle nuove posizioni
    pezzi_da_cambiare = [scacchiera[riga][colonna] for riga, colonna in posizioni_pezzi]
    for i, (riga, colonna) in enumerate(nuove_posizioni):
        nuovo_pezzo = pezzi_da_cambiare[i]
        scacchiera[riga][colonna] = nuovo_pezzo

    return scacchiera

def esegui_mossa(inizio, fine):
    """Esegue il movimento se valido."""
    global ultima_mossa, re_bianco_pos, re_nero_pos
    global scacchiera
    inizio_riga, inizio_col = inizio
    fine_riga, fine_col = fine
    pezzo = scacchiera[inizio_riga][inizio_col]

    if pezzo and pezzo.movimento_valido(scacchiera, inizio, fine, ultima_mossa):
        # Gestione en passant: rimuove il pedone avversario
        if isinstance(pezzo, Pedone) and abs(fine_col - inizio_col) == 1 and scacchiera[fine_riga][fine_col] is None:
            # Determina la posizione del pedone avversario catturato en passant
            if pezzo.colore == 'bianco':
                scacchiera[fine_riga + 1][fine_col] = None  # Rimuove il pedone nero
            else:
                scacchiera[fine_riga - 1][fine_col] = None  # Rimuove il pedone bianco
            print(f"Pedone avversario catturato en passant da {inizio} a {fine}")

        # Simula la mossa
        pezzo_destinazione = scacchiera[fine_riga][fine_col]
        scacchiera[fine_riga][fine_col] = pezzo
        scacchiera[inizio_riga][inizio_col] = None

        # Verifica se lascia il re in scacco
        if re_sotto_scacco(scacchiera, pezzo.colore, ultima_mossa):
            # Annulla la mossa se lascia il re in scacco
            scacchiera[inizio_riga][inizio_col] = pezzo
            scacchiera[fine_riga][fine_col] = pezzo_destinazione
            print(f"Mossa non valida: lascia il re in scacco da {inizio} a {fine}")
            return False

        # Promozione del pedone
        if isinstance(pezzo, Pedone) and (fine_riga == 0 or fine_riga == 7):
            pezzo_promozione = scegli_promozione_grafica(pezzo.colore)  # Richiede la scelta grafica del pezzo di promozione
            scacchiera[fine_riga][fine_col] = pezzo_promozione
            print(f"Pedone promosso a {pezzo_promozione.__class__.__name__} in {fine_riga, fine_col}")

        # Aggiorna la scacchiera se la mossa è valida
        ultima_mossa = (inizio, fine)  # Aggiorna l'ultima mossa

        # Cambia casualmente le posizioni dei pezzi del giocatore, escluso l'ultimo pezzo mosso e il Re
        scacchiera = cambia_pezzi_casualmente(scacchiera, pezzo.colore, (fine_riga, fine_col))

        # Se il pezzo è un re, aggiorna la sua posizione
        if isinstance(pezzo, Re):
            if pezzo.colore == 'bianco':
                re_bianco_pos = (fine_riga, fine_col)
            else:
                re_nero_pos = (fine_riga, fine_col)

        print(f"Mossa eseguita: da {inizio} a {fine}")
        return True

    # Se la mossa non è valida
    print(f"Mossa non valida: da {inizio} a {fine}")
    return False

def scacco_matto(scacchiera, colore_re, ultima_mossa):
    """Controlla se il re di un determinato colore è in scacco matto."""
    # Se il re non è sotto scacco, non può essere scacco matto
    if not re_sotto_scacco(scacchiera, colore_re, ultima_mossa):
        return False
    
    # Verifica se esiste almeno una mossa legale che il giocatore può fare per evitare lo scacco matto
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if pezzo and pezzo.colore == colore_re:
                # Genera tutte le posizioni possibili per il pezzo
                for nuova_riga in range(8):
                    for nuova_colonna in range(8):
                        if pezzo.movimento_valido(scacchiera, (riga, colonna), (nuova_riga, nuova_colonna), ultima_mossa):
                            # Simula la mossa
                            pezzo_destinazione = scacchiera[nuova_riga][nuova_colonna]
                            scacchiera[nuova_riga][nuova_colonna] = pezzo
                            scacchiera[riga][colonna] = None

                            # Controlla se lascia il re in scacco
                            if not re_sotto_scacco(scacchiera, colore_re, ultima_mossa):
                                # Ripristina la posizione originale
                                scacchiera[riga][colonna] = pezzo
                                scacchiera[nuova_riga][nuova_colonna] = pezzo_destinazione
                                return False

                            # Ripristina la posizione originale
                            scacchiera[riga][colonna] = pezzo
                            scacchiera[nuova_riga][nuova_colonna] = pezzo_destinazione
    
    # Se nessuna mossa legale è disponibile, è scacco matto
    return True

# Loop principale
selezionato = None
dragging = False
posizione_iniziale = None
turno = 'bianco'  # Il bianco inizia per primo

# Loop principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            colonna = (x - MARGINE) // DIM_QUADRATO
            riga = y // DIM_QUADRATO

            if 0 <= riga < 8 and 0 <= colonna < 8:
                pezzo = scacchiera[riga][colonna]
                if pezzo and pezzo.colore == turno:
                    selezionato = pezzo
                    posizione_iniziale = (riga, colonna)
                    dragging = True

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            x, y = pygame.mouse.get_pos()
            colonna = (x - MARGINE) // DIM_QUADRATO
            riga = y // DIM_QUADRATO

            if 0 <= riga < 8 and 0 <= colonna < 8:
                if esegui_mossa(posizione_iniziale, (riga, colonna)):
                    # Cambia turno dopo una mossa valida
                    turno = 'nero' if turno == 'bianco' else 'bianco'
                    selezionato = None
                else:
                    scacchiera[posizione_iniziale[0]][posizione_iniziale[1]] = selezionato

            dragging = False






    if event.type == pygame.MOUSEMOTION and dragging:
            disegna_scacchiera(screen, DIM_QUADRATO, MARGINE, BIANCO, GRIGIO, NERO, font)
            disegna_pezzi(screen, scacchiera, DIM_QUADRATO, MARGINE, escluso=posizione_iniziale)
            x, y = pygame.mouse.get_pos()
            if isinstance(selezionato, Pedone):
                screen.blit(white_pawn if selezionato.colore == 'bianco' else black_pawn,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))
            elif isinstance(selezionato, Torre):
                screen.blit(white_rook if selezionato.colore == 'bianco' else black_rook,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))
            elif isinstance(selezionato, Cavallo):
                screen.blit(white_knight if selezionato.colore == 'bianco' else black_knight,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))
            elif isinstance(selezionato, Alfiere):
                screen.blit(white_bishop if selezionato.colore == 'bianco' else black_bishop,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))
            elif isinstance(selezionato, Donna):
                screen.blit(white_queen if selezionato.colore == 'bianco' else black_queen,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))
            elif isinstance(selezionato, Re):
                screen.blit(white_king if selezionato.colore == 'bianco' else black_king,
                            (x - DIM_QUADRATO // 2, y - DIM_QUADRATO // 2))

    if not dragging:
        disegna_scacchiera(screen, DIM_QUADRATO, MARGINE, BIANCO, GRIGIO, NERO, font)
        disegna_pezzi(screen, scacchiera, DIM_QUADRATO, MARGINE)

    pygame.display.flip()
