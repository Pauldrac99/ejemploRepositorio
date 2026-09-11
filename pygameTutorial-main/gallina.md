# Laboratorio 2D: Transformación Multiplicativa de Coordenadas

Mudar el desarrollo de un entorno de texto 1D a un sistema de coordenadas completo en 2D usando **Pygame** es el camino ideal para desmitificar las transformaciones matriciales y el uso de vectores en los videojuegos.

## 📋 Plan del Experimento

1. **El Concepto:** La gallina representa nuestro punto espacial $(x, y)$. Los multiplicadores ingresados desde el teclado $(a, b)$ actúan como nuestra **Matriz de Transformación**.
2. **La Matemática:** Cada vez que se presiona `ENTER`, la nueva posición $(x', y')$ se calcula multiplicando las coordenadas actuales por los factores de escala:  
   $$x' = x \cdot a$$  
   $$y' = y \cdot b$$
3. **El Origen:** Por defecto, el punto $(0,0)$ en Pygame se ubica en la esquina superior izquierda. Para hacer que las matemáticas cartesianas sean intuitivas para los alumnos, calculamos manualmente el "origen" justo en el centro de la ventana del juego.
4. **El Sprite:** Para mantener el script limpio, enfocado puramente en la lógica y evitar dependencias de archivos externos, se utiliza el emoji 🐔 renderizado directamente a través de las fuentes del sistema.

## 👩‍🏫 Dinámicas guiadas para la sesión de clase

### 1. El Misterio de la Gallina Estática (Identidad)
* **Consigna para el alumno:** Configurar los valores de los multiplicadores en $a = 1$ y $b = 1$.
* **Efecto visual:** El sprite de la gallina permanece completamente inmóvil en su posición actual.
* **Lección teórica:** Multiplicar un punto cartesiano por los componentes de una **Matriz Identidad** da como resultado el mismo vector original. No altera el espacio ni altera las distancias respecto al origen.

### 2. Inversión del Espacio (Signos Negativos y Reflexión)
* **Consigna para el alumno:** Digitar un par asimétrico como $a = -1$ y $b = 1$. Luego regresar e intentar con $a = 1$ y $b = -1$.
* **Efecto visual:** La gallina "salta" de un lado del eje hacia el extremo opuesto instantáneamente, actuando como un reflejo en un espejo.
* **Lección teórica:** Introducir signos negativos en los factores de escala equivale a aplicar una **Matriz de Reflexión** sobre los ejes cartesianos. El objeto no tiene velocidad negativa ni desaparece; simplemente se invierte su orientación espacial cambiando de cuadrante.

### 3. El Colapso de una Dimensión (Escala Cero)
* **Consigna para el alumno:** Mover primero a la gallina a cualquier coordenada remota (por ejemplo, aplicando $a = 2$, $b = 2$ un par de veces). Posteriormente, introducir el valor crítico de $a = 0$ y mantener $b = 1$.
* **Efecto visual:** La gallina se aplasta de golpe contra el eje vertical $Y$, perdiendo toda su distancia horizontal. Si el alumno intenta multiplicar $X$ de nuevo por cualquier otro número en el siguiente turno, la gallina jamás podrá salir de esa línea.
* **Lección teórica:** Multiplicar una componente espacial por cero es una transformación lineal destructiva que elimina información. Geométricamente, **colapsa una dimensión** del espacio ($X$), proyectando todo el universo bidimensional ($2D$) sobre una simple línea recta unidimensional ($1D$), haciendo que la transformación sea irreversible.