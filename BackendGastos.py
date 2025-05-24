import json
from tkinter import messagebox
from datetime import date
import os
from dateutil.relativedelta import relativedelta

#Asignarle los json variables
USUARIOS_JSON = "usuarios.json"
CATEGORIASLIM_JSON = "categorias.json"
INGRESOEGRESO_JSON = "ingegr.json"
AHORRO_JSON = "ahorro.json"

class Usuario:
    lista_usuario = []

    def __init__(self, nombre, password):
        self.nombre = nombre
        self.__pass = password
        Usuario.lista_usuario.append(self)
        
    #Validacion de inicio de sesión
    @classmethod
    def iniciar_sesion(cls, nombre, password):
        for usuario in Usuario.lista_usuario:
            if usuario.nombre == nombre and usuario._Usuario__pass == password:
                print(f"Bienvenido {usuario.nombre}, acabas de iniciar sesión")
                return usuario
        print("Datos incorrectos para inicio de sesión")
        return None

    #Carga los usuarios del usuario.json
    @classmethod
    def cargar_usuarios(cls):
        Usuario.lista_usuario.clear()
        if os.path.exists(USUARIOS_JSON):
            with open(USUARIOS_JSON, "r", encoding="utf-8") as file:
                data = json.load(file)
                for usuario_data in data:
                    Usuario(usuario_data["Nombre"], usuario_data["Password"])

    #Lo que contenga la lista_usuario lo guarda en el usuario.json
    @classmethod
    def guardar_usuarios(cls):
        data = []
        for usuario in Usuario.lista_usuario:
            data.append({
                "Nombre": usuario.nombre,
                "Password": usuario._Usuario__pass
            })
        with open(USUARIOS_JSON, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

class Catelim:
    list_catelim = []
    def __init__(self, categoria, tipo, lim_inf, lim_sup, descripcion = None):
        self.categoria = categoria
        self.tipo = tipo
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
        self.descripcion = descripcion

    #Puede guardar una nueva categoria con limites creada 
    # y tambien guarda de la lista list_catelim a categorias.json
    @classmethod
    def guardar_categorias(cls, nuevo = None):
        data = []
        if nuevo is not None:
            for datos in Catelim.list_catelim:
                if datos.categoria == nuevo.categoria:
                    datos.tipo = nuevo.tipo
                    datos.lim_inf = nuevo.lim_inf
                    datos.lim_sup = nuevo.lim_sup
            
            if not nuevo.categoria in Catelim.list_catelim:
                Catelim.list_catelim.append(nuevo)
    
        for datos in Catelim.list_catelim:
            data.append({
                "Categoria": datos.categoria,
                "Tipo": datos.tipo,
                "Limite inferior": datos.lim_inf,
                "Limite superior": datos.lim_sup,
                "Descripcion":datos.descripcion
            })
        with open(CATEGORIASLIM_JSON, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    #Del categorias.json carga los datos a la lista list_catelim
    @classmethod
    def cargar_categorias(cls):
        Catelim.list_catelim.clear()
        if os.path.exists(CATEGORIASLIM_JSON):
            with open(CATEGORIASLIM_JSON, "r", encoding="utf-8") as file:
                data = json.load(file)
                for categoria_lim in data:
                    Cat = Catelim(categoria_lim["Categoria"], categoria_lim["Tipo"], categoria_lim["Limite inferior"], categoria_lim["Limite superior"], categoria_lim["Descripcion"])
                    Catelim.list_catelim.append(Cat)

class IngEgr:
    list_ingegr = []
    def __init__(self, categoria, tipo, cantidad, alerta = None):
        self.categoria = categoria
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = date.today()
        self.periodo = str(self.fecha.year * 100 + self.fecha.month)
        self.alerta = alerta

    #De la lista list_ingegr guarda al ingegr.json
    @classmethod
    def guardar_ingegr(cls):
        data = []
        for datos in IngEgr.list_ingegr:
            data.append({
                "Categoria": datos.categoria,
                "Tipo": datos.tipo,
                "Cantidad": datos.cantidad,
                "Fecha": datos.fecha.isoformat(),
                "Periodo": datos.periodo,
                "Alerta": datos.alerta
            })
        with open(INGRESOEGRESO_JSON, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    #Del ingegr.json carga los datos a la lista list_ingegr
    @classmethod
    def cargar_ingegr(cls):
        IngEgr.list_ingegr.clear()
        if os.path.exists(INGRESOEGRESO_JSON):
            with open(INGRESOEGRESO_JSON, "r", encoding="utf-8") as file:
                data = json.load(file)
                for ingreso_egr in data:
                    Inee = IngEgr(
                        categoria=ingreso_egr["Categoria"],
                        tipo=ingreso_egr["Tipo"],
                        cantidad=ingreso_egr["Cantidad"],
                        alerta=ingreso_egr["Alerta"]
                    )
                    Inee.fecha = date.fromisoformat(ingreso_egr["Fecha"])
                    Inee.periodo = ingreso_egr["Periodo"]
                    IngEgr.list_ingegr.append(Inee)
    
    #Al crear un nuevo Ingreso/Egreso entra en la funcion
    # y de acuerdo al tipo se hace su proceso especifico
    @classmethod
    def registrar_ingegr(cls, nuevo):
        if nuevo.tipo == "I":
            IngEgr.list_ingegr.append(nuevo)
            IngEgr.guardar_ingegr()
            return None
        elif nuevo.tipo == "E":
            alert = IngEgr.validacion_lim(nuevo)
            nuevo.alerta = alert
            IngEgr.list_ingegr.append(nuevo)
            IngEgr.guardar_ingegr()
            return alert

    #Si llega a ser de tipo E (egreso) en la funcion de arriba 
    #Entra y valida si la suma de la categoria que se registro el egreso
    @classmethod
    def validacion_lim(cls, egre):
        suma_totcat = 0
        for aux in IngEgr.list_ingegr:
            if (aux.categoria == egre.categoria and aux.periodo == egre.periodo):
                suma_totcat += aux.cantidad
        suma_totcat += egre.cantidad
        
        for lim in Catelim.list_catelim:
            if lim.categoria == egre.categoria:
                if (suma_totcat < lim.lim_inf):
                    return None
                elif (lim.lim_inf < suma_totcat < lim.lim_sup):
                    return None
                elif (suma_totcat > lim.lim_sup):
                    return "Se ha superado el limite superior, exceso de gasto"


class Ahorro:
    list_ahorro = []
    def __init__(self, periodo, cantidad, alerta = None):
        self.periodo = periodo
        self.cantidad = cantidad
        self.alerta = alerta

    #Imprimira el ahorro del periodo que des o el ultimo ahorro guardado en list_ahorro
    @classmethod
    def impr_ahorro(cls, periodo=None):
        if periodo:
            for ahorro in Ahorro.list_ahorro:
                if ahorro.periodo == periodo:
                    return ahorro.cantidad
            return 0
        else:
            if Ahorro.list_ahorro:
                return Ahorro.list_ahorro[-1].cantidad
            return 0
    
    #Imprimira el ahorro del anterior mes, con el objetivo que sea este la nueva sugerencia de ahorro
    @classmethod
    def impr_ahorroant(cls, periodo):
        fecha_anterior = periodo - relativedelta(months=1)
        periodo_anterior = str(fecha_anterior.year * 100 + fecha_anterior.month)
        for aux in Ahorro.list_ahorro:
            if aux.periodo == periodo_anterior:
                return aux.cantidad
        return None

    #Del list_ahorro guarda los datos a ahorro.json
    @classmethod
    def guardar_ahorros(cls):
        data = []
        for datos in Ahorro.list_ahorro:
            data.append({
                "Periodo": datos.periodo,
                "Cantidad": datos.cantidad,
                "Alerta": datos.alerta
            })
        with open(AHORRO_JSON, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    #Del ahorro.json carga los datos a list_ahorro
    @classmethod
    def cargar_ahorros(cls):
        Ahorro.list_ahorro.clear()
        if os.path.exists(AHORRO_JSON):
            with open(AHORRO_JSON, "r", encoding="utf-8") as file:
                data = json.load(file)
                for ahorro_dat in data:
                    aho = Ahorro(ahorro_dat["Periodo"], ahorro_dat["Cantidad"], ahorro_dat["Alerta"])
                    Ahorro.list_ahorro.append(aho)

    #Cuando se haga un registro de un nuevo Ingreso/Egreso se le haran modificaciones al ahorro
    #si es egreso se resta y le da alerta si el ahorro es menor a 0
    #si es ingreso se le suma y si el ahorro es mayor a 0 elimina cualquier alerta 
    @classmethod
    def calculos_ahorro(cls, registro):
            for aux in Ahorro.list_ahorro:
                if  (aux.periodo == registro.periodo):
                    if registro.tipo == "E":
                        if registro.cantidad <= aux.cantidad:
                            aux.cantidad -= registro.cantidad
                            return None
                        elif registro.cantidad > aux.cantidad:
                            aux.cantidad -= registro.cantidad
                            aux.alerta = "El egreso ha superado al ahorro, posible adeudo"
                            return "El egreso ha superado al ahorro, posible adeudo"
                    if registro.tipo == "I":
                        aux.cantidad += registro.cantidad
                        if aux.cantidad >= 0:
                            aux.alerta = None
                            return None
                        return None
    
    #Esta diseñado por si el usuario no hace el corte de mes el ultimo día de mes
    #Cuando inicie la aplicacion automaticamente validara si hay un Ahorro para el nuevo mes (el mes en el que esta)
    # creara Un ahorro de 0 con el periodo en el que esta (periodo armado en fronted)
    @classmethod
    def inserta_auto(cls, periodo):
        if not any(aux.periodo == periodo for aux in Ahorro.list_ahorro):
            aho = Ahorro(periodo, 0)
            Ahorro.list_ahorro.append(aho)
            Ahorro.guardar_ahorros()

