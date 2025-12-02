# Se desea guardar los datos de una partida de ajedrez en un fichero
# Tablero:              Partida:
#    A B C D E F G H    A B C D E F G H
#
# 8  B N B N B N B N    TNANCNQNKNANCNTN
# 7  N B N B N B N B    PNPNPNPNPNPNPNPN
# 6  B N B N B N B N    B N B N B N B N
# 5  N B N B N B N B    N B N B N B N B
# 4  B N B N B N B N    B N B N B N B N
# 3  N B N B N B N B    N B N B N B N B
# 2  B N B N B N B N    PBPBPBPBPBPBPBPB
# 1  N B N B N B N B    TBCBABKBQBABCBTB
# 
# Las piezas son:   T (Torre Blanca | Negra, 2 de cada)
#                   C (Caballo Blanco | Negro, 2 de cada)
#                   A (Alfil Blanco | Negro, 2 de cada)
#                   Q (Reina Negra | Blanca, 1 de cada)
#                   K (Rey Blanco | Negro, 1 de cada)
#                   P (Peón Blanco | Negro, 8 de cada)
#
# Las piezas se codifican por: TN,A,8 -> Torre Negra en columna A fila 8
# En partida.csv tenemos la colocación inicial del tablero

# Se pide: 
# hacer una función que pase a objetos Python cada una de las piezas del csv
# hacer una función que pase los objetos Python a un fichero csv
# hacer una función que dibuje un tablero con las piezas posicionadas
# Diseña unas clases que representen cada una de las piezas
# Diseña una clase que represente la partida

import os.path as path
import csv


class Pieza:
    '''Clase base para todas las piezas de ajedrez.'''
    
    def __init__(self, nombre: str, columna: str, fila: int):
        '''Método inicializador
        Args:
            nombre(str): TN torre negra, TB torre blanca, ...
            columna(str): de izquierda a derecha A B C D E F G H
            fila(int): de arriba a abajo 8 7 6 5 4 3 2 1 
        '''
        self.nombre = nombre
        self.columna = columna
        self.fila = int(fila)


    # métodos estáticos comunes a todas las piezas. Ayudan al cálculo de movimientos.
    @staticmethod
    def busca_pieza_piezas(nueva_pos:tuple):
        '''Comprueba si hay una pieza en cierta posición en la lista de piezas de la clase partida.
        Args:
            nueva_pos(tuple): formato de ajedrez (fila, columna)
        Returns:
            None|int: None si no hay ninguna pieza | int es el índice donde se encuentra la pieza en Partida.piezas
        '''
        
        fila, columna = nueva_pos[0], nueva_pos[1]
        for i in range(len(Partida.piezas)):
            if Partida.piezas[i].fila == fila and Partida.piezas[i].columna == columna:
                return i
            
        return None


    @staticmethod
    def posicion_normalizada(fila, columna):
        '''retorna la posición normalizada de una pieza en el tablero. En el tablero se usan
        índices de 0 a 7 para filas y columnas para calcular los movimientos más intuitivamente.
        Args:
            fila(int): de 8 a 1
            columna(str): de A a H
        Returns:
            tuple: tupla (fila de 0 a 7, columna de 0 a 7)
        '''
        mapeo_columnas = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        mapeo_filas = {
            8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7 
        }
        return (mapeo_filas[fila], mapeo_columnas[columna])
    

    @staticmethod
    def posición_ajedrez(fila, columna):
        '''retorna posición en notación de ajedrez en el tablero de una pieza.
        Args:
            fila(int): de 0 a 7
            columna(int): de 0 a 7
        Returns:
            tuple: tupla (fila de 8 a 1, columna de A a H)
        '''
        mapeo_columnas = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'
        }
        mapeo_filas = {
            0:8, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1
        }
        return (mapeo_filas[fila], mapeo_columnas[columna])
    
    @staticmethod
    def movimiento_valido(fila:int, col:int, fila_inicial:int, col_inicial:int, lista_casillas:list):
        '''Se le pasa una posición y si el movimiento está permitido se anota en la lista de casillas
        Args:
            fila(int): fila a sondear de 0 a 7
            col(int): columna a sondear de 0 a 7
            fila_inicial(int): fila donde está la pieza que mueve (0 a 7)
            col_inicial(int): columna donde está la pieza que mueve (0 a 7)
            lista_casillas(list): lista donde se guardan los movimientos permitidos
        Returns
            bool: True si casilla vacía | False si casilla no vacía (no se puede continuar en esa dirección) 
        '''
        # casilla vacía
        if Partida.tablero[fila][col] is None:
            lista_casillas.append((fila, col))
            return True
            
        # hay pieza
        if Partida.tablero[fila][col] is not None:
                # mismo color: ya no se puede seguir al norte y se sale
                if Partida.tablero[fila][col].color == Partida.tablero[fila_inicial][col_inicial].color:
                    return False
                else: # distinto color: se puede matar, se añade como movimiento válido y se sale
                    lista_casillas.append((fila, col))
                    return False


