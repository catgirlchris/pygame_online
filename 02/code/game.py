class Game:
    def __init__(self, id):
        self.p1_went = False
        self.p2_went = False 
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        '''Getter del movimiento de le jugader p
        p: [0,1]
        return: Move
        '''
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move

        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    def connected(self):
        '''Comprueba si ambes jugadores están conectades'''
        return self.ready

    def both_went(self):
        return self.p1_went and self.p2_went

    def winner(self):
        '''Comprueba todos los casos y devuelve le jugadore ganadore.'''
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == p2:
            winner = -1
        elif p1+p2 in ('PR', 'RS', 'SP'):
            winner = 0
        else:
            winner = 1

        return winner

    def reset_went(self):
        self.p1_went = False
        self.p2_went = False