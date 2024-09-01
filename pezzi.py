class Pedone:
    def __init__(self, colore):
        self.colore = colore
        self.mossa_doppia = False  # Per tracciare se il pedone ha fatto una mossa doppia

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine
        direzione = -1 if self.colore == 'bianco' else 1

        # Movimento standard del pedone (avanza di una casella)
        if fine_col == inizio_col and fine_riga == inizio_riga + direzione and scacchiera[fine_riga][fine_col] is None:
            self.mossa_doppia = False
            return True

        # Movimento doppio del pedone (solo dalla posizione iniziale)
        if fine_col == inizio_col and fine_riga == inizio_riga + 2 * direzione and scacchiera[fine_riga][fine_col] is None and scacchiera[inizio_riga + direzione][fine_col] is None and (inizio_riga == 6 or inizio_riga == 1):
            self.mossa_doppia = True
            return True

        # Cattura standard
        if abs(fine_col - inizio_col) == 1 and fine_riga == inizio_riga + direzione:
            if scacchiera[fine_riga][fine_col] is not None and scacchiera[fine_riga][fine_col].colore != self.colore:
                self.mossa_doppia = False
                return True

        # Cattura en passant
        if abs(fine_col - inizio_col) == 1 and fine_riga == inizio_riga + direzione:
            pedone_avversario = scacchiera[inizio_riga][fine_col]
            if isinstance(pedone_avversario, Pedone) and pedone_avversario.colore != self.colore and pedone_avversario.mossa_doppia:
                # Verifica se l'ultima mossa corrisponde al pedone avversario che ha fatto una mossa doppia
                if ultima_mossa == ((inizio_riga + 2 * direzione, fine_col), (inizio_riga, fine_col)):
                    print(f"En passant eseguito da {inizio} a {fine}")
                    self.mossa_doppia = False
                    return True

        return False

class Cavallo:
    def __init__(self, colore):
        self.colore = colore

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa=None):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine

        # Il cavallo si muove a "L": due caselle in una direzione e una nell'altra
        movimento_valido = (
            (abs(fine_riga - inizio_riga) == 2 and abs(fine_col - inizio_col) == 1) or
            (abs(fine_riga - inizio_riga) == 1 and abs(fine_col - inizio_col) == 2)
        )

        if movimento_valido:
            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            # Il cavallo può muoversi se la destinazione è vuota o occupata da un pezzo avversario
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                return True

        return False

class Torre:
    def __init__(self, colore):
        self.colore = colore
        self.mossa_effettuata = False

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa=None):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine

        # Verifica movimento in linea retta
        if inizio_riga == fine_riga or inizio_col == fine_col:
            passo_riga = 0 if inizio_riga == fine_riga else (1 if fine_riga > inizio_riga else -1)
            passo_col = 0 if inizio_col == fine_col else (1 if fine_col > inizio_col else -1)
            
            riga_corrente = inizio_riga + passo_riga
            col_corrente = inizio_col + passo_col

            while (riga_corrente != fine_riga or col_corrente != fine_col):
                if scacchiera[riga_corrente][col_corrente] is not None:
                    return False
                riga_corrente += passo_riga
                col_corrente += passo_col

            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                self.mossa_effettuata = True  # Aggiorna l'attributo se la torre viene mossa
                return True
        return False

class Alfiere:
    def __init__(self, colore):
        self.colore = colore

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa=None):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine

        # L'alfiere si muove solo in diagonale
        if abs(fine_riga - inizio_riga) == abs(fine_col - inizio_col):
            passo_riga = (fine_riga - inizio_riga) // max(1, abs(fine_riga - inizio_riga))
            passo_col = (fine_col - inizio_col) // max(1, abs(fine_col - inizio_col))
            riga_corrente = inizio_riga + passo_riga
            col_corrente = inizio_col + passo_col

            # Controllare che non ci siano pezzi lungo il percorso
            while (riga_corrente != fine_riga) and (col_corrente != fine_col):
                if scacchiera[riga_corrente][col_corrente] is not None:
                    return False
                riga_corrente += passo_riga
                col_corrente += passo_col

            # Controllare che la destinazione non sia occupata da un pezzo dello stesso colore
            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                return True

        return False