class Torre(Pieza):
    '''Clase que representa una Torre y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas torres negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas torres blancas hay en el tablero
    '''
    # atributos de clase
    negras = 0
    blancas = 0

    def __init__(self, nombre: str, columna: str, fila: int, color: str, moved: bool) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'TN' | 'TB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre, columna, fila)
        self.color = color
        self.moved = False
        if color == 'N':
            Torre.negras += 1
        else:
            Torre.blancas += 1
    
    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            Torre.negras -=1
        else:
            Torre.blancas -=1

    def pinta(self):
        '''Representación unicode de la pieza'''
        if self.color == 'N':
            return u'\u265c'
        else:
            return u'\u2656'
        
    def mueve(self, nueva_pos:tuple):
        '''Mueve de forma válida la torre. Los turnos se gestionan desde el '__main__' junto con el objeto partida.\n
        Opciones:
            Direcciones: norte, sur, este y oeste.
            Movimiento: hasta pieza que le tapone (si es de color contrario la puede matar)
            Mata: en las direcciones indicadas.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns:
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        destinos = Torre.posibles_movimientos(Torre.posicion_normalizada(self.fila, self.columna))
        print(destinos) # debug
        # movimiento plausive
        if nueva_pos in destinos:

            # se mata una pieza (como viene de posibles movimientos el color es el contrario)
            pos = Torre.busca_pieza_piezas(nueva_pos)
            if pos is not None:
                # quitamos la pieza de la lista
                Partida.piezas_muertas.append(Partida.piezas[pos].nombre) # añadimos nombre a piezas muertas
                Partida.piezas.pop(pos) # borramos pieza y provocamos __del__

            # actualizamos posición de la Torre
            self.fila = nueva_pos[0]
            self.columna = nueva_pos[1]
            # actualizamos tablero
            Partida.tablero = Partida.normaliza_piezas()
            self.moved = True
            return True

        else:

            print('Movimiento no permitido')
            return None
    
    @staticmethod
    def posibles_movimientos(pos_inicial:tuple): 
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        lista_permitidos = []

        fila_inicial, col_inicial  = pos_inicial[0], pos_inicial[1]
        
        # movimientos al NORTE (fila decreciente, columna fija)
        for i in range(fila_inicial-1, -1, -1):
            if not Torre.movimiento_valido(i, col_inicial, fila_inicial, col_inicial, lista_permitidos):
                break
        
        # movimientos al SUR (fila creciente, columna fija)
        for i in range(fila_inicial+1, 8, 1):
            if not Torre.movimiento_valido(i, col_inicial, fila_inicial, col_inicial, lista_permitidos):
                break

        # movimientos al OESTE (fila_fija, columna decreciente)
        for j in range(col_inicial-1, -1, -1):
            if not Torre.movimiento_valido(fila_inicial, j, fila_inicial, col_inicial, lista_permitidos):
                break
            
        # movimientos al ESTE (fila_fija, columna creciente)
        for j in range(col_inicial+1, 8, 1):
            if not Torre.movimiento_valido(fila_inicial, j, fila_inicial, col_inicial, lista_permitidos):
                break
        
        # pasamos a la notación de ajedrez
        nueva_lista = []
        for tupla in lista_permitidos:
            nueva_lista.append(Torre.posición_ajedrez(*tupla))

        return nueva_lista   


class Caballo(Pieza):
    '''Clase que representa un Caballo y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas piezas caballo negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas piezas caballo blancas hay en el tablero
    '''
    # atributos de clase
    negras = 0
    blancas = 0

    def __init__(self, nombre: str, columna: str, fila: int, color: str) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'CN' | 'CB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre, columna, fila)
        self.color = color
        if color == 'N':
            Caballo.negras += 1
        else:
            Caballo.blancas += 1

    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            Caballo.negras -=1
        else:
            Caballo.blancas -=1

    def pinta(self):
        '''representación unicode de la pieza'''
        if self.color == 'N':
            return u'\u265e'
        else:
            return u'\u2658'
        
    def mueve(self, nueva_pos:tuple):
        '''Mueve de forma válida el caballo. Los turnos se gestionan desde el '__main__' junto con el objeto partida.\n
        Opciones:
            Direcciones: norte, sur, este y oeste (teniendo en cuenta que hace un 7 y que se situa al final, NO durante el tramo)
            Movimiento: puede mover si no hay pieza al final del 7 o si la que hay es de color contrario la puede matar
            Mata: en las direcciones indicadas.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns:
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        pass

    @staticmethod
    def posibles_movimientos(pos_inicial:tuple):
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        lista_permitidos = []

        fila_inicial, col_inicial = pos_inicial[0], pos_inicial[1]
        
        # movimientos al NORTE: dos arriba (fila_inicial - 2) + uno izquierda (col_inicial - 1) 
        # y dos arriba (fila_inicial - 2) + uno derecha (col_inicial + 1))

        # NORTE-IZDA
        if (nueva_fila := fila_inicial - 2) in range(8) and (nueva_col := col_inicial - 1) in range(8):
            Caballo.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)
        
        # NORTE-DCHA
        if (nueva_fila := fila_inicial - 2) in range(8) and (nueva_col := col_inicial + 1) in range(8):
            Caballo.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)
             
        # movimientos al SUR: dos abajo (fila_inicial + 2) + uno izquierda (col_inicial - 1) 
        # y dos abajo (fila_inicial + 2) + uno derecha (col_inicial + 1))

        # SUR-IZDA
        pass
            
        # SUR-DCHA
        pass
             
        # movimientos al OESTE: dos izquierda (col_inicial - 2) + 1 abajo (fila_inicial + 1) 
        # y dos izquierda (col_inicial - 2) + 1 arriba (fila_inicial - 1)
        
        # OESTE-ARRIBA
        pass
        
        # OESTE-ABAJO
        pass

        # movimientos al ESTE: dos derecha (col_inicial + 2) + 1 abajo (fila_inicial + 1) 
        # y dos derecha (col_inicial + 2) + 1 arriba (fila_inicial - 1)

        # ESTE-ARRIBA:
        pass

        # ESTE-ABAJO:
        pass
        
        # pasamos a la notación de ajedrez
        nueva_lista = []
        for tupla in lista_permitidos:
            nueva_lista.append(Caballo.posición_ajedrez(*tupla))

        return nueva_lista


