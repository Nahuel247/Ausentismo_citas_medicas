
###################################################################################
#             PROYECTO: MODELO PARA PREDECIR EL AUSENTISMO A LAS CITAS MÉDICAS
#                             CON MACHINE LEARNING
###################################################################################

#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################

########################################
# IMPORTAMOS LAS LIBRERÍAS DE INTERÉS
########################################

import numpy as np
import pandas as pd
import random
from numpy.random import rand
import warnings
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


warnings.filterwarnings('once')

seed=123
np.random.seed(seed) # fijamos la semilla
random.seed(seed)

#############################################
# CREAMOS LAS FUNCIONES QUE VAMOS A UTILIZAR
#############################################


# Definimos función para crear bivariantes
def bivariante(var_exp, var_resp, n_tramos):
    if(var_exp.dtypes!="object"):
        # Tramamos la variable explicativa en n_tramos
        bins = list(sorted(set(np.quantile(var_exp.copy(), np.arange(0,1+(1/n_tramos),1/n_tramos),overwrite_input=True))))
        labels = [f'{round(i,3)}-{round(j,3)}' for i, j in zip(bins[:-1], bins[1:])] # creamos etiquetas
        categorias = pd.cut(var_exp, bins=bins, labels=labels, include_lowest=True, right=True)
        df=pd.DataFrame({'var_exp':var_exp,'categorias':categorias,'var_resp':var_resp})
        # agrupamos para conocer la tasa de incumplimiento según tramo
        df_group= df.groupby('categorias').agg(tasa_malo=('var_resp', np.mean), n=('categorias', len)).reset_index()
    else:
        df = pd.DataFrame({'categorias': var_exp, 'var_resp': var_resp})
        df_group = df.groupby('categorias').agg(tasa_malo=('var_resp', np.mean), n=('categorias', len)).reset_index()

    # Graficamos
    matplotlib.rc_file_defaults()
    fig, ax1 = plt.subplots(figsize=(12, 6))

    sns.barplot(x=df_group['categorias'], y=df_group['n'], alpha=0.5, ax=ax1, color="blue")
    ax1.set( xlabel='Fecha de las cita', ylabel="Número de registros (N)")

    ax2 = ax1.twinx()
    sns.lineplot(x=df_group['categorias'], y=df_group['tasa_malo'], marker='o', sort=False, ax=ax2, color="red")
    ax2.set(ylim=(0, 1), ylabel="Tasa de ausentismo")
    fig.show()


##############################
# CARGAMOS LOS DATOS
##############################

data=pd.read_csv("data.csv",sep=";")

data["Fecha_solicitud"]=pd.to_datetime(data["ScheduledDay"]).dt.date
data["Fecha_cita"]=pd.to_datetime(data["AppointmentDay"]).dt.date
data["Periodo"]=data["AppointmentDay"].str[:7]

data["semana"]=pd.to_datetime(data["AppointmentDay"]).dt.week
data["semana"]=data["semana"].astype(str)
data["Ausentismo"]=np.where(data["No-show"]=="Yes",1,0)


data.rename(columns = {"Scholarship":"Educacion_completa","Age":"Edad", "Hipertension":"Hipertension",
                     "SMS_received":"SMS_recibido","PatientId":"IDpaciente","AppointmentID":"IDcita"}, inplace = True)


################################
# VISUALIZAMOS LOS REGISTROS
###############################

#bivariante(data["semana"],data["Ausentismo"],10)
bivariante(data["Periodo"],data["Ausentismo"],10)