class Donna:
    def __init__(self, colore):
        self.colore = colore

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa=None):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine

        # Movimento in linea retta (come una torre)
        if inizio_riga == fine_riga or inizio_col == fine_col:
            passo_riga = (fine_riga - inizio_riga) // max(1, abs(fine_riga - inizio_riga))
            passo_col = (fine_col - inizio_col) // max(1, abs(fine_col - inizio_col))
            riga_corrente = inizio_riga + passo_riga
            col_corrente = inizio_col + passo_col

            while (riga_corrente != fine_riga or col_corrente != fine_col):
                if scacchiera[riga_corrente][col_corrente] is not None:
                    return False
                riga_corrente += passo_riga
                col_corrente += passo_col

            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                return True

        # Movimento in diagonale (come un alfiere)
        if abs(fine_riga - inizio_riga) == abs(fine_col - inizio_col):
            passo_riga = (fine_riga - inizio_riga) // max(1, abs(fine_riga - inizio_riga))
            passo_col = (fine_col - inizio_col) // max(1, abs(fine_col - inizio_col))
            riga_corrente = inizio_riga + passo_riga
            col_corrente = inizio_col + passo_col

            while (riga_corrente != fine_riga) and (col_corrente != fine_col):
                if scacchiera[riga_corrente][col_corrente] is not None:
                    return False
                riga_corrente += passo_riga
                col_corrente += passo_col

            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                return True

        return False

# Definizione della funzione re_sotto_scacco
def re_sotto_scacco(scacchiera, colore_re, ultima_mossa):
    """Controlla se il re di un determinato colore è sotto scacco."""
    posizione_re = None

    # Trova la posizione del re
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if isinstance(pezzo, Re) and pezzo.colore == colore_re:
                posizione_re = (riga, colonna)
                break
        if posizione_re:
            break

    # Verifica che la posizione del re sia stata trovata
    if posizione_re is None:
        raise ValueError(f"Non è stata trovata la posizione del re {colore_re} sulla scacchiera.")

    # Controlla se qualche pezzo avversario può attaccare il re
    for riga in range(8):
        for colonna in range(8):
            pezzo = scacchiera[riga][colonna]
            if pezzo and pezzo.colore != colore_re:
                if pezzo.movimento_valido(scacchiera, (riga, colonna), posizione_re, ultima_mossa):
                    return True
    return False

class Re:
    def __init__(self, colore):
        self.colore = colore
        self.mossa_effettuata = False

    def movimento_valido(self, scacchiera, inizio, fine, ultima_mossa=None):
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine

        # Verifica se l'arrocco è richiesto
        if abs(fine_col - inizio_col) == 2 and inizio_riga == fine_riga:
            return self.arrocco_valido(scacchiera, inizio, fine)

        # Movimento normale del re
        if abs(fine_riga - inizio_riga) <= 1 and abs(fine_col - inizio_col) <= 1:
            pezzo_destinazione = scacchiera[fine_riga][fine_col]
            if pezzo_destinazione is None or pezzo_destinazione.colore != self.colore:
                # Simula la mossa
                scacchiera[fine_riga][fine_col] = self
                scacchiera[inizio_riga][inizio_col] = None
                sotto_scacco = re_sotto_scacco(scacchiera, self.colore, ultima_mossa)
                # Annulla la mossa simulata
                scacchiera[fine_riga][fine_col] = pezzo_destinazione
                scacchiera[inizio_riga][inizio_col] = self
                if not sotto_scacco:
                    self.mossa_effettuata = True
                    return True
        return False

    def arrocco_valido(self, scacchiera, inizio, fine):
        """Verifica se l'arrocco è una mossa valida."""
        inizio_riga, inizio_col = inizio
        fine_riga, fine_col = fine
        direzione = 1 if fine_col > inizio_col else -1
        torre_col = 7 if direzione == 1 else 0
        torre = scacchiera[inizio_riga][torre_col]

        if not isinstance(torre, Torre) or torre.mossa_effettuata or self.mossa_effettuata:
            return False

        # Verifica che non ci siano pezzi tra il re e la torre
        for col in range(min(inizio_col, torre_col) + 1, max(inizio_col, torre_col)):
            if scacchiera[inizio_riga][col] is not None:
                return False

        # Verifica che il re non sia in scacco o non attraversi caselle minacciate
        for col in range(inizio_col, fine_col + direzione, direzione):
            scacchiera[fine_riga][fine_col] = self  # Simula il re sulla nuova posizione
            scacchiera[inizio_riga][inizio_col] = None
            if re_sotto_scacco(scacchiera, self.colore, None):
                scacchiera[fine_riga][fine_col] = None
                scacchiera[inizio_riga][inizio_col] = self
                return False
            scacchiera[fine_riga][fine_col] = None
        scacchiera[inizio_riga][inizio_col] = self
        scacchiera[fine_riga][fine_col] = None

        # Arrocco valido, sposta la torre
        nuova_posizione_torre = fine_col - direzione
        scacchiera[inizio_riga][nuova_posizione_torre] = torre
        scacchiera[inizio_riga][torre_col] = None
        torre.mossa_effettuata = True
        self.mossa_effettuata = True
        return True