class Alfil(Pieza):
    '''Clase que representa un Alfil y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas piezas Alfil negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas piezas Alfil blancas hay en el tablero
    '''
    # atributos de clase
    negras = 0
    blancas = 0
    def __init__(self, nombre: str, columna: str, fila: int, color: str) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'AN' | 'AB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre, columna, fila)
        self.color = color
        if color == 'N':
            Alfil.negras += 1
        else:
            Alfil.blancas += 1
    
    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            Alfil.negras -=1
        else:
            Alfil.blancas -=1

    def pinta(self):
        '''Representación unicode de la pieza'''
        if self.color == 'N':
            return u'\u265d'
        else:
            return u'\u2657'

    def mueve(self, nueva_pos:tuple):
        '''Mueve de forma válida el alfil. Los turnos se gestionan desde el '__main__' junto con el objeto partida.\n
        Opciones:
            Direcciones: diagonal norte-oeste, diagonal norte-este, diagonal sur-oeste y diagonal sur-este
            Movimiento: puede mover hasta que encuentre una pieza que le tapone. Si es de distinto color la puede matar
            Mata: en las direcciones indicadas.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns:
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        pass

    @staticmethod
    def posibles_movimientos(pos_inicial:tuple):
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        lista_permitidos = []

        fila_inicial, col_inicial  = pos_inicial[0], pos_inicial[1]
        
        # movimientos al NORTE-OESTE (fila decreciente, columna decreciente)
        for i, j in zip(range(fila_inicial-1, -1, -1), range(col_inicial-1, -1, -1)):
            if not Alfil.movimiento_valido(i, j, fila_inicial, col_inicial, lista_permitidos):
                break
        
        # movimientos al NORTE-ESTE (fila decreciente, columna creciente)
        pass

        # movimientos al SUR-OESTE (fila creciente, columna decreciente)
        pass
        
        # movimientos al SUR-ESTE (fila creciente, columna creciente)
        pass
        
        # pasamos a la notación de ajedrez
        nueva_lista = []
        for tupla in lista_permitidos:
            nueva_lista.append(Torre.posición_ajedrez(*tupla))

        return nueva_lista

    
class Queen(Pieza):
    '''Clase que representa una Reina y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas piezas Reina negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas piezas Reina blancas hay en el tablero
    '''    
    # atributos de clase
    negras = 0
    blancas = 0
    def __init__(self, nombre: str, columna: str, fila: int, color: str) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'QN' | 'QB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre, columna, fila)
        self.color = color
        if color == 'N':
            Queen.negras += 1
        else:
            Queen.blancas += 1

    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            Queen.negras -=1
        else:
            Queen.blancas -=1

    def pinta(self):
        '''Representación unicode de la pieza'''
        if self.color == 'N':
            return u'\u265B'
        else:
            return u'\u2655'
        
    def mueve(self, nueva_pos:tuple):
        '''Mueve de forma válida la reina. Los turnos se gestionan desde el '__main__' junto con el objeto partida.\n
        Opciones:
            Direcciones: todas (norte, sur, este, oeste y diagonales)
            Movimiento: puede mover hasta que encuentre una pieza que le tapone. Si es de distinto color la puede matar
            Mata: en las direcciones indicadas.

        Si nos fijamos tiene los movimientos de Torre y Alfil.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        pass
   

    @staticmethod
    def posibles_movimientos(pos_inicial:tuple):
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        
        # nos aprovechamos del código del ALFIL
        # lista_permitidos_ALFIL ya estará en notación ajedrez
        lista_permitidos_ALFIL = Alfil.posibles_movimientos(pos_inicial)
        
        
        # nos aprovechamos del código de la TORRE
        # lista_permitidos_TORRE ya esta en notación ajedrez
        lista_permitidos_TORRE = Torre.posibles_movimientos(pos_inicial)

        return lista_permitidos_ALFIL + lista_permitidos_TORRE


