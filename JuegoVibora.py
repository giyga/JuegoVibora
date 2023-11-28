import time, curses, random, numpy as np
from curses.textpad import rectangle

Rand1, Rand2 = 0, 0
JuegoActivo = True

def GameOver(a): 
    global JuegoActivo
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    a.nodelay(True)
    opcion = ""    
    a.clear()    
    rectangle(a, 0, 0, 12, 33)
    a.addstr(3,10,"GAME OVER")
    a.addstr(6,3,"NO <--- NUEVA PARTIDA ---> SÍ", curses.color_pair(1))    
    a.refresh()
    while JuegoActivo == False:
      try:
        opcion = a.getkey()
      except:
        pass
      if opcion == "KEY_RIGHT":
        main(a)
      elif opcion == "KEY_LEFT":
        quit()

def ImprimeComida(CasillaComida, stdscr):
  global Rand1
  global Rand2
  while CasillaComida == 79:
    Rand1 = random.randint(1,11)
    Rand2 = random.randint(1,32)
    CasillaComida = stdscr.inch(Rand1,Rand2)
  stdscr.addstr(Rand1,Rand2,"*")
def main(stdscr):
  global JuegoActivo
  JuegoActivo = True
  Objeto = ["O"]
  Posiciones = np.array([[6,17],[0,0]]) #Posiciones de cada segmento de la serpiente. El segmento 2 se imprime en la esquina superior izq cuando la long de la vibora es de 1, por lo tanto siempre la cubre el perímetro.
  Comio = False
  x, y = 6, 17
  dir = "KEY_RIGHT"
  CasillaComida = 79
  stdscr.clear()
  stdscr.addstr(x,y,Objeto[0])
  ImprimeComida(CasillaComida, stdscr)
  stdscr.refresh() #Esto desde el while se hará de manera repetida, lo mejor será crear una función aparte
  stdscr.nodelay(True)
  while JuegoActivo == True: #Podría hacer de esto una función para evitar tanta redundancia
    #stdscr.addstr(Rand1,Rand2,"*") ####
    #rectangle(stdscr, 0, 0, 12, 33)
    stdscr.refresh()
    try:
      dir = stdscr.getkey() #Necesito una manera de hacer que no reconozca valores no-direccionales
    except:
      pass
    if dir == "KEY_UP": #Si se presiona una tecla no-direccional una vez, el juego se congela.
      if Posiciones[0,0] == Posiciones[1,0] + 1:
        dir = "KEY_DOWN"
      else:
        try:
          x -= 1          
          stdscr.clear()
          if x == Rand1 and y == Rand2: #Comer y crecer
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == False: #Si la víbora de longitud 1 acaba de comer
              Comio = True
              stdscr.addstr(x,y,Objeto[0])
              ImprimeComida(CasillaComida, stdscr)
            else: #Si la víbora de longitud x > 1 acaba de comer
              Posiciones = np.append(Posiciones,[0,0])
              Posiciones = Posiciones.reshape(int(len(Posiciones)/2),2)
              Comio = True
              stdscr.addstr(x,y,Objeto[0])
              var1, var2 = [0,0],[0,0]
              for i in range(len(Posiciones) - 1): #-1 porque aún no se le añadirá el nuevo segmento
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
              rectangle(stdscr, 0, 0, 12, 33) ###
              ImprimeComida(CasillaComida, stdscr)
          else:
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == True: #Si la víbora de longitud 1 da 1 paso luego de comer
              Comio = False
              stdscr.addstr(x,y,Objeto[0])
              stdscr.addstr(x+1,y,Objeto[0])
              Posiciones[1,0] = x+1
              Posiciones[1,1], Posiciones[0,1] = y, y #Para izquierda y derecha debe hacerse x, x y con los valores [x,1]
              Posiciones[0,0] = x #Ya tienen entonces asignados los valores posicionales, lo que servirá para el algoritmo de movimiento.         
            elif Posiciones[1,0] != 0 and Posiciones[1,1] != 0 and len(Posiciones) >= 2 and Comio == True: #Si la víbora de longitud x > 1 da 1 paso luego de comer ####              
              Comio = False
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones)):
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0])
              rectangle(stdscr, 0, 0, 12, 33)
              stdscr.addstr(Rand1, Rand2, "*") ##REVISAR
              stdscr.refresh()
            else:
              for i in range(2, len(Posiciones) - 1): #LA VÍBORA SE COME A SÍ MISMA 26/11: Funciona, ahora solo necesito implementarlo en el resto de direcciones.
                if Posiciones[i,0] == Posiciones[0,0]-1 and Posiciones[0,1] == Posiciones[i,1]: 
                  JuegoActivo = False
                  break
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
              rectangle(stdscr, 0, 0, 12, 33)
            stdscr.addstr(Rand1, Rand2, "*") 
            #stdscr.addstr(0, 35, str(len(Posiciones))) 
            stdscr.refresh()
        except: 
          rectangle(stdscr, 0, 0, 12, 33)
          JuegoActivo = False
    elif dir == "KEY_DOWN":
      if x == 12:
        JuegoActivo = False       
      else:
        if Posiciones[0,0] == Posiciones[1,0] - 1:
          dir = "KEY_UP"
        else:
          x += 1
          stdscr.clear()        
          if x == Rand1 and y == Rand2: #Comer y crecer
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == False: #Si la víbora de longitud 1 acaba de comer
              Comio = True
              stdscr.addstr(x,y,Objeto[0])
              ImprimeComida(CasillaComida, stdscr)
            else: #Si la víbora de longitud x > 1 acaba de comer
              Posiciones = np.append(Posiciones,[0,0])
              Posiciones = Posiciones.reshape(int(len(Posiciones)/2),2)
              Comio = True
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones) - 1): #-1 porque aún no se le añadirá el nuevo segmento
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
              ImprimeComida(CasillaComida, stdscr)
          else:
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == True: #Si la víbora de longitud 1 da 1 paso luego de comer
              Comio = False
              stdscr.addstr(x,y,Objeto[0])
              stdscr.addstr(x-1,y,Objeto[0])
              Posiciones[1,0] = x-1
              Posiciones[1,1], Posiciones[0,1] = y, y #Para izquierda y derecha debe hacerse x, x y con los valores [x,1]
              Posiciones[0,0] = x #Ya tienen entonces asignados los valores posicionales, lo que servirá para el algoritmo de movimiento.         
            elif Posiciones[1,0] != 0 and Posiciones[1,1] != 0 and len(Posiciones) >= 2 and Comio == True: #Si la víbora de longitud x > 1 da 1 paso luego de comer 
              Comio = False
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0])
              stdscr.addstr(Rand1, Rand2, "*") ##REVISAR
              stdscr.refresh()  
            else:  #POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(2, len(Posiciones) - 1): #LA VÍBORA SE COME A SÍ MISMA
                if Posiciones[0,0]+1 == Posiciones[i,0] and Posiciones[0,1] == Posiciones[i,1]:
                  JuegoActivo = False
                  break
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
            rectangle(stdscr, 0, 0, 12, 33)
            stdscr.addstr(Rand1, Rand2, "*") ##REVISAR. Por qué Rand1 y Rand2 pasan a valer cero? 30/10/2023
            stdscr.refresh() 
    elif dir == "KEY_LEFT":
      if Posiciones[0,1] == Posiciones[1,1] + 1:
        dir = "KEY_RIGHT"
      else:
        try:
          y -= 1
          stdscr.clear()
          if x == Rand1 and y == Rand2: #Comer y crecer
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == False: #Si la víbora de longitud 1 acaba de comer
              Comio = True
              stdscr.addstr(x,y,Objeto[0])
              ImprimeComida(CasillaComida, stdscr)
            else: #Si la víbora de longitud x > 1 acaba de comer
              Posiciones = np.append(Posiciones,[0,0])
              Posiciones = Posiciones.reshape(int(len(Posiciones)/2),2)
              Comio = True
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones) - 1): #-1 porque aún no se le añadirá el nuevo segmento
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
              ImprimeComida(CasillaComida, stdscr)
          else:
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == True: #Si la víbora de longitud 1 da 1 paso luego de comer
              Comio = False
              stdscr.addstr(x,y,Objeto[0])
              stdscr.addstr(x-1,y,Objeto[0])
              Posiciones[1,1] = y+1
              Posiciones[1,0], Posiciones[0,0] = x, x #Para izquierda y derecha debe hacerse x, x y con los valores [x,1]
              Posiciones[0,1] = y #Ya tienen entonces asignados los valores posicionales, lo que servirá para el algoritmo de movimiento.         
            elif Posiciones[1,0] != 0 and Posiciones[1,1] != 0 and len(Posiciones) >= 2 and Comio == True: #Si la víbora de longitud x > 1 da 1 paso luego de comer ####
              Comio = False
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0])
              stdscr.addstr(Rand1, Rand2, "*") ##REVISAR
              stdscr.refresh()
            else:  #POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(2, len(Posiciones) - 1): #LA VÍBORA SE COME A SÍ MISMA
                if Posiciones[0,0] == Posiciones[i,0] and Posiciones[0,1]-1 == Posiciones[i,1]:
                  JuegoActivo = False
                  break
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
            rectangle(stdscr, 0, 0, 12, 33)
            stdscr.addstr(Rand1, Rand2, "*") ##REVISAR. Por qué Rand1 y Rand2 pasan a valer cero? 30/10/2023
            stdscr.refresh()
        except: 
          rectangle(stdscr, 0, 0, 12, 33)
          JuegoActivo = False
    elif dir == "KEY_RIGHT":  ####22/10: Cuando inicia el juego crecer a 2 segmentos y la comida no vuelva a aparecer
      if Posiciones[0,1] == Posiciones[1,1] - 1:
        dir = "KEY_LEFT"
      else:
        if y == 33:
            JuegoActivo = False
        else:
          y += 1
          stdscr.clear()
          if x == Rand1 and y == Rand2: #Comer y crecer
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == False: #Si la víbora de longitud 1 acaba de comer
              Comio = True
              stdscr.addstr(x,y,Objeto[0])
              ImprimeComida(CasillaComida, stdscr)
            else: #Si la víbora de longitud x > 1 acaba de comer
              Posiciones = np.append(Posiciones,[0,0])
              Posiciones = Posiciones.reshape(int(len(Posiciones)/2),2)
              Comio = True
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones) - 1): #-1 porque aún no se le añadirá el nuevo segmento
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA
            ImprimeComida(CasillaComida, stdscr)
          else:
            if Posiciones[1,0] == 0 and Posiciones[1,1] == 0 and len(Posiciones) == 2 and Comio == True: #Si la víbora de longitud 1 da 1 paso luego de comer
              Comio = False
              stdscr.addstr(x,y,Objeto[0])
              stdscr.addstr(x-1,y,Objeto[0])
              Posiciones[1,1] = y-1
              Posiciones[1,0], Posiciones[0,0] = x, x #Para izquierda y derecha debe hacerse x, x y con los valores [x,1]
              Posiciones[0,1] = y #Ya tienen entonces asignados los valores posicionales, lo que servirá para el algoritmo de movimiento.         
            elif Posiciones[1,0] != 0 and Posiciones[1,1] != 0 and len(Posiciones) >= 2 and Comio == True: #Si la víbora de longitud x > 1 da 1 paso luego de comer ####
              Comio = False
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0])
              #stdscr.addstr(Rand1, Rand2, "*") ##REVISAR
              #stdscr.refresh()  
            else:  #POR ACÁ ES QUE ESTÁ EL ERROR QUE HAY QUE CORREGIR A LA FECHA DEL 26/09
              for i in range(2, len(Posiciones) - 1): #LA VÍBORA SE COME A SÍ MISMA
                if Posiciones[0,0] == Posiciones[i,0] and Posiciones[0,1]+1 == Posiciones[i,1]:
                  JuegoActivo = False
                  break
              var1, var2 = [0,0],[0,0]  #MOVIMIENTO DE LA VÍBORA
              for i in range(len(Posiciones)): 
                if i == 0:
                  var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                  Posiciones[i] = [x,y]
                else:
                  if i % 2 == 0:
                    var1[0], var1[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var2
                  else:
                    var2[0], var2[1] = Posiciones[i,0], Posiciones[i,1]
                    Posiciones[i] = var1
                stdscr.addstr(Posiciones[i,0],Posiciones[i,1],Objeto[0]) #Y ACÁ TERMINA EL ALGORITMO DE MOVIMIENTO DE LA VÍBORA            
            rectangle(stdscr, 0, 0, 12, 33)
            stdscr.addstr(Rand1, Rand2, "*") ##REVISAR. Por qué Rand1 y Rand2 pasan a valer cero? 30/10/2023
            stdscr.refresh()
    time.sleep(0.5)
  GameOver(stdscr)
    
curses.wrapper(main)
