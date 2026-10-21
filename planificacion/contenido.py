# -*- coding: utf-8 -*-
"""
Contenido de la Planificacion de Programacion con Python · 1ro a 3ro de Secundaria
Criso
Fuente unica de verdad: de aqui se generan la pagina web y el .docx
"""

DOCENTE = "Criso"
ESCUELA = "El centro"
AREA = "Área de Tecnología / Informática"
TITULO = "Programación y Pensamiento Computacional con Python"
SUBTITULO = "1ro a 3ro de Secundaria · 12 semanas por curso · Sesiones de 45–50 minutos"

PALETA = {
    "navy":  "14213D",
    "n1":    "2563EB", "n1_bg": "EFF6FF",
    "n2":    "16A34A", "n2_bg": "F0FDF4",
    "n3":    "7C3AED", "n3_bg": "F5F3FF",
    "co":    "EA580C", "co_bg": "FFF7ED",
    "gris":  "F8FAFC", "gris2": "FAFBFC",
    "borde": "E2E8F0", "texto": "1E293B", "suave": "64748B",
}

# ---------------------------------------------------------------- HORARIO
HORARIO_CLASES = [
    ("1ro A", "Miércoles", "8:00 – 8:50",   "50 min"),
    ("1ro B", "Jueves",    "11:45 – 12:30", "45 min"),
    ("1ro C", "Viernes",   "9:40 – 10:25",  "45 min"),
    ("2do A", "Jueves",    "8:00 – 8:50",   "50 min"),
    ("2do B", "Viernes",   "8:00 – 8:50",   "50 min"),
    ("2do C", "Jueves",    "8:50 – 9:40",   "50 min"),
    ("3ro A", "Viernes",   "8:50 – 9:40",   "50 min"),
    ("3ro B", "Jueves",    "10:55 – 11:45", "50 min"),
    ("3ro C", "Jueves",    "12:30 – 13:15", "45 min"),
]

HORARIO_COCU = [
    ("Maker · Primaria 1.º–3.º", "Lunes",     "14:15 – 15:45", "90 min"),
    ("Maker · Secundaria A",     "Martes",    "14:15 – 15:45", "90 min"),
    ("Maker · Secundaria B",     "Miércoles", "14:15 – 15:45", "90 min"),
    ("Maker · Secundaria C",     "Jueves",    "14:15 – 15:45", "90 min"),
]

HORARIO_NOTA = (
    "El jueves concentra 5 clases seguidas (2do A, 2do C, 3ro B, 1ro B y 3ro C) más el "
    "cocurricular de la tarde. Es el día que exige tener el material preparado desde el "
    "miércoles: mismo reto proyectado, mismas plantillas abiertas, cero improvisación."
)

# ------------------------------------------------- ESTRUCTURA DE LA CLASE
ESTRUCTURA_CLASE = [
    ("Enganche",        "0 – 5",   "0 – 5",   "Un reto, una pregunta o la demo del resultado final del día. Nunca empezar con teoría."),
    ("Concepto",        "5 – 13",  "5 – 13",  "Demo en vivo de máximo 8 minutos. Se explica solo lo necesario para que puedan intentarlo."),
    ("Práctica y reto", "13 – 38", "13 – 43", "El estudiante construye. En los bloques de 50 min entra además el reto «sube de nivel»."),
    ("Cierre",          "38 – 45", "43 – 50", "Una o dos pantallas compartidas, la evidencia del día y una pregunta de comprensión."),
]

ESTRUCTURA_REGLA = (
    "Regla que sostiene la compresión de 60 a 45 minutos: el concepto nunca pasa de 8 minutos. "
    "Todo lo demás se aprende construyendo, probando, equivocándose y corrigiendo."
)

# ----------------------------------------------------- ENTORNO Y CHULETA
# Desde el 14-09-2026 el curso es en Python en los tres niveles. Python corre
# en el navegador con PyScript, dentro del editor de la propia clase: el
# laboratorio sigue sin instalar nada. Trinket, que era la otra opción, cerró
# el 31-08-2026.
# La clase publicada. Sin la variable, apunta a la app en local.
import os
SITIO = os.environ.get("SITIO_CLASE", "http://localhost:3000").rstrip("/")

PLANTILLA = "Editor de Python de la clase"

ENTORNO = [
    ("Editor de la clase", "el sitio de la clase", "Herramienta principal de 1ro a 3ro: está dentro de cada presentación, con pestañas de Python, HTML y CSS y el resultado al lado. Lo que escriben se guarda con su nota al pulsar Ejecutar."),
    ("pyscript.com", "pyscript.com", "Plan B si el editor de la clase falla en el laboratorio: el editor oficial de PyScript, con index.html y main.py separados. Pide cuenta."),
    ("Teachable Machine", "teachablemachine.withgoogle.com", "Inteligencia artificial sin código ni cuenta: se entrena en el navegador con la cámara o el micrófono. Los tres grados, en las semanas 10 y 11."),
    ("DevTools (F12)", "Navegador", "Inspector para el enganche del periódico y consola donde PyScript enseña sus errores."),
    ("Archivo .html local", "Bloc de notas + navegador", "Plan C: la misma plantilla guardada como .html. Necesita internet igual, porque PyScript se descarga de pyscript.net."),
]

# Antes era la tabla de traducción del plan original en Python a JavaScript.
# Con el curso ya en Python, lo útil es la chuleta de lo que se escribe para
# que el programa hable con la página. Todo el material usa estas formas y no
# otras: dos maneras de hacer lo mismo en la semana 5 es una clase perdida.
PYTHON_EN_PAGINA = [
    ("Mostrar algo rápido",                  'display("Hola")'),
    ("Responder a un clic",                  '@when("click", "#boton")  ·  def jugar(evento):'),
    ("Leer lo que escribieron en una caja",  'document.querySelector("#nombre").value'),
    ("Cambiar un texto de la página",        'document.querySelector("#salida").innerText = "Ganaste"'),
    ("Cambiar una variable desde un botón",  "global puntos  ·  al principio de la función"),
    ("Convertir lo de la caja en número",    'int(document.querySelector("#edad").value)'),
    ("Un número al azar",                    "random.randint(1, 6)  ·  random.choice(opciones)"),
    ("Guardar varios datos",                 "puntos = []  ·  puntos.append(10)  ·  len(puntos)"),
    ("Que no se borre al cerrar la página",  'window.localStorage.setItem("datos", texto)'),
    ("Pasar datos a texto y de vuelta",      "json.dumps(datos)  ·  json.loads(texto)"),
    ("Usar mi modelo de IA",                 "El fragmento de Teachable Machine, la única pieza en JavaScript, deja window.clase y window.confianza. Python los lee y decide."),
]


# ------------------------------------------------------------- NIVELES
def S(n, tema, objetivo, enganche, concepto, practica, reto, cierre, extra, recursos, evidencia):
    return {
        "n": n, "tema": tema, "objetivo": objetivo,
        "bloques": [
            ("0 – 5",   "Enganche", enganche),
            ("5 – 13",  "Concepto", concepto),
            ("13 – 38", "Práctica", practica),
            ("13 – 38", "Reto",     reto),
            ("38 – 45", "Cierre",   cierre),
        ],
        "extra": extra, "recursos": recursos, "evidencia": evidencia,
    }

PRIMERO = {
    "id": "1ro", "color": "n1",
    "titulo": "1RO DE SECUNDARIA",
    "nombre": "Programar con Python, paso a paso y jugando",
    "resumen": "Los mismos doce temas de programación que 2do y 3ro, al ritmo de quien empieza: variables, ciclos, decisiones, listas y funciones, y al final una página con IA.",
    "proposito": (
        (
        "Aprender a programar desde cero y divertirse haciéndolo. La ruta es la misma en los tres grados: "
        "la semana 2 son las variables, y de ahí siguen los ciclos, las decisiones, las listas y las "
        "funciones, cada semana con teoría corta, retos y dos juegos. Después la página empieza a "
        "responder (botones, cajas y azar), se le da forma con HTML y CSS, y el curso cierra entrenando "
        "un modelo de IA sin código, metiéndolo en su página y presentando un proyecto propio."
    )
    ),
    "fases": [
        {"titulo": "Primeros pasos", "semanas": (1, 2), "nota": "Programar es dar órdenes en orden, y las variables guardan lo que el programa necesita recordar."},
        {"titulo": "Python que hace cosas", "semanas": (3, 6), "nota": "Ciclos, decisiones, listas y funciones: con esto ya se puede construir casi cualquier cosa."},
        {"titulo": "La página responde", "semanas": (7, 9), "nota": "Botones, cajas, azar y una página con estructura y estilo propios."},
        {"titulo": "IA y proyecto", "semanas": (10, 12), "nota": "Entrenar un modelo sin código, meterlo en su página y presentar el proyecto."},
    ],
    "semanas": []}


SEGUNDO = {
    "id": "2do", "color": "n2",
    "titulo": "2DO DE SECUNDARIA",
    "nombre": "Programar con Python, con retos de más",
    "resumen": "La misma ruta de 1ro —variables, ciclos, decisiones, listas, funciones, la página y la IA— con retos extra cada semana y un proyecto que vive dentro de su propia página.",
    "proposito": (
        (
        (
        "Los mismos doce temas que 1ro, con la vara un poco más alta. Cada clase trae una diapositiva "
        "«Sube de nivel» con retos extra: el f-string, el while, el and, las listas paralelas, las "
        "funciones que devuelven un valor con return y la lectura de lo que escribe el usuario. El "
        "proyecto final no es un juego suelto: va dentro de la página que construyeron, con su modelo "
        "de IA conectado."
    )
    )
    ),
    "fases": [
        {"titulo": "Primeros pasos", "semanas": (1, 2), "nota": "Programar es dar órdenes en orden, y las variables guardan lo que el programa necesita recordar."},
        {"titulo": "Python que hace cosas", "semanas": (3, 6), "nota": "Ciclos, decisiones, listas y funciones: con esto ya se puede construir casi cualquier cosa."},
        {"titulo": "La página responde", "semanas": (7, 9), "nota": "Botones, cajas, azar y una página con estructura y estilo propios."},
        {"titulo": "IA y proyecto", "semanas": (10, 12), "nota": "Entrenar un modelo sin código, meterlo en su página y presentar el proyecto."},
    ],
    "semanas": []}


TERCERO = {
    "id": "3ro", "color": "n3",
    "titulo": "3RO DE SECUNDARIA",
    "nombre": "Programar con Python para resolver problemas reales",
    "resumen": "La misma ruta de 1ro y 2do con los retos más exigentes: acumuladores, filtros, assert, validación y un umbral de confianza para la IA, y un proyecto que resuelve algo de la escuela.",
    "proposito": (
        (
        (
        "Los mismos doce temas, con los retos más exigentes del curso. En «Sube de nivel» entran la "
        "división entera y el resto, los acumuladores y promedios, combinar and con or, filtrar listas, "
        "probar funciones con assert, validar lo que llega de una caja y decidir con un umbral de "
        "confianza cuándo hacerle caso al modelo. El proyecto final resuelve una necesidad real de la "
        "escuela y se presenta con sus pruebas hechas."
    )
    )
    ),
    "fases": [
        {"titulo": "Primeros pasos", "semanas": (1, 2), "nota": "Programar es dar órdenes en orden, y las variables guardan lo que el programa necesita recordar."},
        {"titulo": "Python que hace cosas", "semanas": (3, 6), "nota": "Ciclos, decisiones, listas y funciones: con esto ya se puede construir casi cualquier cosa."},
        {"titulo": "La página responde", "semanas": (7, 9), "nota": "Botones, cajas, azar y una página con estructura y estilo propios."},
        {"titulo": "IA y proyecto", "semanas": (10, 12), "nota": "Entrenar un modelo sin código, meterlo en su página y presentar el proyecto."},
    ],
    "semanas": []}

NIVELES = [PRIMERO, SEGUNDO, TERCERO]


# --------------------------------------------------------- SEMANA 1
SEMANA1_INTRO = (
    "La primera semana es de presentación, pero nunca de solo hablar. Cada nivel tiene un bloque fijo de "
    "20 minutos y una dinámica preparada de 20 a 25 minutos que se lleva el resto de la clase. Si el bloque "
    "de presentación se acorta, la dinámica se estira; si sobra tiempo, se usa el reto extra. Nadie sale sin "
    "haber hecho algo con las manos. Además, cada nivel tiene un banco de juegos cortos para elegir según "
    "el grupo: para despertar a uno apagado, para uno grande o para cuando sobran diez minutos."
)

SEMANA1_FIJO = [
    ("0 – 5",   "Quién soy",     "Presentación visual: quién eres, qué construyes fuera del aula y qué van a construir ellos este año. Muestra el resultado final del curso, no el temario."),
    ("5 – 10",  "Quiénes son",   "Ronda rápida: nombre + una cosa que usan todos los días que funciona con código. Nadie repite lo del anterior."),
    ("10 – 15", "Cómo trabajamos y cómo se evalúa", "Las tres reglas del laboratorio y el ciclo del curso: construir → probar → equivocarse → corregir → explicar. El error no se castiga, se documenta. Los cinco componentes de la nota en la pizarra: el proyecto no es lo único que cuenta."),
    ("15 – 20", "La idea del día",   "Cinco minutos de concepto con demo antes de la dinámica: qué es un algoritmo en 1ro, las tres capas de una web en 2do, del problema al programa en 3ro."),
]

SEMANA1_DINAMICAS = [
    {"nivel": "1RO", "color": "n1", "nombre": "Programa a un humano",
     "duracion": "20 – 25 min",
     "desc": "Un voluntario hace de robot y solo obedece las tarjetas AVANZA, GIRA IZQUIERDA, GIRA DERECHA, REPITE y SI HAY OBSTÁCULO. Primero lo modelas tú con el robot delante de todos; luego, en parejas, uno escribe la ruta en tarjetas hasta una meta marcada con cinta y el otro la ejecuta. El robot obedece literalmente: si la instrucción es ambigua, se choca, y la pareja marca la tarjeta que falló, la cambia y vuelve a intentar. Son las mismas órdenes que en la semana 3 se escriben en Python.",
     "materiales": "Tarjetas de comandos impresas (un juego por pareja), cinta adhesiva para la salida y la meta, mochilas o sillas como obstáculos.",
     "cierre": "«¿Qué instrucción falló y por qué la computadora no la adivinó?». Ahí queda instalada la definición de algoritmo.",
     "extra": "Repetir la ruta en 6 instrucciones o menos usando REPITE.",
     "guion": [
         ("0 – 5",   "Quién soy",           "Presentación visual: quién eres, qué construyes fuera del aula y qué van a construir ellos este año. Muestra un juego terminado en Python, no el temario."),
         ("5 – 10",  "Quiénes son",         "Ronda rápida: nombre + un juego o una app que usan todos los días. Nadie repite lo del anterior."),
         ("10 – 15", "Reglas y evaluación", "Las tres reglas del laboratorio, el ciclo construir → probar → equivocarse → corregir → explicar, y los cinco componentes de la nota con sus pesos en la pizarra."),
         ("15 – 20", "Algoritmo con demo",  "Pregunta: «¿la computadora entiende lo que uno quiere, o solo lo que uno le dice?». Define algoritmo y haz la demo: un voluntario te dicta 4 pasos para llegar a la puerta y los ejecutas al pie de la letra, incluido el que falla."),
         ("20 – 38", "Programa a un humano", "Explica las tarjetas en 2 minutos con el robot delante. Las parejas escriben su ruta, la ejecutan, marcan la tarjeta que falló y la corrigen. En el minuto 32, dos parejas la ejecutan frente a todos."),
         ("38 – 43", "Juego o diagnóstico", "Si el grupo necesita energía, un juego corto del banco. Si ya está listo, proyecta el QR del diagnóstico de entrada y lo responden ahí mismo."),
         ("43 – 45", "Cierre",              "«¿Qué instrucción falló y por qué la computadora no la adivinó?». Una respuesta en voz alta y a la puerta."),
     ],
     "juegos": [
         ("Adivina mi número", "8 – 10 min",
          "Escribes un número del 1 al 50 en un papel tapado. La clase propone números por turnos y solo respondes «más alto» o «más bajo»; un estudiante cuenta los intentos en la pizarra. Segunda ronda: un estudiante piensa el número y otro adivina frente a todos. Gana quien acierta en menos intentos. Deja que descubran la estrategia de partir por la mitad: con 50 números nunca hacen falta más de 6 intentos. Enseña a comparar y decidir, y es el juego que programan en la semana 7.",
          "Pizarra, marcador y un papel.",
          "Grupo apagado: no pide preparación y todos quieren decir un número."),
         ("Piedra, papel o tijera con reglas SI…ENTONCES", "10 min",
          "Equipos de tres reciben un juego de tarjetas con las reglas escritas en la forma «SI yo saco piedra Y la máquina saca tijera ENTONCES gano yo». El juego está incompleto a propósito: le falta el empate. Cada equipo nombra un árbitro robot que solo puede decidir partidas leyendo las tarjetas; el resto juega contra él. Cuando dos sacan lo mismo, el robot se queda congelado. Gana el primer equipo que encuentra el caso que falta y escribe la tarjeta. Enseña que un programa tiene que cubrir todos los casos, y anticipa la semana 8.",
          "Un juego de reglas incompleto impreso por equipo, tarjetas en blanco.",
          "Sobran 10 min después de la dinámica."),
         ("Simón literal", "8 min",
          "Todos de pie. Das órdenes como en Simón dice, pero la clase es una computadora: si la orden es clara, se ejecuta; si es ambigua, lo correcto es quedarse quieto y decir «error». «Levanta la mano» (¿cuál?), «Toca tu cabeza tres veces» (clara), «Siéntate cuando termine» (¿cuando termine qué?). Quien adivina lo que quisiste decir en vez de obedecer, se sienta. Después un voluntario hace de Simón y la clase le caza las ambigüedades. Gana el último de pie. Enseña que la computadora no rellena lo que falta.",
          "Ninguno.",
          "Grupo grande: juega todo el salón a la vez, en su sitio."),
         ("Dados y puntos", "10 min",
          "Cuatro equipos y un dado. En la pizarra, un marcador PUNTOS = 0 por equipo y la regla escrita: SI sale 6, PUNTOS = PUNTOS + 10; SI sale 1, PUNTOS = 0; SI NO, PUNTOS = PUNTOS + lo que salió. Cada equipo elige una «memoria», la única persona que puede borrar y reescribir su número, y siempre en voz alta. Cinco rondas; gana el equipo con más puntos. Enseña que una variable es un nombre con un valor que se reemplaza y que el azar hace el juego; anticipa las semanas 4 y 6.",
          "Un dado grande o uno normal, pizarra.",
          "Grupo distraído: el marcador de la pizarra los tiene mirando al frente."),
         ("Bug en la ruta", "10 min",
          "Dibuja en la pizarra una cuadrícula de 5 por 5 con salida, meta y dos obstáculos, y al lado un algoritmo de 8 tarjetas que casi funciona: tiene un giro al revés y un REPITE que da una vuelta de más. En parejas, siguen la ruta con el dedo paso a paso y marcan la línea exacta donde el robot se choca. Gana la primera pareja que dice la línea y la arregla cambiando una sola tarjeta. Enseña a depurar siguiendo la ejecución en vez de reescribirlo todo.",
          "Cuadrícula dibujada en la pizarra o impresa por pareja, el algoritmo con errores preparado.",
          "El grupo terminó la ruta antes de tiempo y conviene bajar la energía."),
         ("Relevos de instrucciones", "12 min",
          "Equipos de cinco en fila. Sobre tu escritorio hay una figura sencilla pintada en una cuadrícula (una casa, una flecha). Por turnos, cada estudiante va, mira la figura 5 segundos, vuelve y escribe una sola instrucción en la hoja del equipo: AVANZA 2, GIRA DERECHA, PINTA. Nadie habla. Al terminar, un estudiante de otro equipo ejecuta la hoja pintando en una cuadrícula en blanco. Gana el equipo cuya figura sale igual con menos instrucciones. Enseña que un algoritmo se construye por partes y que cada paso depende del anterior.",
          "Figura en cuadrícula impresa, hojas cuadriculadas, marcadores.",
          "Grupo con mucha energía: se mueven, pero por turnos y en silencio."),
     ]},

    {"nivel": "2DO", "color": "n2", "nombre": "Hackea el periódico",
     "duracion": "20 – 25 min",
     "desc": "Todos abren un periódico digital y pulsan F12. Guiados paso a paso: cambiar el titular desde el inspector, que es la estructura, y cambiar el color de fondo desde los estilos, que es el estilo. Para la tercera capa, el comportamiento, proyectas el editor de la clase: una portada con un botón que al tocarlo cambia el titular desde Python, con @when y document.querySelector(\"#titular\").innerText. Es el truco que engancha al grupo en la primera clase y explica las tres capas de la web sin una sola diapositiva.",
     "materiales": "Navegador con DevTools, proyector y el editor de la clase con la portada y el botón preparados. Acuerdo previo: nada ofensivo, se hace captura y se cierra.",
     "cierre": "«¿El periódico cambió para todo el mundo? ¿Por qué no?». De ahí sale la idea de que el navegador tiene su propia copia.",
     "extra": "Cambiar también una imagen de la portada desde el inspector.",
     "guion": [
         ("0 – 5",   "Quién soy",            "Presentación visual: quién eres, qué construyes fuera del aula y una web tuya real en pantalla: «al final del curso ustedes van a tener la suya, programada con Python»."),
         ("5 – 10",  "Quiénes son",          "Ronda rápida: nombre + una página o app que usan todos los días. Nadie repite lo del anterior."),
         ("10 – 15", "Reglas y evaluación",  "Las tres reglas del laboratorio, el ciclo construir → probar → equivocarse → corregir → explicar, y los cinco componentes de la nota con sus pesos en la pizarra."),
         ("15 – 20", "Tres capas con demo",  "La analogía de la casa: estructura, pintura y electricidad. Demo en el editor de la clase: la misma portada sin estilos, con estilos y con un botón que hace algo."),
         ("20 – 38", "Hackea el periódico",  "F12 en un periódico digital: titular, color de fondo y captura. En el minuto 30 proyectas el editor de la clase y cambias el titular desde Python con el botón. Dos parejas muestran su captura."),
         ("38 – 43", "Juego o diagnóstico",  "Si el grupo necesita energía, un juego corto del banco. Si ya está listo, proyecta el QR del diagnóstico de entrada y lo responden ahí mismo."),
         ("43 – 45", "Cierre",               "«¿El periódico cambió para todo el mundo? ¿Por qué no?». Una respuesta en voz alta y a la puerta."),
     ],
     "juegos": [
         ("Adivina qué muestra Python", "10 min",
          "Proyectas el editor de la clase con cinco fragmentos cortos, uno por vez y sin pulsar Ejecutar: un display con texto, una suma de números, una suma de dos textos entre comillas, un f-string con una variable y un botón que cambia un titular. Cada estudiante escribe en papel qué va a aparecer en la página. Ejecutas y se cuentan aciertos; gana quien suma más. La suma de \"2\" + \"3\" es la trampa que nadie olvida. Enseña a leer código y predecir antes de ejecutar, y presenta Python sin explicar Python.",
          "Editor de la clase con los cinco fragmentos preparados, papel.",
          "Grupo que ya mira el celular: todos contra la pantalla grande."),
         ("Hackea el periódico: modo reto", "10 – 12 min",
          "La dinámica convertida en competencia. Proyectas cinco misiones con puntos: cambiar el titular (1), cambiar el color de fondo (1), cambiar el nombre de un autor (2), cambiar una foto por otra (3) y esconder un anuncio (3). Parejas con F12 y diez minutos; cada misión cuenta solo con captura. Gana la pareja con más puntos y, en empate, el titular más creativo que respete el acuerdo. Enseña a moverse por el inspector y a decidir qué capa hay que tocar en cada misión.",
          "Navegador con DevTools, lista de misiones proyectada.",
          "Sobran 10 min o el grupo terminó la dinámica muy rápido."),
         ("¿IA o humano?", "10 min",
          "Proyectas diez piezas, una por vez: textos cortos, dibujos y fotos, unas hechas por personas y otras generadas con IA. Cada estudiante levanta la mano abierta si cree que es humano y el puño si cree que es IA. Tras cada una revelas el origen y la pista que la delata, o por qué no hay pista. Cada uno lleva su cuenta; gana quien acierta más. Enseña a desconfiar de lo que se ve y abre la conversación sobre para qué sirve la IA y para qué no.",
          "Presentación con diez piezas y su origen anotado.",
          "Grupo grande: participa todo el salón a la vez y no hace falta computadora."),
         ("Enseña a la máquina", "12 min",
          "Desenchufado. Un voluntario hace de máquina y sale del aula mientras el grupo rotula 12 tarjetas con dibujos de frutas y verduras: son sus ejemplos. La máquina vuelve, estudia los ejemplos un minuto y clasifica 6 tarjetas nuevas sin rótulo, diciendo en voz alta en qué se fija. Segunda ronda con otra máquina y ejemplos malos a propósito, todas las frutas rojas: falla con el banano. Gana el equipo que arma el conjunto de ejemplos con el que su máquina acierta más. Enseña que una IA aprende de ejemplos y que ejemplos pobres dan respuestas pobres; es la base de Teachable Machine en la semana 9.",
          "18 tarjetas con dibujos o fotos de frutas y verduras.",
          "Cayó internet o el laboratorio: no necesita pantalla."),
     ]},

    {"nivel": "3RO", "color": "n3", "nombre": "Hackea el periódico + ¿Qué app harías?",
     "duracion": "20 – 25 min",
     "desc": "Misma dinámica de F12 pero más corta (10 min), cerrada con el editor de la clase, donde un botón de Python cambia el titular. Sigue una lluvia de ideas: en equipos listan tres problemas reales de la escuela que se podrían resolver con una aplicación, con datos o con un modelo de IA. Se pegan en la pizarra y se agrupan por tema.",
     "materiales": "Navegador con DevTools, editor de la clase con la portada y el botón, post-its o tarjetas, pizarra.",
     "cierre": "Las ideas quedan fotografiadas: son el banco de ideas del que saldrán los proyectos de la semana 11.",
     "extra": "Cada equipo defiende en 30 segundos cuál de sus ideas es la más viable.",
     "guion": [
         ("0 – 5",   "Quién soy",              "Presentación visual: quién eres, qué construyes fuera del aula y un proyecto real con datos o IA en pantalla. Muestra el resultado final del curso, no el temario."),
         ("5 – 10",  "Quiénes son",            "Ronda rápida: nombre + una app que les resuelve algo y una que les molesta. Nadie repite lo del anterior."),
         ("10 – 15", "Reglas y evaluación",    "Las tres reglas del laboratorio, el ciclo construir → probar → equivocarse → corregir → explicar, y los cinco componentes de la nota con sus pesos en la pizarra."),
         ("15 – 20", "Del problema al programa", "Plantea sin código: «¿cuánto gastó cada curso en la excursión y quién gastó más?». Separa en la pizarra entrada, proceso y salida, y muestra en el editor de la clase las tres líneas de Python que lo resuelven."),
         ("20 – 30", "Hackea el periódico",    "F12 en un periódico digital: titular y color de fondo, con captura. Cierra proyectando el editor de la clase: un botón de Python cambia el titular."),
         ("30 – 40", "¿Qué app harías?",       "En equipos, tres problemas reales de la escuela en post-its, uno por papel. Se pegan en la pizarra, se agrupan por tema y cada equipo defiende en 30 segundos su idea más viable."),
         ("40 – 43", "Juego o diagnóstico",    "Si el grupo necesita energía, un juego corto del banco. Si ya está listo, proyecta el QR del diagnóstico de entrada y lo responden ahí mismo."),
         ("43 – 45", "Cierre",                 "Foto de la pizarra: «esto es el banco de ideas de la semana 11». A la puerta."),
     ],
     "juegos": [
         ("Adivina qué muestra Python", "10 – 12 min",
          "Cinco fragmentos en el editor de la clase, uno por vez y sin pulsar Ejecutar, con más trampa que en 2do: una lista a la que se le hace append y se muestra len, un for que acumula un total, un int() sobre un texto de una caja, una comparación con == entre \"5\" y 5, y un if dentro de un for. Cada estudiante escribe su predicción en papel. Ejecutas: acertar vale 1 punto y explicar la línea que causa la sorpresa vale otro. Gana quien suma más. Enseña a trazar la ejecución y a leer tipos de dato sin ver el resultado.",
          "Editor de la clase con los cinco fragmentos preparados, papel.",
          "Grupo que llega dando por sabido todo: los baja a tierra en diez minutos."),
         ("Hackea el periódico: modo reto", "12 min",
          "Misiones con puntos pensadas para ir más allá del titular: cambiar la tipografía de toda la portada con una sola regla de estilo (2), esconder todos los anuncios a la vez (3), ver la portada en modo celular con el modo dispositivo y capturar qué se rompe (2), averiguar en la pestaña Red cuánto pesa la página (3) y encontrar en Application qué datos guarda de ti (3). Parejas, diez minutos, cada misión con captura. Gana la pareja con más puntos. Enseña que una página es estructura, estilo, comportamiento y también datos que viajan y se guardan.",
          "Navegador con DevTools, lista de misiones proyectada.",
          "Sobran 10 min o el grupo terminó la dinámica muy rápido."),
         ("¿IA o humano?", "12 min",
          "Diez piezas proyectadas (textos, dibujos y fotos) y voto con mano abierta para humano y puño para IA. Un estudiante anota en la pizarra, por pieza, cuántos votaron cada cosa. Al final revelas los orígenes y la clase calcula el porcentaje de aciertos por tipo: ¿qué detectamos peor, el texto, el dibujo o la foto? Cierra con un caso de video falsificado de una persona famosa. Gana quien acierta más, pero el punto es la tabla. Enseña a convertir una intuición en datos y a hablar de los límites y los riesgos de la IA.",
          "Presentación con diez piezas y su origen anotado, pizarra para la tabla.",
          "Grupo grande: participa todo el salón y se analiza entre todos."),
         ("Enseña a la máquina", "15 min",
          "Un experimento con datos, desenchufado. Dos equipos preparan ejemplos rotulados para su «máquina», un voluntario que sale mientras tanto: el equipo A con 12 ejemplos variados de frutas y verduras, el B con 12 ejemplos donde todas las frutas son rojas. Las dos máquinas clasifican el mismo conjunto de prueba de 10 tarjetas y se anotan los aciertos en una tabla. Luego se cambia una sola cosa (6 ejemplos en vez de 12) y se repite. Gana el equipo cuya máquina acierta más, pero se discute qué pesó más, la cantidad o la variedad. Enseña sesgo, conjunto de entrenamiento y conjunto de prueba; en la semana 8 se repite el experimento con Teachable Machine y la cámara.",
          "28 tarjetas con dibujos o fotos, tabla de resultados en la pizarra.",
          "Cayó internet o el laboratorio, o sobran 15 min con un grupo que razona bien."),
     ]},
]


# ------------------------------------------------- BANCO DE DINÁMICAS
DINAMICAS_INTRO = (
    "Actividades cortas para cuando sobra tiempo en cualquier clase: terminaron antes, falló internet, "
    "el grupo llegó tarde o cayó el laboratorio. Están listas para usarse sin preparación previa. "
    "Conviene tener impresas las desenchufadas en una carpeta del escritorio."
)

DINAMICAS = [
    {"grupo": "Desenchufadas · sin computadora", "items": [
        ("El algoritmo del sándwich", "10 min", "1ro · 2do",
         "Un estudiante dicta paso a paso cómo hacer un sándwich y el docente lo ejecuta literalmente. Si dice «pon el pan», pone el paquete entero. La clase corrige hasta lograr instrucciones exactas.",
         "Precisión y ambigüedad en las instrucciones."),
        ("Dibuja lo que te dicto", "12 min", "Todos",
         "En parejas, espalda con espalda. Uno describe una figura geométrica y el otro la dibuja sin verla ni hacer preguntas. Al final comparan los dos dibujos.",
         "Especificación: lo que se entiende no es lo que se dijo."),
        ("Debugging humano", "10 min", "Todos",
         "Se proyecta un algoritmo cotidiano con tres errores escondidos (pasos fuera de orden, uno imposible, uno ambiguo). Gana el equipo que los encuentra todos primero y explica por qué.",
         "Localizar errores antes de ejecutar."),
        ("Ordena la clase", "12 min", "1ro · 2do",
         "Seis estudiantes con un número en la mano se ordenan siguiendo solo la regla «compárate con tu vecino e intercambien si están al revés». Es un algoritmo de ordenamiento ejecutado por personas.",
         "Un algoritmo es una regla simple repetida muchas veces."),
        ("Simón dice binario", "8 min", "1ro",
         "Mano arriba es 1, mano abajo es 0. En fila de cinco estudiantes forman números y la clase los traduce a decimal.",
         "Cómo cuenta realmente una computadora."),
        ("Teléfono descompuesto de instrucciones", "10 min", "Todos",
         "Una instrucción compleja pasa susurrada por cinco personas y la última la ejecuta. Se compara con la original.",
         "Por qué la ambigüedad rompe programas."),
    ]},
    {"grupo": "Digitales · con computadora", "items": [
        ("Encuentra el error", "10 min", "Todos",
         "Se proyecta un fragmento corto de Python con un bug: un if sin los dos puntos al final, una línea con la sangría corrida o una comilla sin cerrar. El primer equipo que lo señale y explique la causa gana el punto. Tres rondas de dificultad creciente; en la última Python no marca nada: el programa corre y hace otra cosa.",
         "Lectura de código y depuración."),
        ("Reto relámpago de CSS", "15 min", "2do · 3ro",
         "Un objetivo visual concreto y único: «una tarjeta con foto redonda, fondo degradado y un botón centrado». Quince minutos, y se muestran todas en pantalla grande.",
         "Aplicar CSS bajo presión de tiempo."),
        ("Cambia el titular", "10 min", "2do · 3ro",
         "F12 en un periódico digital. Nunca falla como enganche y sirve en cualquier momento del año para recordar las tres capas.",
         "Estructura, estilo y comportamiento son capas separadas."),
        ("Adivina qué muestra Python", "10 min", "Todos",
         "Cinco fragmentos cortos de Python proyectados. Cada uno escribe en papel qué va a aparecer en la página antes de pulsar Ejecutar. Se ejecutan y se cuentan aciertos.",
         "Trazar mentalmente la ejecución del código."),
        ("Reto de color", "10 min", "2do · 3ro",
         "Se proyecta un diseño y deben reproducir sus colores exactos usando el cuentagotas del inspector y aplicarlos a su propia página.",
         "Uso del inspector y precisión visual."),
        ("Speedrun del dado", "12 min", "1ro",
         "Reto cronometrado sobre la plantilla: tirar 10 dados y mostrar el total en la página con el menor número de líneas posible. Solo cuenta si funciona; se proyectan las tres versiones más cortas y la clase comprueba que el total cuadra.",
         "Optimización y uso de bucles."),
    ]},
    {"grupo": "Cierres rápidos · 5 minutos", "items": [
        ("Explícalo en una frase", "5 min", "Todos",
         "Cada estudiante resume el concepto del día en una sola oración, sin usar palabras técnicas. Se leen tres en voz alta.",
         "Comprensión real, no memorización."),
        ("Ticket de salida", "5 min", "Todos",
         "Un papel pequeño con dos líneas: qué aprendí hoy y qué no me quedó claro. Se entrega en la puerta y sirve para preparar la clase siguiente.",
         "Retroalimentación inmediata para el docente."),
        ("Enseña a tu compañero", "5 min", "Todos",
         "Dos minutos por turno explicando al de al lado qué hizo hoy y cómo. El que escucha debe hacer una pregunta.",
         "Consolidar explicando."),
    ]},
]

# ---------------------------------------------------------- EVALUACIÓN
EVALUACION_INTRO = (
    "Se conservan los mismos componentes y pesos de la planificación del área, para que los boletines y "
    "los registros no cambien. Lo que se evalúa es el proceso de resolución de problemas, no únicamente "
    "que el código funcione a la primera."
)

EVALUACION = [
    ("Retos prácticos semanales", "30%", "Aplicación de conceptos, intentos, correcciones y explicación de lo hecho."),
    ("Participación y trabajo en clase", "15%", "Colaboración, preguntas, uso responsable del tiempo y del equipo."),
    ("Ejercicios y pequeños programas", "20%", "Evidencias funcionales entregadas y progresión técnica visible."),
    ("Proyecto final", "25%", "Solución, organización del código, pruebas realizadas y mejora aplicada."),
    ("Presentación y explicación", "10%", "Capacidad de comunicar el problema, la lógica y lo aprendido."),
]

RUBRICA_CRITERIOS = ["Funciona", "Está probado", "El código se entiende", "Lo sabe explicar"]
RUBRICA_NIVELES = ["Inicial", "En proceso", "Logrado", "Destacado"]
RUBRICA = [
    ("Funciona", [
        "Se ejecuta pero no cumple el objetivo.",
        "Cumple el objetivo principal, falla en casos secundarios.",
        "Cumple el objetivo y maneja los casos previstos.",
        "Cumple el objetivo y resuelve bien casos que no estaban previstos.",
    ]),
    ("Está probado", [
        "No hay pruebas registradas.",
        "Probó solo el caso ideal.",
        "Registró varios casos, incluyendo uno que falló, y lo corrigió.",
        "Diseñó casos límite y de entrada inválida antes de programar.",
    ]),
    ("El código se entiende", [
        "Todo en un bloque, nombres sin sentido.",
        "Algo organizado, nombres poco claros.",
        "Dividido en funciones con nombres que dicen qué hacen.",
        "Modular, con responsabilidad única y sin repetición innecesaria.",
    ]),
    ("Lo sabe explicar", [
        "No logra explicar qué hace su programa.",
        "Explica qué hace, pero no por qué lo hizo así.",
        "Explica el problema, la solución y una decisión que tomó.",
        "Explica decisiones, alternativas descartadas y qué mejoraría después.",
    ]),
]

PROGRESION = "1ro: pienso como programador y hago juegos en Python  →  2do: construyo mi sitio web y lo programo con Python e IA  →  3ro: diseño soluciones con datos, Python e IA"


# ═════════════════════════════════════════════════════════════════════
#  KAHOOT · DIAGNÓSTICO DE ENTRADA
#
#  Tres Kahoots de entrada, uno por nivel, para jugar en la clase 1.
#
#  No miden lo que se va a enseñar: miden lo que el estudiante trae de antes.
#  Los tres grados siguen la misma ruta, así que los tres bancos preguntan lo
#  mismo con distinta exigencia:
#
#    1ro  no trae nada previo: solo pensamiento computacional. Cero sintaxis.
#    2do  el techo es la ruta de 1ro: display, variables, ciclos, decisiones,
#         listas, funciones, botones con @when, azar y los conceptos de
#         Teachable Machine.
#    3ro  el mismo techo, con las preguntas más exigentes: acumuladores,
#         filtros, return y lectura de lo que llega de una caja.
#
#  La banda es lo que convierte un porcentaje en un diagnóstico. Un 62 % no
#  dice nada; «banda 1 al 80 % y banda 3 al 20 %» dice que la lógica está y
#  el código no, y eso sí cambia cómo se dan las semanas 2 a 4.
# ═══════════════════════════════════════════════════════════════════════

KAHOOT_INTRO = (
    "Diagnóstico de entrada para jugar en la primera clase, después del bloque de concepto. "
    "Veinte preguntas, unos trece minutos con las transiciones. No puntúa para nota: mide de "
    "dónde parte el grupo, no cuánto sabe cada uno. Las secciones de 45 minutos —1ro B, 1ro C "
    "y 3ro C— juegan la variante corta de doce preguntas."
)

KAHOOT_BANDAS = [
    (1, "Base", "Conceptual en lenguaje cotidiano. Si esto falla, no se consolidó el nivel anterior."),
    (2, "Aplicación", "El mismo concepto puesto en una situación concreta. Separa nombrar de aplicar."),
    (3, "Código", "Un fragmento en pantalla. Es la banda que impide que el resultado se infle."),
]

KAHOOT_LECTURA = [
    ("Banda 1 por debajo del 60 %",
     "El nivel anterior no se consolidó. Antes de entrar al temario, dos o tres dinámicas "
     "desenchufadas del banco: el algoritmo del sándwich y debugging humano."),
    ("Banda 1 alta y banda 2 por debajo del 50 %",
     "Saben nombrar, no saben aplicar. El temario sirve tal cual, pero cada semana necesita "
     "más minutos de práctica y menos de concepto. El concepto ya no pasa de 6 minutos."),
    (
        "Banda 3 por debajo del 30 %",
        "Esperable si el grupo no cursó este plan. Alargar las semanas 2 y 3 una clase "
        "más y apoyarse en los retos extra solo con quien ya va suelto. Repasar las variables antes "
        "de entrar a los ciclos de la semana 3."
    ),
    ("Todo por encima del 75 %",
     "El grupo llega con base. Usar el reto «sube de nivel» como práctica principal, no como "
     "extra, y adelantar el banco de ideas del proyecto."),
]

KAHOOT_NOTA = (
    "Es probable que 2do y 3ro salgan bajos, y no significa que el grupo sea flojo: significa "
    "que no cursaron este temario. La conclusión que sale de aquí es cuántos minutos de repaso "
    "meter en las semanas 2 a 4, nunca una nota."
)

# Kahoot acepta estos tiempos y nada más.
KAHOOT_TIEMPOS = (5, 10, 20, 30, 60, 90, 120, 240)
KAHOOT_MAX_PREGUNTA = 120
KAHOOT_MAX_RESPUESTA = 75


def Q(n, banda, origen, pregunta, opciones, correcta, refuerzo, nucleo=False):
    """Una pregunta. `origen` es dónde se enseñó; `refuerzo`, qué hacer si falla."""
    return {
        "n": n, "banda": banda, "origen": origen,
        "pregunta": pregunta, "opciones": list(opciones), "correcta": correcta,
        "segundos": 30 if banda == 3 else 20,
        "refuerzo": refuerzo, "nucleo": nucleo,
    }


# ─── 1RO · mide pensamiento computacional, sin una sola línea de código ────
KAHOOT_1RO = [
Q(1, 1, "—",
  "Un algoritmo es…",
  ["Una lista de pasos ordenados para lograr algo",
   "Un programa de computadora muy complicado",
   "Una fórmula matemática",
   "Un idioma que hablan las computadoras"], 1,
  "Semana 1: definición de algoritmo y la dinámica del robot.", True),

Q(2, 1, "—",
  "Un robot hace exactamente lo que le dices, ni más ni menos. Le dices «pon el pan». ¿Qué hace?",
  ["Pone el paquete entero sobre la mesa",
   "Saca dos rebanadas y las pone",
   "Pregunta cuántas rebanadas",
   "No hace nada porque no entiende"], 1,
  "Semana 1: precisión y ambigüedad. Dinámica del sándwich.", True),

Q(3, 1, "—",
  "¿Por qué importa el orden de los pasos?",
  ["Porque cambiar el orden cambia el resultado",
   "No importa, la computadora los reordena sola",
   "Solo importa en el primer paso",
   "Importa solo si son más de diez pasos"], 1,
  "Semana 1: secuencia. Ejecutar una ruta con los pasos cambiados.", True),

Q(4, 1, "—",
  "¿Una computadora adivina lo que uno quiere?",
  ["No: solo hace lo que se le dice",
   "Sí, si la pregunta está bien hecha",
   "Sí, las modernas sí",
   "Solo cuando está conectada a internet"], 1,
  "Semana 1: la pregunta de cierre del primer día.", True),

Q(5, 1, "—",
  "Una caja rotulada PUNTOS donde el número va cambiando durante el juego. En programación eso es…",
  ["Una variable",
   "Un algoritmo",
   "Una condición",
   "Un programa"], 1,
  "Semana 2: variables como espacio con nombre.", True),

Q(6, 1, "—",
  "Hay que repetir la misma instrucción diez veces. ¿Qué conviene?",
  ["Usar una repetición y escribirla una sola vez",
   "Escribirla diez veces, es más seguro",
   "Escribirla una vez y esperar",
   "Dividirla en diez programas"], 1,
  "Semana 3: bucles. Comparar el código antes y después.", True),

Q(7, 1, "—",
  "«Si está lloviendo llevo paraguas; si no, no lo llevo.» Eso en un programa es…",
  ["Una decisión",
   "Una repetición",
   "Una variable",
   "Un error"], 1,
  "Semana 4: condicionales si / si no."),

Q(8, 1, "—",
  "¿Qué es un programa?",
  ["Instrucciones que la computadora ejecuta en orden",
   "Una aplicación que se descarga",
   "La pantalla que uno ve",
   "El teclado y el mouse juntos"], 1,
  "Semana 1: qué es programar."),

Q(9, 1, "—",
      "Tiras un dado y salen 2, 4 y 6. ¿Qué número sale en la próxima tirada?",
      ["No se puede saber: puede salir cualquiera del 1 al 6",
       "El 8, porque va de dos en dos",
       "El 1, porque todavía no ha salido",
       "El 6 otra vez, porque fue el último"], 1,
      "Semana 8: el azar. Tirar un dado real y pedir que adivinen la siguiente tirada."),

Q(10, 2, "—",
  "En «preparar un jugo de naranja», ¿cuál es la ENTRADA?",
  ["Las naranjas",
   "Exprimirlas",
   "El jugo servido en el vaso",
   "La receta"], 1,
  "Semana 1: entrada, proceso y salida.", True),

Q(11, 2, "—",
  "Buscas un video: escribes el nombre y aparecen resultados. ¿Cuál es la SALIDA?",
  ["La lista de resultados",
   "Lo que escribiste",
   "La búsqueda que hace el sistema",
   "El teclado"], 1,
  "Semana 1: identificar la salida de un proceso.", True),

Q(12, 2, "—",
  "¿Cuál de estas instrucciones NO sirve para un robot?",
  ["Camina un rato",
   "Avanza tres pasos",
   "Gira a la derecha",
   "Repite dos veces: avanza"], 1,
  "Semana 1: eliminar pasos ambiguos.", True),

Q(13, 2, "—",
  "«Avanza, avanza, avanza, avanza» son cuatro instrucciones. ¿Cómo se escribe más corto?",
  ["Repite 4 veces: avanza",
   "Avanza mucho",
   "Avanza rápido",
   "No se puede escribir más corto"], 1,
  "Semana 3: sustituir repetición por bucle."),

Q(14, 2, "—",
  "Dos algoritmos resuelven la misma tarea. ¿Cuál es mejor?",
  ["El que otra persona puede seguir sin preguntar nada",
   "El que tiene más pasos",
   "El que tiene menos pasos siempre",
   "El que escribió el más rápido"], 1,
  "Semana 1: comparar dos algoritmos y justificar.", True),

Q(15, 2, "—",
  "Tu programa hace algo raro. ¿De quién es el error, normalmente?",
  ["De las instrucciones que escribimos",
   "De la computadora, que falla",
   "Del internet",
   "De nadie, a veces pasa"], 1,
  "Semana 1: la computadora no adivina, ejecuta."),

Q(16, 2, "—",
  "¿Para qué sirve que un compañero pruebe tu programa?",
  ["Para descubrir lo que a uno se le escapó",
   "Para que le ponga una nota",
   "Para copiar su solución",
   "Para terminar más rápido"], 1,
  "Semana 12: probar el juego con un compañero antes de presentarlo."),

Q(17, 3, "—",
  "Pasos: 1 enjuagar · 2 poner pasta · 3 cepillar · 4 mojar el cepillo. ¿Cuál está fuera de lugar?",
  ["El 4: mojar el cepillo va antes de poner la pasta",
   "El 1: enjuagar debería ir al final",
   "El 3: cepillar va primero",
   "Ninguno, el orden está bien"], 1,
  "Semana 1: descomponer y ordenar una tarea cotidiana.", True),

Q(18, 3, "—",
  "El robot mira al norte. Ejecuta: AVANZA · GIRA DERECHA · AVANZA. ¿Hacia dónde mira al final?",
  ["Al este",
   "Al norte",
   "Al sur",
   "Al oeste"], 1,
  "Semana 1: trazar mentalmente la ejecución.", True),

Q(19, 3, "—",
  "Pasos: 1 abrir la puerta · 2 sacar la llave · 3 girar la llave. ¿Cuál es el problema?",
  ["Abrir la puerta está antes de girar la llave",
   "Sacar la llave sobra",
   "Falta cerrar la puerta",
   "No hay ningún problema"], 1,
  "Semana 1: detectar el paso imposible antes de ejecutar."),

Q(20, 3, "—",
  "REPITE 3 VECES: [AVANZA, AVANZA]. ¿Cuántos pasos avanza el robot en total?",
  ["6",
   "3",
   "2",
   "5"], 1,
  "Semana 3: qué cuenta exactamente un bucle."),
]


# ─── 2DO · mide lo que 1ro deja: Python con display, variables, @when, random, if/elif, for, listas y def ───
KAHOOT_2DO = [
Q(1, 1, "—",
  "¿Qué hace print(\"Hola\")?",
  ["Muestra el texto Hola",
   "Guarda Hola en una variable",
   "Le pide al usuario que escriba Hola",
   "Crea un botón que dice Hola"], 1,
  "Semana 2: display() y el primer Python dentro del sitio.", True),

Q(2, 1, "—",
  "En programación, una variable es…",
  ["Un nombre que guarda un dato que puede cambiar",
   "Un número que nunca cambia",
   "Una instrucción que se repite",
   "Un error del programa"], 1,
  "Semana 2: variables y tipos de dato.", True),

Q(3, 1, "—",
  "¿Para qué sirve un if?",
  ["Para que el programa elija un camino según una condición",
   "Para repetir instrucciones",
   "Para guardar información",
   "Para mostrar un texto en la página"], 1,
  "Semana 4: if / elif / else y validación.", True),

Q(4, 1, "—",
  "¿Para qué sirve un bucle for?",
  ["Para repetir instrucciones sin escribirlas muchas veces",
   "Para tomar decisiones",
   "Para guardar un dato",
   "Para esperar a que alguien pulse un botón"], 1,
  "Semana 3: for y while.", True),

Q(5, 1, "—",
  "¿Qué es una lista en Python?",
  ["Varios valores guardados en orden bajo un solo nombre",
   "Una variable que solo guarda texto",
   "Un bucle que se repite",
   "Una función que muestra números"], 1,
  "Semana 5: listas que llenan la página.", True),

Q(6, 1, "—",
  "¿Para qué sirve crear una función con def?",
  ["Para agrupar pasos con un nombre y usarlos cuando haga falta",
   "Para guardar una lista de datos",
   "Para repetir algo un número fijo de veces",
   "Para darle color a la página"], 1,
  "Semana 6: funciones y el mini juego.", True),

Q(7, 1, "—",
  "En un if con else, ¿cuándo se ejecuta lo que va dentro del else?",
  ["Solo cuando la condición del if no se cumple",
   "Siempre, después del if",
   "Antes de revisar el if",
   "Nunca, el else es opcional"], 1,
  "Semana 4: los caminos de if / elif / else."),

Q(8, 1, "—",
  "Python marca un error y el programa se detiene. ¿Qué conviene hacer primero?",
  ["Leer el mensaje: dice qué pasó y en qué línea",
   "Borrar todo y empezar de nuevo",
   "Recargar la página hasta que funcione",
   "Cambiar líneas al azar hasta que desaparezca"], 1,
  "Semanas 2 y 3: leer el error antes de tocar el código."),

Q(9, 1, "—",
  "¿Qué hace @when(\"click\", \"#boton\") puesto encima de una función?",
  ["Hace que la función se ejecute al pulsar ese botón",
   "Crea el botón en la página",
   "Repite la función sin parar",
   "Cambia el color del botón"], 1,
  "Semana 7: la calculadora con botones."),

Q(10, 2, "—",
  "Alguien escribe 15 en una caja y tu programa tiene que sumarle 1. ¿Qué hace falta?",
  ["Convertirlo con int() antes de sumar",
   "Nada, Python ya sabe que es un número",
   "Ponerlo entre comillas",
   "Usar display() en vez de print()"], 1,
  "Semana 7: .value siempre llega como texto; int() y float().", True),

Q(11, 2, "—",
  "¿Qué diferencia hay entre = y == ?",
  ["= guarda un valor; == compara dos valores",
   "= compara; == guarda",
   "Son lo mismo, == es más elegante",
   "== solo sirve para texto"], 1,
  "Semana 4: la diferencia entre = y ==.", True),

Q(12, 2, "—",
  "Nota de 90 o más: «excelente»; de 70 o más: «bien»; si no, «en proceso». ¿Qué usas?",
  ["if, elif y else",
   "Un for que cuente hasta 100",
   "Una lista con las tres palabras",
   "Un solo if, sin nada más"], 1,
  "Semana 4: decisiones múltiples y el orden de las condiciones.", True),

Q(13, 2, "—",
  "Quieres simular un dado de 6 caras. ¿Qué escribes?",
  ["random.randint(1, 6)",
   "random.randint(0, 6)",
   "random.randint(1, 7)",
   "random(6)"], 1,
  "Semana 6: la jugada de la máquina al azar.", True),

Q(14, 2, "—",
  "Tienes que guardar los nombres de 20 jugadores. ¿Qué usas?",
  ["Una lista con los 20 nombres",
   "20 variables, una por nombre",
   "Un texto largo separado por comas",
   "Una función por cada jugador"], 1,
  "Semana 5: listas, append y recorrerlas."),

Q(15, 2, "—",
  "Copiaste el mismo bloque de código en tres partes distintas del juego. ¿Qué conviene?",
  ["Convertirlo en una función y llamarla en las tres partes",
   "Dejarlo así, funciona igual",
   "Copiarlo una cuarta vez por si acaso",
   "Borrar dos de las copias"], 1,
  "Semana 6: refactorizar con def."),

Q(16, 2, "—",
  "Tienes nombre = \"Ana\". ¿Qué línea muestra Hola, Ana?",
  ["print(f\"Hola, {nombre}\")",
   "print(\"Hola, {nombre}\")",
   "print(f\"Hola, nombre\")",
   "print(Hola, nombre)"], 1,
  "Semana 2: variables y f-strings en display()."),

Q(17, 3, "—",
  "print(\"15\" + \"15\")   ¿Qué muestra?",
  ["1515",
   "30",
   "\"30\"",
   "Un error"], 1,
  "Semana 2: tipos. Por qué \"15\" + \"15\" da 1515.", True),

Q(18, 3, "—",
  "Mira el bucle for de la imagen. ¿Qué muestra, en orden?",
  ["0, 1 y 2",
   "1, 2 y 3",
   "0, 1, 2 y 3",
   "Solo el 3"], 1,
  "Semana 3: for y el número que range deja fuera.", True),

Q(19, 3, "—",
  "puntos = [10, 20, 30]  ·  puntos.append(40)  ·  print(len(puntos))   ¿Qué muestra?",
  ["4",
   "3",
   "40",
   "[10, 20, 30, 40]"], 1,
  "Semana 5: append() y len()."),

Q(20, 3, "—",
  "edad = \"18\"  ·  print(edad + 1)   ¿Qué pasa?",
  ["Da error: no se puede sumar texto y número",
   "Muestra 19",
   "Muestra 181",
   "Muestra 18"], 1,
  "Semana 7: convertir con int() lo que llega de la caja."),
]


# ─── 3RO · mide lo que 2do deja: HTML, CSS, tipos, if/elif, for, while, listas, def/return y Teachable Machine ───
KAHOOT_3RO = [
Q(1, 1, "—",
  "En Python, ¿cuál de estos valores es un booleano?",
  ["True",
   "\"True\"",
   "1",
   "sí"], 1,
  "Semana 7: los tipos aparecen al escribir la primera versión del problema.", True),

Q(2, 1, "—",
  "¿De qué tipo es \"25\", escrito entre comillas?",
  ["Texto (str), aunque parezca un número",
   "Número entero (int)",
   "Número decimal (float)",
   "Booleano (bool)"], 1,
  "Semana 7: type() al leer las cajas.", True),

Q(3, 1, "—",
  "¿Para qué sirve una función?",
  ["Para agrupar pasos y reutilizarlos con un nombre",
   "Para guardar una lista de datos",
   "Para repetir algo un número fijo de veces",
   "Para dar estilo a la página"], 1,
  "Semana 6: funciones pequeñas que se prueban por separado.", True),

Q(4, 1, "—",
  "¿Qué es una lista en Python?",
  ["Varios valores ordenados bajo un solo nombre",
   "Una variable que solo guarda números",
   "Una función que devuelve varios resultados",
   "Una etiqueta de HTML"], 1,
  "Semana 5: listas de texto y cómo se recorren.", True),

Q(5, 1, "—",
  "¿Cuándo conviene un for y cuándo un while?",
  ["for si sé cuántas veces; while si depende de una condición",
   "for para números y while para texto",
   "while siempre, for es antiguo",
   "Da igual, son idénticos"], 1,
  "Semana 5: recorrer listas con for para buscar y filtrar.", True),

Q(6, 1, "—",
  "¿Qué hace return dentro de una función?",
  ["Devuelve un resultado a quien la llamó",
   "Muestra el resultado en la página",
   "Termina el programa completo",
   "Vuelve a ejecutar la función"], 1,
  "Semana 6: return y assert para probar cada función.", True),

Q(7, 1, "—",
  "¿Qué hace @when(\"click\", \"#boton\") escrito encima de una función?",
  ["La ejecuta cada vez que se pulsa ese botón",
   "Crea un botón nuevo en la página",
   "Cambia el color del botón",
   "La ejecuta una sola vez al abrir la página"], 1,
  "Semana 7: conectar la plantilla al problema de la excursión."),

Q(8, 1, "—",
  "Un bucle infinito es peligroso porque…",
  ["Nunca termina y la página se queda congelada",
   "Borra los datos del programa",
   "Hace que el código sea más lento de escribir",
   "Da un error de color rojo y ya"], 1,
  "Semana 6: casos borde y depuración antes de dar algo por terminado."),

Q(9, 1, "—",
  "En Teachable Machine, ¿qué es una clase?",
  ["Una categoría que el modelo aprende a reconocer",
   "Una sesión del curso de programación",
   "El código que exporta el modelo",
   "La cámara que usa el modelo para ver"], 1,
  "Semana 10: el experimento de datos buenos y datos malos."),

Q(10, 2, "—",
  "En Python, \"3\" * 2 da \"33\". ¿Por qué?",
  ["Porque \"3\" es texto y se repite dos veces",
   "Porque Python multiplica mal",
   "Porque faltan paréntesis",
   "Porque 3 por 2 es 33"], 1,
  "Semana 7: tipos y métodos de texto al leer las cajas.", True),

Q(11, 2, "—",
  "document.querySelector(\"#edad\").value siempre devuelve…",
  ["Texto, aunque escriban un número",
   "Un número, si escriben un número",
   "El tipo que toque, automáticamente",
   "Un booleano"], 1,
  "Semana 11: validar y convertir lo que llega del formulario.", True),

Q(12, 2, "—",
  "¿Cómo sabe Python si un número n es par?",
  ["Si el resto de dividirlo entre 2 es 0: n % 2 == 0",
   "Si n / 2 == 1",
   "Si n tiene dos cifras",
   "Si al dividirlo entre 2 da un número"], 1,
  "Semana 3: conteos sobre un conjunto de datos.", True),

Q(13, 2, "—",
  "¿Qué diferencia hay entre = y == en Python?",
  ["= guarda un valor; == compara dos valores",
   "= compara; == guarda un valor",
   "Son lo mismo, == es más elegante",
   "== solo sirve para texto"], 1,
  "Semana 6: assert compara con ==, y confundirlos es el primer fallo.", True),

Q(14, 2, "—",
  "Un if pregunta «nota mayor o igual que 60» y el elif «mayor o igual que 90». Con 95, ¿qué pasa?",
  ["Entra en el if y el elif nunca se ejecuta",
   "Da un error",
   "Entra en los dos",
   "Entra en el elif porque es más exacto"], 1,
  "Semana 6: probar valores de frontera como casos borde."),

Q(15, 2, "—",
  "Entrenas un modelo solo con fotos de una persona frente a la misma pared. ¿Qué es lo más probable?",
  ["Que falle con otras personas o con otro fondo",
   "Que funcione igual con cualquiera",
   "Que acierte más, porque los datos son parejos",
   "Que no se pueda entrenar así"], 1,
  "Semana 10: el experimento de sesgo con la tabla de 10 casos."),

Q(16, 2, "—",
  "En el modelo de caja de CSS, el padding es…",
  ["El espacio entre el borde y el contenido",
   "El espacio fuera del borde",
   "El grosor del borde",
   "El ancho total del elemento"], 1,
  "Semana 11: una interfaz que también funcione en el celular."),

Q(17, 3, "—",
  "a = [10, 20, 30]  ·  a.append(40)  ·  display(len(a))   ¿Qué muestra?",
  ["4",
   "3",
   "40",
   "[10, 20, 30, 40]"], 1,
  "Semana 5: listas, append y len al filtrar.", True),

Q(18, 3, "—",
  "Mira el bucle for de la imagen. ¿Qué muestra en la página?",
  ["1, 2 y 3",
   "1, 2, 3 y 4",
   "0, 1, 2 y 3",
   "Solo el 3"], 1,
  "Semana 5: recorrer con for y range.", True),

Q(19, 3, "—",
  "Mira el código de la imagen. En la caja #edad escriben 18. ¿Qué pasa?",
  ["Da error: no se puede sumar texto y número",
   "Muestra 19",
   "Muestra 181",
   "Muestra 18"], 1,
  "Semana 7: convertir con int() y float() lo que llega de la página."),

Q(20, 3, "—",
  "def sumar(a, b): a + b   Al usarla, sumar(2, 3) da None. ¿Por qué?",
  ["Le falta return antes de a + b",
   "Los parámetros están mal nombrados",
   "Faltan comillas en a + b",
   "Hay que llamarla dos veces"], 1,
  "Semana 6: return, y un assert que lo habría detectado."),
]

KAHOOT = {"1ro": KAHOOT_1RO, "2do": KAHOOT_2DO, "3ro": KAHOOT_3RO}

# Los tres Kahoots ya montados a partir de esos bancos. Son enlaces de autor:
# abren el Kahoot para lanzarlo, no para jugarlo. Los estudiantes entran en
# kahoot.it con el PIN que sale al proyectar, que es otra cosa.
KAHOOT_ENLACES = {
    "1ro": "https://create.kahoot.it/share/1ro-test/9ab96304-6323-4b26-b921-dd91b04ed174",
    "2do": "https://create.kahoot.it/share/2do-test/dbd6eca6-b7a2-4f3a-88ce-3390725c570a",
    "3ro": "https://create.kahoot.it/share/3ro-test/557eb19f-c7d0-4b0b-b3ba-0accabc4e23f",
}

# --------------------------------------------------- LA SEMANA DIA POR DIA
# (hora, que, tipo)  tipo: clase | cocu | admin
SEMANA_DIAS = [
 {"dia": "Lunes", "clases": 0,
  "bloques": [("8:00 – 9:40",   "Diseño de soluciones tecnológicas", "admin"),
              ("10:55 – 12:30", "Planificación", "admin"),
              ("12:30 – 13:15", "Desarrollo de proyectos", "admin"),
              ("14:15 – 15:45", "Maker · Primaria 1.º–3.º", "cocu")],
  "nota": "Sin clases curriculares, pero por la tarde hay taller: Maker de primaria, 1.º a 3.º. La mañana es para preparar el material de la semana y, sobre todo, para dejar cortado y contado lo que se va a usar en el taller."},
 {"dia": "Martes", "clases": 0,
  "bloques": [("8:00 – 8:50",   "Planificación", "admin"),
              ("8:50 – 10:25",  "Desarrollo de proyectos", "admin"),
              ("10:55 – 12:30", "Diseño de soluciones tecnológicas", "admin"),
              ("14:15 – 15:45", "Maker · Secundaria A", "cocu")],
  "nota": "Tampoco hay clases curriculares. Por la tarde empieza el Maker de secundaria: el mismo taller que se repetirá miércoles y jueves con los otros dos grupos. Se prepara una vez y se imparte tres veces."},
 {"dia": "Miércoles", "clases": 1,
  "bloques": [("8:00 – 8:50",   "1ro A", "clase"),
              ("8:50 – 9:40",   "Atención a padres", "admin"),
              ("9:40 – 10:25",  "Planificación", "admin"),
              ("10:55 – 12:30", "Desarrollo de proyectos", "admin"),
              ("12:30 – 13:15", "Planificación", "admin"),
              ("14:15 – 15:45", "Maker · Secundaria B", "cocu")],
  "nota": "Una sola clase, y es de 1ro. Funciona como ensayo: lo que falle con 1ro A se corrige antes "
          "de repetir la semana con 1ro B el jueves y con 1ro C el viernes."},
 {"dia": "Jueves", "clases": 5,
  "bloques": [("8:00 – 8:50",   "2do A", "clase"),
              ("8:50 – 9:40",   "2do C", "clase"),
              ("9:40 – 10:25",  "Planificación", "admin"),
              ("10:55 – 11:45", "3ro B", "clase"),
              ("11:45 – 12:30", "1ro B", "clase"),
              ("12:30 – 13:15", "3ro C", "clase"),
              ("14:15 – 15:45", "Maker · Secundaria C", "cocu")],
  "nota": "El día crítico: cinco clases y tres niveles distintos, con dos cambios de nivel seguidos "
          "(3ro B → 1ro B → 3ro C). Nada se improvisa. Las dos primeras son la misma clase de 2do "
          "repetida, así que se prepara una sola vez; entre 3ro B y 1ro B hay que cambiar de material "
          "completo en el cambio de hora."},
 {"dia": "Viernes", "clases": 3,
  "bloques": [("8:00 – 8:50",   "2do B", "clase"),
              ("8:50 – 9:40",   "3ro A", "clase"),
              ("9:40 – 10:25",  "1ro C", "clase"),
              ("10:55 – 11:45", "Libre", "admin"),
              ("11:45 – 12:30", "Diseño de soluciones tecnológicas", "admin"),
              ("14:15 – 15:45", "Desarrollo de proyectos", "admin"),],
  "nota": "Tres clases seguidas, una de cada nivel, y con eso queda cerrada la semana: las nueve "
          "secciones vieron su clase. Después del receso el día queda libre de aula."},
]

SEMANA_DIAS_INTRO = (
    "La planificación está organizada por nivel, pero tú das clase por día. Esta es la misma "
    "información ordenada como la vives: qué toca cada día y en qué orden. Cada sección recibe la "
    "semana que le corresponde de su propio nivel."
)


# ─── qué ilustración lleva cada pregunta ──────────────────────────────────
#  Nombre de la escena de ilustra.py y sus parámetros. Las de banda 3 no están
#  aquí: llevan la tarjeta de código o de pasos de IMAGENES.
#
#  La regla al elegir, y la única que puede arruinar esto: la ilustración
#  muestra la ESCENA de la pregunta, nunca la respuesta. En «¿qué es un
#  algoritmo?» la correcta es «una lista de pasos ordenados», así que ahí va un
#  signo de interrogación y no una lista numerada. Una imagen decorativa que
#  regala la respuesta no se nota hasta ver los resultados altos y no entender
#  por qué.
ESCENAS = {
    "1ro": {
        1:  ("duda", {}),                 # qué es un algoritmo
        2:  ("robot_pan", {}),            # «pon el pan»
        3:  ("bloques", {}),              # por qué importa el orden
        4:  ("pantalla_duda", {}),        # ¿la computadora adivina?
        5:  ("cajas", {}),                # variables
        6:  ("repetido", {}),             # repetir diez veces
        7:  ("lluvia_paraguas", {}),      # si llueve, paraguas
        8:  ("pantalla_codigo", {}),      # qué es un programa
        9:  ("bloques", {"rotulos": ["2", "4", "6"]}),            # qué es una página web
        10: ("naranja_vaso", {}),         # la entrada del jugo
        11: ("busqueda", {}),             # la salida de una búsqueda
        12: ("robot", {}),                # instrucción que no sirve
        13: ("huellas", {}),              # avanza cuatro veces
        14: ("balanza", {}),              # dos algoritmos, cuál es mejor
        15: ("bicho", {}),                # de quién es el error
        16: ("dos_personas", {}),         # que un compañero lo pruebe

        # banda 3 · los pasos van en la ilustración, no en el enunciado
        17: ("pasos",  {"lineas": ["1 · Enjuagar", "2 · Poner la pasta",
                                   "3 · Cepillar", "4 · Mojar el cepillo"]}),
        18: ("pasos",  {"lineas": ["AVANZA", "GIRA DERECHA", "AVANZA"]}),
        19: ("pasos",  {"lineas": ["1 · Abrir la puerta", "2 · Sacar la llave",
                                   "3 · Girar la llave"]}),
        20: ("codigo", {"lineas": ["REPITE 3 VECES:", "    AVANZA", "    AVANZA"]}),
    },
    "2do": {
        1:  ("navegador_consola", {}),    # qué hace print
        2:  ("cajas", {}),                # qué es una variable
        3:  ("pantalla_codigo", {}),      # para qué sirve un if
        4:  ("repetido", {}),             # para qué sirve un for
        5:  ("pantalla_duda", {}),        # qué es una lista
        6:  ("maquina", {}),              # para qué sirve def
        7:  ("interruptor", {}),          # cuándo se ejecuta el else
        8:  ("bicho", {}),                # qué hacer con un error
        9:  ("boton", {}),                # qué hace @when
        10: ("teclado", {}),              # sumar a lo que llega de la caja
        11: ("balanza", {}),              # = frente a ==
        12: ("bloques", {}),              # tres categorías de nota
        13: ("duda", {}),                 # simular un dado
        14: ("muchos", {}),               # guardar veinte nombres
        15: ("repetido", {"veces": 3}),   # el mismo bloque tres veces
        16: ("cajas", {"rotulos": ["nombre"]}),  # la f-string

        # banda 3 · el fragmento de código
        17: ("codigo", {"lineas": ['print("15" + "15")']}),
        18: ("codigo", {"lineas": ["for i in range(3):", "    print(i)"]}),
        19: ("codigo", {"lineas": ["puntos = [10, 20, 30]", "puntos.append(40)",
                                   "print(len(puntos))"]}),
        20: ("codigo", {"lineas": ['edad = "18"', "print(edad + 1)"]}),
    },
    "3ro": {
        1:  ("interruptor", {}),          # cuál valor es booleano
        2:  ("cajas", {"rotulos": ["25", "\"25\""]}),   # de qué tipo es "25"
        3:  ("maquina", {}),              # para qué sirve una función
        4:  ("pantalla_duda", {}),        # qué es una lista
        5:  ("repetido", {}),             # cuándo for y cuándo while
        6:  ("pantalla_codigo", {}),      # qué hace return
        7:  ("boton", {}),                # qué hace @when
        8:  ("ciclo", {}),                # el bucle infinito
        9:  ("duda", {}),                 # qué es una clase en Teachable Machine
        10: ("codigo", {"lineas": ['display("3" * 2)', "", "# muestra 33"]}),
        11: ("teclado", {}),              # qué devuelve .value
        12: ("pares", {}),                # cómo saber si un número es par
        13: ("balanza", {}),              # = frente a ==
        14: ("bloques", {}),              # el orden en la cadena if / elif
        15: ("marco_imagen", {}),         # fotos de una sola persona y un solo fondo
        16: ("caja_modelo", {}),          # qué es el padding

        # banda 3 · el fragmento de código
        17: ("codigo", {"lineas": ["a = [10, 20, 30]", "a.append(40)",
                                   "display(len(a))"]}),
        18: ("codigo", {"lineas": ["for i in range(1, 4):", "    display(i)"]}),
        19: ("codigo", {"lineas": ['edad = document.querySelector("#edad").value',
                                   "display(edad + 1)", "", "# escriben 18 en la caja"]}),
        20: ("codigo", {"lineas": ["def sumar(a, b):", "    a + b", "",
                                   "display(sumar(2, 3))"]}),
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  PROGRAMA MAKER · el cocurricular
#
#  Fuente: la guía institucional del programa maker del centro, edición 2026.
#
#  El colegio tiene dos rutas. La curricular es de 1 hora semanal y produce
#  sobre todo trabajo digital; el cocurricular es el PROGRAMA MAKER DE
#  PROFUNDIZACIÓN, de 4 horas semanales, y su producto es un prototipo
#  FÍSICO. Antes de cualquier trayecto técnico, el manual exige la Inducción
#  Maker: 24 horas en 7 talleres, todos de taller y de manos.
#
#  Principios no negociables del manual, que gobiernan cada sesión:
#    · Aprender haciendo con propósito: la técnica aparece atada a una función.
#    · Primero la experiencia, después el nombre técnico.
#    · El error es información: se registra la falla y se cambia UNA variable.
#    · La seguridad no es una charla aparte: es condición para actuar.
#    · Microlecciones por demanda, no exposición.
# ═══════════════════════════════════════════════════════════════════════

MAKER_INTRO = (
    "El cocurricular no es la clase de programación con más horas: es otro programa. "
    "Aquí se construye con las manos, se mide, se rompe, se vuelve a montar y se defiende "
    "delante de otros. La pantalla aparece cuando hace falta, no al revés."
)

# ─── El desfase que hay que tener presente ────────────────────────────────
MAKER_NOTA_TIEMPO = (
    "La guía institucional diseña la inducción como seis semanas a cuatro horas semanales. "
    "Con tres grupos distintos de 90 minutos, cada grupo recibe 1,5 h por semana: 24 ÷ 1,5 = "
    "16 semanas por grupo. La inducción ocupa casi el año entero y ningún grupo llegará este "
    "curso a un trayecto técnico. Si se quiere llegar a robótica con Arduino, hay que juntar "
    "grupos o darles más de una tarde."
)


def _s(n, taller, titulo, proposito, pasos, reto, materiales, evidencia, seguridad=None):
    return {
        "n": n, "taller": taller, "titulo": titulo, "proposito": proposito,
        "pasos": pasos, "reto": reto, "materiales": materiales,
        "evidencia": evidencia, "seguridad": seguridad,
    }


MAKER_SECUNDARIA = {
    "via": "secundaria",
    "horas_sesion": 1.5,   # lo que dura un bloque de este programa
    "nombre": "Inducción Maker",
    "publico": "Secundaria · martes, miércoles y jueves",
    "resumen": "Las 24 horas de inducción que el manual exige antes de robótica o fabricación digital.",
    "nota": MAKER_NOTA_TIEMPO,
    "talleres": [
        {"n": 1, "titulo": "Nadie construye solo", "horas": "1,5 h", "sesiones": [1],
         "producto": "Torre colaborativa y acuerdo maker"},
        {"n": 2, "titulo": "Materiales y herramientas", "horas": "4,5 h", "sesiones": [2, 3, 4],
         "producto": "Pasaporte de materiales y objeto útil"},
        {"n": 3, "titulo": "Medir para construir", "horas": "4,5 h", "sesiones": [5, 6, 7],
         "producto": "Croquis acotado y ensamble de dos piezas"},
        {"n": 4, "titulo": "Qué hay dentro de un dispositivo", "horas": "3 h", "sesiones": [8, 9],
         "producto": "Mapa funcional y objeto rearmado"},
        {"n": 5, "titulo": "Mecanismos y transmisión del movimiento", "horas": "4,5 h", "sesiones": [10, 11, 12],
         "producto": "Mecanismo combinado funcional"},
        {"n": 6, "titulo": "Electricidad segura y práctica", "horas": "1,5 h", "sesiones": [13],
         "producto": "Circuito LED y protocolo CORTAR"},
        {"n": 7, "titulo": "Del problema al prototipo", "horas": "4,5 h", "sesiones": [14, 15, 16],
         "producto": "Soporte regulable V1 → V2 y defensa"},
    ],
    "sesiones": [

_s(1, 1, "La torre que se cae",
   "Descubrir en carne propia por qué un equipo sin acuerdos construye peor que una persona sola.",
   ["Equipos de cuatro. Veinte espaguetis, un metro de cinta, un metro de hilo y un malvavisco. "
    "Dieciocho minutos para la torre más alta que sostenga el malvavisco arriba.",
    "Se mide con cinta métrica delante de todos. Casi todas se caen en el último minuto: eso es el taller.",
    "Segunda ronda, doce minutos, con una regla nueva: hay que probar el malvavisco desde el principio.",
    "Se escribe el acuerdo maker del grupo: cinco frases sobre cómo se trabaja aquí. Se firma y se cuelga."],
   "Que la segunda torre sea más alta que la primera. No por suerte: por lo que aprendieron de la caída.",
   "20 espaguetis, 1 m de cinta, 1 m de hilo y 1 malvavisco por equipo. Cinta métrica. Cartulina para el acuerdo.",
   "Torre en pie con el malvavisco arriba, medida y anotada, y el acuerdo maker firmado por el equipo."),

_s(2, 2, "El pasaporte de materiales",
   "Distinguir materiales por lo que hacen, no por cómo se llaman: qué aguanta, qué se dobla, qué se corta fácil.",
   ["En la mesa: cartón corrugado, cartón fino, madera balsa, plástico de envase, alambre, foam, tela.",
    "Por parejas, cada material pasa tres pruebas: doblar, cortar y aguantar peso. Se anota qué pasó.",
    "Se llena el pasaporte: una ficha por material con sus tres resultados y una frase de para qué sirve.",
    "Puesta en común: ¿qué material elegirías para una bisagra? ¿Y para una pata que aguante un libro?"],
   "Encontrar el material que aguanta más peso sin doblarse, y poder demostrarlo con la prueba, no con la opinión.",
   "Muestras de 6 a 8 materiales por mesa. Tijeras, regla, pesas o botellas de agua. Fichas de pasaporte impresas.",
   "Pasaporte con las tres pruebas de cada material y la elección justificada para dos usos.",
   "Las tijeras se pasan por el mango, nunca por la hoja. Nadie corta hacia su cuerpo."),

_s(3, 2, "Cada herramienta tiene su trabajo",
   "Elegir la herramienta correcta y usarla bien, que es lo que separa un corte limpio de un accidente.",
   ["Estación por estación: tijera, cúter sobre base, regla metálica, punzón, lija, pistola de silicona.",
    "En cada estación se hace un corte o una unión de prueba. El facilitador corrige la postura, no el resultado.",
    "Se monta la lista de verificación del puesto: qué tiene que estar en la mesa antes de empezar.",
    "Prueba de unión: pegar dos cartones de tres formas distintas y ver cuál aguanta al tirar."],
   "Un corte recto de 15 cm hecho con regla metálica que no se pase de un milímetro.",
   "Cúter con base de corte, regla metálica, punzón, lija, pistola de silicona con base. Cartón de sobra.",
   "Lista de verificación del puesto y tres uniones probadas con su resultado anotado.",
   "El cúter solo sobre base de corte y con regla METÁLICA: la de plástico se corta y la mano va detrás. "
   "La pistola de silicona se apoya siempre en su base."),

_s(4, 2, "El objeto útil",
   "Fabricar algo que alguien vaya a usar de verdad, eligiendo material y herramienta con criterio.",
   ["Cada uno elige un encargo real del aula: un organizador de cables, un soporte para el celular, "
    "una caja para los jumpers, un separador de cajones.",
    "Antes de cortar: se dibuja, se elige el material y se escribe por qué ese y no otro.",
    "Se construye. Lo que no aguanta se rehace, no se remienda con más silicona.",
    "Se entrega a quien lo va a usar y se le pregunta si le sirve."],
   "Que el objeto siga entero después de que otra persona lo use durante cinco minutos.",
   "Materiales del pasaporte. Herramientas de la sesión anterior. El objeto real que va a organizar.",
   "Objeto terminado, la justificación escrita del material elegido y el comentario de quien lo usa."),

_s(5, 3, "Medir sin mentir",
   "Medir es un acto técnico con reglas: desde dónde, con qué unidad y con cuánta precisión.",
   ["Se mide el mismo objeto en cinco mesas distintas y se comparan los resultados en la pizarra. Nunca coinciden.",
    "Se busca por qué: desde el cero de la regla, no desde el borde; milímetros, no «un poquito más».",
    "Ronda de medición: diez objetos, en milímetros, por parejas, contrastando entre los dos.",
    "Se introduce el calibre si lo hay, o el truco del papel doblado para medir espesores."],
   "Que dos parejas midan el mismo objeto y no se lleven más de un milímetro de diferencia.",
   "Reglas metálicas, cinta métrica, calibre si hay. Diez objetos variados para medir. Fichas de registro.",
   "Tabla con las diez medidas por pareja y las diferencias explicadas."),

_s(6, 3, "El croquis acotado",
   "Dibujar una pieza de forma que otra persona pueda construirla sin preguntarte nada.",
   ["Se muestra un croquis mal hecho y se pide construir con él. No se puede: faltan cotas.",
    "Qué lleva un croquis: vistas, cotas en milímetros, unidades, y qué NO lleva: sombras ni dibujo bonito.",
    "Cada uno dibuja el croquis acotado de una pieza que ya construyó en el Taller 2.",
    "Intercambio: tu croquis va a otra mesa y ellos dicen si podrían construirlo."],
   "Que otro equipo pueda cortar tu pieza usando solo tu croquis, sin hacerte una sola pregunta.",
   "Papel cuadriculado, lápiz, regla, borrador. Las piezas del Taller 2 para acotar.",
   "Croquis acotado en milímetros, validado por otro equipo."),

_s(7, 3, "Dos piezas que encajan",
   "Fabricar a partir de medidas: si el croquis dice 40 mm, la pieza mide 40 mm.",
   ["Cada pareja recibe el croquis de OTRA pareja y tiene que fabricar esa pieza.",
    "Se fabrica la segunda pieza, la que tiene que encajar con la primera.",
    "Prueba de encaje. Si no entra, se mide dónde está la diferencia en vez de lijar a ciegas.",
    "Se anota la tolerancia: cuánto de más o de menos aguanta el encaje."],
   "Que las dos piezas encajen sin forzarlas y sin que bailen.",
   "Cartón o balsa, cúter, base de corte, regla metálica, lija. Los croquis de la sesión anterior.",
   "Ensamble de dos piezas que encaja, con la medida real anotada junto a la del croquis."),

_s(8, 4, "Abrir para entender",
   "Un aparato no es magia: es un conjunto de partes con funciones, y se puede leer.",
   ["Aparatos viejos sobre la mesa: teclado, radio, ratón, juguete con motor, cargador SIN cable a la red.",
    "Antes de abrir: cada equipo predice qué va a encontrar dentro y lo escribe.",
    "Se abre con destornillador, ordenando los tornillos en la ficha por orden de salida.",
    "Se identifica cada parte: qué entra, qué sale, qué mueve, qué decide."],
   "Encontrar la pieza que convierte una cosa en otra: electricidad en movimiento, movimiento en sonido.",
   "Aparatos en desuso (pedirlos con antelación), destornilladores de estrella y planos, bandejas para tornillos.",
   "Mapa funcional del aparato con las partes nombradas y la predicción inicial contrastada.",
   "Nada que se enchufe a la pared. Ningún aparato con condensador grande: televisores y microondas quedan fuera. "
   "Ninguna pantalla de tubo. Si tiene batería, se retira antes de abrir."),

_s(9, 4, "Volver a armarlo",
   "Desmontar es fácil; montar de vuelta y que funcione es lo que demuestra que se entendió.",
   ["Con el mapa funcional a la vista, se rearma el aparato en orden inverso.",
    "Los tornillos vuelven a su sitio: por eso se ordenaron al salir.",
    "Prueba: si el aparato funcionaba antes, tiene que funcionar ahora.",
    "Lo que sobre se registra y se explica: una pieza sobrante es información, no un fracaso."],
   "Que el aparato quede como estaba. Y si no, saber decir exactamente en qué paso se torció.",
   "Los aparatos y tornillos de la sesión anterior, ordenados. Los mapas funcionales.",
   "Aparato rearmado y el registro de lo que sobró o falló, con su causa."),

_s(10, 5, "Palanca y punto de apoyo",
   "El primer mecanismo: por qué mover el punto de apoyo cambia la fuerza que hace falta.",
   ["Se levanta una mochila pesada con una regla y un lápiz de apoyo. Se mueve el apoyo y se siente el cambio.",
    "Se construyen los tres tipos de palanca en cartón y se prueba cuál levanta más.",
    "Se mide: cuántos centímetros de un lado y cuántos del otro, y qué peso levanta cada una.",
    "Se busca dónde hay palancas alrededor: tijeras, pinzas, el pedal de la basura."],
   "Levantar un objeto que no puedes levantar con un dedo, usando solo cartón y un punto de apoyo.",
   "Cartón grueso, tacos de madera, reglas, chinchetas o brochas como eje, pesas o botellas llenas.",
   "Las tres palancas construidas y la tabla de qué peso levanta cada una."),

_s(11, 5, "Ruedas que mandan sobre otras",
   "Transmitir movimiento de un sitio a otro, y cambiar la velocidad o el sentido al hacerlo.",
   ["Dos ruedas de cartón con dientes: al girar una, la otra gira al revés. Se ve, no se explica antes.",
    "Se cuentan los dientes y se relaciona con las vueltas: la pequeña gira más veces.",
    "Se monta una transmisión por correa con una goma elástica y se compara con los engranajes.",
    "Se añade una tercera rueda y se predice el sentido antes de girar."],
   "Predecir correctamente hacia dónde girará la última rueda de una cadena de tres, antes de moverla.",
   "Cartón grueso, compás o plantillas de engranaje, chinchetas, base de cartón, gomas elásticas.",
   "Tren de engranajes funcionando y la predicción de sentido acertada y anotada."),

_s(12, 5, "El mecanismo combinado",
   "Juntar dos mecanismos distintos para que hagan algo que ninguno hace solo.",
   ["Se muestra un autómata de cartón sencillo funcionando: una leva que sube una figura.",
    "Cada equipo combina dos mecanismos de los vistos: leva y palanca, engranaje y biela.",
    "Se construye, se prueba y se corrige el rozamiento, que es donde siempre se atasca.",
    "Se hace girar veinte veces seguidas: si aguanta, está bien montado."],
   "Que el mecanismo dé veinte vueltas sin atascarse ni despegarse.",
   "Cartón, palos de brocheta, tapones, chinchetas, silicona, gomas. Cajas de cartón como carcasa.",
   "Mecanismo combinado que aguanta veinte ciclos, con el problema de rozamiento resuelto y explicado."),

_s(13, 6, "Electricidad que se puede tocar",
   "Montar un circuito de baja tensión, entender que la corriente va y vuelve, y saber cuándo parar.",
   ["Un LED, una resistencia, una pila y dos cables. Que encienda. Si no enciende, se busca por qué.",
    "Se descubre la polaridad girando el LED: hay un lado por el que la corriente entra.",
    "Por qué la resistencia: se enseña un LED quemado sin ella. Se ve una vez y no se olvida.",
    "Multímetro en continuidad: se comprueba un cable bueno y uno cortado.",
    "Se cierra con el protocolo CORTAR de la escuela."],
   "Que el LED encienda a la primera en el segundo intento, y saber decir por dónde entra y por dónde sale.",
   "Del kit Arduino: LEDs, resistencias de 220 Ω, jumpers, protoboard, portapilas. Multímetro. Un LED quemado.",
   "Circuito LED montado por cada estudiante y la lista de verificación de seguridad aplicada.",
   "NUNCA la red eléctrica: aquí solo hay pilas y 5 V. || FALTA: el protocolo CORTAR aparece nombrado en la "
   "guía institucional como producto de este taller, pero su definición no está en los documentos disponibles. "
   "Pídelo a la coordinación Maker antes de dar esta sesión; no lo improvises."),

_s(14, 7, "El problema de alguien",
   "Un prototipo empieza en una necesidad real de una persona concreta, no en una idea bonita.",
   ["Cada equipo entrevista a alguien de la escuela: conserje, cocina, un docente, un compañero de otro curso.",
    "Se escribe el problema en una frase que empiece por «necesita».",
    "Se convierte en criterios medibles: cuánto peso, cuánto espacio, cuántos segundos.",
    "Se dibujan tres alternativas distintas y se elige una justificando por qué."],
   "Escribir tres criterios que se puedan medir con una regla o un cronómetro. Nada de «que sea bonito».",
   "Fichas de entrevista, papel, lápiz. Acceso a las personas a entrevistar, avisadas antes.",
   "Ficha de proyecto con el problema, el usuario, tres criterios medibles y la alternativa elegida."),

_s(15, 7, "V1, el que falla",
   "Construir rápido y feo para descubrir pronto lo que no se sabía.",
   ["Se construye la primera versión con lo más barato que haya: cartón y cinta. Nada de acabados.",
    "Se prueba CONTRA LOS CRITERIOS, con regla y cronómetro, no a ojo.",
    "Se anota cada fallo con su causa: no «se rompió», sino «se rompió por la unión de arriba al poner 2 kg».",
    "Se elige UNA cosa que cambiar. Una sola: si cambias tres, no sabes cuál funcionó."],
   "Que el V1 falle en algo y que sepas exactamente por qué. Un V1 que no falla es que no lo probaste bien.",
   "Cartón, cinta, silicona, lo que haya. Cronómetro, regla, pesas para las pruebas.",
   "V1 construido, la tabla de pruebas contra los tres criterios, y la variable elegida para cambiar."),

_s(16, 7, "V2 y la defensa",
   "Mejorar una cosa, demostrar con datos que mejoró, y sostenerlo delante de otros.",
   ["Se construye el V2 con el único cambio decidido, cuidando ahora el acabado.",
    "Se repiten las MISMAS pruebas del V1. Mismo criterio, mismo método, para poder comparar.",
    "Se prepara la defensa: problema, usuario, criterios, qué cambió de V1 a V2 y qué dicen los números.",
    "Defensa de tres minutos por equipo. El público pregunta y el equipo responde con evidencia."],
   "Enseñar una tabla donde se vea que V2 es mejor que V1. Con números, no con adjetivos.",
   "El V1 para comparar, materiales para el V2, los instrumentos de medida. Proyector para la defensa.",
   "V2 funcional, la comparación V1–V2 con datos y la defensa hecha delante del grupo."),
]}


MAKER_PRIMARIA = {
    "via": "primaria",
    "horas_sesion": 1.5,   # lo que dura un bloque de este programa
    "nombre": "Taller Maker de Primaria",
    "publico": "Primaria 1.º a 3.º · lunes",
    "resumen": "Construir, probar, mejorar y explicar. Con cartón, a su escala, y las manos siempre ocupadas.",
    "nota": (
        "El colegio prevé LEGO WeDo para estos grados y todavía no hay. Se hace con materiales de "
        "taller y las piezas de baja tensión del kit. El eje no cambia: secuencias y causa-efecto, "
        "después eventos y reacción, y al final mecanismos, ciclos y mejora.\n\n"
        "Noventa minutos con niños de seis a nueve años no se sostienen de una pieza: cada sesión va "
        "en cuatro bloques de unos veinte minutos, y uno de ellos es siempre recoger."
    ),
    "talleres": [
        {"n": 1, "titulo": "Construir y que se caiga", "horas": "6 h", "sesiones": [1, 2, 3, 4],
         "producto": "Mecanismos de cartón que funcionan"},
        {"n": 2, "titulo": "Que encienda y que se mueva", "horas": "6 h", "sesiones": [5, 6, 7, 8],
         "producto": "Un circuito propio y una mano que agarra"},
        {"n": 3, "titulo": "Mi juguete", "horas": "6 h", "sesiones": [9, 10, 11, 12],
         "producto": "Un juguete propio, mejorado y explicado"},
    # Suelta a propósito: se puede dar cualquier semana sin renumerar las doce
    # sesiones que ya existen, igual que «Vuela o no vuela» en Makers Space.
    {"n": 4, "titulo": "Palitos que aguantan", "horas": "1.5 h", "sesiones": [13],
     "producto": "Un puente de palitos que aguanta monedas"},
    ],
    "sesiones": [

_s(1, 1, "La torre más alta",
   "Descubrir que construir en equipo se aprende probando, y que caerse es parte de construir.",
   ["Se enseña una torre de vasos ya hecha. Pregunta: ¿por qué no se cae?",
    "Equipos de tres. Vasos de plástico y cartulinas. Diez minutos para la torre más alta.",
    "Se miden todas con una cinta pegada en la pared. Las que se caen se vuelven a intentar.",
    "Segunda ronda con una regla nueva: la base tiene que ser más ancha que la punta."],
   "Que tu torre aguante de pie mientras cuentas hasta diez en voz alta.",
   "Vasos de plástico (30 por equipo), cartulinas, cinta métrica pegada a la pared.",
   "Torre en pie, medida y anotada en el mural del grupo."),

_s(2, 1, "La palanca que levanta",
   "Entender con el cuerpo que apoyar en un sitio o en otro cambia la fuerza que hace falta.",
   ["Cada uno levanta una mochila con una regla apoyada en un lápiz. Se mueve el lápiz y se nota el cambio.",
    "Se construye una palanca de cartón con una chincheta de eje.",
    "Concurso: ¿quién levanta el libro más pesado con su palanca?",
    "Se busca dónde hay palancas en el aula: tijeras, el pedal del zafacón, un sube y baja."],
   "Levantar con un dedo algo que no puedes levantar con un dedo.",
   "Cartón grueso, chinchetas, lápices, reglas, libros de distinto peso, mochilas.",
   "Palanca de cartón que levanta un libro, y el dibujo de dónde está el punto de apoyo.",
   "Las chinchetas se cuentan al empezar y al recoger. Ninguna se queda en el suelo."),

_s(3, 1, "Subir sin fuerza: la polea",
   "Ver que una cuerda y una rueda cambian hacia dónde se tira y cuánto cuesta.",
   ["Se cuelga una cubeta con cuerda y se levanta a pulso. Cuesta.",
    "Se pasa la cuerda por un carrete colgado y se vuelve a levantar. Cuesta menos y se tira hacia abajo.",
    "Cada equipo monta su polea con un carrete de hilo y un palo.",
    "Reto de carga: cuántos libros sube la polea antes de que la cuerda ceda."],
   "Subir la cubeta hasta arriba tirando hacia abajo, sin tocarla con la mano.",
   "Carretes de hilo vacíos, palos de brocheta, cuerda fina, cubetas pequeñas, libros o pesas.",
   "Polea montada que sube una carga, y la cuenta de cuántos libros aguantó."),

_s(4, 1, "Ruedas con dientes",
   "Descubrir que una rueda puede mandar sobre otra, y que la de al lado gira al revés.",
   ["Se enseñan dos engranajes ya cortados. Se gira uno: el otro gira al revés. Sorpresa primero, explicación después.",
    "Cada uno recorta dos engranajes con plantilla y los clava sobre una base.",
    "Juego de predicción: se añade una tercera rueda y hay que decir hacia dónde girará antes de moverla.",
    "Se pinta una marca en cada rueda para poder contar las vueltas."],
   "Adivinar hacia dónde gira la última rueda antes de tocarla. Tres aciertos seguidos.",
   "Plantillas de engranaje impresas, cartón grueso, tijeras, chinchetas, base de cartón, marcadores.",
   "Tren de tres engranajes que gira, con la predicción acertada anotada."),

_s(5, 2, "Que encienda",
   "Encender una luz con las propias manos y entender que la corriente va y vuelve.",
   ["Un LED, una pila de botón y nada más. Que encienda. Se prueba hasta que se logra.",
    "Se descubre girando el LED que hay un lado correcto: la pata larga y la corta.",
    "Se dibuja el camino de la corriente con el dedo: sale, pasa por el LED y vuelve.",
    "Reto en cadena: encender tres LEDs a la vez con la misma pila."],
   "Encender tu LED sin que nadie te diga cómo, la segunda vez.",
   "LEDs del kit, pilas de botón CR2032 (una por niño), cinta adhesiva.",
   "LED encendido por cada niño y el dibujo del camino de ida y vuelta.",
   "Pilas de botón: se cuentan al dar y al recoger, una por una. No se llevan a la boca ni salen del aula."),

_s(6, 2, "La tarjeta que se ilumina",
   "Hacer un circuito que vive dentro de algo bonito, y que se regala.",
   ["Se enseña una tarjeta terminada: al abrirla, se enciende. Todos quieren hacer una.",
    "Se dibuja el camino del circuito con cinta de cobre o papel de aluminio sobre la cartulina.",
    "Se pega el LED y la pila. Al doblar la tarjeta, los dos extremos se tocan y enciende.",
    "Se decora por fuera. Es un regalo: tiene que quedar bonito."],
   "Que se encienda sola al abrirla y se apague al cerrarla, sin que tengas que apretar nada.",
   "Cartulinas, cinta de cobre o papel de aluminio, LEDs, pilas CR2032, cinta adhesiva, colores.",
   "Tarjeta que enciende al abrirse, terminada y decorada."),

_s(7, 2, "La mano que agarra",
   "Construir algo que imita el cuerpo y descubrir para qué sirven los tendones.",
   ["Se mira la propia mano abriendo y cerrando. ¿Qué tira de los dedos?",
    "Se calca la mano en cartón, se recortan los dedos y se doblan por los nudillos.",
    "Se pasan hilos por pajitas pegadas: al tirar, el dedo se cierra.",
    "Concurso: agarrar y levantar un vaso de plástico con la mano de cartón."],
   "Agarrar un vaso y levantarlo diez centímetros sin que se caiga.",
   "Cartón fino, pajitas, hilo grueso, tijeras, silicona fría, vasos de plástico.",
   "Mano de cartón que cierra los dedos y levanta un vaso."),

_s(8, 2, "Rampas y canicas",
   "Ver que el recorrido se puede diseñar: la canica hace lo que el camino le manda.",
   ["Se suelta una canica por una rampa y se apuesta dónde va a caer. Casi nadie acierta.",
    "Cada equipo construye un recorrido con tubos de cartón, cajas y cinta.",
    "Regla: la canica tiene que llegar a la meta tres veces seguidas. Una vez es suerte.",
    "Se cronometra: el recorrido más lento gana, no el más rápido. Obliga a diseñar."],
   "Que la canica llegue a la meta tres veces seguidas, y que tarde lo más posible.",
   "Tubos de cartón, cajas, cinta de pintor, canicas, cronómetro, tijeras.",
   "Recorrido que funciona tres veces seguidas y su tiempo anotado.",
   "Las canicas se cuentan al empezar y al recoger. Ninguna en la boca ni en el suelo."),

_s(9, 3, "¿Qué hay aquí dentro?",
   "Abrir un aparato y descubrir que por dentro hay piezas que se pueden nombrar.",
   ["Antes de abrir, cada equipo dibuja lo que cree que hay dentro. Se guardan los dibujos.",
    "Se abre con destornillador, poniendo los tornillos en una bandeja.",
    "Se sacan las piezas y se ordenan en la mesa como un mapa.",
    "Se compara con el dibujo del principio: ¿qué acertaron y qué les sorprendió?"],
   "Encontrar la pieza que hace que algo se mueva, y señalarla.",
   "Juguetes viejos con motor, destornilladores pequeños, bandejas para tornillos, papel para el mapa.",
   "Mapa de las piezas dibujado y la comparación con la predicción inicial.",
   "Nada que se enchufe a la pared. Se retiran las pilas antes de abrir. El profesor abre lo que esté duro."),

_s(10, 3, "Mi juguete · lo dibujo",
   "Decidir qué se va a construir y dibujarlo antes de tocar el cartón.",
   ["Se recuerda todo lo aprendido: palanca, polea, engranaje, luz, mano, rampa.",
    "Cada uno elige DOS de esas cosas para su juguete y las dice en voz alta.",
    "Se dibuja el juguete en grande, con las dos piezas señaladas y qué hará cada una.",
    "Se hace la lista de materiales: qué necesito traer o buscar."],
   "Explicarle a un compañero qué hará tu juguete, solo con tu dibujo, y que lo entienda.",
   "Papel grande, colores, los mecanismos de las sesiones anteriores a la vista como ejemplo.",
   "Dibujo del juguete con dos mecanismos señalados y la lista de materiales."),

_s(11, 3, "Mi juguete · lo construyo",
   "Construir lo dibujado y arreglar lo que no sale a la primera.",
   ["Se reparte el material y cada uno monta su juguete siguiendo su propio dibujo.",
    "A mitad de sesión: todos paran y prueban. Lo que no funciona se anota.",
    "Se arregla UNA cosa, la que más molesta. No tres a la vez.",
    "Se prueba otra vez. Si funciona, se refuerza con silicona donde haga falta."],
   "Que tu juguete haga lo que dibujaste. Aunque sea feo: primero que funcione.",
   "Cartón, palos, chinchetas, hilo, pajitas, LEDs y pilas, silicona fría, tijeras.",
   "Juguete que funciona y la nota de qué se arregló y por qué."),

_s(12, 3, "Enséñalo y explícalo",
   "Mejorar una última cosa y contarle a otro lo que hiciste y cómo lo arreglaste.",
   ["Media hora para el último arreglo y para dejarlo bonito: ahora sí se pinta y se decora.",
    "Se ensaya en parejas: te toca contar tu juguete en un minuto.",
    "Feria: las mesas se abren y pasan los de otro curso a probar los juguetes.",
    "Cada uno dice en voz alta una frase: «lo que más me costó fue…»."],
   "Que alguien que no estaba aquí juegue con tu juguete sin que tengas que ayudarle.",
   "Pinturas, papeles de colores, lo necesario para el último arreglo. Mesas para la feria.",
   "Juguete terminado, probado por alguien de fuera, y la frase de cierre dicha en voz alta."),

# ── Taller 4 · Palitos que aguantan ───────────────────────────────────
#  Suelta: se da cualquier semana sin renumerar nada.
#
#  El descubrimiento es el triángulo, y todo lo demás cuelga de ahí: la casa lo
#  usa en el techo y el puente lo usa entero. Por eso el primer peldaño no es
#  una casa, es un cuadrado que se dobla empujándolo con un dedo.
#
#  La silicona la maneja el docente y solo en su mesa. Son niños de seis a
#  nueve años y una pistola pasa de los 150 grados; con treinta en el aula, la
#  única regla que aguanta es que ninguno la toque.
_s(13, 4, "Palitos que aguantan",
   "Descubrir que el cuadrado se dobla y el triángulo no, y usar eso para construir algo que sostenga peso de verdad.",
   ["Cuatro palitos y ligas: arma un cuadrado y empuja una esquina. Se dobla.",
    "Ahora tres palitos: un triángulo. Empuja igual de fuerte. No se mueve. Esa es toda la clase.",
    "En parejas, la casa: paredes apilando palitos en cuadrado y el techo en dos aguas.",
    "El puente: dos vigas largas y triángulos en medio. Se arma en seco, se prueba con la mano y se lleva a la mesa de silicona.",
    "Prueba de carga: el puente entre dos mesas y monedas encima, de una en una, contando en voz alta hasta que ceda.",
    "Cada pareja dice su número y qué le cambiaría. Quien terminó antes enseña el icosaedro."],
   "Que tu puente aguante monedas encima sin partirse, y que sepas decir cuántas aguantó.",
   "Palitos de helado (unos 60 por pareja), ligas, monedas iguales, dos mesas separadas para probar, y UNA pistola de silicona en la mesa del docente.",
   "El puente rotulado con los nombres de la pareja, el número de monedas anotado en el mural y la frase de qué le cambiarían.",
   "La pistola de silicona la maneja solo el docente, en su mesa: ningún niño la sostiene. "
   "|| Se lleva la pieza a la mesa, se señala dónde va y el docente pega. "
   "|| La silicona recién puesta quema aunque no se vea. Se cuenta hasta diez antes de tocar. "
   "|| Los palitos no se parten con los dientes."),
]}


# ═══════════════════════════════════════════════════════════════════════
#  MAKERS SPACE · sesión 1 · la escalera de aviones
#
#  Dos horas, los tres niveles juntos y el mismo material para todos. El
#  cierre es un reto fuera del aula, con jueces y cinta métrica.
#
#  Los aviones se declaran como la secuencia de pliegues que los produce:
#  de ahí salen los diagramas, uno por paso (ver plegado.py). Para corregir
#  un paso se mueve un punto aquí y se regenera; no hay ningún SVG que
#  editar a mano.
#
#  La escalera sube por conceptos, no por dificultad manual. Cada avión
#  añade exactamente una idea nueva, y el orden importa: el alerón del
#  cuarto no significa nada hasta que se ha visto que el primero se tuerce
#  cuando las alas no son iguales.
# ═══════════════════════════════════════════════════════════════════════

import plegado as _P

_W, _H = _P.A4                       # 210 × 297 mm; con carta todo escala igual
_CX = _W / 2                         # la raya del centro, referencia de todo

MAKERS_INTRO = (
    "Makers Space abre con papel y nada más. No porque sea lo más sencillo que hay a mano, "
    "sino porque con una hoja no se puede echar la culpa al material: si un avión se tuerce, "
    "se torció por cómo está doblado. Esa es la primera idea del año y no hace falta "
    "presupuesto para enseñarla."
)

# Por qué vuela un avión: la teoría corta que va antes de doblar la primera hoja,
# en la guía de los aviones y en la presentación del Makers Space. El texto es el
# que pasó Criso, con su fuente.
MAKERS_FISICA = {
    "titulo": "¿Por qué vuela un avión?",
    "intro": "Un avión vuela gracias al equilibrio de cuatro fuerzas físicas y al diseño especial de sus alas.",
    "fuerzas": [
        ("Sustentación", "La fuerza que empuja el avión hacia arriba y vence la gravedad.", "arriba"),
        ("Peso", "La fuerza de la gravedad que tira del avión hacia abajo.", "abajo"),
        ("Empuje", "La fuerza de los motores que impulsa el avión hacia adelante.", "adelante"),
        ("Resistencia", "La fuerza del aire que frena el avance del avión.", "atras"),
    ],
    "fuente": ("EAS Barcelona · ¿Por qué vuelan los aviones?", "https://easbcn.com/por-que-vuelan-los-aviones/"),
}

# ═══════════════════════════════════════════════════════════════════════
#  PALITOS QUE AGUANTAN · Taller Maker de Primaria · sesión 13
#
#  Cuatro construcciones de palitos de helado, de la que sale en dos minutos a
#  la que hay que pensar. El orden no es decorativo: el triángulo es el
#  descubrimiento y las otras dos lo usan —la casa en el techo, el puente
#  entero—. Por eso el primer peldaño no es una casa, es un cuadrado que se
#  vence empujándolo con un dedo.
#
#  Los pasos se dibujan solos desde palitos.py. Aquí solo va lo que hay que
#  decir de cada una.
# ═══════════════════════════════════════════════════════════════════════

PALITOS_INTRO = (
    "Cuatro construcciones con palitos de helado. La primera sale en dos minutos y sirve para "
    "descubrir la única idea de la sesión: el cuadrado se dobla y el triángulo no. Las otras "
    "tres usan esa idea para sostener peso de verdad."
)

PALITOS = [
    {"id": "formas", "n": 1, "nombre": "El cuadrado y el triángulo",
     "apodo": "Dos minutos, sin pegar nada",
     "ensena": "Por qué un triángulo aguanta",
     "idea": "Un cuadrado de cuatro palitos atados flojo se vence de lado en cuanto lo empujas. "
             "Con tres palitos no pasa: para que un triángulo cambie de forma habría que estirar "
             "un palito, y eso no se puede. Toda la sesión sale de aquí.",
     "sirve": "Para verlo con las manos antes de construir nada.",
     "materiales": "Siete palitos y unas ligas. Sin pegamento.",
     "pasos": "formas"},

    {"id": "casa", "n": 2, "nombre": "La casa",
     "apodo": "Apilar y trabar",
     "ensena": "Apilar en cruz y cerrar con un triángulo",
     "idea": "La pared es un montón de palitos uno encima de otro; sola se abre como un acordeón. "
             "Dos palitos de pie en las esquinas la traban, y el techo en dos aguas es otra vez "
             "un triángulo: por eso no se hunde.",
     "sirve": "Para coger la mano con la silicona antes del puente.",
     "materiales": "Unos diecisiete palitos. La pared mide once de alto justo para que los de "
                   "las esquinas sean palitos enteros y no haya que cortar nada.",
     "pasos": "casa"},

    {"id": "puente", "n": 3, "nombre": "El puente",
     "apodo": "El reto: aguanta monedas",
     "ensena": "La celosía: cada hueco, un triángulo",
     "idea": "Dos vigas paralelas y palitos de pie entre ellas se tuercen igual que el cuadrado. "
             "Las diagonales convierten cada hueco en un triángulo, y ahí el puente deja de "
             "torcerse. Es el mismo puente que cruza un río.",
     "sirve": "Se prueba con monedas encima hasta que ceda, y ese número se anota.",
     "materiales": "Trece palitos por lado, y otros tantos para el segundo lado. Los tramos "
                   "miden lo que miden para que la diagonal sea un palito entero.",
     "pasos": "puente"},

    {"id": "icosaedro", "n": 4, "nombre": "El icosaedro",
     "apodo": "Reto extra, para quien termine antes",
     "ensena": "Veinte triángulos hacen una bola",
     "idea": "Cinco triángulos alrededor de un punto forman una estrella plana. Al levantar el "
             "centro se hace una cúpula. Dos cúpulas y un cinturón en zigzag: la bola.",
     "sirve": "Para quien acabe el puente y quiera algo más difícil.",
     "materiales": "Treinta palitos en total. La tapa son diez.",
     "pasos": "icosaedro"},
]

# La guía va colgada de SU sesión y no del programa. Las otras doce sesiones de
# Primaria no llevan paso a paso dibujado, y si esto colgara del programa se les
# metería a todas.
for _ses in MAKER_PRIMARIA["sesiones"]:
    if _ses["n"] == 13:
        _ses["guia"] = PALITOS


MAKERS_REGLAS = [
    "Se dobla en la mesa, no en el aire. Un pliegue hecho al aire nunca sale recto.",
    "Nadie lanza hasta que todos hayan terminado. Un avión en el aire para la clase entera.",
    "Se cambia una cosa cada vez. Si cambias dos y vuela mejor, no sabes cuál lo arregló.",
]

# ─── la escalera ──────────────────────────────────────────────────────────

AVIONES = [

{"id": "dardo",
 "n": 1,
 "nombre": "El Dardo",
 "apodo": "Rápido y recto",
 "ensena": "Simetría",
 "idea": "Los dos lados tienen que ser iguales. Si uno queda más gordo que el otro, "
         "el avión gira hacia ese lado por mucha fuerza que le pongas.",
 "vuela": "Rápido y en línea recta. Llega lejos si lo lanzas fuerte, pero cae pronto: "
          "casi todo el papel está en la punta y casi nada en las alas.",
 "materiales": "Una hoja.",
 "pasos": [
   _P.marcar((_CX, 0), (_CX, _H), (0, 150),
     "Dobla la hoja por la mitad a lo largo y ábrela.",
     detalle="Esa raya del centro es la referencia de todo lo que viene: si la pierdes, el avión sale torcido."),

   _P.llevar_par(((0, 0), (_CX, 105)), ((_W, 0), (_CX, 105)),
     "Dobla las dos esquinas de arriba hasta la raya del centro.",
     detalle="Las dos a la vez y no una y luego la otra: así te sale igual de un lado que del otro."),

   _P.doblar_par(((_CX, 0), _P.bis((_CX, 0), (0, 105), (_CX, _H)), (0, 105)),
                 ((_CX, 0), _P.bis((_CX, 0), (_W, 105), (_CX, _H)), (_W, 105)),
     "Dobla otra vez los bordes inclinados hasta el centro.",
     detalle="La punta se afila y se pone pesada, porque ahí se te ha juntado casi todo el papel."),

   _P.doblar((_CX, 0), (_CX, _H), (200, 150),
     "Dobla el avión por la mitad, hacia atrás.", tipo="montana",
     detalle="Por la raya del centro. Todo lo que has doblado queda por fuera."),

   _P.doblar((_CX, 0), (_CX - 27, _H), (0, 150),
     "Baja el ala, de la punta a la cola.",
     detalle="Da la vuelta al avión y repite igual del otro lado: el borde del ala tiene que caer justo encima del que ya hiciste."),

   _P.vista(_P.frente(18),
     "Abre las alas. De frente tiene que verse una Y.",
     detalle="Las dos planas y en el mismo ángulo. Si ves una N, una ala está más alta y por ahí se va a ir."),
 ]},

{"id": "planeador",
 "n": 2,
 "nombre": "El Planeador",
 "apodo": "El del candado",
 "ensena": "Peso adelante",
 "idea": "La punta doblada hacia dentro y trabada hace de lastre. Con el peso delante el "
         "avión baja despacio en vez de dar volteretas.",
 "vuela": "Lento y largo. No hay que lanzarlo fuerte: se empuja, se suelta y planea. "
          "Es el que gana en tiempo en el aire.",
 "materiales": "Una hoja.",
 "pasos": [
   _P.marcar((_CX, 0), (_CX, _H), (0, 150),
     "Dobla la hoja por la mitad a lo largo y ábrela.",
     detalle="Otra vez la raya del centro."),

   _P.llevar_par(((0, 0), (_CX, 105)), ((_W, 0), (_CX, 105)),
     "Dobla las dos esquinas de arriba hasta el centro.",
     detalle="Igual que en el Dardo: hasta aquí los dos aviones son el mismo."),

   _P.doblar((0, 75), (_W, 75), (_CX, 10),
     "Dobla la punta hacia abajo, que sobresalga.",
     detalle="Aquí se separan del Dardo. Tiene que sobresalir bastante por debajo de los hombros del triángulo."),

   _P.llevar_par(((_CX - 75, 75), (_CX, 128)), ((_CX + 75, 75), (_CX, 128)),
     "Dobla las esquinas al centro sin tapar la punta.",
     detalle="Que se toquen justo encima de ella. La puntita tiene que seguir asomando: la necesitas entera."),

   _P.doblar((0, 128), (_W, 128), (_CX, 145),
     "Sube la puntita y dóblala encima: es el candado.", solo=(_CX, 145),
     detalle="Sobre las dos solapas. Ahora están trabadas y el avión no se abre solo en pleno vuelo."),

   _P.doblar((_CX, 0), (_CX, _H), (200, 200),
     "Dobla el avión por la mitad, hacia atrás.", tipo="montana",
     detalle="El candado queda por fuera, que es donde tiene que estar para que sujete."),

   _P.doblar((_CX, 75), (_CX - 23, _H), (0, 200),
     "Baja el ala, de la nariz a la cola.",
     detalle="Y repite del otro lado. Estas alas son más anchas que las del Dardo: por eso planea en vez de caerse."),

   _P.vista(_P.frente(12),
     "Abre las alas y suéltalo sin lanzarlo.",
     detalle="La Y de frente, más abierta y más plana que la del Dardo. Tiene que irse solo hacia adelante."),
 ]},

{"id": "estable",
 "n": 3,
 "nombre": "El Estable",
 "apodo": "El de las puntas levantadas",
 "ensena": "Estabilidad",
 "idea": "Las puntas de las alas dobladas hacia arriba frenan el balanceo. El avión deja "
         "de irse de lado y aguanta la línea aunque haya corriente.",
 "vuela": "Como el Planeador, pero derecho. Es el que hay que llevar al reto de puntería: "
          "aguanta el rumbo hasta el final.",
 "materiales": "Una hoja.",
 "pasos": [
   _P.marcar((_CX, 0), (_CX, _H), (0, 150),
     "Dobla la hoja por la mitad a lo largo y ábrela.",
     detalle="La raya del centro. Ya te la sabes."),

   _P.llevar_par(((0, 0), (_CX, 105)), ((_W, 0), (_CX, 105)),
     "Dobla las dos esquinas de arriba hasta el centro."),

   _P.doblar((0, 75), (_W, 75), (_CX, 10),
     "Dobla la punta hacia abajo, que sobresalga."),

   _P.llevar_par(((_CX - 75, 75), (_CX, 128)), ((_CX + 75, 75), (_CX, 128)),
     "Dobla las esquinas al centro sin tapar la punta.",
     detalle="La puntita se queda fuera."),

   _P.doblar((0, 128), (_W, 128), (_CX, 145),
     "Sube la puntita y dóblala encima: es el candado.", solo=(_CX, 145),
     detalle="Encima de las dos solapas."),

   _P.doblar((_CX, 0), (_CX, _H), (200, 200),
     "Dobla el avión por la mitad, hacia atrás.", tipo="montana"),

   _P.doblar((_CX - 87, 0), (_CX - 87, _H), (0, 150),
     "Dobla hacia arriba una tira del borde de afuera.",
     detalle="Esto es lo nuevo y va antes de bajar las alas. Un dedo de ancho basta: es el labio que frena el balanceo."),

   _P.doblar((_CX, 75), (_CX - 23, _H), (0, 200),
     "Baja las dos alas, una por cada lado.",
     detalle="Hasta aquí es el Planeador con un labio de más."),

   _P.vista(_P.frente(12, winglet=13),
     "Abre las alas y pon los dos labios de pie.",
     detalle="De frente ves una Y con dos ganchos arriba. Lánzalo al lado del Planeador y mira cuál se va de lado."),
 ]},

{"id": "delta",
 "n": 4,
 "nombre": "El Delta",
 "apodo": "El que se maneja",
 "ensena": "Superficies de control",
 "idea": "Un alerón recortado en la cola y doblado hacia arriba hace que el avión gire. "
         "Es la primera vez que decides tú hacia dónde va, en vez de esperar a ver.",
 "vuela": "Ancho y lento, y hace lo que le pidas. Con los dos alerones arriba sube; con uno "
          "solo, gira hacia ese lado. Es el avión del experimento.",
 "materiales": "Una hoja y tijeras.",
 "pasos": [
   _P.marcar((_CX, 0), (_CX, _H), (0, 150),
     "Dobla la hoja por la mitad a lo largo y ábrela.",
     detalle="La raya del centro."),

   _P.llevar_par(((0, 0), (_CX, 105)), ((_W, 0), (_CX, 105)),
     "Dobla las dos esquinas de arriba hasta el centro."),

   _P.doblar((0, 52.5), (_W, 52.5), (_CX, 10),
     "Dobla la punta abajo, hasta donde se juntan las esquinas.",
     detalle="La nariz queda roma y con tres capas de papel: ese es el peso que necesita delante."),

   _P.doblar((_CX, 0), (_CX, _H), (200, 200),
     "Dobla el avión por la mitad, hacia atrás.", tipo="montana"),

   _P.doblar((_CX, 55), (_CX - 20, _H), (0, 200),
     "Baja las alas, y esta vez muy anchas.",
     detalle="El pliegue va pegado al lomo. Cuanta más ala, más despacio baja."),

   _P.vista(_P.corte_alerones(),
     "Corta un alerón en el borde de atrás de cada ala.",
     detalle="Boca arriba: dos cortes de dos centímetros separados otros dos, y dobla hacia arriba la lengüeta que queda entre ellos."),

   _P.vista(_P.frente(14),
     "Pruébalo tres veces y anota qué hace.",
     detalle="Los dos alerones planos, los dos hacia arriba, y solo el izquierdo. Anota antes de tocar nada más."),
 ]},

{"id": "abeja",
 "n": 5,
 "nombre": "La Abeja",
 "apodo": "El aro que vuela",
 "ensena": "Que no hacen falta alas",
 "idea": "Un cilindro de papel con el borde de delante enrollado y grueso. El aire pasa "
         "por dentro y lo mantiene derecho; el peso del borde le impide encabritarse.",
 "vuela": "Lento, muy derecho y sin caerse de lado. Se lanza como una jabalina, agarrado "
          "por debajo. La primera vez nadie se cree que eso vuele.",
 "materiales": "Una hoja, tijeras y una grapadora o cinta.",
 "pasos": [
   _P.doblar((0, 0), (_W, _W), (_W, 0),
     "Lleva la esquina de arriba a la derecha hasta el lado izquierdo.",
     detalle="El borde de arriba tiene que caer justo encima del borde izquierdo. Así sale un "
             "triángulo y, debajo, una franja que sobra."),

   _P.cortar((0, _W), (_W, _W), (_CX, 100),
     "Corta la franja que sobra por debajo. Guárdala.",
     detalle="No la tires: de ahí sale el ala. Es el único avión que necesita las dos piezas."),

   _P.abrir([(0, 0), (_W, 0), (_W, _W), (0, _W)],
     "Abre el triángulo: te queda un cuadrado con una raya en diagonal.",
     marca=((0, 0), (_W, _W)),
     detalle="Esa diagonal es la que te dice que el cuadrado está bien hecho."),

   _P.doblar((0, _W - 15), (_W, _W - 15), (_CX, _W),
     "Dobla el borde de abajo hacia arriba, dos dedos de ancho.",
     detalle="Este borde va a ser la parte de delante del aro. Cuanto más recto lo dobles, "
             "más derecho vuela."),

   _P.doblar_serie([((0, _W - 30), (_W, _W - 30), (_CX, _W - 20)),
                    ((0, _W - 45), (_W, _W - 45), (_CX, _W - 35)),
                    ((0, _W - 60), (_W, _W - 60), (_CX, _W - 50))],
     "Enróllalo tres veces más sobre sí mismo.",
     detalle="Siempre hacia el mismo lado. Queda un borde grueso y duro: ahí está todo el "
             "peso del avión, y es lo que hace que planee en vez de dar volteretas."),

   _P.vista(_P.aro(1),
     "Dale la vuelta y arquea el papel con los dedos.",
     detalle="Pásalos por encima sin apretar, como quien riza una cinta, hasta que se quede "
             "curvado solo."),

   _P.vista(_P.aro(2),
     "Cierra el aro metiendo una punta dentro de la otra.",
     detalle="Un par de centímetros de solape. Grapa o pega ahí mismo. Tiene que quedar un "
             "cilindro firme, que no se abra al soltarlo."),

   _P.vista(_P.aro(3),
     "De la franja que guardaste, dóblala por la mitad y recorta el ala.",
     detalle="Doblada por la mitad, lo que cortes sale igual de los dos lados. Es la misma "
             "regla del primer avión: si los lados no son iguales, se tuerce."),

   _P.vista(_P.aro(4),
     "Grapa el ala cruzada justo en el centro de arriba.",
     detalle="Dobla un momento el aro por la mitad para encontrar el centro exacto. Si el ala "
             "queda torcida, el avión gira."),

   _P.vista(_P.aro(5),
     "Dobla las puntas del ala hacia arriba y lánzalo por debajo.",
     detalle="Agárralo por debajo, con el borde grueso delante, y empújalo. No lo tires "
             "fuerte: este necesita poco."),
 ]},

{"id": "anillo",
 "n": 6,
 "nombre": "El Anillo",
 "apodo": "Solo un círculo",
 "ensena": "El aire que pasa por dentro",
 "idea": "No tiene alas, ni punta, ni nada pegado. El aire entra por el agujero y sale por "
         "detrás, y con eso basta para que vuele derecho sin tumbarse.",
 "vuela": "Recto y sorprendentemente lejos, girando sobre sí mismo. Se lanza con la boca "
          "hacia delante, como una pelota de fútbol americano. Es el que nadie se cree.",
 "materiales": "Una hoja y cinta adhesiva.",
 "pasos": [
   _P.doblar((_CX, 0), (_CX, _H), (200, 150),
     "Dobla la hoja por la mitad a lo largo.",
     detalle="El pliegue va en el sentido largo de la hoja, no al través. No hay medidas que "
             "respetar: lo único que importa es que salga recto."),

   _P.doblar((_CX / 2, 0), (_CX / 2, _H), (10, 150),
     "Dóblala otra vez igual. Te queda una tira larga.",
     detalle="Unos cuatro dedos de ancho y casi tan larga como la hoja. Ese ancho será lo "
             "hondo que quede el anillo; el largo, lo grande que salga el círculo."),

   _P.vista(_P.anillo(1),
     "Curva la tira con los dedos hasta cerrar el círculo.",
     detalle="Pásalos por encima sin apretar, como quien riza una cinta, y ve juntando las "
             "dos puntas."),

   _P.vista(_P.anillo(2),
     "Mete una punta dentro de la otra y pega ahí.",
     detalle="Dos dedos de solape. Tiene que quedar un círculo firme, que no se abra al "
             "soltarlo, y lo más redondo que puedas: si sale ovalado, cae de lado."),

   _P.vista(_P.anillo(3),
     "Lánzalo con la boca hacia delante, como un balón.",
     detalle="Agárralo por el borde y empújalo recto, dándole un poco de giro. Ahí lo vas a "
             "entender: no hay ni un ala y se va derecho hasta el fondo del patio."),
 ]},

]

# ─── la sesión ────────────────────────────────────────────────────────────

MAKERS_AGENDA = [
    ("0 – 10", "Bienvenida",
     "Qué es Makers Space y las tres reglas. Lanza dos aviones delante de todos: uno bien "
     "hecho y otro con un ala más corta. El segundo se va de lado. Pregunta por qué y no "
     "des la respuesta."),
    ("10 – 20", "El Dardo, todos",
     "Nivel 1 proyectado paso a paso, sin adelantarse. Nadie sube al siguiente hasta que su "
     "Dardo se vea como una Y de frente."),
    ("20 – 30", "Primer vuelo",
     "Dentro del aula y sin medir nada. Solo mirar qué hace cada avión: cuál pica, cuál "
     "gira, cuál flota. Aquí no se compite todavía."),
    ("30 – 55", "Suben la escalera",
     "Cada uno a su ritmo por los niveles 2 a 6, con la guía proyectada o en el celular. "
     "La mesa de materiales abierta. Tú pasas por las mesas, no explicas de pie."),
    ("55 – 65", "Ajuste",
     "Un clip en la nariz, un alerón doblado, una punta levantada. Regla de la casa: se "
     "cambia UNA cosa y se vuelve a lanzar. Si cambias dos, no sabes cuál sirvió."),
    ("65 – 75", "Preparar el reto",
     "Cada uno elige UN avión, le pone nombre y lo rotula. El que no eligió, no compite: "
     "elegir también es parte del trabajo."),
    ("75 – 105", "El reto, fuera",
     "Pasillo o patio. Dos intentos por categoría y cuenta el mejor. Los jueces anotan en "
     "la hoja mientras se lanza, no después."),
    ("105 – 120", "Premiación y cierre",
     "Se leen los resultados por categoría. Pregunta final, la que importa: «¿qué le "
     "cambiaste a tu avión y qué pasó?». Quien sepa contestarla ya es maker."),
]

MAKERS_CORTE = (
    "Si el bloque se recorta a 45 minutos: llega hasta «Primer vuelo», salta el reto y "
    "deja la escalera abierta para la sesión siguiente. Lo que no se puede recortar es la "
    "bienvenida ni el primer vuelo: sin lanzar nada, la clase no ha ocurrido."
)

MAKERS_JURADO_INTRO = (
    "Cinco categorías, no una. Con una sola gana siempre el mismo avión y el resto deja de "
    "intentarlo a los diez minutos. Con cinco, el Dardo arrasa en distancia y pierde en "
    "permanencia, y esa contradicción es justo lo que tienen que descubrir: no existe el "
    "avión mejor, existe el avión mejor para algo."
)

MAKERS_JURADO = [
    ("Distancia", "Cinta métrica",
     "Desde la línea de lanzamiento hasta donde toca el suelo por primera vez. Se mide en "
     "línea recta, no siguiendo la curva que hizo."),
    ("Permanencia", "Cronómetro",
     "Del momento en que sale de la mano al momento en que toca el suelo. Dos jueces "
     "cronometran y se toma el promedio."),
    ("Puntería", "Cinta métrica",
     "Distancia desde el centro de la diana marcada en el suelo hasta donde cayó. Gana el "
     "número más pequeño."),
    ("Diseño", "Jurado, 1 a 5",
     "Pliegues limpios, los dos lados iguales, y un nombre y un rótulo que se entiendan a "
     "tres metros."),
    ("Ingeniería", "Jurado, 1 a 5",
     "Sabe decir qué le cambió al avión y qué pasó al lanzarlo. Un «no sé, salió así» es "
     "un 1 aunque el avión haya ganado en distancia."),
]

MAKERS_REGLAS_RETO = [
    "Dos intentos por categoría. Cuenta el mejor de los dos.",
    "Se lanza desde detrás de la línea, con los pies quietos. No vale correr.",
    "Si el avión se rompe, se arregla con cinta y se vuelve a lanzar. No se hace otro.",
    "El avión que se lanza es el que se rotuló. No se cambia a última hora.",
]

MAKER_SPACE = {
    "via": "space",
    "horas_sesion": 2,   # lo que dura un bloque de este programa
    "nombre": "Makers Space",
    "publico": "1ro, 2do y 3ro juntos · bloque de 2 horas",
    "resumen": "La sesión de apertura: una escalera de cinco aviones de papel y un reto "
               "medido con jueces.",
    "nota": MAKERS_CORTE,
    # Lo que hace que el deck de esta sesión lleve los pliegues dibujados, uno
    # por diapositiva. Cualquier programa que traiga aviones los tendrá; no hay
    # nada en build_taller.py que sepa de Makers Space en particular.
    "aviones": AVIONES,
    # El guion por minutos. En pantalla va la hora y el titular; el párrafo de
    # cada bloque es nota para el docente y vive en la sesión, no en la pared.
    "agenda": MAKERS_AGENDA,
    "talleres": [
        {"n": 1, "titulo": "Vuela o no vuela", "horas": "2 h", "sesiones": [1],
         "producto": "Un avión rotulado, medido y defendido"},
    ],
    "sesiones": [
        _s(1, 1, "La escalera de aviones",
           "Descubrir, doblando papel y midiendo lo que vuela, que un cambio pequeño y "
           "deliberado vale más que lanzar con más fuerza.",
           [a for a in (
             "Bienvenida y las tres reglas. Dos aviones lanzados delante de todos: uno bien "
             "hecho y otro con un ala más corta. ¿Por qué se va de lado?",
             "Nivel 1, el Dardo, todos a la vez y proyectado. Nadie sube hasta que el suyo se "
             "vea como una Y de frente.",
             "Primer vuelo dentro del aula, sin medir. Solo mirar qué hace cada avión.",
             "Suben la escalera a su ritmo: Planeador, Estable, Delta, Abeja y Anillo. Un concepto "
             "nuevo por peldaño y la mesa de materiales abierta.",
             "Ajuste: se cambia UNA cosa y se vuelve a lanzar. Clip en la nariz, alerón "
             "doblado, punta levantada.",
             "Cada uno elige un avión, lo rotula con un nombre y sale al reto.",
             "Reto fuera, con jueces: distancia, permanencia, puntería, diseño e ingeniería. "
             "Dos intentos y cuenta el mejor.",
             "Premiación y la pregunta de cierre: «¿qué le cambiaste y qué pasó?»."
           )],
           "Que tu avión gane en alguna de las cinco categorías, y que sepas decir qué le "
           "hiciste para conseguirlo.",
           "Hojas de sobra —van a fallar pliegues y está bien—, tijeras, cinta adhesiva, "
           "clips, cinta métrica, un cronómetro por juez, cinta de carrocero para la línea "
           "y la diana, y la hoja de jurado impresa.",
           "Un avión rotulado con su nombre, la fila de la hoja de jurado con sus medidas, y "
           "la frase de qué cambió y qué pasó, dicha en voz alta.",
           "Se lanza hacia donde no hay nadie y nadie va a buscar un avión hasta que todos "
           "hayan lanzado. || Las tijeras se pasan cerradas y por el mango. || FALTA: mirar "
           "antes el patio o el pasillo. Un avión que sale por una ventana o cae en una "
           "escalera para la sesión entera."),
    ],
}

# ─── Makers Space · Sesiones 2 a 5 · Electricidad y circuitos en Tinkercad ──
#
# La base es el Módulo 1 «Fundamentos de Robótica y Electrónica» de Actuana
# Education (Laury Emmanuel Jaquez): sus siete ejercicios —LED, pulsador,
# interruptor, potenciómetro y motor DC— repartidos en cuatro bloques de dos
# horas. Los esquemas son propios: los dibuja `circuitos.py` a partir de estas
# listas, así que un circuito se corrige cambiando un componente aquí.
#
# Primero el simulador entero; los kits físicos vienen después y se anuncian al
# cierre de la sesión 5.

TINKERCAD = "https://www.tinkercad.com/circuits"


_SEGURIDAD_SIM = ("En el simulador nada quema de verdad, y por eso es el sitio para equivocarse: "
                  "lo que allí se quema, en la mesa habría sido humo. || Las computadoras se "
                  "cierran con las dos manos y no se mueven con la tapa abierta.")
_MATERIALES_SIM = ("Una computadora por pareja con Tinkercad abierto, el proyector y el código de "
                   "la clase en la pizarra. Todavía no hacen falta componentes.")

MAKERS_CIRCUITOS = [
    {
        "n": 2,
        "titulo": "Enciende tu primer LED",
        "proposito": "Entender por qué una luz se enciende: una fuente, un camino cerrado y algo "
                     "que limite la corriente.",
        "frase": "La electricidad no se explica: se conecta.",
        "idea": ["fuente", "camino", "carga"],
        "reto": "Que tu LED encienda sin quemarse y que sepas decir, señalando, por dónde pasa la "
                "corriente.",
        "evidencia": "Tu circuito guardado en Tinkercad con tu nombre y el esquema del paso 4 "
                     "dibujado en el cuaderno.",
        "pregunta": "¿Qué pasa si quito la resistencia?",
        "tour": {
            "titulo": "Cómo funciona Tinkercad",
            "puntos": [
                ("El nombre.", "Arriba a la izquierda. Bórralo y pon el tuyo: es como se guarda."),
                ("El panel de piezas.", "A la derecha. Escribe «led», «resistor» o «lemon» y aparece."),
                ("Arrastrar.", "Coges la pieza del panel y la sueltas en el lienzo. Ya está puesta."),
                ("Unir.", "Clic en una patita y clic en la otra: sale un cable. Doble clic lo borra."),
                ("Cambiar valores.", "Un clic en la pieza abre su cuadrito: ohmios, voltios, color."),
                ("Simular.", "El botón azul enciende el circuito. Vuelve a tocarlo para parar."),
            ],
        },
        # Solo esta sesión enseña cómo se entra: en las siguientes ya están dentro.
        "entrada": {
            "titulo": "Entra a la clase de Tinkercad",
            "url": "https://www.tinkercad.com/joinclass",
            "pasos": ["Abre tinkercad.com/joinclass",
                      "Toca «Students with Class Code» y escribe el código de la pizarra",
                      "Elige tu apodo: el de la lista, no un invento",
                      "Entra en «Circuits» y crea un circuito nuevo"],
        },
        "pasos": [
            {"titulo": "La pila de limón",
             "frase": "Seis limones en fila hacen una pila de verdad… si les bajas la resistencia.",
             "piezas": ["Lemon Battery ×6 (búscala como «lemon»)", "LED", "Multímetro", "Cables"],
             "meta": {"fuente": None,
                      "serie": ["limon", "limon", "limon", "limon", "limon", "limon", "led:on"],
                      "gnd": False, "nota": "seis limones: unos 3 V y el LED enciende"},
             "arma": ["Arrastra un limón y mídelo con el multímetro: anota los voltios",
                      "Pon seis en fila (clavo con cobre, clavo con cobre) y vuelve a medir",
                      "Conecta el LED al final y simula: todavía no enciende",
                      "Haz clic en cada limón y cambia «Resistance» de 5.90 a 0.05 kΩ"],
             "comprueba": ["Sé cuántos voltios da un limón y cuántos dan seis",
                           "Con 5.90 kΩ el LED no enciende",
                           "Con 0.05 kΩ en los seis, el LED enciende",
                           "Guardé el circuito con mi nombre"],
             "sube": "¿Con cuántos limones enciende si dejas la resistencia en 0.10 kΩ? Pruébalo y "
                     "anótalo.",
             "respuesta": {
                 "porque": "Cada limón da unos 0,5 V y en fila se suman: seis llegan a 3 V, de sobra "
                           "para un LED. Pero el voltaje solo empuja; lo que decide cuánta corriente "
                           "sale es la resistencia que el limón tiene por dentro. Con 5,90 kΩ pasan "
                           "microamperios y no se ve nada; con 0,05 kΩ pasan unos 3 mA y la luz "
                           "aparece. En un limón de verdad esa resistencia baja cuando las placas "
                           "son grandes y están cerca: por eso en las ferias de ciencia usan muchos "
                           "limones y clavos gordos.",
                 "esquema": {"fuente": None,
                             "serie": ["limon:0,05 kΩ", "limon", "limon", "limon", "limon",
                                       "limon", "led:on"],
                             "gnd": False, "nota": "3 V y poca resistencia: ahora sí"}}},
            {"titulo": "El circuito cerrado",
             "frase": "Una pila y un LED. La corriente sale del +, hace un camino y vuelve al –.",
             "piezas": ["Pila de 9 V", "LED", "2 cables"],
             "meta": {"fuente": "9 V", "serie": ["led:quemado"], "gnd": False,
                      "nota": "el LED se quema"},
             "arma": ["Arrastra una pila de 9 V y un LED",
                      "Cable del + a la pata larga del LED",
                      "Cable de la pata corta al –",
                      "Pulsa «Iniciar simulación»"],
             "comprueba": ["Puedo seguir el camino con el dedo y vuelvo al punto de partida",
                           "Tinkercad avisa de que el LED se quemó"],
             "respuesta": {
                 "porque": "El circuito está bien cerrado, y ese es el problema: nada limita la "
                           "corriente, así que pasa toda la que la pila puede dar y el LED no la "
                           "aguanta. Un LED es una puerta de un solo sentido, no un freno.",
                 "esquema": {"fuente": "9 V", "serie": ["led:quemado"], "gnd": False,
                             "nota": "sin nada que la limite, pasa toda la corriente"}}},
            {"titulo": "La resistencia que lo salva",
             "frase": "220 Ω en el camino: pasa menos corriente y el LED vive.",
             "piezas": ["Resistencia de 220 Ω", "LED", "Pila de 5 V"],
             "meta": {"serie": ["resistencia:220 Ω", "led:on"], "nota": "enciende y no se quema"},
             "arma": ["Pon una resistencia entre el + y la pata larga",
                      "Haz clic en la resistencia y escribe 220 Ω",
                      "Cierra el camino hasta el –",
                      "Inicia la simulación"],
             "comprueba": ["El LED enciende", "Nadie avisa de que se quemó",
                           "La resistencia dice 220 Ω, no 220 kΩ"],
             "respuesta": {
                 "porque": "La resistencia se opone al paso de la corriente. Con 220 Ω pasa lo "
                           "justo para que el LED alumbre y no se destruya; con 1 kΩ pasaría menos "
                           "y brillaría poco.",
                 "esquema": {"serie": ["resistencia:220 Ω", "led:on"],
                             "nota": "la resistencia reparte el trabajo"}}},
            {"titulo": "El LED tiene lado",
             "frase": "Le damos la vuelta al LED: el camino sigue cerrado, pero no enciende.",
             "piezas": ["El mismo circuito", "Paciencia"],
             "meta": {"serie": ["resistencia:220 Ω", "led:off"], "nota": "no enciende: está al revés"},
             "arma": ["Gira el LED (tecla R o el botón de rotar)",
                      "Deja todo lo demás igual",
                      "Inicia la simulación",
                      "Vuelve a girarlo y compruébalo"],
             "comprueba": ["Al revés no enciende", "Al derecho vuelve a encender",
                           "Sé decir cuál pata es la larga"],
             "respuesta": {
                 "porque": "El LED es un diodo: deja pasar la corriente en un solo sentido. La pata "
                           "larga es el ánodo (+) y la corta el cátodo (–). Al revés no hay error "
                           "ni humo: simplemente no pasa nada.",
                 "esquema": {"serie": ["resistencia:220 Ω", "led:off"],
                             "nota": "la corriente choca contra la puerta cerrada"}}},
            {"titulo": "Dos LEDs: en fila o cada uno por su lado",
             "frase": "En serie comparten el voltaje y brillan menos. En paralelo, cada uno tiene el suyo.",
             "piezas": ["2 LEDs", "2 resistencias de 220 Ω"],
             "meta": {"serie": ["resistencia:220 Ω"], "ramas": [["led:on"], ["led:on"]],
                      "nota": "en paralelo los dos brillan igual"},
             "arma": ["Primero los dos LEDs en fila, uno detrás de otro: mira el brillo",
                      "Ahora dale a cada LED su propio camino desde el +",
                      "Ponle su resistencia a cada uno",
                      "Compara el brillo de las dos formas"],
             "comprueba": ["Probé las dos formas", "Sé decir en cuál brillan más",
                           "Cada LED tiene su resistencia"],
             "respuesta": {
                 "porque": "En serie, los 5 V se reparten entre los dos LEDs: a cada uno le toca la "
                           "mitad y brillan menos. En paralelo, cada rama recibe los 5 V completos. "
                           "Esto es la ley de Ohm mirada de frente: V = I × R.",
                 "esquema": {"serie": ["resistencia:220 Ω", "led:on", "led:on"],
                             "nota": "en serie se reparten el voltaje"}}},
        ],
    },
    {
        "n": 3,
        "titulo": "Enciende y apaga",
        "proposito": "Controlar el circuito con la mano: un pulsador que vuelve solo y un "
                     "interruptor que se queda como lo dejaste.",
        "frase": "Un circuito que no se puede apagar no sirve.",
        "idea": ["abrir", "cerrar", "controlar"],
        "reto": "Que tu semáforo de mano funcione veinte veces seguidas en manos de otra pareja.",
        "evidencia": "Los tres circuitos guardados y la tabla del diagnóstico con lo que predijiste "
                     "y lo que pasó.",
        "pregunta": "¿En qué se parecen un pulsador y el timbre de tu casa?",
        "pasos": [
            {"titulo": "El pulsador: mientras lo aprietas",
             "frase": "Un interruptor momentáneo: cierra el camino solo mientras tu dedo está encima.",
             "piezas": ["Pulsador", "Resistencia de 220 Ω", "LED"],
             "meta": {"serie": ["pulsador:suelto", "resistencia:220 Ω", "led:off"],
                      "nota": "suelto: el camino está abierto"},
             "arma": ["Corta el camino y mete el pulsador ahí",
                      "Usa dos patas que estén en diagonal",
                      "Inicia la simulación",
                      "Haz clic en el pulsador y no lo sueltes"],
             "comprueba": ["Apretado enciende", "Al soltar se apaga solo",
                           "Sin apretar, el LED está apagado"],
             "respuesta": {
                 "porque": "El pulsador tiene cuatro patas, unidas de dos en dos. Si usas dos patas "
                           "del mismo par, el circuito está siempre cerrado y el botón no hace "
                           "nada: por eso se toman en diagonal.",
                 "esquema": {"serie": ["pulsador:presionado", "resistencia:220 Ω", "led:on"],
                             "nota": "presionado: el camino se cierra"}}},
            {"titulo": "El interruptor: se queda",
             "frase": "El mismo circuito, pero recuerda en qué posición lo dejaste.",
             "piezas": ["Interruptor deslizante", "Resistencia de 220 Ω", "LED"],
             "meta": {"serie": ["interruptor:cerrado", "resistencia:220 Ω", "led:on"],
                      "nota": "queda encendido sin tocar nada"},
             "arma": ["Cambia el pulsador por un interruptor deslizante",
                      "Conecta la pata del centro al camino",
                      "Inicia la simulación",
                      "Deslízalo y suéltalo"],
             "comprueba": ["Se queda encendido sin mantener el clic",
                           "Vuelve a apagarse al deslizarlo",
                           "Sé decir en qué se diferencia del pulsador"],
             "respuesta": {
                 "porque": "El pulsador vuelve solo a su posición; el interruptor se queda. Por eso "
                           "el timbre lleva pulsador y la lámpara lleva interruptor.",
                 "esquema": {"serie": ["interruptor:abierto", "resistencia:220 Ω", "led:off"],
                             "nota": "abierto: el camino se corta"}}},
            {"titulo": "El semáforo de mano",
             "frase": "Dos botones, dos LEDs, dos caminos que salen del mismo +.",
             "piezas": ["2 pulsadores", "2 LEDs", "2 resistencias de 220 Ω"],
             "meta": {"ramas": [["pulsador:suelto", "resistencia:220 Ω", "led:off"],
                                ["pulsador:presionado", "resistencia:220 Ω", "led:on"]],
                      "nota": "cada botón manda en su LED"},
             "arma": ["Duplica lo del paso 1 (Ctrl+C y Ctrl+V también sirven aquí)",
                      "Los dos caminos salen del + y vuelven al –",
                      "Un LED rojo y uno verde",
                      "Pruébalos por turnos y luego los dos a la vez"],
             "comprueba": ["Cada botón enciende solo su LED",
                           "Los dos a la vez encienden los dos",
                           "Ningún LED se queda encendido sin botón"],
             "respuesta": {
                 "porque": "Son dos circuitos en paralelo que comparten la fuente. Lo que pase en "
                           "una rama no cambia la otra, y por eso el semáforo funciona.",
                 "esquema": {"ramas": [["pulsador:presionado", "resistencia:220 Ω", "led:on"],
                                       ["pulsador:suelto", "resistencia:220 Ω", "led:off"]],
                             "nota": "dos ramas, una sola pila"}}},
            {"titulo": "Diagnóstico: rompe y explica",
             "frase": "Tu profe cambia una cosa. Predice qué va a pasar y después compruébalo.",
             "piezas": ["Caso 1: LED al revés", "Caso 2: 220 Ω → 1 kΩ", "Caso 3: cable en el riel equivocado"],
             "meta": {"serie": ["pulsador:presionado", "resistencia:1 kΩ", "led:off"],
                      "nota": "¿por qué no enciende?"},
             "arma": ["Escribe tu predicción ANTES de simular",
                      "Caso 1: gira el LED y mira qué pasa",
                      "Caso 2: sube la resistencia a 1 kΩ y compara el brillo",
                      "Caso 3: mueve un cable de fila y busca el fallo"],
             "comprueba": ["Escribí las tres predicciones antes de probar",
                           "Encontré el fallo del caso 3 sin deshacer todo",
                           "Sé nombrar cada parte: pila, pulsador, resistencia, LED, GND"],
             "respuesta": {
                 "porque": "Caso 1: no enciende, el diodo bloquea. Caso 2: enciende más flojo, "
                           "porque más resistencia es menos corriente. Caso 3: no pasa nada, porque "
                           "una fila de la protoboard no es la de al lado: el camino quedó abierto.",
                 "esquema": {"serie": ["pulsador:presionado", "resistencia:220 Ω", "led:on"],
                             "nota": "así se ve cuando está bien"}}},
        ],
    },
    {
        "n": 4,
        "titulo": "Cuánta corriente pasa",
        "proposito": "Medir en vez de adivinar: el potenciómetro cambia la resistencia y el "
                     "multímetro dice qué está pasando de verdad.",
        "frase": "Medir es saber.",
        "idea": ["voltaje", "resistencia", "corriente"],
        "reto": "Decir, con el número que mediste, cuánta corriente pasa por tu LED.",
        "evidencia": "La tabla con tres medidas (mínimo, medio y máximo) y tu cuenta de V = I × R.",
        "pregunta": "Si subo la resistencia, ¿sube o baja la corriente?",
        "pasos": [
            {"titulo": "El potenciómetro: resistencia con perilla",
             "frase": "Una resistencia que cambia cuando giras. El brillo la sigue.",
             "piezas": ["Potenciómetro de 10 kΩ", "Resistencia de 220 Ω", "LED"],
             "meta": {"serie": ["potenciometro:10 kΩ", "resistencia:220 Ω", "led:on"],
                      "nota": "girando cambia el brillo"},
             "arma": ["Pon el potenciómetro antes de la resistencia",
                      "Usa la pata del centro y una de los lados",
                      "Inicia la simulación",
                      "Gira la perilla de un extremo al otro"],
             "comprueba": ["Al girar cambia el brillo", "En un extremo casi no se ve",
                           "El LED nunca se queda sin su resistencia de 220 Ω"],
             "respuesta": {
                 "porque": "El potenciómetro es una resistencia variable: la perilla mueve un "
                           "cursor y decide cuánta resistencia hay en el camino. La de 220 Ω se "
                           "queda como red de seguridad para cuando el potenciómetro esté en cero.",
                 "esquema": {"serie": ["potenciometro:0 – 10 kΩ", "resistencia:220 Ω", "led:on"],
                             "nota": "más resistencia, menos corriente"}}},
            {"titulo": "El multímetro dice la verdad",
             "frase": "Se conecta en paralelo con lo que quieres medir, como quien escucha al lado.",
             "piezas": ["Multímetro", "El circuito del paso 1"],
             "meta": {"serie": ["potenciometro:10 kΩ", "resistencia:220 Ω", "led:on"],
                      "nota": "mide el voltaje de la resistencia"},
             "arma": ["Arrastra un multímetro y ponlo en «Voltaje»",
                      "Punta roja a un lado de la resistencia, negra al otro",
                      "Inicia la simulación y anota el número",
                      "Gira la perilla y anota otra vez"],
             "comprueba": ["Anoté tres medidas distintas",
                           "El multímetro está en paralelo, no cortando el camino",
                           "Sé qué mide: voltios"],
             "respuesta": {
                 "porque": "El voltaje es la diferencia entre dos puntos, así que el multímetro se "
                           "pone a los lados del componente. Para medir corriente sería al revés: "
                           "cortando el camino y pasando por él.",
                 "esquema": {"serie": ["potenciometro:10 kΩ", "resistencia:220 Ω", "led:on"],
                             "nota": "voltaje: se mide a los lados"}}},
            {"titulo": "La ley de Ohm con tus números",
             "frase": "V = I × R. Si mides V y sabes R, la corriente sale sola.",
             "piezas": ["Tus tres medidas", "Una calculadora"],
             "meta": {"serie": ["resistencia:220 Ω", "led:on"],
                      "nota": "2 V ÷ 220 Ω = 0,009 A = 9 mA"},
             "arma": ["Toma el voltaje que mediste en la resistencia de 220 Ω",
                      "Divide ese voltaje entre 220",
                      "El resultado son amperios: multiplícalo por 1000 y tendrás miliamperios",
                      "Repite con la perilla en otra posición"],
             "comprueba": ["Tengo la corriente en miliamperios",
                           "Con más resistencia me dio menos corriente",
                           "Mi número está entre 1 mA y 20 mA"],
             "respuesta": {
                 "porque": "De V = I × R sale I = V ÷ R. Un LED normal trabaja contento entre 5 mA "
                           "y 20 mA; por encima de eso empieza a sufrir, y ahí está la razón de la "
                           "resistencia de 220 Ω del primer día.",
                 "esquema": {"serie": ["resistencia:220 Ω", "led:on"],
                             "nota": "I = V ÷ R"}}},
            {"titulo": "Reto: la lámpara con dimmer",
             "frase": "Un potenciómetro, dos LEDs y un solo mando para los dos.",
             "piezas": ["Potenciómetro", "2 LEDs", "2 resistencias de 220 Ω"],
             "meta": {"serie": ["potenciometro:10 kΩ"], "ramas": [["led:on"], ["led:on"]],
                      "nota": "los dos suben y bajan juntos"},
             "arma": ["Parte del circuito del paso 1",
                      "Abre dos ramas después del potenciómetro",
                      "Cada rama, su LED y su resistencia",
                      "Gira y comprueba que los dos obedecen"],
             "comprueba": ["Los dos LEDs cambian a la vez",
                           "Cada LED tiene su resistencia",
                           "Guardé el circuito con mi nombre"],
             "respuesta": {
                 "porque": "El potenciómetro está antes del reparto, así que manda sobre las dos "
                           "ramas. Si lo pusieras dentro de una rama, solo obedecería ese LED.",
                 "esquema": {"serie": ["potenciometro:10 kΩ"], "ramas": [["led:on"], ["led:on"]],
                             "nota": "el mando va antes del reparto"}}},
        ],
    },
    {
        "n": 5,
        "titulo": "Que se mueva",
        "proposito": "Pasar de la luz al movimiento: un motor DC, su sentido de giro y su "
                     "velocidad.",
        "frase": "La corriente también mueve cosas.",
        "idea": ["corriente", "campo", "movimiento"],
        "reto": "Que tu motor arranque, pare y cambie de velocidad sin tocar ningún cable.",
        "evidencia": "El circuito del motor con su interruptor y su potenciómetro, guardado y "
                     "explicado en voz alta.",
        "pregunta": "¿Qué cambia si le doy la vuelta a los dos cables del motor?",
        "pasos": [
            {"titulo": "El motor gira",
             "frase": "La corriente hace un campo magnético y el campo empuja al rotor.",
             "piezas": ["Motor DC", "Pila de 9 V", "2 cables"],
             "meta": {"fuente": "9 V", "serie": ["motor:gira"], "gnd": False,
                      "nota": "gira mientras haya camino"},
             "arma": ["Arrastra un motor DC y una pila de 9 V",
                      "Un cable a cada terminal del motor",
                      "Inicia la simulación",
                      "Fíjate en las RPM que muestra Tinkercad"],
             "comprueba": ["El motor gira", "Veo el número de RPM",
                           "Sé qué significa RPM: vueltas en un minuto"],
             "respuesta": {
                 "porque": "Dentro del motor la corriente pasa por unas bobinas y crea un campo "
                           "magnético que empuja al rotor. Por eso un motor no es una bombilla: "
                           "convierte electricidad en movimiento.",
                 "esquema": {"fuente": "9 V", "serie": ["motor:gira"], "gnd": False,
                             "nota": "RPM: vueltas por minuto"}}},
            {"titulo": "Dale la vuelta",
             "frase": "Los mismos dos cables, cambiados de sitio: gira al contrario.",
             "piezas": ["El mismo circuito"],
             "meta": {"fuente": "9 V", "serie": ["motor:invertido"], "gnd": False, "invertida": True,
                      "nota": "gira al revés"},
             "arma": ["Para la simulación",
                      "Cambia el cable del + por el del –",
                      "Vuelve a simular",
                      "Mira hacia dónde gira ahora"],
             "comprueba": ["Gira al contrario", "El motor no se quemó",
                           "Sé decir por qué un LED al revés no enciende y un motor sí funciona"],
             "respuesta": {
                 "porque": "En el motor la polaridad decide el sentido del giro, no si funciona o "
                           "no. El LED es un diodo y solo deja pasar en un sentido; el motor "
                           "acepta los dos, y en cada uno gira hacia un lado.",
                 "esquema": {"fuente": "9 V", "serie": ["motor:invertido"], "gnd": False,
                             "invertida": True, "nota": "el + y el – cambiados"}}},
            {"titulo": "Arranca y para",
             "frase": "El interruptor de la sesión pasada, ahora mandando un motor.",
             "piezas": ["Motor DC", "Interruptor", "Pila de 9 V"],
             "meta": {"fuente": "9 V", "serie": ["interruptor:cerrado", "motor:gira"], "gnd": False,
                      "nota": "cerrado: gira; abierto: para"},
             "arma": ["Mete el interruptor en el camino del motor",
                      "Usa la pata del centro",
                      "Inicia la simulación",
                      "Enciende y apaga tres veces"],
             "comprueba": ["Con el interruptor abierto, el motor está quieto",
                           "Al cerrarlo arranca", "El circuito no se quedó a medias"],
             "respuesta": {
                 "porque": "Es el mismo circuito de siempre, con una carga distinta. Lo que "
                           "aprendiste del LED vale para el motor: fuente, camino cerrado y algo "
                           "que consume.",
                 "esquema": {"fuente": "9 V", "serie": ["interruptor:abierto", "motor:parado"],
                             "gnd": False, "nota": "abierto: el motor no recibe nada"}}},
            {"titulo": "Rápido o despacio",
             "frase": "El potenciómetro le baja la corriente al motor y el motor baja las RPM.",
             "piezas": ["Motor DC", "Potenciómetro de 10 kΩ", "Interruptor", "Pila de 9 V"],
             "meta": {"fuente": "9 V", "serie": ["interruptor:cerrado", "potenciometro:10 kΩ", "motor:gira"],
                      "gnd": False, "nota": "las RPM suben y bajan con la perilla"},
             "arma": ["Añade el potenciómetro entre el interruptor y el motor",
                      "Inicia la simulación",
                      "Gira despacio y mira las RPM",
                      "Anota las RPM en tres posiciones"],
             "comprueba": ["Tengo tres números de RPM distintos",
                           "El motor se puede apagar sin tocar cables",
                           "Guardé el circuito con mi nombre"],
             "respuesta": {
                 "porque": "Más resistencia, menos corriente; menos corriente, campo más débil y "
                           "menos vueltas. Es la misma ley de Ohm de la sesión pasada, ahora "
                           "medida en RPM en vez de en brillo.",
                 "esquema": {"fuente": "9 V",
                             "serie": ["interruptor:cerrado", "potenciometro:0 – 10 kΩ", "motor:gira"],
                             "gnd": False, "nota": "la perilla manda en la velocidad"}}},
        ],
    },
]

# El peldaño que cierra cada sesión no es un ejercicio: es algo que sirve. Se
# marca con "proyecto" y en pantalla lleva su chapa, para qué sirve y por dónde
# subir de nivel. Los kits reales llegarán después; el diseño ya está hecho.
_PROYECTOS = {
    2: {"titulo": "Proyecto: la luz trasera de la bici",
        "para": "Para que te vean de noche. Dos luces rojas que brillan igual, y si una falla la "
                "otra sigue.",
        "frase": "Dos caminos desde la misma pila: cada LED con su resistencia.",
        "piezas": ["Pila de 9 V", "2 LEDs rojos", "2 resistencias de 220 Ω", "Cables"],
        "meta": {"fuente": "9 V", "ramas": [["resistencia:220 Ω", "led:on"],
                                            ["resistencia:220 Ω", "led:on"]],
                 "nota": "las dos luces, igual de fuertes"},
        "arma": ["Circuito nuevo, guardado como «Luz de bici · tu nombre»",
                 "Del + salen dos caminos, cada uno con su resistencia y su LED",
                 "Los dos caminos vuelven al –",
                 "Simula y compara el brillo de las dos luces"],
        "comprueba": ["Las dos luces encienden con el mismo brillo",
                      "Si borro un LED, el otro sigue encendido",
                      "Cada LED tiene su propia resistencia",
                      "Está guardado con mi nombre"],
        "sube": "Añade una tercera luz sin que las otras dos pierdan brillo.",
        "respuesta": {
            "porque": "En paralelo cada rama recibe el voltaje completo, así que las dos luces "
                      "brillan igual y una no depende de la otra. En serie, si se quema un LED se "
                      "apagan todos: es lo que pasaba con las luces viejas de Navidad.",
            "esquema": {"fuente": "9 V", "ramas": [["resistencia:220 Ω", "led:on"],
                                                   ["resistencia:220 Ω", "led:on"],
                                                   ["resistencia:220 Ω", "led:on"]],
                        "nota": "tres ramas: cada una, su resistencia"}}},
    3: {"titulo": "Proyecto: el timbre de la puerta",
        "para": "Para avisar de que alguien llegó: suena mientras lo aprietan y una luz lo "
                "confirma, para quien no oye bien.",
        "frase": "Un pulsador manda sobre dos cosas a la vez: el zumbador y la luz.",
        "piezas": ["Pulsador", "Zumbador (piezo)", "LED", "Resistencia de 220 Ω", "Pila de 5 V"],
        "meta": {"serie": ["pulsador:presionado"],
                 "ramas": [["zumbador:suena"], ["resistencia:220 Ω", "led:on"]],
                 "nota": "apretado: suena y alumbra"},
        "arma": ["Pon el pulsador justo después del +",
                 "Después del pulsador, abre dos caminos: uno al zumbador y otro al LED",
                 "El LED, con su resistencia; el zumbador, sin ella",
                 "Simula y aprieta el botón"],
        "comprueba": ["Al apretar suena y se enciende la luz",
                      "Al soltar se apagan los dos",
                      "El zumbador está en su rama, no en serie con el LED",
                      "Está guardado con mi nombre"],
        "sube": "Un interruptor «modo noche» que deje solo la luz, sin sonido.",
        "respuesta": {
            "porque": "El pulsador está antes del reparto, así que abre y cierra las dos ramas a la "
                      "vez. Si lo pusieras dentro de una rama, solo mandaría en esa. El zumbador no "
                      "necesita resistencia porque ya limita él la corriente que le entra.",
            "esquema": {"serie": ["pulsador:suelto"],
                        "ramas": [["zumbador:callado"], ["resistencia:220 Ω", "led:off"]],
                        "nota": "suelto: silencio y oscuridad"}}},
    4: {"titulo": "Proyecto: la luz de noche que se enciende sola",
        "para": "Para el pasillo o la mesita: cuando baja la luz de la habitación, la lámpara se "
                "enciende sin que nadie la toque.",
        "frase": "La fotorresistencia baja su resistencia a oscuras, y con menos resistencia pasa "
                 "más corriente.",
        "piezas": ["Fotorresistencia (LDR)", "LED", "Resistencia de 220 Ω", "Pila de 5 V"],
        "meta": {"serie": ["ldr:a oscuras", "resistencia:220 Ω", "led:on"],
                 "nota": "a oscuras: la luz se enciende sola"},
        "arma": ["Pon la fotorresistencia en el camino, antes de la resistencia",
                 "Simula y mueve el deslizador de luz que aparece encima de ella",
                 "Mira cómo cambia el brillo del LED",
                 "Mide con el multímetro en dos situaciones: con luz y a oscuras"],
        "comprueba": ["A oscuras el LED brilla más",
                      "Con mucha luz casi se apaga",
                      "Tengo las dos medidas anotadas",
                      "Está guardado con mi nombre"],
        "sube": "Añade un potenciómetro para decidir tú a qué oscuridad se enciende.",
        "respuesta": {
            "porque": "La fotorresistencia es una resistencia que obedece a la luz: mucha luz, "
                      "mucha resistencia y casi no pasa corriente; a oscuras baja y el LED alumbra. "
                      "Es la ley de Ohm otra vez, con el sensor haciendo de perilla.",
            "esquema": {"serie": ["ldr:con luz", "resistencia:220 Ω", "led:off"],
                        "nota": "con luz: la lámpara se apaga sola"}}},
    5: {"titulo": "Proyecto: el ventilador de mesa",
        "para": "Para el aula en mayo: un ventilador con su llave de encendido, su perilla de "
                "velocidad y una luz que avisa de que está trabajando.",
        "frase": "El interruptor y la perilla mandan sobre dos ramas: el motor y la luz de aviso.",
        "piezas": ["Motor DC", "Interruptor", "Potenciómetro de 10 kΩ", "LED",
                   "Resistencia de 220 Ω", "Pila de 9 V"],
        "meta": {"fuente": "9 V", "serie": ["interruptor:cerrado", "potenciometro:0 – 10 kΩ"],
                 "ramas": [["motor:gira"], ["resistencia:220 Ω", "led:on"]], "gnd": False,
                 "nota": "gira y avisa con su luz"},
        "arma": ["Interruptor y potenciómetro en el camino principal",
                 "Después, dos ramas: el motor en una y el LED con su resistencia en la otra",
                 "Simula: enciende, apaga y gira la perilla",
                 "Anota las RPM en tres posiciones"],
        "comprueba": ["Con el interruptor abierto no gira ni se enciende la luz",
                      "La perilla cambia las RPM",
                      "La luz avisa siempre que el motor está encendido",
                      "Tengo tres medidas de RPM anotadas"],
        "sube": "Piensa cómo harías que girara al revés con una sola llave: dibuja el esquema "
                "aunque no lo montes.",
        "respuesta": {
            "porque": "El interruptor y el potenciómetro están antes del reparto, así que mandan "
                      "sobre las dos ramas a la vez. La luz de aviso va en paralelo con el motor, "
                      "no en serie: en serie se robaría parte del voltaje y el motor iría más "
                      "despacio.",
            "esquema": {"fuente": "9 V", "serie": ["interruptor:abierto", "potenciometro:10 kΩ"],
                        "ramas": [["motor:parado"], ["resistencia:220 Ω", "led:off"]], "gnd": False,
                        "nota": "la llave abierta para las dos ramas"}}},
}
for _ses in MAKERS_CIRCUITOS:
    _ses["pasos"].append({**_PROYECTOS[_ses["n"]], "proyecto": True})

MAKER_SPACE["talleres"].append(
    {"n": 2, "titulo": "Electricidad y circuitos en Tinkercad", "horas": "8 h",
     "sesiones": [2, 3, 4, 5],
     "producto": "Cuatro circuitos simulados, medidos y explicados por la pareja"})

for _ses in MAKERS_CIRCUITOS:
    MAKER_SPACE["sesiones"].append({
        **_s(_ses["n"], 2, _ses["titulo"], _ses["proposito"],
             [p["titulo"] for p in _ses["pasos"]],
             _ses["reto"], _MATERIALES_SIM, _ses["evidencia"], _SEGURIDAD_SIM),
        "aviones": False,
        "frase": _ses["frase"],
        # Sin la diapositiva de «Cómo trabajamos» ni la de «La idea»: de la
        # portada al taller, que el tiempo es de ellos.
        "circuitos": _ses["pasos"],
        "entrada": _ses.get("entrada"),
        "tour": _ses.get("tour"),
        "tinkercad": TINKERCAD,
        "pregunta": _ses["pregunta"],
    })


# ─── Makers Space · Sesión 6 · El botón que cambia de color ───────────────
#
# Programación, pero construida por ellos: el botón no se descarga, se escribe
# desde una página en blanco, y en la segunda hora se convierte en algo que
# alguien de la escuela puede usar. Primaria arma el mismo programa con
# tarjetas, sin teclear; secundaria lo escribe línea a línea.

_BOTON_CSS = ("body{font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:90vh;"
              "margin:0;transition:background .3s}\n"
              "button{font-size:1.4rem;padding:.8rem 1.6rem;border:0;border-radius:999px;cursor:pointer}")

MAKERS_BOTON = {
    "intro": ("Un botón que cambia de color es el programa más pequeño que reacciona a una persona. "
              "Hoy lo construyen desde una página en blanco y después lo convierten en algo que alguien "
              "de la escuela pueda usar de verdad."),
    "teoria": {
        "titulo": "Cómo reacciona una página",
        "pasos": [
            ("Algo pasa", "El evento: alguien toca el botón. Sin evento, el programa espera."),
            ("Se ejecuta una orden", "La función: los pasos que escribiste, uno detrás de otro."),
            ("Algo cambia", "El resultado: el color, un texto, un número en la página."),
        ],
        "enlace": "Es lo mismo que programar al robot de la semana 1: órdenes en orden. Ahora "
                  "las lee la computadora y el que toca el botón decide cuándo.",
    },
    "primaria": {
        "colores": [("tomato", "Rojo"), ("gold", "Amarillo"), ("seagreen", "Verde"),
                    ("royalblue", "Azul"), ("orchid", "Morado"), ("orange", "Naranja")],
        "mensajes": ["¡Hola!", "¡Lo logré!", "Silencio, por favor", "¡A jugar!", "Libre", "Ocupado"],
        "textos": ["Tócame", "¡Magia!", "Cambiar", "Rojo", "Verde"],
        "maximo": 3,
    },
    "proyectos": [
        {"id": "semaforo", "emoji": "🚦", "titulo": "Semáforo del aula",
         "para": "Para que el docente diga sin hablar cómo va la clase.",
         "pide": "Tres botones: rojo es silencio, amarillo es trabajo en grupo, verde es que pueden hablar. "
                 "El fondo y el mensaje cambian con cada uno.",
         "sube": "Un cuarto estado inventado por ti, y que el mensaje diga también la hora.",
         "html": '<h1 id="estado">¿Cómo va la clase?</h1>\n'
                 '<div>\n  <button id="rojo">Silencio</button>\n'
                 '  <button id="amarillo">En grupo</button>\n'
                 '  <button id="verde">Pueden hablar</button>\n</div>',
         "css": _BOTON_CSS + "\nh1{font-size:3rem;text-align:center}\ndiv{display:flex;gap:1rem}",
         "py": 'from pyscript import when, document\n\n'
               'def poner(color, texto):\n'
               '    document.body.style.background = color\n'
               '    document.querySelector("#estado").innerText = texto\n\n'
               '@when("click", "#rojo")\n'
               'def silencio(evento):\n'
               '    poner("tomato", "Silencio")\n\n'
               '@when("click", "#amarillo")\n'
               'def grupo(evento):\n'
               '    poner("gold", "Trabajo en grupo")\n\n'
               '# Tu turno: el botón verde\n'},
        {"id": "preguntas", "emoji": "✅", "titulo": "Tablero de preguntas",
         "para": "Para repasar un tema de cualquier materia jugando.",
         "pide": "Una pregunta con tres respuestas. La correcta pone la página en verde y la "
                 "incorrecta en rojo, con un mensaje.",
         "sube": "Una lista de preguntas y un botón «Siguiente» que pase a la próxima.",
         "html": '<h1 id="pregunta">¿Cuánto es 7 × 8?</h1>\n'
                 '<div>\n  <button id="a">54</button>\n  <button id="b">56</button>\n'
                 '  <button id="c">64</button>\n</div>\n<p id="mensaje"></p>',
         "css": _BOTON_CSS + "\ndiv{display:flex;gap:1rem}\np{font-size:1.5rem}",
         "py": 'from pyscript import when, document\n\n'
               'def responder(bien):\n'
               '    if bien:\n'
               '        document.body.style.background = "seagreen"\n'
               '        document.querySelector("#mensaje").innerText = "¡Correcto!"\n'
               '    else:\n'
               '        document.body.style.background = "tomato"\n'
               '        document.querySelector("#mensaje").innerText = "Intenta otra vez"\n\n'
               '@when("click", "#b")\n'
               'def correcta(evento):\n'
               '    responder(True)\n\n'
               '@when("click", "#a")\n'
               'def mal_a(evento):\n'
               '    responder(False)\n\n'
               '# Tu turno: el botón c, y tu propia pregunta\n'},
        {"id": "reflejos", "emoji": "⚡", "titulo": "Juego de reflejos",
         "para": "Para medir quién reacciona más rápido del grupo.",
         "pide": "Al pulsar Empezar, la pantalla se pone roja y, en un momento al azar, verde. "
                 "Hay que tocarla en cuanto cambia: el programa dice cuántos milisegundos tardaste.",
         "sube": "Guardar el mejor tiempo en una variable y decir si batiste tu récord.",
         "html": '<button id="empezar">Empezar</button>\n'
                 '<div id="pantalla">Pulsa Empezar</div>\n<p id="resultado"></p>',
         "css": _BOTON_CSS + "\n#pantalla{width:80vw;height:40vh;display:grid;place-items:center;"
                "font-size:2rem;color:white;background:slategray;border-radius:20px;cursor:pointer}",
         "py": 'import asyncio\nimport random\nimport time\nfrom pyscript import when, document\n\n'
               'inicio = None\n\n'
               '@when("click", "#empezar")\n'
               'async def empezar(evento):\n'
               '    global inicio\n'
               '    inicio = None\n'
               '    pantalla = document.querySelector("#pantalla")\n'
               '    pantalla.style.background = "firebrick"\n'
               '    pantalla.innerText = "Espera el verde…"\n'
               '    await asyncio.sleep(random.uniform(2, 5))\n'
               '    pantalla.style.background = "seagreen"\n'
               '    pantalla.innerText = "¡TOCA!"\n'
               '    inicio = time.time()\n\n'
               '@when("click", "#pantalla")\n'
               'def tocar(evento):\n'
               '    global inicio\n'
               '    if inicio is None:\n'
               '        document.querySelector("#resultado").innerText = "Espera el verde."\n'
               '        return\n'
               '    ms = round((time.time() - inicio) * 1000)\n'
               '    inicio = None\n'
               '    document.querySelector("#resultado").innerText = f"Tardaste {ms} ms"\n'},
        {"id": "letrero", "emoji": "🏷️", "titulo": "Letrero de puerta",
         "para": "Para la puerta del aula, de la biblioteca o del laboratorio.",
         "pide": "Tres botones: libre, ocupado y vuelvo en 5 minutos. El letrero se pone grande, "
                 "con su color y su texto.",
         "sube": "Un botón que cambie el letrero cada vez que se toca, recorriendo una lista de estados.",
         "html": '<h1 id="letrero">LIBRE</h1>\n<div>\n  <button id="libre">Libre</button>\n'
                 '  <button id="ocupado">Ocupado</button>\n  <button id="vuelvo">Vuelvo en 5</button>\n</div>',
         "css": _BOTON_CSS + "\nh1{font-size:5rem;margin:0}\ndiv{display:flex;gap:1rem}",
         "py": 'from pyscript import when, document\n\n'
               'def letrero(color, texto):\n'
               '    document.body.style.background = color\n'
               '    document.querySelector("#letrero").innerText = texto\n\n'
               '@when("click", "#libre")\n'
               'def libre(evento):\n'
               '    letrero("seagreen", "LIBRE")\n\n'
               '# Tu turno: ocupado y vuelvo en 5 minutos\n'},
    ],
    "jurado": [
        ("La que nunca falla", "Otra pareja la usa veinte veces seguidas y nunca se traba."),
        ("La más útil", "La que alguien de la escuela usaría mañana."),
        ("La más creativa", "La idea o el diseño que nadie más tuvo."),
        ("La mejor explicada", "Leen en voz alta la línea que hace el cambio y dicen qué hace."),
    ],
    "reglas": [
        "Primero funciona, después se pone bonito.",
        "Si algo falla, se lee el error: dice la línea.",
        "Se prueba con otra pareja antes de decir que está listo.",
    ],
}

# La progresión que se proyecta: tres botones, cada uno construido sobre el
# anterior. Cada paso es el programa COMPLETO hasta ese punto, para que se
# ejecute solo; las líneas nuevas no se marcan a mano, las calcula el deck
# comparando con el paso anterior.
_PB_CSS = ("body{font-family:system-ui,sans-serif;display:grid;place-items:center;align-content:center;"
           "gap:1rem;min-height:90vh;margin:0}\n"
           "button{font-size:1.4rem;padding:.8rem 1.6rem;border:0;border-radius:999px;cursor:pointer}")
_PB_CSS_SUAVE = _PB_CSS + "\nbody{transition:background .6s}"
_PB_CSS_SALTO = _PB_CSS_SUAVE + "\n@keyframes salto{50%{transform:scale(1.3)}}\n.salta{animation:salto .4s}"
_PB_HTML = '<h1>Mi botón</h1>\n<button id="boton">Tócame</button>'
_PB_HTML_CUENTA = _PB_HTML + '\n<p id="cuenta">0 clics</p>'
_PB_HTML_VARIOS = (_PB_HTML_CUENTA + '\n<div id="colores">\n  <button id="rojo">Rojo</button>\n'
                   '  <button id="verde">Verde</button>\n  <button id="azul">Azul</button>\n</div>')
_PB_HTML_FIESTA = _PB_HTML_VARIOS + '\n<button id="fiesta">🎉 Fiesta</button>'
_PB_SALTO = ('    boton = document.querySelector("#boton")\n'
             '    boton.classList.remove("salta")\n'
             '    boton.offsetWidth\n'
             '    boton.classList.add("salta")\n')
_PB_PONER = ('def poner(color):\n'
             '    global clics\n'
             '    clics += 1\n'
             '    document.body.style.background = color\n'
             '    document.querySelector("#cuenta").innerText = f"{clics} clics · {color}"\n'
             + _PB_SALTO +
             '\n@when("click", "#boton")\n'
             'def cambiar(evento):\n'
             '    poner(random.choice(colores))\n\n'
             '@when("click", "#rojo")\n'
             'def rojo(evento):\n'
             '    poner("tomato")\n\n'
             '@when("click", "#verde")\n'
             'def verde(evento):\n'
             '    poner("seagreen")\n\n'
             '@when("click", "#azul")\n'
             'def azul(evento):\n'
             '    poner("royalblue")\n')
_PB_COLORES = 'colores = ["tomato", "gold", "seagreen", "royalblue", "orchid"]\n'

MAKERS_BOTON["progresion"] = [
    {"titulo": "El botón que cambia el fondo", "pasos": [
        {"titulo": "Un botón con nombre",
         "frase": "HTML pone el botón en la página. Su id es el nombre con que Python lo encuentra.",
         "html": _PB_HTML, "css": _PB_CSS, "py": ""},
        {"titulo": "Que el clic cambie el fondo",
         "frase": "@when une el clic con la función; la función cambia el color del fondo.",
         "html": _PB_HTML, "css": _PB_CSS,
         "py": 'from pyscript import when, document\n\n'
               '@when("click", "#boton")\n'
               'def cambiar(evento):\n'
               '    document.body.style.background = "seagreen"\n'},
    ]},
    {"titulo": "El mismo botón, con colores y animado", "pasos": [
        {"titulo": "Un color distinto en cada clic",
         "frase": "Una lista de colores y random.choice, que elige uno al azar cada vez.",
         "html": _PB_HTML, "css": _PB_CSS,
         "py": 'import random\nfrom pyscript import when, document\n\n' + _PB_COLORES + '\n'
               '@when("click", "#boton")\n'
               'def cambiar(evento):\n'
               '    color = random.choice(colores)\n'
               '    document.body.style.background = color\n'},
        {"titulo": "Que el color se deslice",
         "frase": "Una línea de CSS: transition hace que el fondo cambie despacio. Python no cambia.",
         "html": _PB_HTML, "css": _PB_CSS_SUAVE,
         "py": 'import random\nfrom pyscript import when, document\n\n' + _PB_COLORES + '\n'
               '@when("click", "#boton")\n'
               'def cambiar(evento):\n'
               '    color = random.choice(colores)\n'
               '    document.body.style.background = color\n'},
        {"titulo": "Que el botón salte",
         "frase": "CSS dibuja el salto; Python quita y pone la clase salta en cada clic.",
         "html": _PB_HTML, "css": _PB_CSS_SALTO,
         "py": 'import random\nfrom pyscript import when, document\n\n' + _PB_COLORES + '\n'
               '@when("click", "#boton")\n'
               'def cambiar(evento):\n'
               '    color = random.choice(colores)\n'
               '    document.body.style.background = color\n' + _PB_SALTO},
    ]},
    {"titulo": "La máquina de colores", "pasos": [
        {"titulo": "Contar los clics",
         "frase": "La variable clics suma uno en cada toque; global deja que la función la cambie.",
         "html": _PB_HTML_CUENTA, "css": _PB_CSS_SALTO + "\np{font-size:1.3rem}",
         "py": 'import random\nfrom pyscript import when, document\n\n' + _PB_COLORES + 'clics = 0\n\n'
               '@when("click", "#boton")\n'
               'def cambiar(evento):\n'
               '    global clics\n'
               '    clics += 1\n'
               '    color = random.choice(colores)\n'
               '    document.body.style.background = color\n'
               '    document.querySelector("#cuenta").innerText = f"{clics} clics · {color}"\n' + _PB_SALTO},
        {"titulo": "Una función para muchos botones",
         "frase": "poner(color) hace todo el cambio. Cada botón solo la llama con su color.",
         "html": _PB_HTML_VARIOS,
         "css": _PB_CSS_SALTO + "\np{font-size:1.3rem}\n#colores{display:flex;gap:.6rem}",
         "py": 'import random\nfrom pyscript import when, document\n\n' + _PB_COLORES + 'clics = 0\n\n'
               + _PB_PONER},
        {"titulo": "Modo fiesta",
         "frase": "Un for repite diez veces; await asyncio.sleep espera entre color y color.",
         "html": _PB_HTML_FIESTA,
         "css": _PB_CSS_SALTO + "\np{font-size:1.3rem}\n#colores{display:flex;gap:.6rem}",
         "py": 'import asyncio\nimport random\nfrom pyscript import when, document\n\n' + _PB_COLORES
               + 'clics = 0\n\n' + _PB_PONER +
               '\n@when("click", "#fiesta")\n'
               'async def fiesta(evento):\n'
               '    for i in range(10):\n'
               '        poner(random.choice(colores))\n'
               '        await asyncio.sleep(0.3)\n'},
    ]},
]

# El botón 4 es un proyecto nuevo: el interruptor de tema. El diseño viene
# hecho (variables de color, la píldora, la bolita que se desliza) porque la
# meta es que se vea bien; lo que escriben ellos es el HTML y el Python.
_PB_TEMA_CSS = (":root{--fondo:#0f172a;--texto:#e2e8f0;--tarjeta:#1e293b;--acento:#38bdf8}\n"
                "body.claro{--fondo:#f8fafc;--texto:#0f172a;--tarjeta:#e2e8f0;--acento:#f59e0b}\n"
                "body{font-family:system-ui,sans-serif;display:grid;place-items:center;align-content:center;"
                "gap:1.2rem;min-height:90vh;margin:0;background:var(--fondo);color:var(--texto);"
                "transition:background .5s,color .5s}\n"
                ".interruptor{width:96px;height:52px;padding:6px;border:0;border-radius:999px;"
                "background:var(--tarjeta);box-shadow:inset 0 2px 6px rgba(0,0,0,.35),0 0 0 2px var(--acento);"
                "cursor:pointer}\n"
                ".bola{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;"
                "background:var(--acento);font-size:1.3rem;transition:transform .4s}\n"
                "body.claro .bola{transform:translateX(44px)}")
_PB_TEMA_HTML = ('<h1 id="rotulo">Tema oscuro</h1>\n'
                 '<button id="tema" class="interruptor" aria-label="Cambiar tema">\n'
                 '  <span class="bola" id="bola">🌙</span>\n'
                 '</button>')
_PB_TEMA_PY = ('from pyscript import when, document\n\n'
               '@when("click", "#tema")\n'
               'def cambiar_tema(evento):\n'
               '    document.body.classList.toggle("claro")\n')
MAKERS_BOTON["progresion"].append(
    {"titulo": "El interruptor de tema", "base": {"html": "", "css": _PB_TEMA_CSS, "py": ""}, "pasos": [
        {"titulo": "El interruptor",
         "frase": "El diseño ya viene en CSS. Tú escribes el botón con su bolita y la luna.",
         "html": _PB_TEMA_HTML, "css": _PB_TEMA_CSS, "py": ""},
        {"titulo": "Cambiar de tema",
         "frase": "toggle pone la clase claro si no está y la quita si está. El CSS hace el resto.",
         "html": _PB_TEMA_HTML, "css": _PB_TEMA_CSS, "py": _PB_TEMA_PY},
        {"titulo": "El ícono que sigue al tema",
         "frase": "Un if pregunta si la página está en claro y pone el sol o la luna.",
         "html": _PB_TEMA_HTML, "css": _PB_TEMA_CSS,
         "py": _PB_TEMA_PY +
               '    if document.body.classList.contains("claro"):\n'
               '        document.querySelector("#bola").innerText = "☀️"\n'
               '        document.querySelector("#rotulo").innerText = "Tema claro"\n'
               '    else:\n'
               '        document.querySelector("#bola").innerText = "🌙"\n'
               '        document.querySelector("#rotulo").innerText = "Tema oscuro"\n'},
    ]})
# El botón 1 arranca con el estilo puesto: el primer paso es escribir HTML.
MAKERS_BOTON["progresion"][0]["base"] = {"html": "", "css": _PB_CSS, "py": ""}


def _bonito(css):
    """El CSS de la progresión se escribe compacto aquí y se enseña como lo
    escribiría una persona: una declaración por línea. En el editor, las
    líneas de 120 caracteres se cortaban y no se entendía qué era cada cosa."""
    out, ind, buf = [], 0, ""
    for ch in css:
        if ch == "{":
            out.append("  " * ind + buf.strip() + " {")
            ind, buf = ind + 1, ""
        elif ch in ";}":
            if buf.strip():
                k, _, v = buf.strip().partition(":")
                out.append("  " * ind + f"{k.strip()}: {v.strip()};")
            buf = ""
            if ch == "}":
                ind -= 1
                out.append("  " * ind + "}")
        elif ch == "\n":
            buf += " "
        else:
            buf += ch
    return "\n".join(out)


for _b in MAKERS_BOTON["progresion"]:
    for _p in _b["pasos"] + ([_b["base"]] if "base" in _b else []):
        _p["css"] = _bonito(_p["css"])



def _M(fondo="#ffffff", h1="Mi botón", botones=("Tócame",), p=None, nota=None, tinta="#111111",
       salto=False):
    """Un cuadro de la meta: cómo se ve la página en un momento. build_taller
    lo dibuja como una ventanita; un botón que empieza por «interruptor:» es el
    del tema, con su bolita a la izquierda (oscuro) o a la derecha (claro)."""
    return {"fondo": fondo, "h1": h1, "botones": list(botones), "p": p, "nota": nota,
            "tinta": tinta, "salto": salto}


_OSC, _CLA = "#0f172a", "#f8fafc"
_PB_VARIOS = ("Tócame", "Rojo", "Verde", "Azul")
# (piezas, flecha entre cuadros, cuadros) de cada paso, en orden.
_PB_METAS = [
    [(['<button>', 'id="boton"'], "escribes HTML",
      [_M(h1="", botones=(), nota="página en blanco"), _M(nota="aparece el botón")]),
     (['@when("click", "#boton")', 'def cambiar(evento):', 'document.body.style.background'], "clic",
      [_M(), _M("seagreen", nota="el fondo cambia")])],
    [(['import random', 'colores = [...]', 'random.choice(colores)'], "clic",
      [_M(), _M("tomato"), _M("gold", nota="un color al azar")]),
     (['transition: background .6s'], "clic",
      [_M("tomato"), _M("#f1a33c", nota="se desliza…"), _M("gold", nota="…despacio")]),
     (['@keyframes salto', '.salta{animation: salto .4s}', 'classList.add("salta")'], "clic",
      [_M("gold"), _M("orchid", salto=True, nota="el botón salta")])],
    [(['clics = 0', 'global clics', 'f"{clics} clics"'], "clic × 3",
      [_M(p="0 clics"), _M("gold", p="3 clics · gold", nota="cuenta y dice el color")]),
     (['def poner(color):', 'poner("tomato")'], "clic en Rojo",
      [_M(botones=_PB_VARIOS, p="0 clics"), _M("tomato", botones=_PB_VARIOS, p="1 clics · tomato",
                                              nota="cada botón, su color")]),
     (['import asyncio', 'async def fiesta(evento):', 'await asyncio.sleep(0.3)'], "clic en 🎉",
      [_M("tomato", botones=_PB_VARIOS + ("🎉 Fiesta",), p="1 clics"),
       _M("royalblue", botones=_PB_VARIOS + ("🎉 Fiesta",), p="6 clics", nota="cambia solo…"),
       _M("orchid", botones=_PB_VARIOS + ("🎉 Fiesta",), p="11 clics", nota="…diez veces")])],
    [(['class="interruptor"', '<span class="bola">🌙</span>'], "escribes HTML",
      [_M(_OSC, h1="", botones=(), tinta="#e2e8f0", nota="solo el diseño"),
       _M(_OSC, h1="Tema oscuro", botones=("interruptor:oscuro",), tinta="#e2e8f0", nota="el interruptor")]),
     (['@when("click", "#tema")', 'classList.toggle("claro")'], "clic",
      [_M(_OSC, h1="Tema oscuro", botones=("interruptor:oscuro",), tinta="#e2e8f0"),
       _M(_CLA, h1="Tema oscuro", botones=("interruptor:claro",), nota="la página pasa a claro")]),
     (['classList.contains("claro")', 'if … else', 'innerText = "☀️"'], "clic",
      [_M(_OSC, h1="Tema oscuro", botones=("interruptor:oscuro:🌙",), tinta="#e2e8f0"),
       _M(_CLA, h1="Tema claro", botones=("interruptor:claro:☀️",), nota="sol y rótulo nuevos")])],
]
for _b, _metas in zip(MAKERS_BOTON["progresion"], _PB_METAS):
    assert len(_b["pasos"]) == len(_metas), _b["titulo"]
    for _p, (_piezas, _flecha, _cuadros) in zip(_b["pasos"], _metas):
        _p["piezas"], _p["meta"] = _piezas, {"flecha": _flecha, "cuadros": _cuadros}


MAKERS_BOTON_AGENDA = [
    ("0 – 10", "Bienvenida",
     "Proyecta la guía con el botón ya hecho y tócalo delante de todos. «Hoy lo construyen ustedes "
     "desde cero, y después lo convierten en algo que sirva.»"),
    ("10 – 20", "Cómo reacciona una página",
     "Algo pasa, se ejecuta una orden, algo cambia. Conéctalo con el robot de la semana 1."),
    ("20 – 60", "Construcción por niveles",
     "Primaria arma su botón con tarjetas, sin teclear. Secundaria lo escribe en cuatro pasos: HTML, "
     "CSS, @when y la lista de colores con el contador."),
    ("60 – 95", "El proyecto real",
     "Cada pareja elige uno: semáforo del aula, tablero de preguntas, juego de reflejos o letrero de "
     "puerta. Primaria hace el suyo con tarjetas y hasta tres botones."),
    ("95 – 112", "Muestra y jueces",
     "Cada pareja prueba el proyecto de otra y lo apunta en la hoja: nunca falla, útil, creativa y "
     "mejor explicada."),
    ("112 – 120", "Cierre",
     "«¿Qué pasa primero, el clic o la función?». Guardan su código y apagan las computadoras."),
]

MAKER_SPACE["resumen"] = ("Proyectos de dos horas que se construyen con las propias manos: la escalera "
                          "de aviones de papel, cuatro sesiones de electricidad y circuitos en "
                          "Tinkercad, y el botón que cambia de color, programado por ellos.")
MAKER_SPACE["talleres"].append(
    {"n": 3, "titulo": "El botón que cambia de color", "horas": "2 h", "sesiones": [6],
     "producto": "Un proyecto real programado por la pareja y probado por otra"})
MAKER_SPACE["sesiones"].append({
    **_s(6, 3, "El botón que cambia de color",
         "Programar desde una página en blanco un botón que reacciona, y convertirlo en algo que "
         "alguien de la escuela pueda usar.",
         [t for _, t, _ in MAKERS_BOTON_AGENDA],
         "Que tu proyecto funcione veinte veces seguidas en manos de otra pareja, y que sepas leer "
         "en voz alta la línea que hace el cambio.",
         "Una computadora por pareja con la guía abierta en /makers/boton, el proyector y la hoja "
         "de jurado impresa. Nada que instalar ni comprar.",
         "Su proyecto funcionando en la guía, la fila de la hoja de jurado y la línea del cambio "
         "leída en voz alta.",
         "Primaria y secundaria trabajan en zonas distintas del aula: cada una con su guía abierta. "
         "|| Las computadoras se cierran con las dos manos y no se mueven con la tapa abierta."),
    "aviones": False,              # esta sesión no lleva la escalera de aviones
    # El deck es solo código: portada, la idea en tres palabras, la progresión
    # de tres botones, tu turno y cierre. La agenda y la guía completa siguen
    # en /makers/boton para el docente y las computadoras.
    "frase": "Programar se aprende programando.",
    "dinamica": [("Mira", "El profe enseña la meta y toca el botón."),
                 ("Escribe", "El piloto teclea, el copiloto lee la meta y las piezas."),
                 ("Prueba", "Ejecutar. ¿Hace lo de la meta? Mano arriba."),
                 ("Compara", "El profe abre su código: comparan y corrigen.")],
    "idea": ["clic", "función", "cambio"],
    "progresion": MAKERS_BOTON["progresion"],
    "pregunta": "¿Qué pasa primero, el clic o la función?",
})


# ─── Taller 5 · Pensar jugando (área de cómputo) ─────────────────────────
#
# El programa se muda al área de cómputo: los mismos noventa minutos, pero
# con juegos de programación y lógica en vez de cartón. El ritmo es el de
# siempre —nada de una hora y media de pantalla seguida—: diez minutos sin
# computadora para plantar la idea, el modelo en el proyector, dos vueltas de
# juego en parejas con cambio de piloto, el reto del día y el cierre.
#
# Las trece sesiones de taller no se tocan: están ahí para cuando se vuelva.

_JUEGOS = {
    "codemonkey": ("CodeMonkey", "https://www.codemonkey.com/es/",
                   "Con la cuenta de la clase. 2.º y 3.º"),
    "codemonkey_jr": ("CodeMonkey Jr.", "https://www.codemonkey.com/es/",
                      "Dentro de CodeMonkey, el curso con dibujos: 1.º, que todavía no lee"),
    "laberinto": ("Blockly · Laberinto", "https://blockly.games/maze?lang=es",
                  "Sin cuenta, se abre y se juega"),
    "codeorg": ("Code.org · cursos por edad", "https://studio.code.org/courses?lang=es-MX",
                "Curso A para 1.º, B o C para 2.º y 3.º"),
    "disney": ("El juego de Disney",
               "https://e304920c.content.disney.io/index.html?level=2&language=esla&character=1"
               "&gameProgress=A&tutorialVideoProgress=A&audioOn=1&logoOn=0",
               "Sin cuenta. Guárdalo en los favoritos de cada máquina"),
}


def _agenda_computo(desenchufado, modelo, reto):
    """El guion de las sesiones de cómputo. Cambian el juego y el reto; el
    reparto del tiempo no, porque es lo que sostiene a un grupo de seis a
    nueve años delante de una pantalla."""
    return [
        ("0 – 10", "Sin computadora", desenchufado),
        ("10 – 20", "El profe lo enseña", modelo),
        ("20 – 45", "Primera vuelta en parejas", "Uno maneja el ratón (piloto) y el otro lee y "
                                                 "dice qué hacer (copiloto)."),
        ("45 – 50", "Cambio de piloto", "Se cambian los papeles sin discutir: lo marca el reloj."),
        ("50 – 65", "Segunda vuelta", "Cada pareja sigue donde estaba, ahora con el otro al ratón."),
        ("65 – 80", "El reto del día", reto),
        ("80 – 90", "Cierre", "Pantallas apagadas. Cada pareja dice «hoy aprendí a…» y sella su "
                              "pasaporte."),
    ]


_MATERIALES_COMPUTO = ("El área de cómputo: una computadora por pareja, el proyector encendido y "
                       "audífonos si los hay. En papel, solo el pasaporte de sellos.")
_SEGURIDAD_COMPUTO = ("Las sillas pegadas a la mesa y nada de comida ni bebida junto a los "
                      "teclados. || Se entra solo a las páginas de la clase: nada de buscar otros "
                      "juegos. || Los audífonos, a volumen bajo: si no se oye al profe, está muy "
                      "alto.")

MAKER_PRIMARIA["publico"] = "Primaria 1.º a 3.º · lunes y miércoles"
MAKER_PRIMARIA["talleres"].append(
    {"n": 5, "titulo": "Pensar jugando · área de cómputo", "horas": "6 h",
     "sesiones": [14, 15, 16, 17],
     "producto": "El pasaporte sellado y los cuatro retos pasados"})
MAKER_PRIMARIA["nota"] += (
    "\n\nDe la sesión 14 en adelante el programa se da en el área de cómputo, con juegos de "
    "programación y lógica, lunes y miércoles. Son dos semanas de puente: de la 18 en adelante el "
    "plan se ajusta a lo que diga la capacitación."
)

MAKER_PRIMARIA["sesiones"] += [
    {**_s(14, 5, "Órdenes exactas",
          "Descubrir que la computadora hace exactamente lo que se le dice, ni más ni menos, y que "
          "el orden de las órdenes cambia el resultado.",
          ["Sin computadora: el robot de la clase, que solo obedece órdenes de una palabra.",
           "En el proyector, un nivel modelo resuelto en voz alta, equivocándose a propósito.",
           "Primera vuelta en parejas, cada grado en su ruta.",
           "Cambio de piloto y segunda vuelta.",
           "El reto del día y el cierre con el pasaporte."],
          "Pasar el nivel del día sin ayuda y saber decir, señalando, qué orden iba primero.",
          _MATERIALES_COMPUTO,
          "El pasaporte con el primer sello y el nivel pasado, enseñado en la pantalla.",
          _SEGURIDAD_COMPUTO),
     "agenda": _agenda_computo(
         "El robot de la clase: un niño es el robot y los demás le dan órdenes de una palabra "
         "—adelante, gira, para— para llevarlo hasta la puerta. Si la orden es confusa, el robot se "
         "queda quieto.",
         "Un nivel del juego resuelto en el proyector, en voz alta y equivocándose a propósito: "
         "«puse girar antes de avanzar y mira dónde terminé».",
         "El nivel marcado en la pizarra. Quien lo pasa se vuelve embajador y ayuda a otra pareja, "
         "sin tocarle el ratón."),
     "enlaces": [_JUEGOS["codemonkey_jr"], _JUEGOS["codemonkey"], _JUEGOS["laberinto"]]},

    {**_s(15, 5, "Repetir sin cansarse",
          "Ver que cuando algo se repite hay una forma más corta de escribirlo, y que esa forma "
          "corta se llama repetir.",
          ["Sin computadora: la coreografía de cuatro pasos, repetida hasta cansarse.",
           "En el proyector: el mismo nivel con doce órdenes y con tres.",
           "Primera vuelta en parejas, con los niveles de repetir.",
           "Cambio de piloto y segunda vuelta.",
           "El reto: pasar el nivel con el menor número de bloques."],
          "Pasar el nivel del día usando repetir, y decir cuántos bloques te ahorraste.",
          _MATERIALES_COMPUTO,
          "El pasaporte con el segundo sello y el número de bloques escrito en el mural.",
          _SEGURIDAD_COMPUTO),
     "agenda": _agenda_computo(
         "La coreografía: palmada, palmada, pie, vuelta. Se repite cuatro veces cantando el número. "
         "«¿Les dije veinte cosas o les dije cuatro, cuatro veces?»",
         "El mismo nivel dos veces en el proyector: primero con doce órdenes, después con un "
         "repetir y tres. Se cuentan los bloques en voz alta.",
         "El nivel del día, pero con premio al que use menos bloques. Se apuntan los números en el "
         "mural y se comparan al final."),
     "enlaces": [_JUEGOS["laberinto"], _JUEGOS["codemonkey"], _JUEGOS["codemonkey_jr"]]},

    {**_s(16, 5, "Si pasa esto, haz aquello",
          "Entender que un programa puede decidir: mira cómo está el mundo y hace una cosa u otra.",
          ["Sin computadora: las tarjetas de «si… entonces…» con cosas de su día.",
           "En el proyector, un nivel donde el camino cambia según lo que haya delante.",
           "Primera vuelta con el juego de Disney.",
           "Cambio de piloto y segunda vuelta.",
           "El reto del día y el cierre."],
          "Pasar un nivel en el que el camino cambia, y contar en una frase qué decidió el programa.",
          _MATERIALES_COMPUTO,
          "El pasaporte con el tercer sello y la frase «si… entonces…» dicha en voz alta.",
          _SEGURIDAD_COMPUTO),
     "agenda": _agenda_computo(
         "Tarjetas de si… entonces…: «si llueve, paraguas», «si suena el timbre, fila». Cada niño "
         "inventa una y la dice; los demás contestan qué pasa si NO se cumple.",
         "Un nivel donde el camino cambia según lo que haya delante, resuelto en el proyector: "
         "«aquí el programa mira antes de moverse».",
         "El nivel marcado del juego de Disney. Quien lo pasa se lo cuenta a otra pareja antes de "
         "seguir al siguiente."),
     "enlaces": [_JUEGOS["disney"], _JUEGOS["codemonkey"], _JUEGOS["laberinto"]]},

    {**_s(17, 5, "Buscar el error",
          "Perderle el miedo al error: un programa que falla no está roto, está diciendo dónde "
          "mirar.",
          ["Sin computadora: el programa con un paso cambiado, que la clase arregla entre todos.",
           "En el proyector: un nivel que falla, y la búsqueda del paso culpable.",
           "Primera vuelta: niveles rotos a propósito que hay que arreglar.",
           "Cambio de piloto y segunda vuelta.",
           "Muestra final: cada pareja enseña su mejor nivel en la pantalla."],
          "Arreglar un programa que falla y decir qué paso estaba mal.",
          _MATERIALES_COMPUTO,
          "El pasaporte completo con los cuatro sellos y el nivel enseñado a la clase.",
          _SEGURIDAD_COMPUTO),
     "agenda": _agenda_computo(
         "El sándwich mal explicado: el profe sigue al pie de la letra las órdenes de la clase para "
         "hacer un sándwich y sale mal. Entre todos se busca el paso que faltaba.",
         "Un nivel que falla en el proyector. En vez de borrar todo, se prueba paso a paso hasta "
         "encontrar el culpable.",
         "Muestra: cada pareja enseña en su pantalla el nivel que más le costó y cuenta qué "
         "arregló. Dos minutos cada una."),
     "enlaces": [_JUEGOS["codemonkey"], _JUEGOS["laberinto"], _JUEGOS["disney"]]},
]


# ═══════════════════════════════════════════════════════════════════════
#  Technovation · Chicas que crean
#
#  Un club aparte: equipos de chicas que eligen un problema de su comunidad y
#  lo convierten en una app. El currículum oficial de Technovation (división
#  Senior) se abre por unidades —las dos primeras, el 8 y el 15— así que estas
#  dos sesiones son el arranque con lo que ya se tiene en el aula: CodeMonkey
#  y el juego de Disney. Cuando las unidades estén abiertas, sus actividades
#  entran en el hueco que cada sesión deja marcado.
# ═══════════════════════════════════════════════════════════════════════

MAKER_CHICAS = {
    "via": "chicas",
    "horas_sesion": 1.5,
    "nombre": "Technovation · Chicas que crean",
    "publico": "Chicas de secundaria 1.º a 3.º · una vez por semana",
    "resumen": "Dos semanas jugando a pensar como programadora, con sitios que se abren y se "
               "juegan: ni cuentas, ni instalar nada.",
    "nota": (
        "El currículum de Technovation se abre por unidades —la 1 el 8 y la 2 el 15— y estas dos "
        "sesiones no dependen de él: son una ruta de juegos de lógica. Cuando se abran las "
        "unidades, su contenido entra encima de esta base.\n\n"
        "Lo que se quitó de la presentación y puedes usar cuando quieras: el mural de «lo que me "
        "molesta» (tres problemas por cabeza, agrupados en la pizarra), la ficha del problema (a "
        "quién le pasa, cada cuánto, cómo lo resuelven hoy), el mini-pitch de treinta segundos y "
        "la app dibujada en tres pantallas de papel.\n\n"
        "Ninguno de los sitios pide registro; CodeMonkey va con la cuenta de la clase. "
        "Comprobado el 2 de octubre de 2026: blockly.games está bloqueado por el filtro de DNS "
        "(resuelve a la página de bloqueo), así que no está en la ruta. Prueba las direcciones en "
        "una máquina del laboratorio antes de la sesión: el filtro de allá puede ser otro."
    ),
    "talleres": [
        {"n": 1, "titulo": "La ruta de juegos", "horas": "3 h", "sesiones": [1, 2],
         "producto": "El pasaporte con las metas de los dos días"},
    ],
    "sesiones": [
        {**_s(1, 1, "Que la máquina te obedezca",
              "Descubrir, jugando, que un programa es una lista de órdenes en orden, y que "
              "repetir se escribe una sola vez.",
              ["Calentamiento: el laberinto clásico, los diez primeros niveles.",
               "Una aventura entera de Minecraft, que ya pide bucles.",
               "CodeMonkey con la cuenta de la clase.",
               "Para las que llegan antes: la fiesta de baile.",
               "Cierre: qué repitieron con un bucle en vez de escribirlo cinco veces."],
              "Pasar los veinte niveles del laberinto y terminar una aventura de Minecraft.",
              "Una computadora por chica, audífonos si los hay, el proyector y el pasaporte "
              "impreso. Nada que instalar ni registrar.",
              "El pasaporte con las metas del día marcadas y una frase dicha en voz alta.",
              None),
         "escueta": True,          # de la portada al guion: ni propósito ni material proyectados
         "agenda": [
             ("0 – 10", "El laberinto", "Todas a la vez, los diez primeros niveles. Es el "
                                        "calentamiento: dar órdenes en orden."),
             ("10 – 40", "Minecraft", "Una aventura entera. En cuanto se repiten pasos, aparece "
                                      "el bucle: ahí es donde hay que pararlas y preguntar."),
             ("40 – 70", "CodeMonkey", "Con la cuenta de la clase, donde cada una se quedó. Aquí "
                                       "ya se escribe código, no solo bloques."),
             ("70 – 85", "Si llegaste antes", "Fiesta de baile: eventos. «Cuando suene esto, haz "
                                              "aquello» es exactamente lo mismo que hará su app."),
             ("85 – 90", "Cierre", "Pantallas apagadas. Cada una dice qué repitió con un bucle en "
                                   "vez de escribirlo cinco veces."),
         ],
         "enlaces": [
             ("Laberinto clásico", "https://studio.code.org/hoc/1",
              "Code.org, en español. Se abre y se juega"),
             ("Minecraft · Hora del Código", "https://code.org/minecraft",
              "Elige una aventura y entra sin cuenta"),
             ("CodeMonkey", "https://www.codemonkey.com/es/", "Con la cuenta de la clase"),
             ("Fiesta de Baile", "https://hourofcode.com/dance", "El extra, si llegas antes"),
         ],
         "metas": [
             ("Laberinto clásico", "Pasar los 20 niveles."),
             ("Minecraft", "Terminar una aventura completa."),
             ("CodeMonkey", "Avanzar cinco niveles desde donde estabas."),
             ("Fiesta de Baile", "Que tu baile reaccione a la música, no que solo se mueva."),
         ]},

        {**_s(2, 1, "Que la máquina decida sola",
              "Pasar de dar órdenes a decidir: que el programa mire cómo está el mundo y elija. Y "
              "aprender a leer código antes de escribirlo.",
              ["Calentamiento con el juego de Disney: repetir y decidir.",
               "Compute It: leer un programa y predecir qué hace antes de probar.",
               "CodeMonkey, donde se quedó cada una.",
               "Para las que llegan antes: Silent Teacher o Flexbox Froggy.",
               "Cierre: una regla que descubrieron sin que nadie se la dijera."],
              "Predecir bien lo que hace un programa antes de ejecutarlo, tres veces seguidas.",
              "Una computadora por chica, audífonos si los hay, el proyector y el pasaporte. "
              "Nada que instalar ni registrar.",
              "El pasaporte completo y la regla descubierta, escrita en el mural.",
              None),
         "escueta": True,
         "agenda": [
             ("0 – 10", "El juego de Disney", "El de siempre, como calentamiento: aquí el camino "
                                              "cambia según lo que haya delante."),
             ("10 – 40", "Compute It", "Se lee el código y se dice en voz alta qué va a pasar "
                                       "ANTES de darle. Equivocarse aquí es el ejercicio."),
             ("40 – 70", "CodeMonkey", "Donde se quedó cada una. Ahora tocan las condiciones."),
             ("70 – 85", "Si llegaste antes", "Silent Teacher: nadie explica nada y hay que "
                                              "deducir las reglas. O Flexbox Froggy, que es el "
                                              "premio."),
             ("85 – 90", "Cierre", "Cada una cuenta una regla que descubrió sola. Aviso: con las "
                                   "unidades de Technovation abiertas, la próxima sesión cambia."),
         ],
         "enlaces": [
             ("El juego de Disney",
              "https://e304920c.content.disney.io/index.html?level=2&language=esla&character=1"
              "&gameProgress=A&tutorialVideoProgress=A&audioOn=1&logoOn=0",
              "El que ya usan. Sin cuenta"),
             ("Compute It", "https://compute-it.toxicode.fr/", "Casi sin texto: se lee código"),
             ("CodeMonkey", "https://www.codemonkey.com/es/", "Con la cuenta de la clase"),
             ("Silent Teacher", "https://silentteacher.toxicode.fr/",
              "Para las que van rápido: deduce las reglas de Python"),
             ("Flexbox Froggy", "https://flexboxfroggy.com/#es", "El premio, en español"),
         ],
         "metas": [
             ("El juego de Disney", "Pasar el nivel donde el camino cambia solo."),
             ("Compute It", "Acertar tres predicciones seguidas antes de ejecutar."),
             ("CodeMonkey", "Pasar un nivel que use una condición."),
             ("Silent Teacher o Froggy", "Llegar al nivel 10 de cualquiera de los dos."),
         ]},
    ],
}


# Makers Space va primero: es la puerta de entrada al programa, no un anexo.
# El cocurricular no se publica en esta copia: el material sigue escrito
# aquí abajo, pero no sale ni en la web, ni en el Word, ni en las rutas de
# la app. Para volver a publicarlo, basta con devolver los cuatro a la lista.
MAKER_PROGRAMAS = []  # [MAKER_SPACE, MAKER_SECUNDARIA, MAKER_PRIMARIA, MAKER_CHICAS]


# ═══════════════════════════════════════════════════════════════════════
#  DIAGNÓSTICO DE ENTRADA
#
#  No mide lo que saben de programación —para eso estaba el Kahoot— sino con
#  qué llegan: qué aparato tienen, para qué lo usan de verdad, si en casa
#  alguien mira, y si distinguen lo que se ve de lo que es.
#
#  Las opciones están escritas para que ninguna dé vergüenza marcar. «Ninguno
#  propio, uso el de la casa» va en la lista y no escondido en «otro»: en un
#  aula de treinta hay varios, y si la única respuesta honesta es la que
#  incomoda, la encuesta miente.
#
#  La pregunta del video falso no interroga sobre el riesgo, pone un caso.
#  Preguntar «¿sabes protegerte?» solo mide lo que creen de sí mismos.
#
#  ─── Las seis que se añadieron después ───
#  Las diez primeras dicen con qué llegan. Estas seis dicen qué se puede
#  hacer en clase, que no es lo mismo y se descubre tarde:
#
#  · `internet` y `trae_aparato` deciden si una práctica se puede mandar a
#    casa o tiene que caber entera en la hora. Sin esto, la mitad de una
#    tarea se convierte en «no pude».
#  · `teclado` e `ingles` son el peaje de JavaScript. Se escribe mucho y
#    todo está en inglés; quien no lo trae de antes no se atasca en la
#    lógica, se atasca en encontrar la tecla y en leer `unexpected token`.
#  · `ya_programo` es la que más cambia la planificación: si media aula vio
#    Scratch en primaria, la semana 1 de 1ro sobra tal como está escrita.
#  · `quiere_crear` va al final y es abierta a propósito. No se tabula: se
#    lee. De ahí salen los ejemplos con los que se da el resto del año, que
#    valen más cuando son suyos y no míos.
#
#  Quince y no veinte: en 1ro, pasadas cinco o seis pantallas más, se
#  empieza a marcar cualquier cosa por salir, y entonces los datos ya no
#  dicen nada.
# ═══════════════════════════════════════════════════════════════════════

# El vídeo de la diapositiva de evaluación. Va aquí y no incrustado en el
# generador porque es contenido: cambiar de vídeo tiene que ser cambiar un id,
# no editar HTML.
#
# «Lo que la mayoría de las escuelas NO enseñan», de code.org, doblado al
# español. 5:44. Salen Bill Gates, Zuckerberg, will.i.am y Chris Bosh contando
# cómo empezaron a programar de adolescentes.
#
# Se eligió por quién lo hizo, que es la única garantía real que hay sobre un
# vídeo ajeno: una fundación educativa que produce ese material para
# proyectarlo en aulas. El anterior era de un canal pequeño de gaming y hubo
# que quitarlo por el lenguaje.
#
# El riesgo que queda es otro: la copia en español es una resubida de un
# particular y algún día puede desaparecer. Si pasa, el original en inglés del
# canal oficial es `nKIu9yen5nc`, la misma película y la misma duración.
VIDEO_EVAL = ("mpFMrPRiQm4", "Lo que la mayoría de las escuelas no enseñan")

DIAGNOSTICO_INTRO = (
    "Quince preguntas, cuatro minutos. No es un examen y no lleva nota: sirve para saber de "
    "dónde parte el grupo y no explicar lo que ya saben ni dar por sabido lo que no."
)

DIAGNOSTICO_CIERRE = (
    "Ya está. Con esto sé de dónde partimos y puedo armar las próximas semanas para este "
    "grupo y no para un grupo imaginario. Gracias."
)

# (id, pregunta, tipo, opciones)   tipo: una | varias | texto
DIAGNOSTICO = [
    ("aparatos", "¿Qué aparatos tienes en casa que puedas usar?", "varias",
     ["Celular propio", "Celular de alguien de la casa", "Tablet",
      "Computadora portátil", "Computadora de mesa", "Consola de videojuegos",
      "Ninguno todavía"]),

    ("mas_usa", "¿Cuál usas más?", "una",
     ["El celular", "La tablet", "La computadora", "La consola",
      "Ninguno, casi no uso"]),

    ("para_que", "¿Para qué lo usas más?", "una",
     ["Jugar", "Ver videos o redes", "Hablar con gente",
      "Tareas y cosas de la escuela", "Buscar y aprender cosas"]),

    ("internet", "En tu casa, ¿cómo te conectas a internet?", "una",
     ["Wifi de la casa", "Con los datos del celular", "En casa de un familiar o vecino",
      "Solo en la escuela", "Casi nunca me conecto"]),

    ("sabe_hacer", "¿Cuáles de estas cosas ya sabes hacer solo?", "varias",
     ["Escribir un documento", "Hacer una presentación",
      "Usar una hoja de cálculo", "Buscar algo en internet",
      "Mandar un correo con un archivo adjunto",
      "Guardar un archivo y volver a encontrarlo", "Ninguna todavía"]),

    ("teclado", "Escribiendo en un teclado, ¿cómo te va?", "una",
     ["Escribo rápido sin mirar las teclas", "Escribo bien, pero mirando",
      "Busco las teclas una por una", "Casi no he usado un teclado"]),

    ("ingles", "Palabras como start, file, save, error, ¿las entiendes?", "una",
     ["Casi todas", "Algunas", "Casi ninguna", "Las reconozco de los juegos"]),

    # Cada opción dice para qué es. Con los nombres sueltos, quien tocó HTML
    # sin saber que se llamaba HTML marcaba «ninguna», y el dato salía mal
    # justo en la pregunta que más decide cómo se da la semana 1.
    ("ya_programo", "¿Cuáles de estas has hecho alguna vez?", "varias",
     ["Scratch — programar arrastrando bloques de colores",
      "Roblox Studio — hacer tus propios juegos, no solo jugarlos",
      "Minecraft con redstone o comandos",
      "HTML — el esqueleto de una página web",
      "CSS — los colores y el diseño de la página",
      "JavaScript — lo que hace que la página reaccione",
      "Python — escribir programas con texto, como los de verdad",
      "La Hora del Código o code.org",
      "Robótica — programar un robot o un carrito",
      "Ninguna todavía"]),

    ("apps", "¿Cuáles de estas aplicaciones usas?", "varias",
     ["WhatsApp", "TikTok", "Instagram", "YouTube", "Roblox", "Minecraft",
      "Canva", "Word o Documentos de Google", "Zoom o Meet", "Ninguna"]),

    ("juegos", "¿Cuáles son tus videojuegos favoritos?", "texto", []),

    ("ia", "¿Usas inteligencia artificial, tipo ChatGPT?", "una",
     ["No sé qué es", "Sé qué es, pero no la uso", "La he probado alguna vez",
      "La uso a veces", "La uso casi todos los días",
      "La uso para las tareas"]),

    ("cuentas", "Aparte de la cuenta de la escuela, ¿tienes cuenta propia en algo?", "varias",
     ["Un correo mío", "Redes sociales", "Juegos en línea",
      "Una tienda o app de compras", "No, ninguna"]),

    ("supervision", "En tu casa, ¿alguien revisa lo que haces en el celular o la computadora?", "una",
     ["Sí, seguido", "A veces", "Casi nunca", "No, nunca",
      "No tengo aparato propio"]),

    ("real", "Un video donde una persona famosa dice algo que nunca dijo, ¿puede existir?", "una",
     ["Sí, hoy se puede fabricar", "No, si hay video es porque pasó",
      "No lo sé"]),

    # Abierta y la última: se responde con la guardia baja, ya de salida.
    ("quiere_crear", "Si pudieras hacer algo tuyo este año, ¿qué te gustaría crear?",
     "texto", []),
]


# ═══════════════════════════════════════════════════════════════════════
#  ACTIVIDADES DE CADA CLASE
#
#  Lo que el estudiante hace dentro de la presentación de cada semana:
#  votación en grupo, ejemplo con notas, cuatro retos con respuesta al
#  instante, un mini juego, el código de partida en el editor de la clase, un reto por
#  equipos con reloj y el ticket de salida. El contrato está en
#  actividades.py y build_curso.py lo valida antes de escribir nada.
#
#  Una semana sin entrada aquí conserva la presentación anterior.
# ═══════════════════════════════════════════════════════════════════════

# Sitios para seguir practicando en casa: gratis y sin instalar nada.
RECURSOS_PYTHON = [
    ("Python Tutor", "https://pythontutor.com/python-compiler.html",
     "Pega tu código y míralo ejecutarse paso a paso: ves cómo cambia cada variable."),
    ("futurecoder", "https://es.futurecoder.io/course/",
     "Curso de Python desde cero con ejercicios que se corrigen solos. Gratis y sin cuenta."),
    ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
     "Python completo en el navegador, sin instalar nada, para probar tus propias ideas."),
]
RECURSOS_3RO = [
    ("Python Tutor", "https://pythontutor.com/python-compiler.html",
     "Visualiza tu código línea por línea: ideal para trazar variables, bucles y listas."),
    ("futurecoder", "https://es.futurecoder.io/course/",
     "Curso de Python con retos que se corrigen solos y ayudas cuando te trabas. Gratis."),
    ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
     "Cuadernos de Python en el navegador para experimentar con datos, sin cuenta."),
]


# ── 1ro · semanas 2 a 12 ────────────────────────────────────────────────────


# ── 2do · semanas 1 a 4 ─────────────────────────────────────────────────────


# ── 2do · semanas 5 a 8 ─────────────────────────────────────────────────────


# ── 2do · semanas 9 a 12 ────────────────────────────────────────────────────
_PIEZA_TM = '''<h2>Mi IA</h2>
<button id="encender">Encender cámara</button>
<button id="que-ves">¿Qué ves?</button>
<div id="camara"></div>
<p id="respuesta"></p>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.3.1/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@0.8/dist/teachablemachine-image.min.js"></script>
<script>
  // La pieza de Teachable Machine: se pega sin tocar. Solo cambia el enlace.
  const URL_MODELO = "PEGA_AQUI_TU_ENLACE/";
  window.clase = ""; window.confianza = 0;
  let modelo, camara;
  async function encender() {
    modelo = await tmImage.load(URL_MODELO + "model.json", URL_MODELO + "metadata.json");
    camara = new tmImage.Webcam(220, 220, true);
    await camara.setup(); await camara.play();
    document.getElementById("camara").appendChild(camara.canvas);
    requestAnimationFrame(mirar);
  }
  async function mirar() {
    camara.update();
    const p = await modelo.predict(camara.canvas);
    let mejor = p[0];
    for (const x of p) if (x.probability > mejor.probability) mejor = x;
    window.clase = mejor.className; window.confianza = mejor.probability;
    requestAnimationFrame(mirar);
  }
  document.getElementById("encender").addEventListener("click", encender);
</script>'''


# ── 3ro · semanas 1 a 4 ─────────────────────────────────────────────────────


# ── 3ro · semanas 5 a 8 ─────────────────────────────────────────────────────


# ── 3ro · semanas 9 a 12 ────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════════
#  TEORÍA DE CADA SEMANA
#
#  Tres diapositivas cortas antes del ejemplo y los retos: la idea con un
#  ejemplo de la vida real, sus partes, y una pregunta para comprobar que se
#  entendió. Se valida con actividades.validar_teoria.
# ═══════════════════════════════════════════════════════════════════════


# ── La ruta del curso: las mismas 12 semanas para 1ro, 2do y 3ro ───────────
# 2do y 3ro corren la misma clase; lo que sube de nivel vive en EXTRAS.

CURSO_SEMANAS = [
    S(1, "Presentación del curso + «Programa a un humano»",
  "Conocer la dinámica de la clase y comprender qué es un algoritmo y por qué las instrucciones deben ser exactas y ordenadas.",
  "Preséntate en 3 minutos con la presentación visual: quién eres, qué construyes y qué van a construir ellos este año, juegos escritos en Python que corren en la página. Cierra con la pregunta: «¿una computadora entiende lo que uno quiere, o solo lo que uno le dice?».",
  "Sigue el guion de la dinámica de la semana 1: ronda de nombres, las tres reglas del laboratorio y cómo se evalúa. Define algoritmo como objetivo + pasos ordenados + ejecución, y haz la demo: un voluntario te dicta 4 pasos para llegar a la puerta y los ejecutas al pie de la letra, incluido el que falla.",
  "Elige un voluntario como «robot». En parejas, uno programa y otro ejecuta una ruta por el aula hasta la meta de cinta usando solo las tarjetas AVANZA, GIRA IZQUIERDA, GIRA DERECHA, REPITE 2 VECES y SI HAY OBSTÁCULO.",
  "Llegar a la meta con un máximo de 10 tarjetas. Cada pareja marca con una X la tarjeta que falló en el primer intento y corrige su algoritmo.",
  "Dos parejas ejecutan su algoritmo frente a la clase. Pregunta de cierre: «¿qué instrucción falló y por qué la computadora no la adivinó?». Anuncia que en la semana 2 esas mismas órdenes se escriben en Python.",
  "Elige un juego del banco de la semana 1 según el grupo: «Adivina mi número» si está apagado, «Bug en la ruta» si terminó la ruta antes de tiempo.",
  "Tarjetas de comandos impresas, cinta adhesiva, objetos del aula. Presentación del docente, proyector.",
  "Algoritmo escrito en tarjetas, ejecutado y corregido tras detectar al menos un error."),
    S(2, "Variables: guardar mi nombre y mis números",
  "Guardar un texto y un número en variables, distinguir los dos tipos y hacer una suma sencilla.",
  "Tres cajas de zapatos rotuladas NOMBRE, EDAD y VIDAS, y papelitos con valores. Mete «Luna» en NOMBRE y 12 en EDAD, y pregunta: «¿en qué se diferencia lo que metí en cada caja?».",
  "Modela nombre = \"Luna\": el signo = guarda el valor en la caja. Después edad = 12, sin comillas, y marca la diferencia entre texto y número. Muestra cada caja con display(nombre) y display(edad). Cierra con una suma: puntos = 2 + 3 y display(puntos), para que vean que Python hace la cuenta y guarda el resultado.",
  "Cada estudiante crea la ficha de su jugador con tres variables (nombre, edad y color favorito), las muestra con display() y agrega una suma de dos números.",
  "Cambiar el valor de una variable a mitad del programa y mostrarla dos veces, para ver que la caja se queda con lo último que se guardó.",
  "«¿Cuál de tus variables guarda texto y cuál guarda un número?». Dos estudiantes leen su ficha en voz alta y la clase dice el tipo de cada una.",
  "Guardar dos números en variables y mostrar su suma, su resta y su multiplicación.",
  PLANTILLA + ", tres cajas rotuladas y papelitos, proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: tres variables propias mostradas con display() y una suma que se ve en la página."),
    S(3, "Ciclos: repetir con for",
  "Repetir líneas con for y range sin copiarlas, y acumular un total dentro del ciclo.",
  "Reto relámpago: «muestren ¡Hola! cinco veces». Cuando alguien copie la línea cinco veces, pregunta: «¿y si fueran mil?».",
  "Modela for i in range(5): con sus dos puntos y su sangría: lo corrido a la derecha es lo que se repite. Después el acumulador: total = 0 antes del ciclo y total = total + n adentro, que también se escribe total += n. Cierra con range(10, 0, -1) para contar hacia atrás.",
  "Cada estudiante escribe tres ciclos: saludar cinco veces, sumar del 1 al 10 y la cuenta regresiva del 10 al 1 terminando en «¡Despegue!».",
  "La tabla del 5 con un solo ciclo: 5, 10, 15 hasta 50, cada número en su línea.",
  "«¿Qué pasa si total = 0 se escribe dentro del ciclo?». Se prueba en vivo y se ve que nunca acumula.",
  "Mostrar solo los números pares del 2 al 20 usando el tercer número de range, el del salto.",
  PLANTILLA + ", proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: los tres ciclos funcionando: el saludo, la suma y la cuenta regresiva."),
    S(4, "Decisiones: if / elif / else",
  "Tomar decisiones comparando valores con if, elif y else, y distinguir = de ==.",
  "Juega «Adivina mi número» con la clase: piensas un número del 1 al 20 y solo respondes «más alto» o «más bajo». Pregunta: «¿qué regla sigo cada vez que contesto?».",
  "Modela secreto = 13 e intento = 8, y después if intento == secreto:, elif intento < secreto: y else:, con los dos puntos y la sangría. Insiste en que = guarda y == compara. Quita los dos puntos a propósito y lee el error con la clase.",
  "Cada estudiante escribe su «adivina el número»: cambia el valor de intento, vuelve a ejecutar y comprueba que salen los tres mensajes.",
  "Agregar una rama más: si el intento se pasa por más de cinco, que diga «te pasaste por mucho».",
  "El editor proyectado: la clase dicta valores de intento y predice qué mensaje saldrá antes de ejecutar.",
  "Contar en una variable cuántos intentos hicieron falta y mostrarlo al acertar.",
  PLANTILLA + ", proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: if / elif / else y tres pruebas anotadas: acierto, más alto y más bajo."),
    S(5, "Listas: muchos datos en una sola caja",
  "Guardar varios datos en una lista, agregarles elementos, contarlos y recorrerlos con un ciclo.",
  "«¿Cómo guardarían diez preguntas sin crear diez variables?». Deja que propongan antes de responder.",
  "Modela frutas = [\"mango\", \"piña\"] con corchetes y comas, frutas.append(\"coco\"), len(frutas) y frutas[0], que es la primera y no la segunda. Después recórrela con el for de la semana 3.",
  "Cada estudiante hace su lista de cinco cosas de un tema suyo, le agrega una con append, muestra cuántas hay y las recorre con un ciclo.",
  "Mostrar solo los elementos que cumplen algo, con un if dentro del ciclo.",
  "Intercambio: cada uno lee la lista del compañero. «¿Qué pasa si pides una posición que no existe?» — se prueba en vivo y se lee el error.",
  "Una segunda lista del mismo largo y mostrar las dos juntas, posición por posición.",
  PLANTILLA + ", proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: una lista propia de cinco o más elementos, un append, el conteo y el recorrido."),
    S(6, "Funciones: mis propias órdenes",
  "Guardar pasos con un nombre y volver a usarlos, con parámetros para cambiar lo que hacen.",
  "Escribe en la pizarra las mismas cuatro líneas repetidas tres veces con pequeños cambios. «¿Y si pudieran darle un nombre a ese bloque y llamarlo cuando quieran?».",
  "Modela def saludar(nombre): con sus dos puntos y su sangría, y llámala dos veces con nombres distintos. Después def escena(texto, opcion): con dos parámetros, para ver que la misma función sirve para muchas escenas. Señala que si nadie la llama, no pasa nada.",
  "Cada estudiante escribe tres funciones (una escena, un saludo y una despedida) y las llama en orden para contar una historia corta.",
  "Una función con dos parámetros usada al menos tres veces con valores distintos.",
  "«¿Cuántas líneas te ahorró la función?». Se cuentan en voz alta las líneas repetidas que desaparecieron.",
  "Una función que reciba un número y muestre su tabla de multiplicar, usando el ciclo de la semana 3.",
  PLANTILLA + ", hoja para el mapa de la historia, proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: tres funciones propias, llamadas al menos cinco veces en total."),
    S(7, "Botones que hacen algo: el clicker",
  "Hacer que el programa responda a un clic y lea lo que el jugador escribe en una caja de texto.",
  "Proyecta un clicker: un botón «¡Toca!» que suma un punto por clic. Reta a un voluntario a llegar a 30 en diez segundos. «Hoy hacen el suyo.»",
  "En la plantilla, señala el botón con id boton y el párrafo con id salida. Modela @when(\"click\", \"#boton\") sobre def jugar(evento):, con global puntos como primera línea para que la función pueda cambiar el marcador. Dentro: puntos += 1 y document.querySelector(\"#salida\").innerText = f\"Puntos: {puntos}\". Explica += : puntos += 1 es lo mismo que puntos = puntos + 1. Y la f del f-string, que mete la variable dentro del texto. Explica la sangría: lo que pertenece a la función va corrido a la derecha.",
  "Construir un clicker con tema propio (galletas, goles, monedas): un botón que suma, el marcador en la página y un segundo botón que reinicia a 0.",
  "Agregar una caja de texto donde el jugador escribe cuánto vale cada clic, leída con int(document.querySelector(\"#valor\").value). Probar qué pasa si escriben una palabra y anotar el error.",
  "«¿Qué pasa primero, el clic o la función?». Un estudiante señala en su editor la línea que conecta el botón con el código.",
  "Conectar una función de la semana 6 a un botón: al tocarlo, cuenta una escena de la historia.",
  PLANTILLA + ", proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: clicker funcional: botón que suma, botón de reinicio y marcador que se actualiza en la página."),
    S(8, "El azar: dados y moneda",
  "Usar números y elecciones al azar para que el juego no sea igual cada vez.",
  "Tira un dado real tres veces y anota los resultados en la pizarra. «¿Quién adivina el siguiente?». Nadie: eso es lo que hace divertido un juego.",
  "Modela import random al inicio, random.randint(1, 6) para el dado y random.choice([\"cara\", \"cruz\"]) para la moneda, cada uno en su botón. Pulsa el botón diez veces frente a la clase: los resultados cambian y el código no.",
  "Construir la mesa de juego: botón «Tirar dado» que muestra el número, botón «Lanzar moneda» que muestra cara o cruz, y un marcador de puntos que suma lo que sale en el dado.",
  "Dos dados a la vez: mostrar los dos números y la suma, por ejemplo «4 + 5 = 9».",
  "Pregunta: «con dos dados, ¿qué sale más, el 2 o el 7?». Cada uno responde con lo que vio en su editor y lo comprueban ahí mismo con un ciclo de 1000 tiradas, como el de la semana 3.",
  "Un botón «Premio sorpresa» que elige con random.choice entre cinco premios inventados por el estudiante.",
  PLANTILLA + ", un dado y una moneda reales, proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: dado, moneda y marcador que suma lo que sale."),
    S(9, "Mi página a mi gusto: HTML y CSS",
  "Dar estructura a una página con etiquetas que dicen qué es cada parte, y darle estilo con CSS.",
  "Muestra la misma página sin CSS y con CSS: «es el mismo contenido; lo que cambia es cómo se ve».",
  "En el editor de la clase, la pestaña HTML es lo que va dentro del body: header, main, section, h1, p, img con su texto alternativo y ul con li. En la pestaña CSS, el selector y sus reglas: color, background, font-size y padding. Modela una regla y cámbiala en vivo.",
  "Cada estudiante arma su página: un título con su nombre, una sección «Sobre mí» con una frase y una imagen, una lista de tres intereses y un pie. Después le pone color de fondo, color de letra y tamaños.",
  "Crear la sección «Mi IA» con su título y un párrafo que diga «Aquí va el modelo que voy a entrenar». Se queda vacía hasta la semana 10.",
  "Revisión cruzada: el compañero señala una etiqueta que cambiaría y una regla de CSS que le gustó. «¿Qué pasa si la imagen no carga?» — se enseña en vivo para qué sirve el texto alternativo.",
  "Un botón con estilo propio: bordes redondeados, color y un cambio al pasar el mouse con :hover.",
  "Editor de la clase, plantilla base de la página, proyector.",
  "Tu código en el editor de la clase, guardado con tu nota: la página estructurada, con estilo propio y la sección «Mi IA» creada."),
    S(10, "IA sin código: entreno mi modelo con Teachable Machine",
  "Entrenar un modelo de clasificación con Teachable Machine y comprobar que una IA aprende de los ejemplos que recibe, con sus aciertos, sus errores y sus sesgos.",
  "Proyecta un modelo ya entrenado con dos clases, «pulgar arriba» y «pulgar abajo», y deja que tres estudiantes lo prueben frente a la cámara. Luego pide a alguien que enseñe la mano abierta: «¿qué dijo? ¿por qué no dijo que no sabe?».",
  "En teachablemachine.withgoogle.com, proyecto de imagen, sin cuenta; menciona que también hay de audio y de pose. Tres ideas: una clase es una respuesta posible, los ejemplos son lo único que aprende y se prueba con casos que no vio. Entrena en vivo con 10 fotos por clase y enseña la barra de confianza.",
  "En parejas eligen un tema con dos o tres clases (gestos, objetos del estuche, sonidos con el micrófono o posturas), graban al menos 30 ejemplos por clase, entrenan y prueban con casos nuevos: otra mano, otro fondo, otra luz. Al terminar exportan con Export Model → Upload my model, copian el enlace y lo pegan con una captura en la sección «Mi IA» de su sitio.",
  "Sesgo a propósito: entrenar una clase con solo 5 ejemplos, todos con el mismo fondo y la misma persona, probarla con alguien distinto y anotar qué falla. Después añadir ejemplos variados y comparar la confianza.",
  "Dos parejas enseñan un caso en el que su modelo se equivocó. Pregunta: «¿el modelo es tonto, o aprendió exactamente lo que le enseñamos?».",
  "Añadir una clase «nada» con fotos del fondo vacío y comprobar si el modelo deja de inventar respuestas cuando no hay nadie delante.",
  "Teachable Machine, cámara web o micrófono, objetos del aula, modelo de demostración ya entrenado, editor de la clase, proyector.",
  "Enlace del modelo y captura en la sección «Mi IA» del sitio + dos líneas escritas: un caso en que falló y qué ejemplos lo corrigieron."),
    S(11, "Mi IA dentro de mi sitio",
  "Conectar el modelo de Teachable Machine al sitio y escribir en Python la lógica que decide qué hacer con lo que el modelo ve.",
  "Proyecta el sitio de demostración: enciendes la cámara, haces un gesto, pulsas «¿Qué ves?» y el sitio responde con un mensaje distinto para cada clase. «Hoy su modelo de la semana 10 entra en su sitio.»",
  "Dilo tal cual: «el modelo trae su pieza en JavaScript, que se pega sin tocar; nuestro código es el Python que decide qué hacer». Se pega la pieza de Teachable Machine de la plantilla con el enlace del modelo de la semana 10. Esa pieza deja dos datos: window.clase y window.confianza. Modela el botón «¿Qué ves?» con @when y un if / elif / else que lee window.clase.",
  "Cada uno pega la pieza con el enlace de su modelo, comprueba que la cámara enciende (si no arranca dentro de la clase, abrir el editor en pantalla completa) y escribe la función del botón «¿Qué ves?»: un mensaje para cada clase de su modelo, escrito en la página con .innerText.",
  "Usar window.confianza: si no llega a 0.8, responder «No estoy seguro» en lugar de adivinar.",
  "Dos estudiantes prueban el sitio de otro con un caso que el modelo no conoce. Pregunta: «¿quién decidió qué responder, la IA o tu Python?».",
  "Llevar la cuenta de cuántas veces ha visto cada clase y mostrar el marcador, o que la respuesta cambie además el titular del sitio.",
  PLANTILLA + " con la pieza de Teachable Machine, modelo de la semana 10, cámara web, proyector.",
  "Sitio con el modelo propio funcionando y un if / elif / else en Python que responde distinto a cada clase + captura de un caso con poca confianza."),
    S(12, "Proyecto: mi juego",
  "Mejorar uno de los juegos del curso hasta hacerlo propio, probarlo con un compañero, corregirlo y presentarlo.",
  "Cada estudiante elige cuál de sus juegos va a mejorar (dado, adivina el número, piedra papel o tijera, quiz o aventura) y escribe en una frase qué le va a agregar.",
  "Repaso de los requisitos mínimos en la pizarra: un botón, una variable que cambia, una decisión, y algo al azar o una lista. Presenta la hoja de prueba: acción → resultado esperado → resultado real.",
  "Programar las mejoras. A mitad del bloque intercambian computadoras: el compañero juega, llena tres filas de la hoja de prueba y anota qué falla.",
  "Corregir al menos un error encontrado por el compañero y dejar un comentario con # que diga qué se arregló.",
  "Presentaciones de 1 minuto: qué juego es, qué le agregó, un error encontrado y cómo lo resolvió.",
  "Se amplía el tiempo de presentaciones para cubrir a todo el grupo y se vota el juego más divertido y el mejor probado.",
  PLANTILLA + ", hoja de pruebas impresa, rúbrica de proyecto, proyector.",
  "Tu juego mejorado en el editor de la clase, guardado con tu nota, hoja con tres pruebas hechas por un compañero, un error corregido y presentación oral."),
]

CURSO_ACT = {
    1: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primer algoritmo",
            "dinamica": {
                "titulo": "El robot humano",
                "minutos": 3,
                "pasos": [
                    "Un voluntario hace de robot: solo obedece lo que le dicen, tal cual, sin adivinar.",
                    "La clase le dicta los pasos para sentarse en una silla.",
                    "Cuando el robot hace algo raro, se arregla ese paso: ahí se ve qué es «exacto».",
                ],
            },
            "taller2": {
                "tipo": "ordenar",
                "misiones": [
                    {"pista": "Piensa qué no se puede hacer antes: ¿te secas con las manos aún sucias?",
                     "pide": "Toca los pasos en orden: lavarte las manos.",
                     "pasos": ["Secarte", "Abrir la llave", "Enjabonarte", "Enjuagarte"],
                     "orden": [1, 2, 3, 0]},
                    {"pista": "Antes de escribir hay que poder ver la pantalla.",
                     "pide": "Ahora: mandar un mensaje por el teléfono.",
                     "pasos": ["Escribir el mensaje", "Desbloquear el teléfono", "Enviar", "Abrir la app"],
                     "orden": [1, 3, 0, 2]},
                    {"pista": "Lo primero es tener con qué: el pan.",
                     "pide": "Hacer un sándwich de queso.",
                     "pasos": ["Poner el queso", "Sacar dos panes", "Cerrar el sándwich", "Untar la mantequilla"],
                     "orden": [1, 3, 0, 2]},
                    {"pista": "Mira hacia dónde apunta el robot: primero lo que puede hacer sin girar.",
                     "pide": "El robot mira al frente. La bandera está 2 al frente y 3 a su derecha.",
                     "pasos": ["Gira a la derecha", "Levanta la bandera", "Avanza 2", "Avanza 3"],
                     "orden": [2, 0, 3, 1]},
                ],
            },
        },
        "hoy": "Vas a programar a un robot humano con tarjetas, sin tocar la computadora.",
        "escena": "robot",
        "calentamiento": {
            "pregunta": "Le dices a un robot «tráeme agua». ¿Qué hace?",
            "opciones": ["Te trae un vaso de agua", "Nada: nadie le dio los pasos",
                         "Te pregunta dónde está el agua", "Adivina lo que quieres"],
            "correcta": 1,
            "por_que": "Un robot no adivina: solo cumple pasos exactos. «Tráeme agua» son muchos pasos que nadie le dio.",
        },
        "ejemplo": {
            "titulo": "Un algoritmo para llegar a la puerta",
            "lenguaje": "tarjetas",
            "codigo": ["AVANZA 3 pasos", "GIRA A LA DERECHA", "AVANZA 2 pasos", "ABRE LA PUERTA"],
            "notas": [(1, "Cada tarjeta es una sola orden, y exacta: cuántos pasos, no «un poco»."),
                      (2, "Girar no mueve al robot: solo cambia hacia dónde mira."),
                      (4, "El objetivo va al final. Si falta, el robot llega y se queda parado.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "tarjetas",
             "codigo": ["El robot empieza mirando a la pizarra", "GIRA A LA DERECHA", "GIRA A LA DERECHA"],
             "opciones": ["Mira a la pizarra", "Mira hacia atrás", "Mira a la derecha", "Mira a la izquierda"],
             "correcta": 1,
             "explica": "Dos giros a la derecha son media vuelta: queda de espaldas a la pizarra."},
            {"tipo": "completa", "lenguaje": "tarjetas",
             "codigo": ["Hay que doblar la esquina a la izquierda", "AVANZA 4 pasos", "___", "AVANZA 2 pasos"],
             "opciones": ["GIRA A LA IZQUIERDA", "GIRA A LA DERECHA", "AVANZA 1 paso"],
             "correcta": 0,
             "explica": "Para doblar primero hay que girar. Avanzar sin girar lo estrella contra la pared."},
            {"tipo": "ordena", "lenguaje": "tarjetas",
             "enunciado": "Ordena el algoritmo para lavarte las manos.",
             "lineas": ["Abre la llave", "Mójate las manos", "Ponte jabón", "Frota 20 segundos",
                        "Enjuágate", "Cierra la llave"]},
            {"tipo": "error", "lenguaje": "tarjetas",
             "lineas": ["AVANZA 3 pasos", "GIRA A LA DERECHA", "AVANZA UN POQUITO", "ABRE LA PUERTA"],
             "mala": 2, "arreglo": "AVANZA 2 pasos",
             "explica": "«Un poquito» no es exacto: el robot no sabe cuánto es. Una computadora tampoco."},
        ],
        "juego": {
            "tipo": "robot", "titulo": "Lleva al robot hasta la bandera",
            "pista": "10 TARJETAS O MENOS",
            "tam": 5, "inicio": [0, 4, "N"], "meta": [4, 0],
            "muros": [[2, 0], [2, 1], [1, 3], [3, 3], [3, 2]],
            "max": 10, "cartas": ["AVANZA", "GIRA_IZQ", "GIRA_DER", "REPITE_2"],
        },
        "practica": {
            "tipo": "desenchufada", "titulo": "Programa a un humano",
            "pasos": ["En parejas: uno es el robot y el otro programa.",
                      "Marquen con cinta la salida y la meta. Pongan una mochila de obstáculo.",
                      "Escriban la ruta en tarjetas: máximo 10.",
                      "El robot obedece al pie de la letra. Si choca, marquen con X la tarjeta que falló.",
                      "Cambien esa tarjeta y vuelvan a intentar. Después cambian de rol."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Por qué la computadora no adivina lo que quieres?",
                   "respuesta": "Porque solo sigue las instrucciones exactas que le das, en orden. "
                                "Si un paso es ambiguo, se equivoca o se para."},
        "chuleta": {
            "titulo": "Un buen algoritmo",
            "lineas": [
                ("Objetivo", "Primero se dice a dónde se quiere llegar."),
                ("Paso exacto", "«Avanza 3 pasos», no «ve por ahí»."),
                ("En orden", "Enjabonarse antes de enjuagarse. Al revés no sirve."),
                ("Uno por línea", "Un paso por renglón: así se encuentra el error."),
                ("Probar", "Hacerlo tal cual lo escribiste y ver dónde falla."),
                ("Arreglar", "Se cambia el paso que falló, no todo el algoritmo."),
            ],
        },
        "recursos": [
            ("Hora del Código · Laberinto", "https://studio.code.org/hoc/1",
             "Veinte niveles de pasos en orden, con bloques. Sin cuenta y en español."),
            ("Lightbot", "https://lightbot.com/hour-of-code.html",
             "Un robot que enciende luces: el mismo juego de dar pasos exactos."),
            ("Blockly · Laberinto", "https://blockly.games/maze?lang=es",
             "Los algoritmos en bloques, de lo fácil a lo difícil."),
        ],
        "juego2": {
            "tipo": "clasifica", "titulo": "¿Paso exacto o paso vago?", "pista": "TOCA Y CLASIFICA",
            "cubetas": ["Exacto (sirve)", "Vago (no sirve)"],
            "items": [["Avanza 3 pasos", 0], ["Ve por ahí", 1], ["Gira a la derecha", 0],
                      ["Haz algo bonito", 1], ["Abre la puerta", 0], ["Camina un poquito", 1],
                      ["Espera 5 segundos", 0], ["Más o menos por allá", 1],
                      ["Enciende la luz del cuarto", 0], ["Arregla eso", 1]],
        },
    },
    2: {
        "definir_primero": True,
        "primera": {
            "dinamica": {"titulo": "Dicta y escribe", "minutos": 3, "pasos": [
                "El docente dicta una caja: «una caja llamada vidas con un 3».",
                "Todos la escriben en el cuaderno como en Python: vidas = 3.",
                "Se escribe la buena en la pizarra y cada quien revisa la suya: el nombre, el =, las comillas.",
            ]},
            "montana": {"misiones": [
                {"pide": "Crea una caja llamada nombre que guarde el texto Luna.", "var": "nombre", "tipo": "str", "valor": "Luna"},
                {"pide": "Crea una caja llamada vidas con el número 3.", "var": "vidas", "tipo": "int", "valor": "3"},
                {"pide": "Crea puntos y guarda en ella la suma 2 + 3 (escribe la suma).", "var": "puntos", "tipo": "int", "valor": "5", "exige": "+"},
                {"pide": "Crea mis_puntos con el número 10. Ojo: un nombre no lleva espacios.", "var": "mis_puntos", "tipo": "int", "valor": "10"},
                {"pide": "Te pegó un enemigo: cambia vidas a 2.", "var": "vidas", "tipo": "int", "valor": "2"},
            ]},
        },
        "hoy": "Vas a guardar tu nombre y tus números en variables y a hacer tu primera suma.",
        "escena": "cajas",
        "calentamiento": {
            "pregunta": "¿Cuál de estas líneas guarda un texto?",
            "opciones": ['nombre = "Luna"', "nombre = Luna", "nombre = 12", "nombre"],
            "correcta": 0,
            "por_que": "El texto siempre va entre comillas. Sin comillas, Python cree que es otra caja.",
        },
        "ejemplo": {
            "titulo": "La ficha de mi jugador",
            "lenguaje": "python",
            "codigo": ["from pyscript import display", "",
                       'nombre = "Luna"     # texto', "edad = 12           # número",
                       "vidas = 3           # número", "",
                       "display(nombre)", "display(edad)", "",
                       "puntos = 2 + 3      # una suma", "display(puntos)"],
            "notas": [(3, "El texto va entre comillas: es de tipo texto."),
                      (4, "Los números van sin comillas."),
                      (10, "Python hace la cuenta y guarda el resultado: 5.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ['nombre = "Luna"', "display(nombre)"],
             "opciones": ["Luna", "nombre", '"Luna"', "Error"],
             "correcta": 0, "explica": "display muestra lo que hay dentro de la caja, sin las comillas."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["edad ___ 12", "display(edad)"],
             "opciones": ["=", "==", "+"],
             "correcta": 0, "explica": "El signo = guarda el 12 dentro de la caja edad."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena para que muestre 7.",
             "lineas": ["manzanas = 4", "peras = 3", "total = manzanas + peras", "display(total)"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["nombre = Luna", "edad = 12", "display(nombre)"],
             "mala": 0, "arreglo": 'nombre = "Luna"',
             "explica": "Sin comillas, Python busca una caja llamada Luna y no la encuentra."},
        ],
        "juego": {
            "tipo": "clasifica", "titulo": "¿Texto o número?", "pista": "TOCA Y CLASIFICA",
            "cubetas": ["Texto (entre comillas)", "Número (sin comillas)"],
            "items": [['"Luna"', 0], ["12", 1], ['"12"', 0], ["3", 1], ['"rojo"', 0], ["0", 1],
                      ['"3 vidas"', 0], ["100", 1], ['"0"', 0], ["7", 1]],
        },
        "juego2": {
            "tipo": "torre", "titulo": "La torre de variables", "pista": "SOLO SUBEN LAS BIEN ESCRITAS",
            "meta": 5,
            "lineas": [
                {"txt": 'nombre = "Luna"', "ok": True},
                {"txt": "edad = 12", "ok": True},
                {"txt": "vidas = 3", "ok": True},
                {"txt": 'color = "azul"', "ok": True},
                {"txt": "puntos = 0", "ok": True},
                {"txt": 'equipo = "Tigres"', "ok": True},
                {"txt": "nombre = Luna", "ok": False, "porque": "Al texto le faltan las comillas."},
                {"txt": "12 = edad", "ok": False, "porque": "El nombre de la caja va a la izquierda del =."},
                {"txt": "mis puntos = 0", "ok": False, "porque": "Un nombre no lleva espacios: mis_puntos."},
                {"txt": "2puntos = 5", "ok": False, "porque": "Un nombre no puede empezar con un número."},
            ],
        },
        "practica": {
            "tipo": "editor", "titulo": "La ficha de mi jugador",
            "html": "<h1>Mi ficha</h1>",
            "css": "body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:24px;font-size:1.4rem}",
            "py": ('from pyscript import display\n\n'
                   'nombre = "Tu nombre"\n'
                   'edad = 12\n'
                   'vidas = 3\n\n'
                   'display(nombre)\n'
                   'display(edad)\n\n'
                   '# Tu turno: guarda tu color favorito en una variable y muéstralo\n'
                   '# Tu turno: guarda dos números y muestra su suma\n'),
            "pasos": ["Pulsa Ejecutar y mira tu ficha en la página.",
                      "Cambia nombre y edad por los tuyos. El texto va entre comillas; el número, no.",
                      "Crea una variable color con tu color favorito y muéstrala.",
                      "Crea dos números, súmalos en una variable total y muéstrala.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Por qué Luna va entre comillas y 12 no?",
                   "respuesta": "Luna es texto y el texto va entre comillas. 12 es un número y va sin comillas."},
        "recursos": RECURSOS_PYTHON,
        "chuleta": {"titulo": "Variables en Python", "lineas": [
            ('nombre = "Luna"', "Guarda un texto: va entre comillas."),
            ("edad = 12", "Guarda un número: sin comillas."),
            ("display(nombre)", "Muestra lo que hay dentro de la caja."),
            ("puntos = 2 + 3", "Python hace la cuenta y guarda el 5."),
            ("edad = 13", "Volver a guardar cambia el valor de la caja."),
        ]},
    },
    3: {
        "hoy": "Vas a repetir con for: saludar cinco veces, sumar del 1 al 10 y una cuenta regresiva.",
        "escena": "repetido",
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primer ciclo",
            "dinamica": {
                "titulo": "Repite conmigo",
                "minutos": 3,
                "pasos": [
                    "El docente pide en voz alta: «un ciclo que repita 3 veces».",
                    "Todos escriben la cabecera en el cuaderno: for i in range(3):",
                    "Se escribe la buena en la pizarra y cada quien revisa la suya: los dos puntos y la sangría.",
                ],
            },
            "escalera": {
                "misiones": [
                    {"pide": "Escribe un ciclo que repita 5 veces.", "secuencia": [0, 1, 2, 3, 4]},
                    {"pide": "Ahora uno que cuente del 1 al 10.", "secuencia": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
                    {"pide": "Uno que cuente hacia atrás, del 5 al 1.", "secuencia": [5, 4, 3, 2, 1]},
                    {"pide": "Uno que vaya de 2 en 2: 2, 4, 6, 8, 10.", "secuencia": [2, 4, 6, 8, 10]},
                    {"pide": "El último: de 5 en 5 hasta el 25.", "secuencia": [5, 10, 15, 20, 25]},
                ],
            },
        },
        "calentamiento": {
            "pregunta": "¿Cuántas veces se repite for i in range(10)?",
            "opciones": ["9", "10", "11", "1"],
            "correcta": 1,
            "por_que": "range(10) da 0, 1, 2… hasta 9: son diez vueltas.",
        },
        "ejemplo": {
            "titulo": "Tres ciclos", "lenguaje": "python",
            "codigo": ["from pyscript import display", "",
                       "for i in range(5):", '    display("¡Hola!")', "",
                       "total = 0", "for n in range(1, 11):",
                       "    total = total + n   # o total += n", 'display("Suma del 1 al 10:", total)', "",
                       "for n in range(10, 0, -1):", "    display(n)", 'display("¡Despegue!")'],
            "notas": [(3, "range(5) repite cinco veces lo que está debajo con sangría."),
                      (8, "El acumulador: total guarda lo que llevaba y le suma n."),
                      (11, "El tercer número es el salto: -1 cuenta hacia atrás.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["for i in range(3):", "    display(i)"],
             "opciones": ["1 · 2 · 3", "0 · 1 · 2", "0 · 1 · 2 · 3", "3"],
             "correcta": 1, "explica": "range(3) empieza en 0 y no llega al 3."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["total = 0", "for i in range(5):", "    total ___ 2", "display(total)"],
             "opciones": ["+=", "=", "-="],
             "correcta": 0, "explica": "+= acumula: en cinco vueltas suma 2 cada vez y queda 10."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena la cuenta regresiva.",
             "lineas": ["for n in range(3, 0, -1):", "    display(n)", 'display("¡Despegue!")']},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["total = 0", "for i in range(10):", "total += 1", "display(total)"],
             "mala": 2, "arreglo": "    total += 1",
             "explica": "Sin sangría, total += 1 no está dentro del for: Python da un IndentationError."},
        ],
        "juego": {
            "tipo": "bucle", "titulo": "La máquina de sumar", "pista": "PRIMERO APUESTA, DESPUÉS MIRA",
            "modo": "for", "var": "dado",
            "iterable": {"lista": [4, 2, 6, 1, 5, 3, 6, 2, 4, 5]},
            "acumula": {"var": "total", "op": "+=", "inicio": 0, "usa": "var"},
            "apuesta": {"pregunta": "Diez tiradas: 4, 2, 6, 1, 5, 3, 6, 2, 4 y 5. ¿Con cuánto termina total?",
                        "opciones": ["28", "38", "48"], "correcta": 1},
            "cuerpo": ["    total += dado"],
        },
        "practica": {
            "tipo": "editor", "titulo": "Mis tres ciclos",
            "html": "<h1>Mis ciclos</h1>",
            "css": "body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:24px;font-size:1.3rem}",
            "py": ("from pyscript import display\n\n"
                   "for i in range(5):\n"
                   '    display("¡Hola!")\n\n'
                   "total = 0\n"
                   "for n in range(1, 11):\n"
                   "    total = total + n\n"
                   'display("Suma del 1 al 10:", total)\n\n'
                   "# Tu turno: la cuenta regresiva del 10 al 1 y «¡Despegue!»\n"
                   "# Tu turno: la tabla del 5 (5, 10, 15 ... 50)\n"),
            "pasos": ["Pulsa Ejecutar y mira los cinco saludos y la suma.",
                      "Cambia el 5 por otro número y vuelve a ejecutar.",
                      "Escribe la cuenta regresiva del 10 al 1 con range(10, 0, -1).",
                      "Escribe la tabla del 5 con un solo ciclo.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Por qué total = 0 va antes del for y no adentro?",
                   "respuesta": "Porque si va adentro vuelve a 0 en cada vuelta y nunca acumula."},
        "chuleta": {
            "titulo": "Ciclos en Python",
            "lineas": [
                ("for i in range(5):", "Repite cinco veces lo que va debajo con sangría."),
                ("    display(i)", "La sangría manda: solo esto se repite."),
                ("range(1, 11)", "Del 1 al 10. El hasta nunca entra."),
                ("range(10, 0, -1)", "Cuenta hacia atrás: el salto puede ser negativo."),
                ("total = 0", "El acumulador se pone en cero ANTES del ciclo."),
                ("    total += n", "Dentro, suma lo de esta vuelta a lo que llevaba."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Pega tu ciclo y míralo vuelta por vuelta: ves cómo cambia el acumulador."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Curso de Python desde cero con ejercicios que se corrigen solos. Gratis y sin cuenta."),
            ("Blockly · Laberinto", "https://blockly.games/maze?lang=es",
             "Los mismos bucles, pero en bloques y con un laberinto que resolver."),
        ],
        "juego2": {
            "tipo": "vueltas", "titulo": "La fábrica de números", "pista": "MUEVE DESDE, HASTA Y SALTO",
            "rondas": [
                {"objetivo": [0, 1, 2, 3, 4], "pista": "El de siempre: range con un solo número."},
                {"objetivo": [1, 2, 3, 4, 5], "pista": "Ahora no empieza en 0. ¿Dónde se pone el desde?"},
                {"objetivo": [2, 4, 6, 8, 10], "pista": "De dos en dos: eso es el salto."},
                {"objetivo": [10, 9, 8, 7, 6], "pista": "Hacia atrás: el salto puede ser negativo."},
                {"objetivo": [20, 15, 10, 5], "pista": "Hacia atrás y de cinco en cinco. La última."},
            ],
        },
    },
    4: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera decisión",
            "dinamica": {
                "titulo": "El portero",
                "minutos": 3,
                "pasos": [
                    "El docente hace de portero y dice en voz alta una edad: 15, 18, 21.",
                    "La clase canta «pasa» o «no pasa» y dice por qué.",
                    "Todos escriben en el cuaderno la línea del portero: if edad >= 18:",
                ],
            },
            "taller2": {
                "tipo": "condicion",
                "ejemplo": "if edad >= 18:",
                "misiones": [
                    {"pista": "«O más» incluye el 18: hay un comparador que dice «mayor o igual».",
                     "pide": "Que pase solo quien tenga 18 años o más.",
                     "variable": "edad", "casos": [15, 18, 20], "espera": [False, True, True],
                     "sale": "pasan 18 y 20"},
                    {"pista": "«No es igual» tiene su propio comparador: míralo en Los comparadores.",
                     "pide": "Que pase cualquiera menos el que tenga 13.",
                     "variable": "edad", "casos": [12, 13, 14], "espera": [True, False, True],
                     "sale": "pasan 12 y 14"},
                    {"pista": "Aquí la variable ya no es edad, es nota. Y «más de» deja fuera al 70.",
                     "pide": "Ahora la variable es nota: que pase quien saque más de 70.",
                     "variable": "nota", "casos": [65, 70, 85], "espera": [False, False, True],
                     "sale": "pasa solo 85"},
                    {"pista": "Es texto: va entre comillas. Y «Ana» no es lo mismo que «ana».",
                     "pide": "Con nombre: que salude solo si es exactamente Ana.",
                     "variable": "nombre", "casos": ['"Ana"', '"ana"', '"Luis"'],
                     "espera": [True, False, False], "sale": "pasa solo Ana"},
                    {"pista": "«Menos de 5» deja fuera al 5.",
                     "pide": "La última, con vidas: que pase quien tenga menos de 5.",
                     "variable": "vidas", "casos": [2, 5, 7], "espera": [True, False, False],
                     "sale": "pasa solo 2"},
                ],
            },
        },
        "hoy": "Vas a decidir con if, elif y else: acertaste, más alto o más bajo.",
        "escena": "balanza",
        "calentamiento": {
            "pregunta": "¿Qué hace == en Python?",
            "opciones": ["Guarda un valor", "Compara si dos cosas son iguales", "Suma dos números", "Muestra un texto"],
            "correcta": 1,
            "por_que": "= guarda y == compara. if intento == secreto: pregunta si los dos son iguales.",
        },
        "ejemplo": {
            "titulo": "Adivina el número", "lenguaje": "python",
            "codigo": ["from pyscript import display", "", "secreto = 13", "intento = 8", "",
                       "if intento == secreto:", '    display("¡Acertaste!")',
                       "elif intento < secreto:", '    display("Más alto")',
                       "else:", '    display("Más bajo")'],
            "notas": [(4, "Cambia este número y vuelve a ejecutar: pasas por las tres ramas."),
                      (6, "== compara. Un solo = guardaría, no compararía."),
                      (8, "elif es «si no, prueba esto otro».")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["intento = 7", "secreto = 12", "if intento == secreto:", '    display("¡Acertaste!")',
                        "else:", '    display("No es ese")'],
             "opciones": ["¡Acertaste!", "No es ese", "¡Acertaste! · No es ese", "Error"],
             "correcta": 1, "explica": "7 no es igual a 12, así que se salta el if y entra al else."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["if intento ___ secreto:", '    display("¡Acertaste!")'],
             "opciones": ["==", "=", "!="],
             "correcta": 0,
             "explica": "== pregunta si son iguales. Un solo = guarda y aquí da error; != es justo lo contrario."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena el if / else.",
             "lineas": ["if intento == secreto:", '    display("¡Acertaste!")', "else:", '    display("No es ese")']},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["secreto = 5", "intento = 5", "if intento == secreto", '    display("¡Acertaste!")'],
             "mala": 2, "arreglo": "if intento == secreto:",
             "explica": "Al if le faltan los dos puntos: Python da un SyntaxError en esa línea."},
        ],
        "juego": {"tipo": "ppt", "titulo": "Piedra, papel o tijera", "pista": "MIRA QUÉ RAMA DECIDIÓ"},
        "practica": {
            "tipo": "editor", "titulo": "Mi adivina el número",
            "html": "<h1>Adivina el número</h1>",
            "css": "body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:24px;font-size:1.3rem}",
            "py": ("from pyscript import display\n\n"
                   "secreto = 13\n"
                   "intento = 8\n\n"
                   "if intento == secreto:\n"
                   '    display("¡Acertaste!")\n'
                   "elif intento < secreto:\n"
                   '    display("Más alto")\n'
                   "else:\n"
                   '    display("Más bajo")\n\n'
                   "# Tu turno: cambia intento hasta ver los tres mensajes\n"
                   "# Tu turno: una rama más para cuando te pasas por más de cinco\n"),
            "pasos": ["Pulsa Ejecutar y mira qué mensaje sale.",
                      "Cambia intento hasta ver los tres mensajes.",
                      "Quita los dos puntos de un if a propósito, lee el error y arréglalo.",
                      "Agrega una rama más con elif para cuando te pasas por más de cinco.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Qué diferencia hay entre = y ==?",
                   "respuesta": "= guarda un valor en una variable; == compara si dos valores son iguales."},
        "juego2": {
            "tipo": "clasifica", "titulo": "¿Se cumple o no se cumple?", "pista": "LEE EL VALOR Y DECIDE",
            "cubetas": ["Se cumple · entra al if", "No se cumple · va al else"],
            "items": [["vidas = 0 · if vidas == 0:", 0],
                      ["edad = 12 · if edad >= 18:", 1],
                      ["nota = 85 · if nota > 70:", 0],
                      ['nombre = "Ana" · if nombre == "ana":', 1],
                      ["puntos = 10 · if puntos != 10:", 1],
                      ["hora = 7 · if hora < 8:", 0],
                      ["vidas = 3 · if vidas == 0:", 1],
                      ["temp = 30 · if temp >= 30:", 0],
                      ["monedas = 5 · if monedas > 5:", 1],
                      ['clase = "gato" · if clase == "gato":', 0]],
        },
        "chuleta": {
            "titulo": "Decisiones en Python",
            "lineas": [
                ("if edad >= 18:", "Pregunta algo que solo puede ser verdadero o falso."),
                ("    display(\"Entras\")", "La sangría dice qué pasa si se cumple."),
                ("else:", "Lo que pasa cuando NO se cumple."),
                ("elif nota >= 70:", "Otra pregunta, solo si la de arriba falló."),
                ("==   !=", "Igual a… y distinto de…"),
                ("=", "Un solo igual GUARDA. No compara."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Pega tu if y mira qué rama se enciende con cada valor."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Curso de Python desde cero con ejercicios que se corrigen solos. Gratis y sin cuenta."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Python en el navegador para probar tus condiciones sin instalar nada."),
        ],
    },
    5: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera lista",
            "dinamica": {
                "titulo": "La fila del recreo",
                "minutos": 3,
                "pasos": [
                    "Cinco voluntarios se paran en fila: son la lista.",
                    "El docente dice «append» y llega uno al final; dice «posición 0» y se adelanta el primero.",
                    "Todos escriben en el cuaderno la lista de la fila con corchetes y comas.",
                ],
            },
            "taller2": {
                "tipo": "lista",
                "ejemplo": 'equipo = ["Ana", "Luis"]',
                "misiones": [
                    {"pista": "Los corchetes abren y cierran la lista; los nombres van entre comillas.",
                     "pide": "Crea la lista equipo con Ana y Luis, en ese orden.",
                     "variable": "equipo", "lista": [], "espera": ["Ana", "Luis"],
                     "sale": "['Ana', 'Luis']"},
                    {"pista": "Añadir al final tiene su palabra: .append( )",
                     "pide": "Ahora añade a Sofía al final.",
                     "variable": "equipo", "lista": ["Ana", "Luis"], "espera": ["Ana", "Luis", "Sofía"],
                     "sale": "['Ana', 'Luis', 'Sofía']", "ejemplo": 'equipo.append("…")'},
                    {"pista": "Para sacar a alguien hay que decir a cuál, entre comillas.",
                     "pide": "Saca a Luis del equipo.",
                     "variable": "equipo", "lista": ["Ana", "Luis", "Sofía"], "espera": ["Ana", "Sofía"],
                     "sale": "['Ana', 'Sofía']", "ejemplo": 'equipo.remove("…")'},
                    {"pista": "El primero es la posición 0.",
                     "pide": "Cambia al primero por Beto. Acuérdate: el primero es la posición 0.",
                     "variable": "equipo", "lista": ["Ana", "Sofía"], "espera": ["Beto", "Sofía"],
                     "sale": "['Beto', 'Sofía']", "ejemplo": 'equipo[0] = "…"'},
                    {"pista": "Una lista vacía son dos corchetes sin nada dentro.",
                     "pide": "Empieza de nuevo: deja el equipo vacío.",
                     "variable": "equipo", "lista": ["Beto", "Sofía"], "espera": [],
                     "sale": "[]", "ejemplo": "equipo = []"},
                ],
            },
        },
        "hoy": "Vas a guardar muchos datos en una lista, contarlos y recorrerlos con un ciclo.",
        "escena": "muchos",
        "calentamiento": {
            "pregunta": "preguntas = [\"a\", \"b\", \"c\"]. ¿Qué es preguntas[0]?",
            "opciones": ["\"a\"", "\"b\"", "\"c\"", "Error"],
            "correcta": 0,
            "por_que": "Las posiciones empiezan en 0: preguntas[0] es la primera.",
        },
        "ejemplo": {
            "titulo": "Mi lista de frutas", "lenguaje": "python",
            "codigo": ["from pyscript import display", "", 'frutas = ["mango", "piña"]',
                       'frutas.append("coco")', "", "display(len(frutas))", "display(frutas[0])", "",
                       "for fruta in frutas:", "    display(fruta)"],
            "notas": [(3, "Una lista: muchos datos entre corchetes, separados por comas."),
                      (4, "append agrega al final."),
                      (9, "El ciclo recorre la lista: una vuelta por elemento.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ['frutas = ["mango", "piña"]', 'frutas.append("coco")', "display(len(frutas))"],
             "opciones": ["2", "3", "coco", "4"],
             "correcta": 1, "explica": "Había 2 frutas y append agrega una más: len da 3."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ['equipos = ["Tigres", "Leones"]', 'equipos.___("Águilas")', "display(equipos)"],
             "opciones": ["append", "add", "push"],
             "correcta": 0, "explica": "En Python se agrega al final de una lista con append."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena para mostrar la pregunta que agregaste.",
             "lineas": ["preguntas = []", 'preguntas.append("¿2 + 2?")', "display(preguntas[0])"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ['colores = ["rojo", "azul", "verde"]', "display(len(colores))", "display(colores[3])"],
             "mala": 2, "arreglo": "display(colores[2])",
             "explica": "Hay 3 colores, pero las posiciones son 0, 1 y 2: colores[3] da IndexError."},
        ],
        "juego": {
            "tipo": "caza", "titulo": "Caza la posición", "pista": "SE EMPIEZA A CONTAR EN 0",
            "nombre": "preguntas",
            "inicial": ["¿2 + 2?", "¿Capital de RD?", "¿Color del cielo?", "¿Mejor equipo?"],
            "extra": ["¿Cuántos días tiene octubre?"],
            "rondas": 8, "gana": 6,
        },
        "practica": {
            "tipo": "editor", "titulo": "Mi lista",
            "html": "<h1>Mi lista</h1>",
            "css": "body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:24px;font-size:1.3rem}",
            "py": ("from pyscript import display\n\n"
                   'cosas = ["mango", "piña"]\n'
                   '# Tu turno: completa tu lista hasta cinco cosas de tu tema\n\n'
                   'cosas.append("coco")\n'
                   'display("Tengo", len(cosas), "cosas")\n\n'
                   "for cosa in cosas:\n"
                   "    display(cosa)\n\n"
                   "# Tu turno: muestra solo las que empiezan con m, con un if dentro del ciclo\n"),
            "pasos": ["Pulsa Ejecutar y mira tu lista.",
                      "Completa la lista hasta cinco cosas de un tema tuyo.",
                      "Agrega una más con append y mira cómo cambia el conteo.",
                      "Muestra solo algunas, con un if dentro del ciclo.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Por qué frutas[0] es la primera y no la segunda?",
                   "respuesta": "Porque las posiciones empiezan en 0: la primera es la 0 y la segunda es la 1."},
        "juego2": {
            "tipo": "carrera", "titulo": "Listas relámpago", "pista": "45 SEGUNDOS DE LISTAS", "segundos": 45,
            "preguntas": [
                {"pregunta": "gustos = [\"a\", \"b\", \"c\"]. ¿Qué es gustos[0]?", "opciones": ["\"a\"", "\"b\"", "\"c\""], "correcta": 0},
                {"pregunta": "¿Qué da len([\"mango\", \"piña\"])?", "opciones": ["2", "1", "3"], "correcta": 0},
                {"pregunta": "¿Qué agrega un elemento al final?", "opciones": ["append", "len", "in"], "correcta": 0},
                {"pregunta": "Una lista tiene 3 elementos. ¿Cuál es la última posición?", "opciones": ["2", "3", "1"], "correcta": 0},
                {"pregunta": "¿Qué da \"mango\" in [\"mango\", \"coco\"]?", "opciones": ["True", "False", "Error"], "correcta": 0},
                {"pregunta": "Pedir una posición que no existe da…", "opciones": ["IndexError", "None", "0"], "correcta": 0},
                {"pregunta": "¿Qué hace for g in gustos:?", "opciones": ["Pasa por cada elemento", "Borra la lista", "Cuenta hasta 10"], "correcta": 0},
                {"pregunta": "¿Qué da gustos[-1]?", "opciones": ["El último", "El primero", "Error"], "correcta": 0},
            ],
        },
        "chuleta": {
            "titulo": "Listas en Python",
            "lineas": [
                ('frutas = ["mango", "uva"]', "Una lista: entre corchetes y separada por comas."),
                ("frutas[0]", "El primero. Se cuenta desde 0, no desde 1."),
                ('frutas.append("piña")', "Añade al final."),
                ('frutas.remove("uva")', "Saca el que digas, si está."),
                ("len(frutas)", "Cuántos hay dentro."),
                ("for f in frutas:", "Recorre la lista de uno en uno."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Mira cómo crece tu lista paso a paso, con las posiciones a la vista."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Tiene un capítulo entero de listas con ejercicios que se corrigen solos."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Python en el navegador para probar append, remove y len sin instalar nada."),
        ],
    },
    6: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera función",
            "dinamica": {
                "titulo": "La máquina de saludar",
                "minutos": 3,
                "pasos": [
                    "Un voluntario es la máquina: recibe un papelito con un nombre y dice «Hola, …».",
                    "La clase la llama tres veces con nombres distintos: una máquina, muchos usos.",
                    "Todos escriben en el cuaderno la cabecera: def saluda(nombre):",
                ],
            },
            "taller2": {
                "tipo": "funcion",
                "ejemplo": "def saluda(nombre):",
                "misiones": [
                    {"pista": "Empieza con def, después el nombre, los paréntesis y los dos puntos.",
                     "pide": "Escribe la cabecera de una función saluda que reciba nombre.",
                     "nombre": "saluda", "parametros": ["nombre"], "sale": "def saluda(nombre):"},
                    {"pista": "Dos parámetros van dentro del paréntesis, separados por una coma.",
                     "pide": "Otra: suma, que reciba dos números, a y b.",
                     "nombre": "suma", "parametros": ["a", "b"], "sale": "def suma(a, b):"},
                    {"pista": "Si no recibe nada, los paréntesis van vacíos.",
                     "pide": "Una que no recibe nada: titulo.",
                     "nombre": "titulo", "parametros": [], "sale": "def titulo():"},
                    {"pista": "Los parámetros se llaman como dice la misión, en ese orden.",
                     "pide": "La última: ficha, que recibe nombre y edad.",
                     "nombre": "ficha", "parametros": ["nombre", "edad"], "sale": "def ficha(nombre, edad):"},
                ],
            },
        },
        "hoy": "Vas a crear tus propias órdenes con def y llamarlas cuando quieras.",
        "escena": "huellas",
        "calentamiento": {
            "pregunta": "¿Para qué sirve una función con def?",
            "opciones": ["Para repetir un nombre", "Para guardar pasos con nombre y reusarlos",
                         "Para borrar variables", "Para mostrar errores"],
            "correcta": 1,
            "por_que": "def guarda un bloque de pasos con un nombre. Cada vez que escribes su nombre con (), se ejecutan.",
        },
        "ejemplo": {
            "titulo": "Mis propias órdenes", "lenguaje": "python",
            "codigo": ["from pyscript import display", "", "def saludar(nombre):",
                       '    display("¡Hola,", nombre + "!")', "", "def escena(texto, opcion):",
                       "    display(texto)", '    display("Puedes:", opcion)', "",
                       'saludar("Luna")', 'saludar("Marcos")',
                       'escena("Estás frente a una cueva.", "entrar o huir")'],
            "notas": [(3, "def crea la orden; lo de adentro va con sangría."),
                      (10, "Llamarla es escribir su nombre con paréntesis."),
                      (12, "La misma función sirve para muchas escenas: cambian los paréntesis.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["def saludar(nombre):", '    display("Hola,", nombre)', "", 'saludar("Ana")', 'saludar("Leo")'],
             "opciones": ["Hola, Ana · Hola, Leo", "Hola, nombre · Hola, nombre", "Hola, Ana", "Nada"],
             "correcta": 0, "explica": "La función se llama dos veces, cada una con un nombre distinto."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["___ cofre():", '    display("¡Encontraste el tesoro!")'],
             "opciones": ["def", "function", "if"],
             "correcta": 0, "explica": "En Python una función se crea con def, su nombre, paréntesis y dos puntos."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena: primero se crea la función y después se usa.",
             "lineas": ["def final():", '    display("Fin de la aventura")', "final()"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["def puente():", '    display("Cruzas el puente")', "puente"],
             "mala": 2, "arreglo": "puente()",
             "explica": "Sin paréntesis la función no se ejecuta: solo se nombra y no pasa nada."},
        ],
        "juego": {
            "tipo": "aventura", "titulo": "La cueva del dragón", "pista": "CADA SALA ES UNA FUNCIÓN",
            "inicio": "entrada",
            "salas": {
                "entrada": {"texto": "Estás frente a una cueva oscura. Se oye un ruido adentro.",
                            "opciones": [["Entrar con la linterna", "cueva"], ["Rodear la montaña", "rio"]]},
                "cueva": {"texto": "Hay dos túneles: uno brilla y el otro huele a humo.",
                          "opciones": [["Ir al que brilla", "tesoro"], ["Ir al del humo", "dragon"]]},
                "rio": {"texto": "Un río corta el camino. Hay un bote viejo en la orilla.",
                        "opciones": [["Subir al bote", "tesoro"], ["Volver a la cueva", "entrada"]]},
                "dragon": {"texto": "¡Un dragón dormido! Se despierta y te persigue hasta la salida. Fin: sin tesoro.",
                           "opciones": []},
                "tesoro": {"texto": "¡Encontraste el cofre del tesoro! Fin: ganaste.", "opciones": []},
            },
        },
        "practica": {
            "tipo": "editor", "titulo": "Mi historia con funciones",
            "html": "<h1>Mi historia</h1>",
            "css": "body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:24px;font-size:1.3rem}",
            "py": ("from pyscript import display\n\n"
                   "def escena(texto, opcion):\n"
                   "    display(texto)\n"
                   '    display("Puedes:", opcion)\n\n'
                   'escena("Estás frente a una cueva.", "entrar o huir")\n'
                   'escena("Dentro hay un cofre.", "abrirlo o salir")\n\n'
                   "# Tu turno: una función saludar(nombre) y otra despedida()\n"
                   "# Tu turno: llama a escena tres veces más para seguir la historia\n"),
            "pasos": ["Pulsa Ejecutar y lee las dos escenas.",
                      "Llama a escena tres veces más para seguir tu historia.",
                      "Crea una función saludar(nombre) y llámala con dos nombres.",
                      "Crea una despedida() sin paréntesis por dentro y llámala al final.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Qué te ahorra escribir una función?",
                   "respuesta": "Escribir los mismos pasos una sola vez: después se llaman con su nombre las veces que haga falta."},
        "juego2": {
            "tipo": "carrera", "titulo": "¿Qué hace esta función?", "pista": "45 SEGUNDOS", "segundos": 45,
            "preguntas": [
                {"pregunta": "¿Con qué palabra se crea una función?", "opciones": ["def", "for", "if"], "correcta": 0},
                {"pregunta": "def saludar(): ¿qué le falta al final de la línea?", "opciones": ["dos puntos", "un punto", "nada"], "correcta": 0},
                {"pregunta": "¿Cómo se llama a una función llamada jugar?", "opciones": ["jugar()", "jugar", "def jugar"], "correcta": 0},
                {"pregunta": "Lo que va dentro de la función, ¿cómo se escribe?", "opciones": ["Con sangría", "Pegado al borde", "Entre comillas"], "correcta": 0},
                {"pregunta": "¿Para qué sirve una función?", "opciones": ["Guardar pasos y repetirlos", "Guardar un número", "Pintar la página"], "correcta": 0},
                {"pregunta": "def sumar(a, b): a y b son…", "opciones": ["Lo que recibe", "Lo que devuelve", "Errores"], "correcta": 0},
                {"pregunta": "¿Qué hace return?", "opciones": ["Devuelve un resultado", "Borra la función", "Repite"], "correcta": 0},
                {"pregunta": "Si nadie la llama, la función…", "opciones": ["No hace nada", "Se ejecuta igual", "Da error"], "correcta": 0},
            ],
        },
        "chuleta": {
            "titulo": "Funciones en Python",
            "lineas": [
                ("def saluda(nombre):", "Se crea una vez: nombre, paréntesis y dos puntos."),
                ('    display("Hola, " + nombre)', "Lo de dentro, con sangría: es lo que hace."),
                ('saluda("Ana")', "Se llama todas las veces que quieras."),
                ("def suma(a, b):", "Puede recibir varios parámetros, separados por comas."),
                ("    return a + b", "return devuelve el resultado a quien la llamó."),
                ("total = suma(2, 3)", "Y ese resultado se puede guardar."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Mira cómo entra y sale el programa de tu función en cada llamada."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Ejercicios de funciones que se corrigen solos, en español y sin cuenta."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Python en el navegador para escribir tus funciones sin instalar nada."),
        ],
    },
    7: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primer botón",
            "dinamica": {
                "titulo": "El timbre de la clase",
                "minutos": 3,
                "pasos": [
                    "El docente dibuja tres botones en la pizarra y les pone nombre: #sumar, #reiniciar, #apagar.",
                    "Toca uno y pregunta: ¿qué función tendría que dispararse?",
                    "Todos escriben en el cuaderno la línea que las engancha: @when(\"click\", \"#sumar\")",
                ],
            },
            "taller2": {
                "tipo": "evento",
                "ejemplo": '@when("click", "#boton")',
                "misiones": [
                    {"pista": "Dentro van dos cosas entre comillas: el evento y el botón, con su #.",
                     "pide": "Engancha tu función al botón de sumar puntos, que se llama #sumar.",
                     "id": "sumar", "sale": "click en #sumar"},
                    {"pista": "Igual que la anterior: solo cambia el nombre del botón.",
                     "pide": "Ahora al de volver a empezar: #reiniciar.",
                     "id": "reiniciar", "sale": "click en #reiniciar"},
                    {"pista": "El # va pegado al nombre, dentro de las comillas.",
                     "pide": "Al botón que apaga la música: #apagar.",
                     "id": "apagar", "sale": "click en #apagar"},
                    {"pista": "La última: cuidado con no dejarte ninguna comilla.",
                     "pide": "Y al último, el que enseña la ayuda: #ayuda.",
                     "id": "ayuda", "sale": "click en #ayuda"},
                ],
            },
        },
        "hoy": "Vas a hacer un clicker: un botón que suma puntos cada vez que lo tocas.",
        "escena": "boton",
        "calentamiento": {
            "pregunta": "Empieza en 0 y cada toque suma 1. Tocas 3 veces. ¿Cuánto marca?",
            "opciones": ["1", "3", "0", "30"],
            "correcta": 1,
            "por_que": "Cada clic ejecuta la función una vez: 0 + 1 + 1 + 1 = 3.",
        },
        "ejemplo": {
            "titulo": "Un botón que suma",
            "lenguaje": "python",
            "codigo": ['from pyscript import when, document', '', 'puntos = 0', '',
                       '@when("click", "#boton")', 'def jugar(evento):', '    global puntos', '    puntos += 1',
                       '    salida = document.querySelector("#salida")', '    salida.innerText = f"Puntos: {puntos}"'],
            "notas": [(5, "Conecta el botón #boton con la función de abajo."),
                      (8, "+= suma 1 a lo que ya había: es lo mismo que puntos = puntos + 1."),
                      (10, "La f mete la variable dentro del texto del marcador.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["puntos = 5", "puntos += 1", "puntos += 1", "display(puntos)"],
             "opciones": ["5", "6", "7", "51"],
             "correcta": 2, "explica": "Cada línea es como un clic: 5 + 1 + 1 = 7."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ['@when("click", "#boton")', "def jugar(evento):", "    ___", "    puntos += 1"],
             "opciones": ["global puntos", "puntos = 0", "return puntos"],
             "correcta": 0, "explica": "Sin global, la función no puede cambiar la variable puntos de afuera."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena el clicker.",
             "lineas": ['@when("click", "#boton")', "def jugar(evento):", "    global puntos", "    puntos += 1"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ['@when("click", "boton")', "def jugar(evento):", "    global puntos", "    puntos += 1"],
             "mala": 0, "arreglo": '@when("click", "#boton")',
             "explica": "Sin el # no busca el id boton: busca una etiqueta llamada boton, que no existe."},
        ],
        "juego": {
            "tipo": "marcador", "titulo": "30 puntos en 10 segundos", "pista": "TOCA Y MIRA LA VARIABLE",
            "variables": {"puntos": 0},
            "cajas": [{"var": "valor", "valor": "1"}],
            "botones": [
                {"texto": "¡Toca!", "linea": "puntos += 1", "var": "puntos", "op": "+=", "valor": 1},
                {"texto": "¡Toca con la caja!", "linea": "puntos = puntos + int(valor)",
                 "calc": {"izq": "puntos", "op": "+", "der": "valor", "convertir": "int", "destino": "puntos"}},
                {"texto": "Reiniciar", "linea": "puntos = 0", "var": "puntos", "op": "=", "valor": 0},
            ],
            "meta": {"var": "puntos", "valor": 30, "segundos": 10},
        },
        "practica": {
            "tipo": "editor", "titulo": "Mi clicker",
            "html": ('<h1>Mi clicker</h1>\n<button id="boton">¡Toca!</button>\n'
                     '<button id="reiniciar">Reiniciar</button>\n<p id="salida">Puntos: 0</p>'),
            "css": ("body{font-family:system-ui,sans-serif;text-align:center;padding:30px;background:#0f172a;color:#f8fafc}\n"
                    "button{font-size:1.6rem;padding:.8rem 1.6rem;margin:.4rem;border-radius:12px;border:0;cursor:pointer}\n"
                    "#salida{font-size:2rem}"),
            "py": ('from pyscript import when, document\n\n'
                   'puntos = 0\n\n'
                   '@when("click", "#boton")\n'
                   'def jugar(evento):\n'
                   '    global puntos\n'
                   '    puntos += 1\n'
                   '    document.querySelector("#salida").innerText = f"Puntos: {puntos}"\n\n'
                   '# Tu turno: haz que #reiniciar ponga puntos en 0\n'),
            "pasos": ["Pulsa Ejecutar y toca el botón.",
                      "Cambia el tema: galletas, goles o monedas, en el título y en el botón.",
                      "Programa el botón Reiniciar con su propio @when y global.",
                      "Reto: agrega una caja con id valor y suma int() de lo que escriban.",
                      "Escribe una palabra en la caja, anota el error y pulsa Ejecutar: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Qué línea conecta el botón con tu función?",
                   "respuesta": "@when(\"click\", \"#boton\"), justo encima de def jugar(evento):"},
        "juego2": {
            "tipo": "clasifica", "titulo": "¿De qué tipo es?", "pista": "TOCA Y CLASIFICA",
            "cubetas": ["str", "int", "float", "bool"],
            "items": [['"18"', 0], ["18", 1], ["1.62", 2], ["True", 3], ['"True"', 0], ["0", 1], ["3.0", 2],
                      ["False", 3], ['"Hola"', 0], ["-7", 1]],
        },
        "chuleta": {
            "titulo": "Botones y eventos",
            "lineas": [
                ('<button id="sumar">+1</button>', "En el HTML: el botón y su id."),
                ("from pyscript import when, display", "Se trae when, que es quien escucha."),
                ('@when("click", "#sumar")', "Engancha la función de abajo a ese botón."),
                ("def sumar(evento):", "La función del clic recibe el evento."),
                ("    global puntos", "Para cambiar una variable de afuera."),
                ("    puntos += 1", "Y ahí se suma."),
            ],
        },
        "recursos": [
            ("PyScript · ejemplos", "https://pyscript.com/@examples",
             "Ejemplos oficiales con botones y eventos, listos para tocar y cambiar."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Para seguir con funciones y variables, que es lo que un botón dispara."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Python en el navegador para probar la función antes de engancharla."),
        ],
    },
    8: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primer azar",
            "dinamica": {
                "titulo": "El dado de la clase",
                "minutos": 3,
                "pasos": [
                    "El docente tira un dado real cinco veces y se anotan los números en la pizarra.",
                    "¿Se puede saber el próximo? No: eso es el azar, y el programa hace lo mismo.",
                    "Todos escriben en el cuaderno la línea del dado: random.randint(1, 6)",
                ],
            },
            "taller2": {
                "tipo": "azar",
                "ejemplo": "random.randint(1, 6)",
                "misiones": [
                    {"pista": "randint lleva dos números: el primero y el último, y los dos pueden salir.",
                     "pide": "Un dado normal: un número al azar del 1 al 6.",
                     "desde": 1, "hasta": 6, "sale": "números del 1 al 6"},
                    {"pista": "Lo mismo de antes, cambiando el hasta.",
                     "pide": "Ahora uno grande: del 1 al 100.",
                     "desde": 1, "hasta": 100, "sale": "números del 1 al 100"},
                    {"pista": "Son dos resultados: el 0 y el 1.",
                     "pide": "Una moneda: 0 o 1.",
                     "desde": 0, "hasta": 1, "sale": "0 o 1"},
                    {"pista": "Cuando se elige de una lista, la función es otra: choice.",
                     "pide": "Y ahora elige al azar un color de la lista colores.",
                     "tipo": "choice", "variable": "colores", "lista": ["rojo", "azul", "verde"],
                     "sale": "uno de la lista", "ejemplo": "random.choice(colores)"},
                ],
            },
        },
        "hoy": "Vas a usar el azar para tirar dados y lanzar monedas que nunca salen igual.",
        "escena": None,
        "calentamiento": {
            "pregunta": "¿Qué números puede dar random.randint(1, 6)?",
            "opciones": ["Del 1 al 5", "Del 1 al 6", "Del 0 al 6", "Solo el 6"],
            "correcta": 1,
            "por_que": "randint incluye los dos extremos: 1, 2, 3, 4, 5 y 6. Como un dado.",
        },
        "ejemplo": {
            "titulo": "Un dado y una moneda",
            "lenguaje": "python",
            "codigo": ['import random', 'from pyscript import when, document', '',
                       '@when("click", "#dado")', 'def tirar(evento):', '    numero = random.randint(1, 6)',
                       '    salida = document.querySelector("#salida")', '    salida.innerText = f"Salió {numero}"', '',
                       '@when("click", "#moneda")', 'def lanzar(evento):', '    lado = random.choice(["cara", "cruz"])',
                       '    salida = document.querySelector("#salida")', '    salida.innerText = lado'],
            "notas": [(1, "import random trae las herramientas del azar."),
                      (6, "randint(1, 6): un número del 1 al 6, los dos incluidos."),
                      (12, "choice elige uno de la lista.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["dado = random.randint(1, 6)", "display(dado)"],
             "opciones": ["Siempre 6", "Un número del 1 al 6", "La palabra dado", "Un número del 0 al 5"],
             "correcta": 1, "explica": "Cada vez que se ejecuta elige un número nuevo entre 1 y 6."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["import random", 'moneda = random.___(["cara", "cruz"])'],
             "opciones": ["choice", "randint", "cara"],
             "correcta": 0, "explica": "choice elige al azar uno de los elementos de la lista."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena el botón que tira el dado.",
             "lineas": ['@when("click", "#dado")', "def tirar(evento):", "    numero = random.randint(1, 6)",
                        "    display(numero)"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["import random", "dado = random.randint(1, 6)", 'display("Salió dado")'],
             "mala": 2, "arreglo": 'display(f"Salió {dado}")',
             "explica": "Así sale la palabra «dado», no el número. Hacen falta la f y las llaves."},
        ],
        "juego": {"tipo": "dado", "titulo": "Tira el dado hasta llegar a 20", "pista": "EL CÓDIGO NO CAMBIA, EL NÚMERO SÍ"},
        "practica": {
            "tipo": "editor", "titulo": "Mi mesa de juego",
            "html": ('<h1>Mesa de juego</h1>\n<button id="dado">Tirar dado</button>\n'
                     '<button id="moneda">Lanzar moneda</button>\n<p id="salida">¡A jugar!</p>\n<p id="puntos">Puntos: 0</p>'),
            "css": ("body{font-family:system-ui,sans-serif;text-align:center;padding:30px;background:#0f172a;color:#f8fafc}\n"
                    "button{font-size:1.4rem;padding:.7rem 1.4rem;margin:.4rem;border-radius:12px;border:0;cursor:pointer}\n"
                    "#salida{font-size:2.4rem}"),
            "py": ('import random\n'
                   'from pyscript import when, document\n\n'
                   'puntos = 0\n\n'
                   '@when("click", "#dado")\n'
                   'def tirar(evento):\n'
                   '    global puntos\n'
                   '    numero = random.randint(1, 6)\n'
                   '    puntos += numero\n'
                   '    document.querySelector("#salida").innerText = f"Salió {numero}"\n'
                   '    document.querySelector("#puntos").innerText = f"Puntos: {puntos}"\n\n'
                   '@when("click", "#moneda")\n'
                   'def lanzar(evento):\n'
                   '    lado = random.choice(["cara", "cruz"])\n'
                   '    document.querySelector("#salida").innerText = lado\n'),
            "pasos": ["Pulsa Ejecutar y tira el dado diez veces: el código no cambia y el número sí.",
                      "Lanza la moneda y comprueba que salen cara y cruz.",
                      "Reto: tira dos dados a la vez y muestra algo como «4 + 5 = 9».",
                      "Extra: un botón «Premio sorpresa» que elige con random.choice entre cinco premios.",
                      "Pulsa Ejecutar una última vez: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Por qué el mismo código da un número distinto cada vez?",
                   "respuesta": "Porque random.randint elige un número al azar cada vez que se ejecuta."},
        "chuleta": {
            "titulo": "El azar en Python",
            "lineas": [
                ("import random", "Primero se trae la caja del azar. Una sola vez, arriba."),
                ("random.randint(1, 6)", "Un número entero al azar. El 1 y el 6 sí entran."),
                ("random.choice(colores)", "Elige uno de los de la lista."),
                ("dado = random.randint(1, 6)", "Se guarda para usarlo después."),
                ("if dado == 6:", "Y con un if se decide qué pasa con lo que salió."),
                ("random.shuffle(cartas)", "Revuelve la lista entera, como barajar."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Corre tu programa varias veces y mira cómo cambia solo lo del azar."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Ejercicios de Python que se corrigen solos, en español y sin cuenta."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Tira el dado cien veces en el navegador y mira qué sale."),
        ],
        "juego2": {
            "tipo": "clasifica", "titulo": "¿randint o choice?", "pista": "TOCA Y CLASIFICA",
            "cubetas": ["randint (un número)", "choice (uno de la lista)"],
            "items": [["Un dado del 1 al 6", 0], ["El color de la camiseta", 1],
                      ["Cuántos puntos da el golpe: 1 a 10", 0], ["Qué carta sale de la baraja", 1],
                      ["El número de la rifa", 0], ["Qué pregunta toca del examen", 1],
                      ["Los segundos que espera: 1 a 5", 0], ["Qué enemigo aparece", 1]],
        },
    },
    9: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera etiqueta",
            "dinamica": {
                "titulo": "La página de papel",
                "minutos": 3,
                "pasos": [
                    "En la pizarra se dibuja una página: título grande, párrafo, botón.",
                    "La clase le pone nombre a cada parte: eso es h1, eso es p, eso es button.",
                    "Todos escriben en el cuaderno su título: <h1>Mi sitio</h1>, abierto y cerrado.",
                ],
            },
            "taller2": {
                "tipo": "etiqueta",
                "ejemplo": "<h1>Mi sitio</h1>",
                "unidad": "etiqueta",
                "misiones": [
                    {"pista": "El título más grande es h1. Se abre, va el texto y se cierra con la barra.",
                     "pide": "Escribe el título grande de tu página: tiene que decir Mi sitio.",
                     "etiqueta": "h1", "texto": "Mi sitio", "sale": "<h1>Mi sitio</h1>"},
                    {"pista": "Un párrafo es p.",
                     "pide": "Ahora un párrafo que diga Hola a todos.",
                     "etiqueta": "p", "texto": "Hola a todos", "sale": "<p>Hola a todos</p>"},
                    {"pista": "Un escalón por debajo de h1.",
                     "pide": "Un título más pequeño que diga Sobre mí.",
                     "etiqueta": "h2", "texto": "Sobre mí", "sale": "<h2>Sobre mí</h2>"},
                    {"pista": "La etiqueta se llama igual que en inglés: button.",
                     "pide": "Y un botón que diga Entrar.",
                     "etiqueta": "button", "texto": "Entrar", "sale": "<button>Entrar</button>"},
                ],
            },
        },
        "hoy": "Vas a darle estructura a tu página con etiquetas y estilo propio con CSS.",
        "escena": "etiqueta",
        "calentamiento": {
            "pregunta": "¿Para qué sirve el atributo alt en una imagen?",
            "opciones": ["Para cambiar el tamaño", "Para describirla si no carga", "Para ponerle borde", "Para enlazarla"],
            "correcta": 1,
            "por_que": "alt describe la imagen: se lee si no carga y lo usan los lectores de pantalla.",
        },
        "ejemplo": {
            "titulo": "El esqueleto de mi sitio",
            "lenguaje": "html",
            "codigo": ["<header>", "  <h1>Ana Pérez</h1>", "</header>", "<main>", "  <section>",
                       "    <h2>Sobre mí</h2>", '    <img src="foto.jpg" alt="Ana sonriendo">',
                       "    <p>Me gusta el béisbol.</p>", "  </section>", "  <section>", "    <h2>Mi IA</h2>",
                       "  </section>", "</main>", "<footer>2026</footer>"],
            "notas": [(1, "header: la cabecera del sitio."),
                      (7, "img con alt: describe la foto."),
                      (11, "La sección Mi IA queda lista para la semana 10.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "html",
             "codigo": ['<a href="https://mlb.com">Béisbol</a>'],
             "opciones": ["Un enlace que dice Béisbol", "La página mlb.com adentro", "Un botón azul"],
             "correcta": 0, "explica": "a crea un enlace: se ve el texto y al tocarlo abre la dirección de href."},
            {"tipo": "completa", "lenguaje": "html",
             "codigo": ["<ul>", "  <li>Dibujar</li>", "  <___>Programar</li>", "</ul>"],
             "opciones": ["li", "ul", "p"],
             "correcta": 0, "explica": "Cada elemento de una lista va en su propio li."},
            {"tipo": "ordena", "lenguaje": "html",
             "enunciado": "Ordena las partes del sitio de arriba abajo.",
             "lineas": ["<header>Mi nombre</header>", "<main>Mis secciones</main>", "<footer>Contacto</footer>"]},
            {"tipo": "error", "lenguaje": "html",
             "lineas": ["<section>", "  <h2>Sobre mí</h2>", '  <img src="yo.png">', "</section>"],
             "mala": 2, "arreglo": '  <img src="yo.png" alt="Mi foto">',
             "explica": "A la imagen le falta alt: si no carga, nadie sabe qué había."},
        ],
        "juego": {
            "tipo": "portada", "titulo": "Hackea la portada", "pista": "UNA TARJETA POR CAPA",
            "cartas": {
                "html": [
                    {"id": "h1_python", "codigo": "<h1>¡Hay clase de Python!</h1>",
                     "titular": "¡Hay clase de Python!", "etiqueta": "h1", "explica": "Es el titular correcto."},
                    {"id": "p_python", "codigo": "<p>¡Hay clase de Python!</p>",
                     "titular": "¡Hay clase de Python!", "etiqueta": "p",
                     "explica": "p es un párrafo chiquito: el titular principal va en h1."},
                    {"id": "h1_otro", "codigo": "<h1>Mañana no hay clase</h1>",
                     "titular": "Mañana no hay clase", "etiqueta": "h1",
                     "explica": "Es un h1, pero dice otra cosa: revisa el texto de la misión."},
                ],
                "css": [
                    {"id": "fondo_azul", "codigo": "body { background: #1e3a8a; color: white; }",
                     "fondo": "#1e3a8a", "letra": "#ffffff", "explica": "Fondo azul y letras blancas."},
                    {"id": "letra_azul", "codigo": "body { color: #1e3a8a; }",
                     "fondo": None, "letra": "#1e3a8a",
                     "explica": "color pinta las letras, no el fondo: para el fondo es background."},
                    {"id": "fondo_rojo", "codigo": "body { background: #dc2626; color: white; }",
                     "fondo": "#dc2626", "letra": "#ffffff",
                     "explica": "Ese fondo es rojo y la misión pide azul."},
                ],
                "py": [
                    {"id": "cambia", "codigo": '@when("click", "#boton") → "¡Última hora!"',
                     "al_tocar": "¡Última hora!", "explica": "El clic cambia el titular."},
                    {"id": "sin_numeral", "codigo": '@when("click", "boton") → "¡Última hora!"',
                     "al_tocar": None,
                     "explica": "Sin el # no encuentra el botón con id boton: el clic no hace nada."},
                    {"id": "otro_texto", "codigo": '@when("click", "#boton") → "Hola"',
                     "al_tocar": "Hola",
                     "explica": "El botón funciona, pero el titular tiene que decir ¡Última hora!."},
                ],
            },
            "misiones": [
                {"texto": "El titular de la portada tiene que decir «¡Hay clase de Python!».",
                 "html": "h1_python", "css": None, "py": None},
                {"texto": "El mismo titular, y ahora la portada con fondo azul.",
                 "html": "h1_python", "css": "fondo_azul", "py": None},
                {"texto": "Titular, fondo azul, y al tocar el botón el titular cambia a «¡Última hora!».",
                 "html": "h1_python", "css": "fondo_azul", "py": "cambia"},
            ],
        },
        "practica": {
            "tipo": "editor", "titulo": "El esqueleto de mi sitio",
            "html": ('<header>\n  <h1>Tu nombre</h1>\n</header>\n<main>\n  <section>\n    <h2>Sobre mí</h2>\n'
                     '    <p>Una frase sobre ti.</p>\n  </section>\n  <section>\n    <h2>Mis intereses</h2>\n'
                     '    <ul>\n      <li>Interés 1</li>\n    </ul>\n  </section>\n  <section>\n    <h2>Mi IA</h2>\n'
                     '    <p>Aquí va el modelo que voy a entrenar.</p>\n  </section>\n</main>\n<footer>Hecho por mí</footer>'),
            "css": "", "py": "",
            "pasos": ["Escribe tu nombre en el h1 y una frase sobre ti.",
                      "Agrega una imagen o avatar con su texto alt.",
                      "Completa la lista con tres intereses.",
                      "Agrega un enlace a una página que te guste.",
                      "Deja lista la sección Mi IA y pulsa Ejecutar: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Qué pasa si la imagen no carga y no tiene alt?",
                   "respuesta": "Queda un hueco sin explicación; con alt se lee qué había y los lectores de pantalla lo pueden decir."},
        "juego2": {
            "tipo": "css", "titulo": "Mueve los controles y mira el CSS", "pista": "CADA CONTROL ES UNA LÍNEA",
            "controles": [
                {"prop": "justify-content", "tipo": "opciones", "valores": ["flex-start", "center", "space-between", "flex-end"]},
                {"prop": "flex-direction", "tipo": "opciones", "valores": ["row", "column"]},
                {"prop": "gap", "tipo": "slider", "min": 0, "max": 40, "unidad": "px"},
                {"prop": "padding", "tipo": "slider", "min": 0, "max": 40, "unidad": "px"},
                {"prop": "background-color", "tipo": "opciones", "valores": ["#ffffff", "#fef3c7", "#dbeafe", "#dcfce7"]},
            ],
            "hijos": 4,
        },
        "chuleta": {
            "titulo": "HTML y CSS",
            "lineas": [
                ("<h1>Mi sitio</h1>", "Se abre, va el contenido y se cierra con la barra."),
                ("<p>Un párrafo.</p>", "Texto normal."),
                ('<button id="ir">Entrar</button>', "Un botón. El id es su nombre para Python."),
                ("h1 { color: aqua; }", "CSS: a quién y qué se le cambia."),
                ("body { background: #0f172a; }", "El fondo de toda la página."),
                (".caja { padding: 16px; }", "El punto es una clase: se repite donde quieras."),
            ],
        },
        "recursos": [
            ("MDN · HTML para principiantes", "https://developer.mozilla.org/es/docs/Learn/HTML",
             "La referencia de verdad, en español y gratis. Busca la etiqueta que te haga falta."),
            ("CSS Diner", "https://flukeout.github.io/",
             "Un juego de 32 niveles para aprender a apuntar con CSS. Sin cuenta."),
            ("CodePen", "https://codepen.io/pen/",
             "Escribe HTML y CSS y míralo al instante. No hace falta registrarse para probar."),
        ],
    },
    10: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primer entrenamiento",
            "dinamica": {
                "titulo": "Entrenar a la clase",
                "minutos": 3,
                "pasos": [
                    "El docente enseña cinco fotos de perros y cinco de gatos y dice de cuál es cada una.",
                    "Enseña una nueva y la clase decide: eso es entrenar y después predecir.",
                    "¿Y si solo hubiéramos visto perros negros? Ahí aparece el problema de los ejemplos.",
                ],
            },
            "taller2": {
                "tipo": "clasificar",
                "misiones": [
                    {"pista": "Mira los ejemplos con los que lo entrenaste: ¿a cuál se parece este?",
                     "pide": "Entrenas un modelo con «mano abierta» y «puño». Llega una foto con los cinco dedos estirados. ¿A qué clase va?",
                     "grupos": ["Mano abierta", "Puño"], "correcto": 0,
                     "porque": "Los dedos estirados son justo los ejemplos de mano abierta."},
                    {"pista": "Cuenta los ejemplos de cada clase: ¿están parejos?",
                     "pide": "Tienes 50 fotos de mano abierta y 3 de puño. ¿Qué le falta a tu modelo?",
                     "grupos": ["Más ejemplos de puño", "Más clases", "Nada: ya está listo"], "correcto": 0,
                     "porque": "Con 3 ejemplos de puño casi siempre va a responder «mano abierta»."},
                    {"pista": "51 % es casi una moneda al aire.",
                     "pide": "El modelo responde «puño» con 51 % de confianza. ¿Qué conviene hacer?",
                     "grupos": ["Creerle sin más", "Pedir más ejemplos y volver a entrenar"], "correcto": 1,
                     "porque": "51 % es casi una moneda al aire: el modelo está dudando."},
                    {"pista": "Un modelo solo reconoce lo que se parece a lo que vio.",
                     "pide": "Entrenaste solo con fotos de tu cara. Llega la de un compañero. ¿Qué esperas?",
                     "grupos": ["Que acierte igual", "Que falle o dude"], "correcto": 1,
                     "porque": "Un modelo solo reconoce lo que se parece a sus ejemplos."},
                ],
            },
        },
        "hoy": "Vas a entrenar tu propio modelo de inteligencia artificial, sin escribir código.",
        "escena": "caja_modelo",
        "calentamiento": {
            "pregunta": "Entrenas un modelo solo con fotos tuyas. ¿Qué pasa si lo prueba otra persona?",
            "opciones": ["Acierta igual", "Puede equivocarse: nunca la vio", "Se apaga", "Pide más fotos"],
            "correcta": 1,
            "por_que": "El modelo solo aprende de los ejemplos que le das. Si todos son tuyos, otra cara lo confunde.",
        },
        "ejemplo": {
            "titulo": "Cómo aprende un modelo",
            "lenguaje": "tarjetas",
            "codigo": ["CLASES: pulgar arriba, pulgar abajo", "EJEMPLOS: 30 fotos de cada clase",
                       "ENTRENAR: el modelo busca patrones", "PROBAR: con una mano que nunca vio",
                       "CONFIANZA: qué tan seguro está, de 0 a 100 %"],
            "notas": [(1, "Una clase es una respuesta posible."),
                      (2, "Los ejemplos son lo único de lo que aprende."),
                      (4, "Se prueba con casos que no vio.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "tarjetas",
             "codigo": ["Clase A: 30 fotos variadas", "Clase B: 5 fotos, todas iguales", "Pruebas la clase B con otra luz"],
             "opciones": ["Acierta seguro", "Probablemente se equivoca", "Crea una clase C"],
             "correcta": 1, "explica": "Con pocos ejemplos iguales el modelo no aprendió la variedad del mundo real."},
            {"tipo": "completa", "lenguaje": "tarjetas",
             "codigo": ["Quieres que diga «nada» si no hay nadie", "Agregas una clase con: ___"],
             "opciones": ["fotos del fondo vacío", "más fotos tuyas", "una foto borrosa"],
             "correcta": 0, "explica": "Para que aprenda «nada» necesita ejemplos de nada: el fondo vacío."},
            {"tipo": "ordena", "lenguaje": "tarjetas",
             "enunciado": "Ordena los pasos en Teachable Machine.",
             "lineas": ["Crear un proyecto de imagen", "Nombrar las clases", "Grabar ejemplos de cada clase",
                        "Entrenar el modelo", "Probar con casos nuevos"]},
            {"tipo": "error", "lenguaje": "tarjetas",
             "lineas": ["Clase gato: 30 fotos de gatos", "Clase perro: 30 fotos de perros", "Pruebo con las mismas fotos"],
             "mala": 2, "arreglo": "Pruebo con fotos nuevas que no vio",
             "explica": "Probar con las mismas fotos no mide nada: esas ya las conoce."},
        ],
        "juego": {"tipo": "ia", "titulo": "Así responde un modelo", "pista": "TOCA UN EJEMPLO Y MIRA LA CONFIANZA"},
        "practica": {
            "tipo": "enlace", "titulo": "Entreno mi modelo",
            "url": "https://teachablemachine.withgoogle.com/train", "boton": "Abrir Teachable Machine",
            "pasos": ["En parejas elijan un tema con dos o tres clases: gestos, objetos del estuche o sonidos.",
                      "Graben al menos 30 ejemplos por clase, con variedad.",
                      "Entrenen y prueben con casos nuevos: otra mano, otro fondo, otra luz.",
                      "Exporten el modelo, súbanlo y copien el enlace que les da.",
                      "Peguen el enlace y una captura en la sección Mi IA de su sitio."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿El modelo es tonto o aprendió exactamente lo que le enseñamos?",
                   "respuesta": "Aprendió lo que le enseñamos: si los ejemplos son pocos o iguales, sus errores vienen de ahí."},
        "juego2": {
            "tipo": "clasifica", "titulo": "¿Este dato ayuda o confunde al modelo?", "pista": "PIENSA EN LA VARIEDAD",
            "cubetas": ["Ayuda", "Confunde"],
            "items": [["Fotos de tres personas distintas", 0], ["30 fotos por clase", 0], ["Dos fondos diferentes", 0],
                      ["Luz de día y luz de tarde", 0], ["Todas las fotos con el mismo fondo", 1],
                      ["Solo 5 fotos por clase", 1], ["Una clase con 50 fotos y otra con 5", 1],
                      ["Fotos de otro objeto metidas en una clase", 1]],
        },
        "chuleta": {
            "titulo": "Entrenar un modelo",
            "lineas": [
                ("Clase", "Cada cosa que quieres que reconozca: mano abierta, puño."),
                ("Ejemplos", "Las fotos de cada clase. Muchas y variadas."),
                ("Equilibrio", "Más o menos la misma cantidad en cada clase."),
                ("Entrenar", "El modelo busca el patrón. Dura unos segundos."),
                ("Confianza", "Con cuánta seguridad responde. 51 % es dudar."),
                ("Probar", "Enseñarle algo que NO estaba en los ejemplos."),
            ],
        },
        "recursos": [
            ("Teachable Machine", "https://teachablemachine.withgoogle.com/",
             "Entrena tu propio modelo con la cámara. Gratis y sin instalar nada."),
            ("Machine Learning for Kids", "https://machinelearningforkids.co.uk/?lang=es",
             "Proyectos guiados de IA en español. Se puede probar sin cuenta."),
            ("Quick, Draw!", "https://quickdraw.withgoogle.com/",
             "Dibuja y mira a una IA adivinar: 50 millones de ejemplos detrás."),
        ],
    },
    11: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera decisión con IA",
            "dinamica": {
                "titulo": "El modelo dice, Python decide",
                "minutos": 3,
                "pasos": [
                    "Un voluntario hace de modelo: solo puede decir una clase y un porcentaje.",
                    "Otro hace de Python: con eso decide qué pasa en la página.",
                    "Todos escriben en el cuaderno la línea que decide: if clase == \"mano abierta\":",
                ],
            },
            "taller2": {
                "tipo": "condicion",
                "ejemplo": 'if clase == "mano abierta":',
                "misiones": [
                    {"pista": "clase es texto: va entre comillas, igual que sale en la pantalla del modelo.",
                     "pide": "Que salude solo cuando el modelo diga mano abierta.",
                     "variable": "clase", "casos": ['"mano abierta"', '"puño"', '"nada"'],
                     "espera": [True, False, False], "sale": "solo con mano abierta"},
                    {"pista": "«Todo menos» es «distinto de».",
                     "pide": "Ahora que avise cuando el modelo diga cualquier cosa MENOS puño.",
                     "variable": "clase", "casos": ['"puño"', '"mano abierta"', '"nada"'],
                     "espera": [False, True, True], "sale": "con todo menos puño"},
                    {"pista": "Aquí la variable es confianza, y es un número: sin comillas.",
                     "pide": "Que actúe solo si la confianza pasa de 80.",
                     "variable": "confianza", "casos": [50, 80, 95],
                     "espera": [False, False, True], "sale": "solo con 95"},
                    {"pista": "«Por debajo de» es menor que.",
                     "pide": "La última: que avise cuando la confianza esté por debajo de 60.",
                     "variable": "confianza", "casos": [40, 60, 90],
                     "espera": [True, False, False], "sale": "solo con 40"},
                ],
            },
        },
        "hoy": "Vas a conectar tu modelo de IA a tu sitio y decidir en Python qué hacer con lo que ve.",
        "escena": "caja_modelo",
        "calentamiento": {
            "pregunta": "El modelo dice «pulgar arriba» con 55 % de confianza. ¿Qué debería hacer tu sitio?",
            "opciones": ["Obedecer siempre", "Decir que no está seguro", "Borrar el modelo", "Pedir otra foto"],
            "correcta": 1,
            "por_que": "Con poca confianza es mejor no adivinar. Eso no lo decide la IA: lo decide tu Python.",
        },
        "ejemplo": {
            "titulo": "Python decide qué hacer",
            "lenguaje": "python",
            "codigo": ['from pyscript import when, document, window', '', '@when("click", "#que-ves")',
                       'def que_ves(evento):', '    clase = window.clase', '    salida = document.querySelector("#respuesta")',
                       '    if clase == "pulgar arriba":', '        salida.innerText = "¡Me alegra!"',
                       '    elif clase == "pulgar abajo":', '        salida.innerText = "Ánimo, mañana mejora"',
                       '    else:', '        salida.innerText = "No reconozco eso"'],
            "notas": [(1, "window trae los datos que deja la pieza del modelo."),
                      (5, "window.clase: lo que el modelo cree que ve."),
                      (7, "Tu Python decide qué responder a cada clase.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ['clase = "pulgar abajo"', 'if clase == "pulgar arriba":', '    display("¡Bien!")', "else:",
                        '    display("Ánimo")'],
             "opciones": ["¡Bien!", "Ánimo", "pulgar abajo"],
             "correcta": 1, "explica": "La clase no es pulgar arriba, así que entra al else."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["if confianza ___ 0.8:", '    display("No estoy seguro")'],
             "opciones": ["<", ">=", "="],
             "correcta": 0, "explica": "Si la confianza es menor que 0.8, mejor no adivinar."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena la respuesta del sitio.",
             "lineas": ["clase = window.clase", 'if clase == "gato":', '    display("Miau")', "else:",
                        '    display("No es un gato")']},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["clase = window.clase", 'if clase == "Gato":', '    display("Miau")'],
             "mala": 1, "arreglo": 'if clase == "gato":',
             "explica": "La clase se escribe igual que en Teachable Machine: «Gato» no es «gato» y nunca coincide."},
        ],
        "juego": {"tipo": "ia", "titulo": "¿Qué ve el modelo y qué decide Python?", "pista": "TOCA UN EJEMPLO"},
        "practica": {
            "tipo": "editor", "titulo": "Mi IA dentro de mi sitio",
            "html": _PIEZA_TM,
            "css": "body{font-family:system-ui,sans-serif;padding:24px}\nbutton{font-size:1.2rem;padding:.5rem 1rem;border-radius:10px}\n#respuesta{font-size:1.8rem}",
            "py": ('from pyscript import when, document, window\n\n'
                   '@when("click", "#que-ves")\n'
                   'def que_ves(evento):\n'
                   '    clase = window.clase\n'
                   '    salida = document.querySelector("#respuesta")\n'
                   '    if clase == "":\n'
                   '        salida.innerText = "Primero enciende la cámara"\n'
                   '    elif clase == "Clase 1":\n'
                   '        salida.innerText = "Mensaje para la clase 1"\n'
                   '    else:\n'
                   '        salida.innerText = "Mensaje para otra clase"\n'
                   '    # Tu turno: si window.confianza no llega a 0.8, responde «No estoy seguro»\n'),
            "pasos": ["Pega el enlace de tu modelo de la semana 10 en URL_MODELO.",
                      "Pulsa Ejecutar y enciende la cámara; si no arranca, abre el editor en pantalla completa.",
                      "Cambia «Clase 1» por los nombres exactos de tus clases y escribe un mensaje para cada una.",
                      "Reto: si window.confianza no llega a 0.8, responde «No estoy seguro».",
                      "Prueba con un caso que el modelo no conoce y pulsa Ejecutar: tu código se guarda con tu nota."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Quién decidió qué responder, la IA o tu Python?",
                   "respuesta": "La IA solo dice qué cree ver y con cuánta confianza; qué hacer con eso lo decide mi Python."},
        "juego2": {
            "tipo": "ramas", "titulo": "Mueve la confianza y mira qué decide Python", "pista": "EL UMBRAL ES 0.8",
            "variable": "confianza", "entrada": "slider", "min": 0, "max": 1, "paso": 0.05, "secreto": False,
            "ramas": [{"op": ">=", "valor": 0.8, "mensaje": "Marcar como prestada"},
                      {"op": ">=", "valor": 0.5, "mensaje": "No estoy seguro: no hago nada"},
                      {"op": "else", "mensaje": "No reconozco ningún objeto"}],
        },
        "chuleta": {
            "titulo": "IA y Python juntos",
            "lineas": [
                ("window.clase", "Lo que el modelo cree ver, en texto."),
                ("window.confianza", "Con cuánta seguridad lo dice: 0 a 100."),
                ("clase = window.clase", "Se guarda en una variable tuya."),
                ('if clase == "puño":', "Y ahí decides tú, no el modelo."),
                ("if confianza > 80:", "Actuar solo cuando está seguro."),
                ("else:", "Y qué hacer cuando duda."),
            ],
        },
        "recursos": [
            ("Teachable Machine", "https://teachablemachine.withgoogle.com/",
             "Vuelve a entrenar tu modelo y copia el enlace para usarlo en tu página."),
            ("PyScript · ejemplos", "https://pyscript.com/@examples",
             "Ejemplos de Python dentro de una página, para ver cómo se conectan las piezas."),
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Prueba tus if con valores a mano antes de enchufarlos al modelo."),
        ],
    },
    12: {
        "definir_primero": True,
        "primera": {
            "titulo": "Tu primera prueba",
            "dinamica": {
                "titulo": "Lo esperado y lo real",
                "minutos": 3,
                "pasos": [
                    "El docente escribe tres líneas en la pizarra y tapa el resultado.",
                    "Cada quien escribe en el cuaderno lo que ESPERA que salga.",
                    "Se destapa: donde no coincide, ahí hay algo que arreglar.",
                ],
            },
            "taller2": {
                "tipo": "exacto",
                "ejemplo": "Escribe el resultado",
                "unidad": "respuesta",
                "misiones": [
                    {"pista": "Haz tú la resta: 3 menos 1.",
                     "pide": "vidas = 3 y después vidas = vidas - 1. ¿Qué muestra display(vidas)?",
                     "espera": ["2"], "ayuda": "Quítale uno a 3.", "sale": "un número"},
                    {"pista": "El + pega los dos textos tal cual, con su coma y su espacio.",
                     "pide": 'nombre = "Ana". ¿Qué muestra display("Hola, " + nombre)?',
                     "espera": ["Hola, Ana"], "ayuda": "El + pega los dos textos tal cual.",
                     "sale": "un saludo"},
                    {"pista": "range(3) empieza en 0 y el 3 no entra.",
                     "pide": "for i in range(3): display(i). ¿Qué números salen? Sepáralos con comas.",
                     "espera": ["0, 1, 2", "0,1,2"], "ayuda": "range(3) empieza en 0 y el 3 no entra.",
                     "sale": "tres números"},
                    {"pista": "Suma 1 + 2 + 3.",
                     "pide": "total = 0 y for n in range(1, 4): total += n. ¿Cuánto vale total al final?",
                     "espera": ["6"], "ayuda": "Suma 1 + 2 + 3.", "sale": "un número"},
                ],
            },
        },
        "hoy": "Vas a mejorar tu mejor juego del curso, probarlo con un compañero y presentarlo.",
        "escena": "pruebas",
        "calentamiento": {
            "pregunta": "¿Qué es lo primero que haces si tu juego falla?",
            "opciones": ["Borrar todo y empezar", "Leer el error: dice la línea", "Pedir otra computadora", "Cambiar de juego"],
            "correcta": 1,
            "por_que": "El error es una pista: dice la línea y qué esperaba Python.",
        },
        "ejemplo": {
            "titulo": "La hoja de prueba",
            "lenguaje": "python",
            "codigo": ["# Acción -> esperado -> real", "# Tiro el dado -> un número del 1 al 6 -> OK",
                       "# Escribo Piedra -> funciona -> FALLA", "",
                       "jugada = jugada.lower()  # arreglé la prueba 2"],
            "notas": [(1, "Cada fila: lo que haces, lo que debería pasar y lo que pasó."),
                      (3, "Una prueba que falla es un error encontrado, no un fracaso."),
                      (5, "El arreglo va con un comentario que dice qué se corrigió.")],
        },
        "retos": [
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["puntos = 0", "for i in range(4):", "    puntos += 5", "if puntos == 20:",
                        '    display("¡Ganaste!")', "else:", '    display("Sigue")'],
             "opciones": ["¡Ganaste!", "Sigue", "20", "Error"],
             "correcta": 0, "explica": "Cuatro vueltas de 5 dan 20, así que el if se cumple."},
            {"tipo": "completa", "lenguaje": "python",
             "codigo": ["vidas = 3", "if vidas ___ 0:", '    display("Game over")'],
             "opciones": ["==", "=", "+="],
             "correcta": 0, "explica": "Para preguntar si vidas es 0 se compara con ==."},
            {"tipo": "ordena", "lenguaje": "python",
             "enunciado": "Ordena el botón que suma un punto y lo muestra.",
             "lineas": ['@when("click", "#boton")', "def jugar(evento):", "    global puntos", "    puntos += 1",
                        "    display(puntos)"]},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ['premios = ["gorra", "balón"]', "n = len(premios)", "display(premios[n])"],
             "mala": 2, "arreglo": "display(premios[n - 1])",
             "explica": "len da 2, pero la última posición es 1: premios[2] da IndexError."},
        ],
        "juego": {
            "tipo": "carrera", "titulo": "Carrera de repaso del curso", "pista": "60 SEGUNDOS, TODO EL CURSO",
            "segundos": 60,
            "preguntas": [
                {"pregunta": "¿Qué hace display(\"Hola\")?", "opciones": ["Escribe Hola en la página", "Escribe Hola en la consola", "Guarda Hola"], "correcta": 0},
                {"pregunta": "puntos = 10 y después puntos -= 3. ¿Cuánto vale?", "opciones": ["13", "7", "3"], "correcta": 1},
                {"pregunta": "¿Qué conecta un botón con una función?", "opciones": ["@when(\"click\", \"#boton\")", "def boton():", "display(boton)"], "correcta": 0},
                {"pregunta": "¿Qué números puede dar random.randint(1, 6)?", "opciones": ["Del 1 al 6", "Del 0 al 6", "Del 1 al 5"], "correcta": 0},
                {"pregunta": "¿Qué signo compara si dos cosas son iguales?", "opciones": ["==", "=", "+="], "correcta": 0},
                {"pregunta": "¿Cuántas vueltas da for i in range(5)?", "opciones": ["4", "5", "6"], "correcta": 1},
                {"pregunta": "lista = [\"a\", \"b\"]. ¿Qué es lista[1]?", "opciones": ["\"a\"", "\"b\"", "Error"], "correcta": 1},
                {"pregunta": "¿Qué agrega un elemento al final de una lista?", "opciones": ["append", "len", "pop"], "correcta": 0},
                {"pregunta": "¿Qué palabra crea una función?", "opciones": ["def", "if", "for"], "correcta": 0},
                {"pregunta": "¿Qué convierte el texto \"12\" en el número 12?", "opciones": ["int(\"12\")", "str(12)", "display(\"12\")"], "correcta": 0},
                {"pregunta": "Si el if no se cumplió, ¿qué se revisa después?", "opciones": ["El elif de abajo", "Nada más", "El mismo if otra vez"], "correcta": 0},
                {"pregunta": "¿Para qué sirve global dentro de una función?", "opciones": ["Para cambiar una variable de afuera", "Para borrar la variable", "Para mostrarla"], "correcta": 0},
            ],
        },
        "practica": {
            "tipo": "editor", "titulo": "Mi juego mejorado",
            "html": '<h1>Mi juego</h1>\n<button id="boton">Jugar</button>\n<p id="salida"></p>',
            "css": ("body{font-family:system-ui,sans-serif;text-align:center;padding:30px;background:#0f172a;color:#f8fafc}\n"
                    "button{font-size:1.5rem;padding:.7rem 1.5rem;border-radius:12px;border:0;cursor:pointer}\n"
                    "#salida{font-size:2rem}"),
            "py": ('import random\n'
                   'from pyscript import when, document\n\n'
                   '# Pega aquí el juego que vas a mejorar.\n'
                   '# Requisitos: un botón, una variable que cambia,\n'
                   '# una decisión con if y algo al azar o una lista.\n\n'
                   'puntos = 0\n\n'
                   '@when("click", "#boton")\n'
                   'def jugar(evento):\n'
                   '    global puntos\n'
                   '    puntos += random.randint(1, 6)\n'
                   '    if puntos >= 20:\n'
                   '        texto = f"¡Ganaste con {puntos}!"\n'
                   '    else:\n'
                   '        texto = f"Llevas {puntos}"\n'
                   '    document.querySelector("#salida").innerText = texto\n'),
            "pasos": ["Elige qué juego vas a mejorar y escribe en una frase qué le vas a agregar.",
                      "Pega tu juego en el editor y programa la mejora.",
                      "A mitad de clase cambia de computadora: tu compañero llena tres filas de la hoja de prueba.",
                      "Corrige al menos un error que encontró y déjalo explicado con #.",
                      "Presenta en 1 minuto: qué juego es, qué le agregaste y qué error arreglaste."],
        },
        "reto_dia": None,
        "salida": {"pregunta": "¿Qué error te encontró tu compañero y cómo lo arreglaste?",
                   "respuesta": "Una buena respuesta dice la línea, qué pasaba, qué debería pasar y el cambio que lo corrigió."},
        "chuleta": {
            "titulo": "Probar un programa",
            "lineas": [
                ("Acción", "Qué hiciste: «puse 0 vidas»."),
                ("Esperado", "Qué tenía que pasar, escrito ANTES de probar."),
                ("Real", "Qué pasó de verdad, tal cual, sin adornos."),
                ("Arreglo", "Qué línea cambiaste. Una sola cada vez."),
                ("Caso raro", "El 0, el vacío, el número enorme: ahí se rompe."),
                ("Volver a probar", "Después de arreglar, se repite la prueba."),
            ],
        },
        "recursos": [
            ("Python Tutor", "https://pythontutor.com/python-compiler.html",
             "Corre tu programa línea por línea y mira dónde deja de hacer lo esperado."),
            ("futurecoder", "https://es.futurecoder.io/course/",
             "Para seguir practicando todo el curso en vacaciones. Gratis y sin cuenta."),
            ("JupyterLite", "https://jupyter.org/try-jupyter/lab/",
             "Python en el navegador para probar tus casos raros sin instalar nada."),
        ],
        "juego2": {
            "tipo": "clasifica", "titulo": "¿De qué semana es esta línea?", "pista": "REPASO DEL CURSO",
            "cubetas": ["Variable", "Ciclo", "Decisión", "Lista"],
            "items": [['nombre = "Luna"', 0], ["for i in range(5):", 1], ["if vidas == 0:", 2],
                      ['frutas = ["uva"]', 3], ["edad = 12", 0], ["else:", 2],
                      ['frutas.append("piña")', 3], ["total += n", 1],
                      ["elif nota >= 70:", 2], ["len(frutas)", 3]],
        },
    },
}

CURSO_TEORIA = {
    1: {
        "idea": {"titulo": "¿Qué es un algoritmo?",
                 "texto": "Una lista de pasos exactos y ordenados para lograr un objetivo.",
                 "ejemplo": "Una receta, las instrucciones para armar un juguete o la ruta que te da el GPS: todos son algoritmos."},
        "partes": {"titulo": "Las partes de un algoritmo",
                   "puntos": [("Objetivo claro", "Se sabe qué se quiere lograr: llegar a la puerta, hacer un jugo."),
                              ("Pasos exactos", "Nada de «un poquito»: 3 pasos, gira a la derecha."),
                              ("En orden", "El orden cambia el resultado: primero abrir la puerta y después salir.")],
                   "escena": "robot"},
        "compruebo": {"pregunta": "¿Cuál de estos SÍ es un algoritmo?",
                      "opciones": ["«Haz algo bonito»", "«Camina 3 pasos, gira a la derecha, abre la puerta»", "«Ve por ahí»"],
                      "correcta": 1,
                      "por_que": "Tiene un objetivo, pasos exactos y un orden. Los otros dos no dicen qué hacer."},
    },
    2: {
        "idea": {"titulo": "¿Qué es una variable?",
                 "texto": "Una caja con nombre donde el programa guarda un dato para usarlo después.",
                 "ejemplo": "Como el casillero con tu nombre pegado: el nombre no cambia, lo que metes dentro sí."},
        "partes": {"titulo": "Las partes de una variable",
                   "puntos": [("El nombre", "Cómo se llama la caja: nombre, edad, vidas."),
                              ("El valor", "Lo que guarda. Se mete con el signo =."),
                              ("Dos tipos", "Texto entre comillas: \"Luna\". Número sin comillas: 12."),
                              ("Mostrar", "display(nombre) enseña lo que hay dentro de la caja.")],
                   "ejemplos": ['nombre = "Luna"', "edad = 12", "vidas = 3", 'color = "azul"', "puntos = 2 + 3"],
                   "escena": "cajas"},
        "compruebo": {"pregunta": "¿Cuál de estas líneas guarda un número?",
                      "opciones": ["edad = 12", "edad = \"12\"", "edad"],
                      "correcta": 0,
                      "por_que": "Sin comillas es un número. Con comillas, \"12\" es texto."},
    },
    3: {
        "idea": {"titulo": "¿Qué es un bucle?",
                 "texto": "Un bucle repite unas líneas varias veces sin tener que escribirlas de nuevo.",
                 "ejemplo": "Hacer 10 sentadillas: no piensas diez órdenes distintas, repites la misma diez veces."},
        "partes": {"titulo": "Las partes de un ciclo",
                   "puntos": [("La cabecera", "for i in range(5): dice cuántas vueltas y termina en dos puntos."),
                              ("La sangría", "Lo corrido a la derecha es lo que se repite. Lo demás, no."),
                              ("El range", "range(desde, hasta, salto). El hasta nunca entra."),
                              ("El acumulador", "total = 0 antes del ciclo; total += n adentro, vuelta a vuelta.")],
                   "ejemplos": ["for i in range(5):",
                                '    display("¡Hola!")',
                                "total = 0",
                                "for n in range(1, 11):",
                                "    total += n",
                                "display(total)"],
                   "escena": "repetido"},
        "compruebo": {"pregunta": "¿Qué números da range(1, 5)?",
                      "opciones": ["1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4"],
                      "correcta": 0,
                      "por_que": "Empieza en el primero y se para antes del segundo: el hasta nunca entra."},
    },
    4: {
        "idea": {"titulo": "¿Qué es una decisión?",
                 "texto": "Un if revisa una condición: si es verdadera hace una cosa; si no, el else hace otra.",
                 "ejemplo": "Si llueve, llevo paraguas; si no, llevo gorra. En el juego: si acertaste, ganas; si no, sigues."},
        "partes": {"titulo": "Las partes de una decisión",
                   "puntos": [("if condición:", "Pregunta algo que solo puede ser verdadero o falso."),
                              ("==", "Compara si dos valores son iguales. Un solo = guarda."),
                              ("Dos puntos y sangría", "Lo que va dentro del if se corre a la derecha."),
                              ("else:", "Lo que pasa cuando la condición es falsa.")],
                   "ejemplos": ['edad = 15', 'if edad >= 18:', '    display("Entras")', 'else:', '    display("Todavía no")'],
                   "escena": "lluvia_paraguas"},
        "compruebo": {"pregunta": "Te quedan 3 vidas. Con if vidas == 0: display(\"Game Over\"), ¿sale Game Over?",
                      "opciones": ["No: 3 no es igual a 0", "Sí: siempre se muestra", "Sí: porque todavía tienes vidas"],
                      "correcta": 0,
                      "por_que": "El if solo entra cuando vidas vale 0. Con 3 la condición es falsa y se la salta."},
    },
    5: {
        "idea": {"titulo": "¿Qué es una lista?",
                 "texto": "Una lista guarda muchos datos en una sola variable, en orden.",
                 "ejemplo": "La lista de la compra, la playlist de canciones o las preguntas de un quiz."},
        "partes": {"titulo": "Las partes de una lista",
                   "puntos": [("Corchetes", "preguntas = [\"a\", \"b\", \"c\"]: comas entre cada dato."),
                              ("Posiciones", "Empiezan en 0: preguntas[0] es la primera."),
                              ("append", "Agrega un dato al final de la lista."),
                              ("len", "Dice cuántos datos hay.")],
                   "ejemplos": ['frutas = ["mango", "uva"]', 'frutas.append("piña")', 'display(frutas[0])', 'display(len(frutas))'],
                   "escena": "muchos"},
        "compruebo": {"pregunta": "frutas = [\"mango\", \"piña\", \"coco\"]. ¿Qué es frutas[1]?",
                      "opciones": ["\"mango\"", "\"piña\"", "\"coco\""],
                      "correcta": 1,
                      "por_que": "Las posiciones empiezan en 0: la posición 1 es la segunda, piña."},
    },
    6: {
        "idea": {"titulo": "¿Qué es una función?",
                 "texto": "Un bloque de pasos con nombre que puedes usar todas las veces que quieras.",
                 "ejemplo": "«Lávate los dientes» es una función: nadie te repite los pasos cada noche, solo dice su nombre."},
        "partes": {"titulo": "Las partes de una función",
                   "puntos": [("def nombre():", "Crea la función. Lo de adentro va con sangría."),
                              ("Parámetros", "Datos que recibe, como escena(texto, op1, op2)."),
                              ("Llamarla", "Se escribe su nombre con paréntesis: cueva()."),
                              ("Menos repetición", "Se escribe una vez y se usa en muchas partes.")],
                   "ejemplos": ['def saluda(nombre):', '    display("Hola, " + nombre)', 'saluda("Ana")', 'saluda("Luis")'],
                   "escena": "maquina"},
        "compruebo": {"pregunta": "Escribes def cofre(): pero nunca escribes cofre(). ¿Qué pasa?",
                      "opciones": ["Se ejecuta igual", "No se ejecuta nunca", "Da error siempre"],
                      "correcta": 1,
                      "por_que": "Crear la función no la ejecuta: hay que llamarla con su nombre y paréntesis."},
    },
    7: {
        "idea": {"titulo": "¿Qué es un evento?",
                 "texto": "Algo que pasa en la página, como un clic, y que hace que se ejecute una función.",
                 "ejemplo": "Tocas el timbre (el evento) y suena la campana (la función). Si nadie lo toca, no suena."},
        "partes": {"titulo": "Las partes de un evento",
                   "puntos": [("El botón", "Está en el HTML y tiene un nombre único: su id."),
                              ("@when", "Conecta el clic de ese botón con la función de abajo."),
                              ("def", "La función: los pasos que se ejecutan en cada clic."),
                              ("global y +=", "global deja cambiar la variable de afuera; puntos += 1 es puntos = puntos + 1.")],
                   "ejemplos": ['from pyscript import when, display', '@when("click", "#boton")', 'def sumar(evento):', '    display("¡Clic!")'],
                   "escena": "boton"},
        "compruebo": {"pregunta": "Si nadie toca el botón, ¿se ejecuta su función?",
                      "opciones": ["Sí, siempre", "No, espera el clic", "Solo una vez al abrir"],
                      "correcta": 1,
                      "por_que": "La función del @when solo corre cuando pasa el evento: el clic."},
    },
    8: {
        "idea": {"titulo": "¿Qué es el azar en un programa?",
                 "texto": "El azar hace que el programa elija un valor distinto cada vez, y así el juego nunca es igual.",
                 "ejemplo": "Tirar un dado, barajar las cartas o mezclar las preguntas de un quiz."},
        "partes": {"titulo": "Las partes del azar",
                   "puntos": [("import random", "Trae las herramientas del azar al programa."),
                              ("random.randint(1, 6)", "Un número entero del 1 al 6, los dos incluidos."),
                              ("random.choice(lista)", "Elige un elemento de la lista, por ejemplo cara o cruz.")],
                   "ejemplos": ['import random', 'dado = random.randint(1, 6)', 'colores = ["rojo", "azul"]', 'display(random.choice(colores))'],
                   "escena": "muchos"},
        "compruebo": {"pregunta": "¿Puede random.randint(1, 6) dar un 6?",
                      "opciones": ["Sí", "No, llega hasta el 5", "Solo si se repite"],
                      "correcta": 0,
                      "por_que": "randint incluye los dos extremos: el 1 y el 6."},
    },
    9: {
        "idea": {"titulo": "¿Qué son HTML y CSS?",
                 "texto": "El HTML dice qué es cada parte de la página; el CSS dice cómo se ve.",
                 "ejemplo": "Como las etiquetas de las cajas de una mudanza: «cocina», «libros». Dicen qué hay adentro."},
        "partes": {"titulo": "Las partes de una etiqueta",
                   "puntos": [("Abrir y cerrar", "Casi todas se abren y se cierran: h1 y después /h1."),
                              ("Estructura", "header, main, section y footer ordenan el sitio."),
                              ("Contenido", "h1 a h3, p, li, img con su alt y a con su href."),
                              ("CSS", "Un selector y sus reglas: color, background, font-size.")],
                   "escena": "etiqueta"},
        "compruebo": {"pregunta": "¿Qué etiqueta usarías para el título principal del sitio?",
                      "opciones": ["h1", "p", "footer"],
                      "correcta": 0,
                      "por_que": "h1 es el título más importante de la página."},
    },
    10: {
        "idea": {"titulo": "¿Cómo aprende una IA?",
                 "texto": "Un modelo de IA aprende a reconocer patrones a partir de muchos ejemplos, no de reglas escritas.",
                 "ejemplo": "Nadie le explica a un bebé qué es un perro: ve muchos perros y aprende a reconocerlos."},
        "partes": {"titulo": "Las partes de un modelo",
                   "puntos": [("Clases", "Las respuestas posibles: pulgar arriba o pulgar abajo."),
                              ("Ejemplos", "Fotos o sonidos de cada clase: de ellos aprende."),
                              ("Entrenar", "El modelo busca qué tienen en común los ejemplos."),
                              ("Confianza", "Qué tan seguro está de su respuesta, de 0 a 100 %.")],
                   "escena": "caja_modelo"},
        "compruebo": {"pregunta": "Si todas las fotos son de la misma persona, el modelo…",
                      "opciones": ["Aprende de todos igual", "Puede fallar con otras personas", "Se niega a entrenar"],
                      "correcta": 1,
                      "por_que": "Aprende solo de lo que ve: con una sola persona, eso es lo único que conoce. Eso es sesgo."},
    },
    11: {
        "idea": {"titulo": "¿Quién decide, la IA o tú?",
                 "texto": "El modelo dice qué cree ver y con cuánta confianza; tu Python decide qué hacer con eso.",
                 "ejemplo": "Un radar detecta algo y dice «80 % seguro de que es un avión»; la persona decide si actúa."},
        "partes": {"titulo": "Las partes de la conexión",
                   "puntos": [("La pieza del modelo", "Es JavaScript y se pega sin tocar; solo cambia el enlace."),
                              ("window.clase", "Lo que el modelo cree que ve."),
                              ("window.confianza", "Qué tan seguro está, de 0 a 1."),
                              ("Tu if / elif", "Una respuesta distinta para cada clase.")],
                   "ejemplos": ['clase = window.clase', 'if clase == "mano abierta":', '    display("¡Hola!")', 'else:', '    display("Esperando…")'],
                   "escena": "caja_modelo"},
        "compruebo": {"pregunta": "El modelo dice «gato» con 0.4 de confianza. ¿Qué debería hacer tu sitio?",
                      "opciones": ["Decir «Miau» seguro", "Decir «No estoy seguro»", "Apagar la cámara"],
                      "correcta": 1,
                      "por_que": "Con poca confianza es mejor no adivinar, y eso lo decide tu código."},
    },
    12: {
        "idea": {"titulo": "¿Qué es probar un programa?",
                 "texto": "Usarlo con casos pensados antes y comparar lo que se esperaba con lo que pasó.",
                 "ejemplo": "Antes de vender un carro lo prueban con frenadas y curvas. Tu juego también necesita su prueba."},
        "partes": {"titulo": "Las partes de una prueba",
                   "puntos": [("Acción", "Lo que haces: tiro el dado, escribo Piedra."),
                              ("Esperado", "Lo que debería pasar."),
                              ("Real", "Lo que pasó de verdad."),
                              ("Arreglo", "Si no coinciden, se corrige y se anota con #.")],
                   "ejemplos": ['vidas = 3', 'vidas = vidas - 1', 'display(vidas)', '# esperado: 2'],
                   "escena": "pruebas"},
        "compruebo": {"pregunta": "Esperabas «Ganaste» y salió «Perdiste». ¿Qué encontraste?",
                      "opciones": ["Un error para corregir", "Un fracaso", "Nada importante"],
                      "correcta": 0,
                      "por_que": "Una prueba que falla es un error encontrado: justo lo que buscabas."},
    },
}

EXTRAS = {
    "2do": {
        2: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
         "codigo": ["vidas = 3", "vidas -= 1", "vidas += 2", "display(vidas)"],
         "opciones": ["3", "4", "5", "6"],
         "correcta": 1, "explica": "3 - 1 + 2 = 4: cada línea cambia lo que había."}], "extra": 'Mostrar el marcador en una sola línea con un f-string: f"{jugador}: {puntos} pts".'},
        3: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ["cuenta = 3", "while cuenta > 0:", "    display(cuenta)", "    cuenta -= 1"],
             "opciones": ["3 · 2 · 1", "3 · 2 · 1 · 0", "1 · 2 · 3"],
             "correcta": 0, "explica": "Cuando cuenta llega a 0, la condición es False y el bucle termina antes de mostrarlo."},
            {"tipo": "error", "lenguaje": "python",
             "lineas": ["cuenta = 5", "while cuenta > 0:", '    display("¡Vamos!")'],
             "mala": 2, "arreglo": "    cuenta -= 1",
             "explica": "Nadie cambia cuenta, así que la condición siempre es True: el bucle no termina nunca."}],
            "extra": 'Repetir con while mientras el total sea menor que 100, y contar cuántas vueltas hicieron falta.'},
        4: {"retos_extra": [{"tipo": "completa", "lenguaje": "python",
             "codigo": ["if nota ___ 100:", '    display("Nota no válida")'],
             "opciones": [">", "=>", "=="],
             "correcta": 0, "explica": "Mayor que se escribe >; => no existe en Python."}], "extra": 'Encadenar dos condiciones con and: solo gana quien acierta y usa menos de cinco intentos.'},
        5: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ['frutas = ["mango", "piña"]', 'frutas.append("coco")', "display(frutas[2])"],
             "opciones": ["mango", "piña", "coco", "IndexError"],
             "correcta": 2, "explica": "append puso coco en la posición 2, la tercera."}], "extra": 'Una segunda lista con las respuestas y mostrar cada pregunta junto a la suya.'},
        6: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ["def doble(n):", "    return n * 2", "", "display(doble(4) + 1)"],
             "opciones": ["8", "9", "10", "doble(4) + 1"],
             "correcta": 1, "explica": "doble(4) devuelve 8, y a eso se le suma 1."}], "extra": 'Una función que devuelva un valor con return y usarlo en otra función.'},
        7: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ['a = "7"', 'b = "3"', "display(a + b)"],
             "opciones": ["10", "73", "Error", "a + b"],
             "correcta": 1, "explica": "Son textos: .value también llega así, y + los pega."}], "extra": 'Leer con int() lo que escriben en una caja y sumarlo al marcador.'},
        8: {"extra": 'Simular 100 tiradas con un ciclo y contar cuántas veces salió cada número.'},
        9: {"retos_extra": [{"tipo": "predice", "lenguaje": "css",
             "codigo": [".fila {", "  display: flex;", "}"],
             "opciones": ["Los hijos quedan uno al lado del otro", "Los hijos quedan uno debajo de otro", "Desaparecen"],
             "correcta": 0, "explica": "display: flex pone a los hijos en fila por defecto."}], "extra": 'Acomodar la página en columnas con Flexbox y que se vea bien en el celular.'},
        10: {"retos_extra": [{"tipo": "predice", "lenguaje": "tarjetas",
             "codigo": ["Clase A: 30 fotos variadas", "Clase B: 5 fotos, todas iguales", "Pruebas la clase B con otra luz"],
             "opciones": ["Acierta seguro", "Probablemente se equivoca", "Crea una clase C"],
             "correcta": 1, "explica": "Con pocos ejemplos iguales el modelo no aprendió la variedad del mundo real."}], "extra": 'Probar el modelo con diez casos nuevos y anotar cuántos acertó.'},
        11: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ['clase = "pulgar abajo"', 'if clase == "pulgar arriba":', '    display("¡Bien!")', "else:",
                        '    display("Ánimo")'],
             "opciones": ["¡Bien!", "Ánimo", "pulgar abajo"],
             "correcta": 1, "explica": "La clase no es pulgar arriba, así que entra al else."}], "extra": 'Que la página cambie de color según lo que ve el modelo.'},
        12: {"evidencia": 'Tu código en el editor de la clase, guardado con tu nota: el proyecto funcionando dentro de su página, probado por un compañero.'},
    },
    "3ro": {
        2: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
         "codigo": ["x = 7", "y = x", "x = x * 2", "display(x, y)"],
         "opciones": ["14 7", "14 14", "7 14", "7 7"],
         "correcta": 0, "explica": "y copió el 7 antes de que x cambiara: x termina en 14 y y sigue en 7."}], "extra": 'Calcular con // y % cuántas cosas alcanzan y cuánto sobra, e intercambiar dos variables.'},
        3: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ["notas = [60, 80, 100]", "display(max(notas) - min(notas))"],
             "opciones": ["40", "100", "60", "240"],
             "correcta": 0, "explica": "El mayor es 100 y el menor 60: la diferencia es 40."},
            {"tipo": "predice", "lenguaje": "python",
             "codigo": ["notas = [60, 80, 100]", "total = 0", "for n in notas:", "    total += n",
                        "display(total / len(notas))"],
             "opciones": ["80.0", "240", "100", "3"],
             "correcta": 0,
             "explica": "El ciclo acumula 240 y lo reparte entre las tres notas: el promedio es 80.0."}],
            "extra": 'Un acumulador que saque el promedio y cuente cuántos están por debajo de él.'},
        4: {"retos_extra": [{"tipo": "completa", "lenguaje": "python",
         "codigo": ["nota = 75", "asistencia = 90", "if nota >= 60 ___ asistencia >= 80:", '    display("Aprobado")'],
         "opciones": ["and", "or", "if"],
         "correcta": 0, "explica": "Para aprobar hacen falta las dos condiciones a la vez: and."}], "extra": 'Combinar and y or en una sola condición y probar los valores de frontera.'},
        5: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ['nombres = ["Ana", "Luis", "Eva"]', "hallados = []", "for n in nombres:",
                        '    if "a" in n.lower():', "        hallados.append(n)", "display(hallados)"],
             "opciones": ["['Ana', 'Eva']", "['Ana']", "['Ana', 'Luis', 'Eva']"],
             "correcta": 0, "explica": "«ana» y «eva» tienen a; «luis» no."}], "extra": 'Filtrar la lista en una lista nueva con los que cumplen una condición.'},
        6: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ["def doble(n):", "    return n * 2", "assert doble(3) == 6", "assert doble(0) == 1", 'display("Todo pasó")'],
             "opciones": ["Todo pasó", "AssertionError", "6"],
             "correcta": 1, "explica": "doble(0) devuelve 0, no 1: el segundo assert falla y el programa se detiene ahí."}], "extra": 'Probar tus funciones con assert: tres pruebas que pasen y una que falle a propósito.'},
        7: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ['nombre = "  aNA  "', "display(nombre.strip().title())"],
             "opciones": ["aNA", "Ana", "  Ana  ", "ANA"],
             "correcta": 1, "explica": "strip quita los espacios de los lados y title pone la primera en mayúscula."}], "extra": 'Validar la caja vacía y el texto que no es número, sin que el programa se caiga.'},
        8: {"extra": 'Comparar 1000 tiradas de uno y de dos dados, y explicar por qué no salen igual.'},
        9: {"retos_extra": [{"tipo": "completa", "lenguaje": "css",
             "codigo": [".fila {", "  display: flex;", "  ___: center;", "}"],
             "opciones": ["justify-content", "text-color", "center"],
             "correcta": 0, "explica": "justify-content reparte a los hijos a lo largo de la fila."}], "extra": 'Guardar el diseño en variables de CSS y cambiar todo el tema desde un solo lugar.'},
        10: {"retos_extra": [{"tipo": "predice", "lenguaje": "tarjetas",
             "codigo": ["Versión A: 10 fotos, una persona, un fondo", "Versión B: 30 fotos, tres personas, dos fondos",
                        "Las dos se prueban con un fondo nuevo"],
             "opciones": ["A acierta más", "B acierta más", "Aciertan igual"],
             "correcta": 1, "explica": "B vio más variedad: le cuesta menos reconocer el objeto en un fondo que no conocía."}], "extra": 'Medir el modelo con una tabla de diez casos y calcular su porcentaje de acierto.'},
        11: {"retos_extra": [{"tipo": "predice", "lenguaje": "python",
             "codigo": ["confianza = 0.75", "if confianza < 0.8:", '    display("No estoy seguro")', "else:", '    display("Lo veo")'],
             "opciones": ["Lo veo", "No estoy seguro", "0.75"],
             "correcta": 1, "explica": "0.75 es menor que 0.8: Python prefiere no adivinar."}], "extra": 'Usar un umbral de confianza: si el modelo duda, que pida ayuda en vez de decidir.'},
        12: {"evidencia": 'Tu código en el editor de la clase, guardado con tu nota: el proyecto que resuelve algo real de la escuela, con sus pruebas anotadas.'},
    },
}


def _semanas_de(nid):
    """Las 12 sesiones, con el «sube de nivel» y la evidencia del grado."""
    fuera = EXTRAS.get(nid, {})
    salida = []
    for s in CURSO_SEMANAS:
        cambia = {k: v for k, v in fuera.get(s['n'], {}).items() if k in ('extra', 'evidencia')}
        salida.append({**s, **cambia} if cambia else dict(s))
    return salida


def _actividades_de(nid):
    """Las mismas actividades para todos, más los retos extra del grado."""
    fuera = EXTRAS.get(nid, {})
    salida = {}
    for n, a in CURSO_ACT.items():
        ex = fuera.get(n, {}).get('retos_extra')
        salida[n] = {**a, 'retos_extra': ex} if ex else a
    return salida


PRIMERO["semanas"] = _semanas_de("1ro")
SEGUNDO["semanas"] = _semanas_de("2do")
TERCERO["semanas"] = _semanas_de("3ro")

ACTIVIDADES = {"1ro": _actividades_de("1ro"), "2do": _actividades_de("2do"), "3ro": _actividades_de("3ro")}
TEORIA = {"1ro": CURSO_TEORIA, "2do": CURSO_TEORIA, "3ro": CURSO_TEORIA}
