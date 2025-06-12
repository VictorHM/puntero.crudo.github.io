# Introduccion
En los ultimos años, según iba aprendiendo más y más sobre programación, me di cuenta que hay muchos temas y conceptos fundamentales que resultan grandes desconocidos.  Es más, resulta complicado aprenderlos o encontrar fuentes donde hacerlo, sin tener que leer cientos de webs, blogs y documentos para poner todo en conjunto.

Por ello, mi idea es poner todas las cosas que he aprendido sobre estos temas en un solo lugar, tratando de hacerlo de forma lógica y que resulte sencillo estudiarlas en su contexto y conectándolo con otros conceptos relacionados.

¿Por qué considero que hay tanto desconocimiento sobre ciertos temas? Porque hay muchos lenguajes de programación de alto nivel que ocultan esos detalles para mejorar su usabilidad y capacidad de aprendizaje. Y esos lenguajes han sido usados por una gran mayoría de nuevos programadores, no necesariamente de CS, que nunca han sido expuestos a los conceptos internos. 

Todo se intentará explicar usando dos lenguajes: Python y C++.
El motivo es doble: permitir que gente que no conoce C++ pueda tener una forma de entrar en los conceptos, siendo primero explicados con un lenguaje que pueden conocer y mostrar como ese lenguaje oculta los conceptos que se tratan al usuario y como se haría en un lenguaje que no oculta. Ejemplo de esto sería la memoria y el uso de la stack y la heap. El segundo motivo es profundizar en Python y ver como se realizan esos pasos que se le ocultan al usuario para entender mejor como funciona.

# Temas
Esta es una lista que iré modificando:

- La Torre de Babel que nunca fue: todos los lenguajes acaban creando binario equivalente. La CPU funciona con bits y memoria. 
- La Eleccion: eficiencia vs. simplicidad. Python permite centrarse en el problema a resolver, ignorando detalles de ejecución, de recursos y demás.  C++ (y C, Rust y probablemente Zig) no oculta esos detalles, porque a cambio ofrece el control para crear software más eficiente. Todo tiene un precio.
- Lo que te oculta Python de la memoria: diferencias entre stack y heap. Como Python gestiona la memoria y como se hace en C++ o C.
- Tipos de datos: para qué? La realidad es que el tipo de dato determina la cantidad de memoria necesaria para almacenarlo. Si tu no decides el tipo de dato, alguien lo hará por ti. Y puede no ser la mejor opción.
- Intérpretes, compiladores y JIT.

[ESTOS PUNTOS SE IRAN MODIFICANDO SEGUN SEA NECESARIO O VEA QUE FALTA O SOBRA]

# La Torre de Babel
Programa en Python y programa en C++ que sean sustancialmente distintos. Python mucho más sencillo que el de C++ (un simple Hola Mundo podría valer).

C++ es más complejo y necesita más código que el de Python. Es un ejemplo tonto, pero por qué esto es así? Mostrar (y ver en mi caso) qué ocurre en Python detrás del escenario. Mostrar si es posible que codigo binario genera python.
