
###################################################################################
#             PROYECTO: MODELO PARA PREDECIR LA DEMANDA DE PRODUCTOS
#                             CON MACHINE LEARNING
###################################################################################

#######################################
# Autor: Nahuel Canelo
# Correo: nahuelcaneloaraya@gmail.com
#######################################


########################################
# IMPORTAMOS LAS LIBRERIAS DE INTERÉS
########################################

import numpy as np
import pandas as pd
np.random.seed(123)
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from tabulate import tabulate
import warnings
warnings.filterwarnings('once')


#############################################
# CREAMOS LAS FUNCIONES QUE VAMOS A UTILIZAR
#############################################


def tabla_eficiencia(var_exp,var_resp,n_tramos):
    bins = list(
        sorted(set(np.quantile(var_exp.copy(), np.arange(0, 1 + (1 / n_tramos), 1 / n_tramos), overwrite_input=True))))
    bins[len(bins)-1]=1
    labels = [f'{round(i, 3)}-{round(j, 3)}' for i, j in zip(bins[:-1], bins[1:])]  # creamos etiquetas
    categorias = pd.cut(var_exp, bins=bins, labels=labels, include_lowest=True, right=True)
    df = pd.DataFrame({'var_exp': var_exp, 'rangos_prob': categorias, 'var_resp': var_resp})
    # agrupamos para conocer la tasa de incumplimiento según tramo
    df_group = df.groupby('rangos_prob').agg(n=('rangos_prob', len), n_malos=('var_resp', sum),
                                            tasa_malo=('var_resp', np.mean)).reset_index()
    print(tabulate(df_group, headers=df_group.columns))
    return df_group



# SE CREA UNA FUNCIÓN PARA EVALUAR DISTINTOS INDICADORES
def metricas_eficiencia(y_test,predicciones):
    mat_confusion = confusion_matrix(y_true=y_test,y_pred=predicciones)
    accuracy = accuracy_score(y_true=y_test,y_pred=predicciones,normalize=True)

    print("Matriz de confusión")
    print("-------------------")
    print(mat_confusion)
    print("")
    print(f"El accuracy de test es: {100 * accuracy} %")

    print(classification_report(
            y_true=y_test,
            y_pred=predicciones))



# SE CONSTRUYE LA FUNCIÓN DE GINI
def gini_generico(actual, pred):
    assert (len(actual) == len(pred))
    all = np.asarray(np.c_[actual, pred, np.arange(len(actual))], dtype=np.float)
    all = all[np.lexsort((all[:, 2], -1 * all[:, 1]))]
    totalLosses = all[:, 0].sum()
    giniSum = all[:, 0].cumsum().sum() / totalLosses

    giniSum -= (len(actual) + 1) / 2.
    return giniSum / len(actual)


def gini(actual, pred):
    return gini_generico(actual, pred) / gini_generico(actual, actual)

##########################################
# CONSTRUIMOS EL MODELO
##########################################

# limpiamos la data
data_artificial=data.drop(["No-show","Periodo","AppointmentDay","Neighbourhood","Fecha_cita","Fecha_solicitud","ScheduledDay",
                 "Handcap","Gender","semana"],axis=1)

X=data_artificial.drop(["Ausentismo","IDpaciente", "IDcita"],axis=1).copy()
y=data_artificial["Ausentismo"].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)


#--------- VALIDACIÓN CRUZADA ---------#
data_dmatrix = xgb.DMatrix(data=X_train,label=y_train)

params = {'objective':'binary:logistic', "subsample": 0.4,"colsample_bytree": 0.4,'eta': 0.1, 'max_depth': 3}

# Ajustamos el modelo
xgb_cv = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3, metrics = 'gini', num_boost_round=3000, seed=123)



#--------- ENTRENAMOS EL MODELO ---------#

parametros = ({"objective": "binary:logistic",
               "eval_metric": "logloss",
               "subsample": 0.7,
              "colsample_bytree": 0.4,
               "learning_rate": 0.1, #1
               "max_depth": 3,
               "n_estimators": 3000
               })

modelo = xgb.XGBClassifier(**parametros)
modelo.fit(X_train,y_train)


#################
#   DESEMPEÑO
#################


#------------train ----------#

# Métricas para variable respuesta categórica
y_train_pred = modelo.predict(X = X_train)
metricas_eficiencia(y_train,y_train_pred)


# Métricas para variable respuesta continua
y_train_pred = pd.DataFrame(modelo.predict_proba(X = X_train)).loc[:,1]
gini(y_train,y_train_pred)
roc_auc_score(y_train,y_train_pred)

n_tramos=10
var_exp=y_train_pred
var_resp=y_train.reset_index().copy().Ausentismo

tabla_eficiencia(var_exp,var_resp,10)


#------------test ----------#

# Métricas para variable respuesta categórica
y_test_pred = modelo.predict(X = X_test)
metricas_eficiencia(y_test,y_test_pred)


# Métricas para variable respuesta continua
y_test_pred = pd.DataFrame(modelo.predict_proba(X = X_test)).loc[:,1]
gini(y_test,y_test_pred)
roc_auc_score(y_test,y_test_pred)


n_tramos=10
var_exp=y_test_pred
var_resp=y_test.reset_index().copy().Ausentismo

tabla_eficiencia(var_exp,var_resp,10)

