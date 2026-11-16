import numpy as np

def limpiar_entradas(tabla):
    """Aplicar las reglas fijas del proyecto sin aprender de los datos."""
    datos = tabla.copy()

    # No se puede predecir sin una superficie válida
    superficie = datos["CONSTRUCTEDAREA"]
    if (superficie.isna() | ~np.isfinite(superficie) | (superficie <= 0)).any():
        raise ValueError("La superficie debe ser un número positivo y finito.")

    # Dormitorios extremadamente poco plausibles
    dormitorios = datos["ROOMNUMBER"]
    ratio = superficie / dormitorios.where(dormitorios > 0)
    sospechosos = (dormitorios > 0) & (ratio < 5)

    datos.loc[sospechosos, "ROOMNUMBER"] = np.nan

    # Corrección del registro geográfico auditado.
    # ASSETID y PERIOD sirven para esta regla, no como predictores.
    caso_geografico = (
        datos["ASSETID"].eq("A7501251371917084834")
        & datos["PERIOD"].eq(201806)
    )

    columnas_geograficas = [
        "LONGITUDE",
        "LATITUDE",
        "DISTANCE_TO_CITY_CENTER",
        "DISTANCE_TO_METRO"
    ]
    datos.loc[caso_geografico, columnas_geograficas] = np.nan

    return datos