class King(Pieza):
    '''Clase que representa un Rey y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas piezas Rey negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas piezas Rey blancas hay en el tablero
    '''
    # atributos de clase
    negras = 0
    blancas = 0
    def __init__(self, nombre: str, columna: str, fila: int, color: str, moved: bool) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'KN' | 'KB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre, columna, fila)
        self.color = color
        self.moved = False
        if color == 'N':
            King.negras += 1
        else:
            King.blancas += 1

    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            King.negras -= 1
        else:
            King.blancas -= 1

    def pinta(self):
        if self.color == 'N':
            return u'\u265A'
        else:
            return u'\u2654'
        
    def enroque(self):
        """
        Verifica las condiciones para el enroque. Devuelve una lista de posiciones destino 
        normalizadas del rey si el enroque es posible en ese lado.
        """
        if self.moved:
            return False
        
        else:
            if self.color == 'N':
                if (n_large_enroque := (Partida.tablero[7][1] is None and Partida.tablero[7][2] is None and Partida.tablero[7][3] is None)) or (n_short_enroque := (Partida.tablero[7][5] is None and Partida.tablero[7][6] is None)):
                    if n_large_enroque:
                        pass
                    if n_short_enroque:
                        pass
                else:
                    return False
            else:
                if (b_large_enroque := (Partida.tablero[0][1] is None and Partida.tablero[0][2] is None and Partida.tablero[0][3] is None)) or (b_short_enroque := (Partida.tablero[0][5] is None and Partida.tablero[0][6] is None)):
                    if b_large_enroque:
                        pass
                    if b_short_enroque:
                        pass
                else:
                    return False
    
    def mueve(self, nueva_pos:tuple):
        '''Mueve de forma válida el rey. Los turnos se gestionan desde el '__main__' junto con el objeto partida.
        De momento, no se implementa el enroque.\n
        Opciones:
            Direcciones: Todas (norte, sur, este, oeste y diagonales. Solo puede recorrer distancia 1.
            Movimiento: puede mover si no hay pieza o si la que hay es de color contrario la puede matar
            Mata: en las direcciones indicadas.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns:
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        destinos = King.posibles_movimientos(King.posicion_normalizada(self.fila, self.columna))
        print(destinos)

        if nueva_pos in destinos:
            pos = King.busca_pieza_piezas(nueva_pos)
            
            if pos is not None:
                Partida.piezas_muertas.append(Partida.piezas[pos].nombre)
                Partida.piezas.pop(pos)

            self.fila = nueva_pos[0]
            self.columna = nueva_pos[1]
            Partida.tablero = Partida.normaliza_piezas()
            self.moved = True
            return True
        
        return None

 
    @staticmethod
    def posibles_movimientos(pos_inicial:tuple):
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        lista_permitidos = []

        fila_inicial, col_inicial = pos_inicial[0], pos_inicial[1]
        
        # movimiento al NORTE: decremento fila y mantengo columna
        if (nueva_fila := fila_inicial - 1) in range(8):
            King.movimiento_valido(nueva_fila, col_inicial, fila_inicial, col_inicial, lista_permitidos)
        
        # movimiento al SUR: incremento fila y mantengo columna
        if(nueva_fila := fila_inicial + 1) in range(8):
            King.movimiento_valido(nueva_fila, col_inicial, fila_inicial, col_inicial, lista_permitidos)

        # movimiento al OESTE: mantengo fila y decremento columna
        if (nueva_col := col_inicial - 1) in range(8):
            King.movimiento_valido(fila_inicial, nueva_col, fila_inicial, col_inicial, lista_permitidos)
        
        # movimiento al ESTE: mantengo fila y incremento columna
        if (nueva_col := col_inicial + 1) in range(8):
            King.movimiento_valido(fila_inicial, nueva_col, fila_inicial, col_inicial, lista_permitidos)

        # Diagonal NORTE-IZDA: decremento fila y decremento columna
        if (nueva_fila := fila_inicial - 1) in range(8) and (nueva_col := col_inicial - 1) in range(8):
            King.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)
        
        # Diagonal NORTE-DCHA: decremento fila y incremento columna
        if (nueva_fila := fila_inicial - 1) in range(8) and (nueva_col := col_inicial + 1) in range(8):
            King.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)

        # Diagonal SUR-IZDA: incremento fila y decremento columna
        if (nueva_fila := fila_inicial + 1) in range(8) and (nueva_col := col_inicial - 1) in range(8):
            King.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)
            
        # Diagonal SUR-DCHA: incremento fila y incremento columna
        if (nueva_fila := fila_inicial + 1) in range(8) and (nueva_col := col_inicial + 1) in range(8):
            King.movimiento_valido(nueva_fila, nueva_col, fila_inicial, col_inicial, lista_permitidos)
        
        # pasamos a la notación de ajedrez
        nueva_lista = []
        for tupla in lista_permitidos:
            nueva_lista.append(King.posición_ajedrez(*tupla))

        return nueva_lista


class Peon(Pieza):
    '''Clase que representa un Peón y hereda de Pieza.
    Attributes:
        negras(int): atributo de clase que indica cuantas piezas Peón negras hay en el tablero
        blancas(int): atributo de clase que indica cuantas piezas Peón blancas hay en el tablero
    '''
    # atributos de clase
    negras = 0
    blancas = 0
    def __init__(self, nombre: str, columna: str, fila: int, color: str) -> None:
        '''Método inicializador
        Args:
            nombre(str): 'KN' | 'KB'
            columna(str): 'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'
            fila(int): 1|2|3|4|5|6|7|8
            color(str): color de la pieza 'B' | 'N'
        '''
        super().__init__(nombre,columna,fila)
        self.color = color
        if color == 'N':
            Peon.negras += 1
        else:
            Peon.blancas += 1

    def __del__(self):
        '''Consecuencia de matar una pieza. Esto se ejecuta antes de borrar el objeto.'''
        if self.color == 'N':
            Peon.negras -= 1
        else:
            Peon.blancas -= 1

    def pinta(self):
        '''Representación unicode de la pieza'''
        if self.color == 'N':
            return u'\u265f'
        else:
            return u'\u2659'  

    def mueve(self, nueva_pos):
        '''mueve de forma válida el peón (si es su turno)\n
        Opciones:
            - siempre mueve hacia adelante
            - si está en la casilla de salida mueve 1 o 2 en su dirección
            - en otro caso solo mueve 1
            - mueve si no hay pieza que le tapone
            - mata adelantando una posición en diagonal
            - Promoción: Cuando un peón alcanza la última fila del tablero, puede promocionarse a cualquiera de las otras piezas (dama, torre, alfil o caballo). 
            - Al paso: Si un peón enemigo avanza dos casillas en su primer movimiento y queda a su lado en la misma fila, el peón puede capturarlo como si este solo hubiera avanzado una casilla. Esta es una captura especial y solo se puede realizar en el siguiente turno del oponente. 
            - Estos 2 movimientos especiales no están implementados de momento.
        Se trabaja con el tablero normalizado para mejor comodidad.
        Args:
            nueva_pos(tuple): nueva posición (numero_fila, letra_columna)
        Returns:
            None|True: Si el movimiento no es válido retorna None | True si es válido
        '''
        destinos = Peon.posibles_movimientos(Peon.posicion_normalizada(self.fila, self.columna))
        print(destinos)

        if nueva_pos in destinos:
            pos = Peon.busca_pieza_piezas(nueva_pos)
            if pos is not None:
                Partida.piezas_muertas.append(Partida.piezas[pos].nombre)
                Partida.piezas.pop(pos)
            
            self.fila = nueva_pos[0]
            self.columna = nueva_pos[1]
            Partida.tablero = Partida.normaliza_piezas()
            return True
        return None
    
    @staticmethod
    def posibles_movimientos(pos_inicial:tuple):
        '''Trabajamos con tablero normalizado y devolvemos una lista con los movimientos válidos (en notación ajedrez).
        Args:
            pos_inicial(tuple): posición normalizada
        Returns:
            list: lista de destinos permitidos (notación ajedrez)
        '''
        lista_permitidos = []

        fila_inicial, col_inicial = pos_inicial[0], pos_inicial[1]

        # según el color se incrementa la fila ('N') o se decrementa ('B') y se calcula la fila de posición inicial
        if Partida.tablero[fila_inicial][col_inicial].color == 'N':
            direccion = 1
            fila_posicion_inicial = 1
        else:
            direccion = -1
            fila_posicion_inicial = 6
        
        # comprobar avance 1 (no puede matar)
        if (nueva_fila := fila_inicial + direccion) in range(8):
            if Partida.tablero[nueva_fila][col_inicial] is None:
                lista_permitidos.append((nueva_fila, col_inicial))
        
        # comprobar avance 2 (solo si está en fila inicial y no puede matar)
        if fila_inicial == fila_posicion_inicial:
            # comprobar que no haya una pieza que le tapone para mover 2
            if (fila_inicial + direccion, col_inicial) in lista_permitidos:
                # comprobar que la casilla está vacía
                nueva_fila = fila_inicial + 2 * direccion
                if Partida.tablero[nueva_fila][col_inicial] is None:
                    lista_permitidos.append((nueva_fila, col_inicial))

        # comprobar matar en diagonal a la derecha
        if (nueva_fila:= fila_inicial + direccion) in range(8) and (nueva_col := col_inicial + 1) in range (8):
            if Partida.tablero[nueva_fila][nueva_col] is not None:
                if Partida.tablero[fila_inicial][col_inicial].color != Partida.tablero[nueva_fila][nueva_col].color:
                    lista_permitidos.append((nueva_fila, nueva_col))

        # comprobar matar en diagonal a la izquierda
        if (nueva_fila:= fila_inicial + direccion) in range(8) and (nueva_col := col_inicial - 1) in range (8):
            if Partida.tablero[nueva_fila][nueva_col] is not None:
                if Partida.tablero[fila_inicial][col_inicial].color != Partida.tablero[nueva_fila][nueva_col].color:
                    lista_permitidos.append((nueva_fila, nueva_col))

        # pasamos a la notación de ajedrez
        nueva_lista = []
        for tupla in lista_permitidos:
            nueva_lista.append(Peon.posición_ajedrez(*tupla))

        return nueva_lista
    
class Partida:
    '''Singleton para una partida.
    Attributes:
        fichero(str): fichero desde el que se ha cargado la partida.
        piezas(list): Atributo de clase. Lista de piezas en notación ajedrez.
        tablero(list[list]): Atributo de clase. Matriz que representa el tablero en notación normalizada.
        piezas_muertas(list): Atributo de clase. Lista con nombres de piezas muertas.
        instance(Partida): Atributo de clase. Para implementar el singleton
    '''
    # atributos de clase
    fichero = None # fichero desde el que se ha cargado la partida
    piezas = None # lista: piezas en posición [A..I][8..1]
    tablero = None # matriz: todo el tablero [0..7][0..7]
    piezas_muertas = None
    instance = None # solo una

    def __new__(cls):
        '''patrón Singleton'''
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance
    
    def __init__(self, jugada=1, turno='B') -> None:
        '''Método inicializador
        Args:
            jugada(int): comienza por 1 y cada vez que tiran las negras se incrementa en 1
            turno(str): comienza por 'B' cuando tiran las blancas pasa a 'N' cuando tiren las negras pasa a 'B' ...
        '''
        Partida.piezas = self.carga_partida()
        Partida.tablero = Partida.normaliza_piezas()
        
        nombre_ext = Partida.fichero.split('.')
        fichero_con = nombre_ext[0] + '.con'
        
        # se carga una partida comenzada
        if (path.exists(fichero_con)):
            # cargamos el fichero de contexto

            with open(fichero_con, 'r') as fr:
                
                lista = fr.readline().split(',')
                # quito algún \n odioso
                if lista:
                    for i in range(len(lista)):
                        lista[i] = lista[i].rstrip()
                Partida.piezas_muertas = lista
                self.jugada = int(fr.readline())
                self.turno = fr.readline()

        else: # partida nueva
            Partida.piezas_muertas = []
            self.jugada = jugada
            self.turno = turno

    def guarda_partida(self):
        '''Guarda la partida en curso en:
            - fichero csv: posición de las piezas
            - fichero con: piezas muertas (primera línea), la jugada en curso (segunda línea) y el turno (tercera línea)
        
        '''
        fichero_csv = input('Nombre del fichero para guardar la partida (INTRO para "partida_saved.csv"): ')
        if fichero_csv == '':
            fichero_csv = 'partida_saved.csv'
        try:
            escritura_piezas(Partida.piezas, fichero_csv)
        except Exception as err:
            print(f'Ocurrió un error {err}')

        # preparamos nombre fichero para guardar
        nombre_ext = fichero_csv.split('.')
        fichero_con = nombre_ext[0] + '.con'

        # preparamos la línea de piezas_muertas
        lineas = ''
        for nombre_pieza in Partida.piezas_muertas:
            lineas = nombre_pieza + ', '

        # si hay piezas muertas quito la última ','
        if lineas:
            lineas = lineas[:len(lineas) - 1]

        # añado '\n'
        lineas += '\n'

        # preparamos la línea de jugada
        lineas += str(self.jugada)

        # añado '\n'
        lineas += '\n'

        # preparamos la línea de turno
        lineas += self.turno

        with open(fichero_con, 'w') as fw:
            fw.writelines(lineas)

    def muestra_tablero(self):
        '''muestra por pantalla el tablero en formato ajedrez'''
        Partida.dibuja()

    @classmethod
    def dibuja(cls):
        tab = [
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
            ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
        ]
        mapeo_columnas = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        mapeo_filas = {
            8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7 
        }

        for pieza in Partida.piezas:
            tab[mapeo_filas[pieza.fila]][mapeo_columnas[pieza.columna]] = ' ' + pieza.pinta() + ' '
    
        print('   A  B  C  D  E  F  G  H')
        print()
        f = 8
        for fila in tab:
            print(f, end=' ')
            f -= 1
            for celda in fila:
                print(celda, end='')
            print()

    @classmethod
    def normaliza_piezas(cls):
        '''genera una matriz con índices normalizados (de 0 a 7) para trabajar cómodamente los movimientos
        
        :returns (list(list)): matriz que se guarda en Partida.tablero
        '''
        tab = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        mapeo_columnas = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        mapeo_filas = {
            8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7 
        }

        for pieza in cls.piezas:
            tab[mapeo_filas[pieza.fila]][mapeo_columnas[pieza.columna]] = pieza

        return tab

    @staticmethod
    def carga_partida():
        '''Carga la partida desde un fichero csv
        
        TO DO: falta cargar jugada, turno y piezas_muertas
        '''
        fichero_csv = input('Nombre del fichero con la partida (INTRO para "partida.csv"): ')
        if fichero_csv == '':
            fichero_csv = 'partida.csv'
        try:
            lista_piezas = list(lectura_piezas(fichero_csv))
        except Exception as err:
            print(f'Ocurrió un error {err}')
            raise Exception('Fichero no encontrado')
        
        # lo guardamos para poder, desde __init__, inicializar correctamente el contexto de la partida
        Partida.fichero = fichero_csv
        # identificamos cada pieza y creamos una subclase específica
        nueva_lista = []
    
        for pieza in lista_piezas:
            if pieza.nombre == 'TN':
                nueva_lista.append(Torre(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'TB':
                nueva_lista.append(Torre(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue
            if pieza.nombre == 'CN':
                nueva_lista.append(Caballo(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'CB':
                nueva_lista.append(Caballo(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue
            if pieza.nombre == 'AN':
                nueva_lista.append(Alfil(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'AB':
                nueva_lista.append(Alfil(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue
            if pieza.nombre == 'QN':
                nueva_lista.append(Queen(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'QB':
                nueva_lista.append(Queen(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue
            if pieza.nombre == 'KN':
                nueva_lista.append(King(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'KB':
                nueva_lista.append(King(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue
            if pieza.nombre == 'PN':
                nueva_lista.append(Peon(pieza.nombre, pieza.columna, pieza.fila, 'N'))
                continue
            if pieza.nombre == 'PB':
                nueva_lista.append(Peon(pieza.nombre, pieza.columna, pieza.fila, 'B'))
                continue

        del lista_piezas # ya no se necesita
        return nueva_lista

# este podría ser un método estático de clase
def lectura_piezas(nombre_fichero):
    with open(nombre_fichero, 'r') as fr:
        reader = csv.reader(fr)
        tiene_cabecera = csv.Sniffer().has_header(fr.read(512))
        fr.seek(0) # coloca la posición de lectura al inicio de nuevo
        if tiene_cabecera:
            cabecera = next(reader) # ignora la cabecera
        for fila in reader:
            yield Pieza(*fila)

# este podría ser un método estático de clase
def escritura_piezas(lista_piezas, fichero_salida):
    with open(fichero_salida, 'w') as fw:
        columnas = ['nombre', 'columna', 'fila']
        writer = csv.DictWriter(fw, fieldnames=columnas, extrasaction='ignore')
        writer.writeheader()
        for planeta in lista_piezas:
            # __dict__ in Python represents a dictionary or any mapping object
            #  that is used to store the attributes of the object. mappingproxy objects
            valores = planeta.__dict__
            writer.writerow(valores)


if __name__ == '__main__':

    '''
    lista = list(lectura_piezas('partida.csv'))

    escritura_piezas(lista, 'partida2.csv')
    
    tn1 = Torre('TN', 'A', 8, 'N')
    print(tn1.pinta())
    print(Torre.negras)
    print(Torre.blancas)

    tb1 = Torre('TB', 'A', 8, 'B')
    print(tn1.pinta())
    print(Torre.negras)
    print(Torre.blancas)

    lista = carga_partida()
    for pieza in lista:
        print(pieza)
    '''
    
    partida = Partida()
    partida.muestra_tablero()
    # partida.guarda_partida()

    '''
    # test torre
    Partida.piezas[Pieza.busca_pieza_piezas((5,'B'))].mueve((2,'B'))
    partida.muestra_tablero()
    print(Peon.negras, Peon.blancas)
    print(Partida.piezas_muertas)
    '''
    '''
    # test caballo
    Partida.piezas[Pieza.busca_pieza_piezas((6,'C'))].mueve((5,'A'))
    #partida.guarda_partida()
    #partida.carga_partida()
    partida.muestra_tablero()
    print(Peon.negras, Peon.blancas)
    print(Partida.piezas_muertas) 
    print(Partida.piezas[Pieza.busca_pieza_piezas((5, 'A'))].nombre)
    print(Partida.piezas[Pieza.busca_pieza_piezas((5, 'A'))].pinta())
    '''

    '''
    # test alfil
    Partida.piezas[Pieza.busca_pieza_piezas((7,'B'))].mueve((1,'H'))
    partida.muestra_tablero()
    print(Torre.negras, Torre.blancas)
    print(Partida.piezas_muertas)
    '''

    '''
    # test queen
    Partida.piezas[Pieza.busca_pieza_piezas((6,'F'))].mueve((2,'F'))
    partida.muestra_tablero()
    print(Peon.negras, Peon.blancas)
    print(Partida.piezas_muertas)
    '''

    '''
    # test king
    Partida.piezas[Pieza.busca_pieza_piezas((7,'E'))].mueve((6,'F'))
    partida.muestra_tablero()
    print(Peon.negras, Peon.blancas)
    print(Partida.piezas_muertas)
    '''

    '''
    # test peon
    Partida.piezas[Pieza.busca_pieza_piezas((4,'H'))].mueve((5,'G'))
    Partida.piezas[Pieza.busca_pieza_piezas((7,'F'))].mueve((5,'F'))
    partida.muestra_tablero()
    print(Peon.negras, Peon.blancas)
    print(Partida.piezas_muertas)
    '''