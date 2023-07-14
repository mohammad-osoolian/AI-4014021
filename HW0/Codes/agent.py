import random

#################################################################################
# Functions
#################################################################################

########### Video Link ##########################################################
# https://drive.google.com/file/d/1ecHbIisDgaXiG8ZQmIsswfxm2fZmezRi/view?usp=sharing
#################################################################################

def update_condition(game_state):
    condition = [
            # horizontal
            (game_state[0], game_state[1], game_state[2], game_state[3]),
            (game_state[1], game_state[2], game_state[3], game_state[4]),
            (game_state[5], game_state[6], game_state[7], game_state[8]),
            (game_state[6], game_state[7], game_state[8], game_state[9]),
            (game_state[10], game_state[11], game_state[12], game_state[13]),
            (game_state[11], game_state[12], game_state[13], game_state[14]),
            (game_state[15], game_state[16], game_state[17], game_state[18]),
            (game_state[16], game_state[17], game_state[18], game_state[19]),
            (game_state[20], game_state[21], game_state[22], game_state[23]),
            (game_state[21], game_state[22], game_state[23], game_state[24]),

            # vertical
            (game_state[0], game_state[5], game_state[10], game_state[15]),
            (game_state[5], game_state[10], game_state[15], game_state[20]),
            (game_state[1], game_state[6], game_state[11], game_state[16]),
            (game_state[6], game_state[11], game_state[16], game_state[21]),
            (game_state[2], game_state[7], game_state[12], game_state[17]),
            (game_state[7], game_state[12], game_state[17], game_state[22]),
            (game_state[3], game_state[8], game_state[13], game_state[18]),
            (game_state[8], game_state[13], game_state[18], game_state[23]),
            (game_state[4], game_state[9], game_state[14], game_state[19]),
            (game_state[9], game_state[14], game_state[19], game_state[24]),

            # diagonal
            (game_state[0], game_state[6], game_state[12], game_state[18]),
            (game_state[6], game_state[12], game_state[18], game_state[24]),
            (game_state[4], game_state[8], game_state[12], game_state[16]),
            (game_state[8], game_state[12], game_state[16], game_state[20]),
            (game_state[1], game_state[7], game_state[13], game_state[19]),
            (game_state[5], game_state[11], game_state[17], game_state[23]),
            (game_state[3], game_state[7], game_state[11], game_state[15]),
            (game_state[9], game_state[13], game_state[17], game_state[21]),
        ]
    return condition

def checkp2win(game_state):
    for i in range(25):
        if game_state[i] == None:
            game_state[i] = False 
            condition = update_condition(game_state)
            for check in condition:
                    if check == (False, False, False, False):
                        game_state[i] = None
                        return i
            game_state[i] = None
    return None

def checkp1win(game_state):
    for i in range(25):
        if game_state[i] == None:
            game_state[i] = True  
            condition = update_condition(game_state)  
            for check in condition:
                    if check == (True, True, True, True):
                        game_state[i] = None
                        return i
            game_state[i] = None
    return None

def ai_action(game_state) -> int:
    ''' Generate and play move from tic tac toe AI'''
    strategic_places = [
                        [12], 
                        [11, 13, 7, 17], 
                        [6, 8, 16, 18], 
                        [0, 4, 20, 24], 
                        [2, 10, 14, 22]
                        ]
                    
    if game_state.count(2) > 0:
            return 0
    
    p2win = checkp2win(game_state)
    if p2win != None:
        return p2win
    p1win = checkp1win(game_state)
    if p1win != None:
        return p1win
    
    for level in strategic_places:
        random.shuffle(level)
        for index in level:
            if game_state[index] == None:
                return index

    emptyStates = []
    for i in range(0,25):     
        if game_state[i] is None:
            emptyStates.append(i)
        
    random_index = random.choice(emptyStates)
    return random_index
