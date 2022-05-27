
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
import seaborn as sns
warnings.filterwarnings('once')

seed=123
np.random.seed(seed) # fijamos la semilla
random.seed(seed)

#############################################
# CREAMOS LAS FUNCIONES QUE VAMOS A UTILIZAR
#############################################

# Definimos función para crear bivariantes
def bivariante(variable,var_exp, var_resp, n_tramos):
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
    fig, ax1 = plt.subplots(figsize=(12, 6))

    sns.barplot(x=df_group['categorias'], y=df_group['n'], alpha=0.5, ax=ax1, color="blue")
    ax1.set( xlabel=variable, ylabel="Número de registros (N)")

    ax2 = ax1.twinx()
    sns.lineplot(x=df_group['categorias'], y=df_group['tasa_malo'], marker='o', sort=False, ax=ax2, color="red")
    ax2.set(ylim=(0, 1), ylabel="Tasa de ausentismo")
#    ax2.set(ylabel="Tasa de ausentismo")

    fig.show()


####################################################
# CREAMOS ALGUNAS VARIABLES DE INTERES
####################################################


data["Dias_espera"]=(data["Fecha_cita"]-data["Fecha_solicitud"]).dt.days
data["Dias_semana"]=pd.to_datetime(data["ScheduledDay"]).dt.dayofweek

data["Genero_masculino"]=np.where(data["Gender"]=="M",1,0)



#Nos quedamos con aquellos registros con valores consistentes
data=data[(data.Dias_espera > 0) & (data.Edad > 0)]



##############################
# VISUALIZAMOS ALGUNOS CASOS
##############################

bivariante("Edad",data["Edad"],data["Ausentismo"],10)
bivariante("Dias_espera",data["Dias_espera"],data["Ausentismo"],10)


bivariante("Educación completa",data["Educacion_completa"].astype(str),data["Ausentismo"],10)
#bivariante("Genero",data["Gender"].astype(str),data["Ausentismo"],10)

bivariante("Hipertensión",data["Hipertension"].astype(str),data["Ausentismo"],10)
bivariante("Diabetes",data["Diabetes"].astype(str),data["Ausentismo"],10)
bivariante("Alcoholismo",data["Alcoholism"].astype(str),data["Ausentismo"],10)
bivariante("SMS_recibido",data["SMS_recibido"].astype(str),data["Ausentismo"],10)




