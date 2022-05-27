# Modelo para predecir el ausentismo en citas médicas

En Chile, 1 de cada 5 pacientes que solicitan una hora médica no se presenta finalmente, lo que genera pérdidas de hasta 35 millones de dólares al año. A lo anterior,
hay que agregar el impacto negativo que el ausentismo tiene sobre la lista de espera, ya que las persona que no se presenta le quita la posibilidad de ser
atendido a otra que, si lo necesita, además de persistir el malestar la persona podría volver a solicitar una hora de atención volviendo a quitar un cupo de salud
médica. Para evitar lo anterior, muchos centros de salud llaman a cada uno de los pacientes con cita, para asegurar su asistencia, tarea no menor.

¿Y si utilizamos un modelo para identificar a los pacientes más probables de ausentarse, y que se gestionen solo a esos pacientes?

En este repositorio encontraran el desarrollo metodológico para identificar, a través de Machine Learning, aquellos pacientes más probables de ausentarse, 
en particular:


* Se utilizó el modelo XGboost, una metodología que se basa en árboles de decisiones.

* Se utilizó una base de datos de citas médicas con 3 meses de información, además cuenta con más de 100 mil registros de citas, información del paciente al momento de solicitar la cita y la marca sobre si asiste o no a la cita médica. Los datos fueron descargados desde la página de Kaggle:
 https://www.kaggle.com/datasets/joniarroba/noshowappointments?select=KaggleV2-May-2016.csv

* Dada la poca información disponible, no se pudieron construir variables históricas o relacionadas con el tipo de especialidad que se quiere asistir. quedando pendiente para otro proyecto.


# Ausentismo según periodo

A continuación se muestra la tasa de ausentismo para cada uno de los meses con información. Se observa que la tasa de ausentismo es constante para los tres meses.


[![Ausentismo-periodo.png](https://i.postimg.cc/zfkRSKFX/Ausentismo-periodo.png)](https://postimg.cc/bGsJqG5K)

# Análisis descriptivo de la distribución del ausentismo
A continuación se muestra los resultados de un análisis descriptivo 

*Días de espera*

Entre mayor sea el número de espera la probabilidad de que se ausente un paciente incrementa.

[![Dias-espera.png](https://i.postimg.cc/hvrDrcH7/Dias-espera.png)](https://postimg.cc/5QXW9d9x)

*Edad*

Las personas más jóvenes tienen una mayor probabilidad de ausentarse.

[![Edad.png](https://i.postimg.cc/4NNDPgv6/Edad.png)](https://postimg.cc/jCm3qBF2)

*Genero*

No se observan diferencias entre mujeres y hombres sobre el ausentismo

[![Genero.png](https://i.postimg.cc/brpw3wp0/Genero.png)](https://postimg.cc/XG1Wv3ZX)

*Hipertensión*

Las personas no hipertensas son más probables de ausentarse a la cita médica.

[![Hipertensi-n.png](https://i.postimg.cc/xCRXrzsp/Hipertensi-n.png)](https://postimg.cc/njXFBCfq)

*Diabetes*

[![Diabetes.png](https://i.postimg.cc/W1y2R3p6/Diabetes.png)](https://postimg.cc/qN8fyp3z)


*Alcoholismo*

Las personas con alcoholismo son más propensas a ausentarse.

[![Alcoholismo.png](https://i.postimg.cc/B6V9d7BY/Alcoholismo.png)](https://postimg.cc/vgfNnzjf)


# Cross-validation
Para asegurar la robustez del modelo y su correcta parametrización, se optó por utilizar la metodología de croos-validation, que consiste en utilizar cierto porcentaje de la muestra de desarrollo para entrenar el modelo y el resto para probar el efecto que tiene los parámetros sobre el desempeño del modelo ante datos nuevos. Para este proyecto se dejaron fijos valores como la profundidad del árbol, el porcentaje de variables que se van a utilizar, etc. y se hizo variar el número de árboles del modelo (n_estimators), con el fin de obtener el conjunto de parámetros que asegurasen la robustez del modelo ante un conjunto de datos nuevos.

[![cross-validation.png](https://i.postimg.cc/4yrXpS3y/cross-validation.png)](https://postimg.cc/QKJL3S1Z)


# Tablas de eficiencia (en test)
Para el modelo se obtuvo un gini de 28 en train y 22 en test, lo que indicaría que el modelo podría ser mejorado.

A continuación, se muestra la tabla de eficiencia y el número de registros que comenten ilícitos según tramos de probabilidad. Se puede observar que en el último tramo la tasa de ausentismo es del 41% valor que está arriba de la tasa de ausentismo de la base de datos (28%), lo que significa que hay una mayor probabilidad de encontrar pacientes que se van a ausentar en este grupo que si se tomará desde cualquier punto en la base de datos sin un modelo.

[![Tabla-eficiencia.png](https://i.postimg.cc/NfkyFxV0/Tabla-eficiencia.png)](https://postimg.cc/hfh43VKF)


# Estrategia de gestión
Según estos antecedentes se recomienda contactar aquellos pacientes que se encuentran en el último y penúltimo tramo de mayor probabilidad. 



# SIGUIENTES ETAPAS
* Incorporar la especialidad médica solicitada
* Construir variables históricas.
