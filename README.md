# Modelo para prevenir el ausentismo en las citas médicas

En Chile, 1 de cada 5 pacientes que solicitan una hora médica no se presenta finalmente, lo que genera pérdidas de hasta 35 millones de dólares al año. A lo anterior,
hay que agregar el impacto negativo que el ausentismo tiene sobre la lista de espera, ya que las persona que no se presenta le quita la posibilidad de ser
atendido a otra que si lo necesita, además de persistir el malestar la persona podría volver a solicitar una hora de atención volviendo a quitar un cupo de salud
médica. Para evitar lo anterior, muchos centros de salud llaman a cada uno de los pacientes con cita, para asegurar su asistencia, tarea no menor.

¿Y si utilizamos un modelo para identificar a los pacientes más probables de ausentarse, y que se gestionen solo a esos pacientes?

En este repositorio encontraran el desarrollo metodológico para identificar, a través de Machine Learning, aquellos pacientes más probable de ausentarse, 
en particular:


* Se utilizó el modelo XGboost, una metodología que se basa en árboles de decisiones.

* Se utilizó una base de datos de citas médicas con 3 meses de información. Los datos fueron descargados desde la página de Kaggle, que cuenta con más de 100 mil registros de citas, información del paciente al momento de solicitar la cita y la marca sobre si asiste o no a la cita médica:
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

Las personas más jovenes tienen una mayor probabilidad de ausentarse.

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
Para el modelo se obtiene un gini igual a 0.897 indicador de que el modelo tiene una alta capacidad para discretizar entre clientes que cometen ilícitos y los que no.
A continuación, se muestra la tabla de eficiencia y el número de registros que comenten ilícitos según tramos de probabilidad. Se puede observar que en el último tramo la tasa de registros que comenten ilícitos es del 88%, que equivalen al 56% de los ilícitos totales (22/37), es decir nuestro **“recall”**. 

[![Tabla-eficiencia.png](https://i.postimg.cc/NfkyFxV0/Tabla-eficiencia.png)](https://postimg.cc/hfh43VKF)


# Estrategia de gestión
Según estos antecedentes si se van a visitar a todos los registros con marca 1 (según el modelo: 23 registros) 21 de ellos serían ilícitos (91%: precision), que corresponde al 54% de los ilícitos totales. Ahora, si se va a visitar a aquellos registros que tienen la probabilidad más alta de ilícito (último tramo: 25 registros) 22 de ello serían ilícito (88%), que corresponden al 56% de los ilícitos totales (22/39). Por otro lado, si va a visitar a los dos deciles más riesgosos, se estaría cubriendo el 85% (31/39) de los ilícitos totales, sin embargo, de los 50 registros que se irá a visitar solo el 62% (31/50) serían ilícitos. Dado lo anterior, solo basta considerar el costo y la ganancia de ir a visitar n registros con x% de ilícito para determinar la estrategia de gestión optima.



# SIGUIENTES ETAPAS
* Desarrollo de un análisis al modelo y definición de gestiones
* Realizar análisis según tipo de intervención para guiar la gestión de aquellos que generen mayor retorno.
* Desarrollo de un Dashbord para su ejecución 




