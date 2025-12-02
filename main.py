# Aquí montáis el código que implementa una partida de ajedrez entre 2 jugadores
# Cosas:
# - Montar un menú: guardar partida, abrir partida, mover pieza, ver piezas muertas y salir.
# - Gestionar la jugada y turno. Jugada comienza en 1 y va avanzando. Una jugada comienza cuando 
#   tiran las blancas 'B' y termina cuando tiran las negras 'N' entonces se pasa a la jugada 2.
# - Tras cada tirada de un turno mostrar el tablero y el menú.
# - Otras cosas que queráis hacer.
#
# HAVE FUN!

from ajedrez_hxh import Pieza, Torre, Caballo, Alfil, Queen, King, Peon, Partida
import re

mapeo_pieza_unicode = {
        'KB': u'\u2654',
        'QB': u'\u2655',
        'TB': u'\u2656',
        'AB': u'\u2657',
        'CB': u'\u2658',
        'PB': u'\u2659',
        'KN': u'\u265A',
        'QN': u'\u265B',
        'TN': u'\u265C',
        'AN': u'\u265D',
        'CN': u'\u265E',
        'PN': u'\u265F',
    }

def menu():
    '''Muestra un menú por pantalla
    Returns:
        int: opción escogida
    '''
    
    print('1) Abrir partida 2) Guardar partida 3) Mover pieza 4) Ver piezas muertas 5) Salir')
    opcion = input('Escoge opción: ')

    # validación
    modelo = re.compile(r'[12345]')
    while modelo.fullmatch(opcion) == None:
        opcion = input('Escoge opción (entre 1 y 5): ')

    return int(opcion)

if __name__ == '__main__':

    partida = None

    print('\n*** AJEDREZ HUMANO vs. HUMANO ***')

    opcion = menu()

    while opcion != 5:

        # Abrir
        if opcion == 1:

            try:
                partida = Partida()
            except Exception as err:
                print('No se encontró el fichero indicado. Comprueba que exista y pulsa 1)')
            else:
                print()
                print(f'Jugada: {partida.jugada} | Turno: {partida.turno}')
                print()
                partida.muestra_tablero()
            
        # guardar
        if opcion == 2:
            # Si existe la partida
            if partida:
                # piezas, posiciones y contexto
                partida.guarda_partida()

            else:
                print('Todavía no hay una partida cargada. Escoge la opción 1).')

        # mover
        if opcion == 3:
            # si existe la partida
            if partida:

                jugada = partida.jugada
                turno = partida.turno

                # Origen
                while True:   

                    print(f'Tiran las {"NEGRAS" if turno =="N" else "BLANCAS"}')

                    # Pedimos posición origen
                    while True:
                        try:
                            fila_origen = int(input(f'Fila (numero) de la pieza a mover: '))
                        except Exception as err:
                            print('No es un entero')
                        else:
                            if fila_origen in range(1, 9): # correcto
                                break
                            else:
                                print('Ha de ser un entero de 1 a 8')
                
                    while True:
                        try:
                            col_origen  = input(f'Columna (letra) de la pieza a mover: ')
                            col_origen = col_origen.upper()
                        except Exception as err:
                            print('Ocurrió un error inesperado')
                        else:
                            if col_origen in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                                break
                            else:
                                print('Ha de ser una letra de "A" hasta "H"')

                    # miramos que haya una pieza y que sea del color del turno
                    index = Pieza.busca_pieza_piezas((fila_origen, col_origen))

                    if index is not None:
                        if Partida.piezas[index].color != turno:
                            print(f'La pieza {fila_origen}, {col_origen} no es de color {"NEGRO" if turno =="N" else "BLANCO"}')                   
                        else:
                            break
                    else:
                        print('La casilla {fila_origen}, {col_origen} no tiene ninguna pieza')

                # Destino
                while True:

                    # Pedimos posición destino
                    while True:
                        try:
                            fila_destino = int(input(f'Fila destino (numero) de la pieza a mover: '))
                        except Exception as err:
                            print('No es un entero')
                        else:
                            if fila_destino in range(1, 9): # correcto
                                break
                            else:
                                print('Ha de ser un entero de 1 a 8')

                    while True:
                        try:
                            col_destino  = input(f'Columna destino (letra) de la pieza a mover: ')
                            col_destino = col_destino.upper()
                        except Exception as err:
                            print('Ocurrió un error inesperado')
                        else:
                            if col_destino in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                                break
                            else:
                                print('Ha de ser una letra de "A" hasta "H"')

                    # movemos
                    if Partida.piezas[index].mueve((fila_destino, col_destino)) is None:
                        pass
                    else:
                        # comprobamos si se ha matado el rey
                        if turno == 'B':

                            if King.negras == 0:
                                print('LAS BLANCAS HAN GANADO!!! Para nueva partida pulsa 1)')
                                print()
                                print(f'Jugada: {partida.jugada} | Turno: {partida.turno}')
                                print()
                                partida.muestra_tablero()

                                break

                        else:

                            if King.blancas == 0:
                                print('LAS NEGRAS HAN GANADO!!! Para nueva partida pulsa 1)')
                                print()
                                print(f'Jugada: {partida.jugada} | Turno: {partida.turno}')
                                print()
                                partida.muestra_tablero()

                                break

                        print('Movimiento realizado con éxito. Para volver a mover pulsa la opción 3).')
                        if turno == 'B':
                            partida.turno = 'N'
                        if turno == 'N':
                            partida.turno = 'B'
                            partida.jugada += 1

                        print()
                        print(f'Jugada: {partida.jugada} | Turno: {partida.turno}')
                        print()
                        partida.muestra_tablero()

                        break
            else:
                print('Todavía no hay una partida cargada. Escoge la opción 1).')

        if opcion == 4:
            # si existe la partida
            if partida:
                lista_pm = []
                for nombre in Partida.piezas_muertas:
                    lista_pm.append(mapeo_pieza_unicode[nombre])
                print(lista_pm)
            else:
                print('Todavía no hay una partida cargada. Escoge la opción 1).')

        opcion = menu()
        
    print(f'GRACIAS POR UTILIZAR EL JUEGO!!!')