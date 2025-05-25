import tkinter as tk
from tkinter import ttk, messagebox
from BackendGastos import *
from datetime import datetime, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk

def ventanainicio():
    global venta1, entrada1, entrada2, FECHA_ACTUAL, PERIODO_ACTUAL, FECHA_HOY, PERIODO_ANTERIOR
    #Carga de archivos json a listas para su uso
    Usuario.cargar_usuarios()
    IngEgr.cargar_ingegr()
    Ahorro.cargar_ahorros()
    Catelim.cargar_categorias()
    
    #Asigno valor a variables de fechas y periodos para su uso
    FECHA_HOY = datetime.today()
    FECHA_ACTUAL = FECHA_HOY.strftime("%Y-%m-%d")
    temp_per = str(FECHA_HOY.year * 100 + FECHA_HOY.month)
    #En la variable aho carga el ultimo valor de la lista ahorro.lis_ahorro 
    aho = Ahorro.get_last_ahorro()

    #Al iniciar la app valida si el ahorro cargado en aho esta abierto 
    #Y si el periodo es menor al periodo en el que esta, 
    #invocara la funcion cierra periodo, para cerrar el periodo regresado y creara un nuevo periodo para el actual
    #y se guardara en la funcion inserta_aho, tambien se igualara a la variable global PERIODO_ACTUAL
    #el periodo para el nuevo ahorro que se creo para trabajar con el 
    #En el caso que el periodo del ahorro cargado en aho sea mayor(caso que no existe) o que sea igual
    #se igualara a mi variable global PERIODO_ACTUAL el periodo del ahorro que trae registrado la variable aho
    if aho.estatus == "AB":
        if temp_per > aho.periodo:
            Ahorro.cierra_periodo(aho.periodo)
            aho1 = Ahorro(temp_per, 0)
            PERIODO_ACTUAL = temp_per
            Ahorro.inserta_aho(aho1)
        else:
            PERIODO_ACTUAL = aho.periodo
    
    temp_fecha = date(int(PERIODO_ACTUAL[0:4]), int((PERIODO_ACTUAL[4:6])),1)
    temp_fecha = temp_fecha - relativedelta(months=1)
    PERIODO_ANTERIOR = str(temp_fecha.year * 100 + temp_fecha.month)
    
    #Crear tipos de fuentes de escritura
    fuente_titulo = ("Helvetica", 15, "bold")
    fuente_label = ("Helvetica", 12)
    fuente_entry = ("Helvetica", 11)

    #Crear la ventana inicio de sesión
    venta1 = tk.Tk()
    venta1.title("Inicio de Sesión - Gestor de Gastos")
    venta1.geometry("450x500")
    venta1.resizable(False, False)
    venta1.configure(bg="#F5F6F5")
    venta1.iconbitmap("C://Users//Usuario//Documents//Programa Phyton//PROYECTO FINAL GASTOS//Icogasto.ico")

    #Creacion de fondo
    canvas = tk.Canvas(venta1, width=450, height=500, highlightthickness=0, bg="#F5F6F5")
    canvas.pack(fill="both", expand=True)
    
    imagen = Image.open("C://Users//Usuario//Documents//Programa Phyton//PROYECTO FINAL GASTOS//Portadagestion.jpeg")
    imagen = imagen.resize((450, 500), Image.LANCZOS)
    imagen = imagen.convert("RGBA")
    imagen.putalpha(50)
    fondo = ImageTk.PhotoImage(imagen)
    canvas.create_image(0, 0, anchor=tk.NW, image=fondo)
    canvas.image = fondo

    title_frame = tk.Frame(canvas, bg="#2C3E50", bd=0)
    canvas.create_window(225, 80, window=title_frame)
    tk.Label(title_frame, text="Administrador de Gastos Familiares", font=fuente_titulo, bg="#2C3E50", fg="white", pady=10, padx=20).pack()

    login_frame = ttk.Frame(canvas, style="Card.TFrame")
    canvas.create_window(225, 300, window=login_frame)
    
    style = ttk.Style()
    style.configure("Card.TFrame", background="white")
    style.configure("Custom.TButton", font=fuente_label, padding=10)
    
    ttk.Label(login_frame, text="Usuario:", font=fuente_label, background="white").grid(row=0, column=0, padx=10, pady=(20,5), sticky="e")
    entrada1 = ttk.Entry(login_frame, font=fuente_entry, width=25)
    entrada1.grid(row=0, column=1, padx=10, pady=(20,5))
    
    ttk.Label(login_frame, text="Contraseña:", font=fuente_label, background="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entrada2 = ttk.Entry(login_frame, show="*", font=fuente_entry, width=25)
    entrada2.grid(row=1, column=1, padx=10, pady=5)
    
    ttk.Button(login_frame, text="Iniciar Sesión", style="Custom.TButton", command=inicio).grid(row=2, column=0, columnspan=2, pady=20)

    venta1.protocol("WM_DELETE_WINDOW", alcerrar)
    venta1.mainloop()

def alcerrar():
    venta1.destroy()

def inicio():
    usuario = entrada1.get()
    password = entrada2.get()
    usuario_iniciar = Usuario.iniciar_sesion(usuario, password)
    if usuario_iniciar is None:
        messagebox.showerror("Error", "El Usuario o la contraseña son incorrectos")
    else:
        venta1.destroy()
        root = tk.Tk()
        GastosApp(root)
        root.mainloop()

class GastosApp:
    def __init__(self, root):
        #Creacion de ventana de pestañas
        self.root = root
        self.root.title("Sistema Gestor de Gastos")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#F5F6F5")
        self.root.iconbitmap("C://Users//Usuario//Documents//Programa Phyton//PROYECTO FINAL GASTOS//Icogasto.ico")

        #Creacion de estilo fuentes, botones, pestaña, tabla, frames
        self.fuente_titulo = ("Helvetica", 16, "bold")
        self.fuente_label = ("Helvetica", 11)
        self.fuente_entry = ("Helvetica", 10)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#F5F6F5")
        style.configure("TNotebook.Tab", background="#ADD8E6", foreground="black", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#2C3E50")], foreground=[("selected", "white")])
        style.configure("TFrame", background="#F5F6F5")
        style.configure("Card.TFrame", background="white", relief="flat")
        style.configure("Custom.TButton", font=self.fuente_label, padding=8)
        style.configure("Treeview", font=self.fuente_entry, rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        #Creacion de pestañas
        self.notebook = ttk.Notebook(root, style="TNotebook")
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        #Pestaña de categorias
        self.tab_categorias = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_categorias, text='Categorías y Límites')
        self.setup_categorias()

        #Pestaña de Ingresos/Egresos
        self.tab_ingegr = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ingegr, text='Ingresos/Egresos')
        self.setup_ingegr()

        #Pestaña de ahorro
        self.tab_ahorro = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ahorro, text='Ahorro')
        self.setup_ahorro()

        #Pestaña de busquedas
        self.tab_busqueda = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_busqueda, text='Búsqueda')
        self.setup_busqueda()

        #Pestaña de reportes
        self.tab_reporte = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reporte, text='Reportes')
        self.setup_reporte()

    #Diseño de pestaña categorias
    def setup_categorias(self):
        frame_cat = ttk.LabelFrame(self.tab_categorias, text="Registrar Categorías", style="Card.TFrame")
        frame_cat.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(frame_cat, text="Categoría:", font=self.fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.categoria_entry = ttk.Entry(frame_cat, font=self.fuente_entry, width=30)
        self.categoria_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_cat, text="Egreso(E)/Ingreso(I):", font=self.fuente_label).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.tipo_combobox = ttk.Combobox(frame_cat, values=["E", "I"], state="readonly", font=self.fuente_entry, width=27)
        self.tipo_combobox.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame_cat, text="Límite Inferior ($):", font=self.fuente_label).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.lim_inf_entry = ttk.Entry(frame_cat, font=self.fuente_entry, width=30)
        self.lim_inf_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(frame_cat, text="Límite Superior ($):", font=self.fuente_label).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.lim_sup_entry = ttk.Entry(frame_cat, font=self.fuente_entry, width=30)
        self.lim_sup_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(frame_cat, text="Registrar", style="Custom.TButton", command=self.registrar_categoria).grid(row=4, column=0, columnspan=2, pady=15)

        frame_lista = ttk.LabelFrame(self.tab_categorias, text="Categorías Registradas", style="Card.TFrame")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        #Diseño de impresion de datos de categorias
        columns = ("Categoría", "Tipo", "Límite Inferior", "Límite Superior")
        self.tree_categoria = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_categoria.heading(col, text=col)
            self.tree_categoria.column(col, width=150, anchor="center")
        self.tree_categoria.pack(fill='both', expand=True, padx=5, pady=5)
        
        #Actualizar la tabla de categorias
        self.actualizar_lista_categorias()

        ttk.Button(frame_lista, text="Actualizar Lista", style="Custom.TButton", command=self.actualizar_lista_categorias).pack(pady=10)

    #Diseño de pestaña Ingresos/Egresos
    def setup_ingegr(self):
        frame_ingegr = ttk.LabelFrame(self.tab_ingegr, text="Registrar Ingreso/Egreso", style="Card.TFrame")
        frame_ingegr.pack(pady=10, padx=10, fill='x')

        #Cargara a la variable con las Categorias y descripciones si es que las tiene que esten
        #en la lista de Categorias Catelim.list_catelim
        categorias = [f"{cat.categoria} - {cat.descripcion}" if cat.descripcion is not None else cat.categoria for cat in Catelim.list_catelim]
        
        ttk.Label(frame_ingegr, text="Categoría:", font=self.fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.categoria_combobox = ttk.Combobox(frame_ingegr, values=categorias, state="readonly", font=self.fuente_entry, width=55)
        self.categoria_combobox.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame_ingegr, text="Cantidad ($):", font=self.fuente_label).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cantidad_entry = ttk.Entry(frame_ingegr, font=self.fuente_entry, width=30)
        self.cantidad_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(frame_ingegr, text="Ahorro Actual:", font=self.fuente_label).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.ahorro_actual_label = ttk.Label(frame_ingegr, text=str(Ahorro.impr_ahorro(PERIODO_ACTUAL)), font=self.fuente_label)
        self.ahorro_actual_label.grid(row=0, column=3, padx=10, pady=5)

        ttk.Label(frame_ingegr, text="Sugerencia de Ahorro:", font=self.fuente_label).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.sugerencia_ahorro_label = ttk.Label(frame_ingegr, text=str(Ahorro.impr_ahorro(PERIODO_ANTERIOR)), font=self.fuente_label)
        self.sugerencia_ahorro_label.grid(row=1, column=3, padx=10, pady=5)

        ttk.Button(frame_ingegr, text="Registrar", style="Custom.TButton", command=self.registrar_ingegr).grid(
            row=3, column=0, columnspan=2, pady=15)

        frame_lista = ttk.LabelFrame(self.tab_ingegr, text="Ingresos/Egresos del Período", style="Card.TFrame")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)
        
        #Diseño de impresion de datos de Ingresos/Egresos
        columns = ("Categoría", "Tipo", "Cantidad", "Fecha", "Período", "Alerta")
        self.tree_ingegr = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_ingegr.heading(col, text=col)
            self.tree_ingegr.column(col, width=150, anchor="center")
        self.tree_ingegr.pack(fill='both', expand=True, padx=5, pady=5)

        #Actualizar la tabla de Ingresos/Egresos
        self.actualizar_lista_ingegr()

        ttk.Button(frame_lista, text="Actualizar Lista", style="Custom.TButton", command=self.actualizar_lista_ingegr).pack(pady=10)

    #Diseño de pestaña ahorro
    def setup_ahorro(self):
        frame_ahorro = ttk.LabelFrame(self.tab_ahorro, text="Corte de Mes", style="Card.TFrame")
        frame_ahorro.pack(pady=10, padx=10, fill='x')

        self.ahorro_per_label = ttk.Label(frame_ahorro, text=f"Período: {PERIODO_ACTUAL}", font=self.fuente_titulo)
        self.ahorro_per_label.grid(row=0, column=0, padx=10, pady=5)
        self.ahorro_label = ttk.Label(frame_ahorro, text=f"Importe ($): {Ahorro.impr_ahorro(PERIODO_ACTUAL)}", font=self.fuente_titulo)
        self.ahorro_label.grid(row=1, column=0, padx=10, pady=5)
        #ttk.Label(frame_ahorro, text="Solo puede hacer cierre", font=self.fuente_titulo).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(frame_ahorro, text=f"Fecha: {FECHA_ACTUAL}", font=self.fuente_titulo).grid(row=2, column=0, padx=10, pady=5)

        ttk.Button(frame_ahorro, text="Realizar Corte", style="Custom.TButton", command=self.corte_mes).grid(row=3, column=0, pady=15)

    #Diseño de pestaña busqueda
    def setup_busqueda(self):
        frame_busqueda = ttk.LabelFrame(self.tab_busqueda, text="Búsqueda de Registros", style="Card.TFrame")
        frame_busqueda.pack(pady=10, padx=10, fill='x')

        categorias = [cat.categoria for cat in Catelim.list_catelim]
        ttk.Label(frame_busqueda, text="Categoría:", font=self.fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.categoria_bus_combobox = ttk.Combobox(frame_busqueda, values=categorias, state="readonly", font=self.fuente_entry, width=20)
        self.categoria_bus_combobox.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_busqueda, text="Egreso(E)/Ingreso(I):", font=self.fuente_label).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.tipo_bus_entry = ttk.Combobox(frame_busqueda, values=["E", "I"], state="readonly", font=self.fuente_entry, width=17)
        self.tipo_bus_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(frame_busqueda, text="Rango de Importes:", font=self.fuente_label).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cantidad1_bus_entry = ttk.Entry(frame_busqueda, font=self.fuente_entry, width=10)
        self.cantidad1_bus_entry.grid(row=1, column=1, padx=(10,5), pady=5)
        self.cantidad2_bus_entry = ttk.Entry(frame_busqueda, font=self.fuente_entry, width=10)
        self.cantidad2_bus_entry.grid(row=1, column=2, padx=(5,10), pady=5)

        ttk.Label(frame_busqueda, text="Rango de Fechas (YYYY-MM-DD):", font=self.fuente_label).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.fecha1_bus_entry = ttk.Entry(frame_busqueda, font=self.fuente_entry, width=10)
        self.fecha1_bus_entry.grid(row=2, column=1, padx=(10,5), pady=5)
        self.fecha2_bus_entry = ttk.Entry(frame_busqueda, font=self.fuente_entry, width=10)
        self.fecha2_bus_entry.grid(row=2, column=2, padx=(5,10), pady=5)

        ttk.Button(frame_busqueda, text="Buscar", style="Custom.TButton", command=self.validar_busqueda).grid(
            row=3, column=0, columnspan=4, pady=15)

        frame_lista = ttk.LabelFrame(self.tab_busqueda, text="Registros Encontrados", style="Card.TFrame")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        #Diseño de impresion de Busquedas
        columns = ("Categoría", "Tipo", "Importe", "Fecha", "Período")
        self.tree_busqueda = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_busqueda.heading(col, text=col)
            self.tree_busqueda.column(col, width=150, anchor="center")
        self.tree_busqueda.pack(fill='both', expand=True, padx=5, pady=5)

    #Diseño de pestaña reporte 
    def setup_reporte(self):
        frame_reporte = ttk.LabelFrame(self.tab_reporte, text="Generación de Reportes", style="Card.TFrame")
        frame_reporte.pack(pady=10, padx=10, fill='x')

        ttk.Label(frame_reporte, text="Período (YYYYMM):", font=self.fuente_label).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.periodo_entry = ttk.Entry(frame_reporte, font=self.fuente_entry, width=20)
        self.periodo_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(frame_reporte, text="Generar Reporte", style="Custom.TButton", command=self.generar_reporte).grid(
            row=1, column=0, columnspan=2, pady=15)

        frame_lista = ttk.LabelFrame(self.tab_reporte, text="Reporte Generado", style="Card.TFrame")
        frame_lista.pack(pady=10, padx=10, fill='both', expand=True)

        #Diseño de impresion de reportes
        columns = ("Categoría", "Tipo", "Alertas", "Total por Categoría", "Ahorro del Período")
        self.tree_reporte = ttk.Treeview(frame_lista, columns=columns, show='headings')
        for col in columns:
            self.tree_reporte.heading(col, text=col)
            self.tree_reporte.column(col, width=120, anchor="center")
        self.tree_reporte.pack(fill='both', expand=True, padx=5, pady=5)

    #Registro de categorias, recibe la informacion de los campos 
    #que se registren en la pestaña categoria
    def registrar_categoria(self):
        categoria = self.categoria_entry.get()
        tipo = self.tipo_combobox.get()
        lim_inf_str = self.lim_inf_entry.get()
        lim_sup_str = self.lim_sup_entry.get()

        if not categoria or not tipo or not lim_inf_str or not lim_sup_str:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
    
        try:
            lim_inf = int(lim_inf_str) if lim_inf_str else None
        except ValueError:
            messagebox.showerror("Error", "Ingrese correctamente eL intervalo 1")
            return

        try:
            lim_sup = int(lim_sup_str) if lim_sup_str else None
        except ValueError:
            messagebox.showerror("Error", "Ingrese correctamente intervalo 2")
            return
        
        if lim_sup < lim_inf:
            messagebox.showerror("Error", "El intervalo 2 es menor que el 1")
            return
        
        nueva_categoria = Catelim(categoria, tipo, lim_inf, lim_sup)
        Catelim.guardar_categorias(nueva_categoria) 
        
        messagebox.showinfo("Éxito", " Categoria registrada correctamente")

        #Se actualizara la lista con la nueva categoria que se haya dado en la pestaña ingegr y en la de busquedas
        self.actualizar_lista_categorias()
        categorias = [f"{cat.categoria} - {cat.descripcion}" if cat.descripcion is not None else cat.categoria for cat in Catelim.list_catelim]
        self.categoria_combobox.config(values=categorias)
        categorias = [cat.categoria for cat in Catelim.list_catelim]
        self.categoria_bus_combobox.config(values=categorias)
        #Limpia los campos donde el usuario dio los datos para el registro
        self.limpiar_campos_categorias()
    
    #Registro ingreso/egreso, recibe la informacion de los 
    #campos que se dieron en la pestaña ingegr
    def registrar_ingegr(self):
        seleccion = self.categoria_combobox.get()
        #Del combobox_categorias que se genera en la pestaña Categorias 
        #se toma solo la categoria sin la descripcion
        categoria = seleccion.split(" - ")[0]
        cantidad_str = self.cantidad_entry.get()
        
        if not categoria or not cantidad_str:
            messagebox.showerror("Error", "Ingrese TODOS LOS CAMPOS")
            return
        
        try:
            cantidad = int(cantidad_str) if cantidad_str else None
        except ValueError:
            messagebox.showerror("Error", "Ingrese correctamente la cantidad")
            return
        
        for aux in Catelim.list_catelim:
            if aux.categoria == categoria:
                tipo = aux.tipo

        registro = IngEgr(categoria, tipo, cantidad)
        mensaje_lim = IngEgr.registrar_ingegr(registro)
        mensaje_ahorro = Ahorro.calculos_ahorro(registro)

        #Arrojara las alertas de limite superado, exceso de gasto
        if mensaje_lim is not None:
            messagebox.showwarning("Precaucion", mensaje_lim)

        #Arrojara las alertas de Ahorro negativo y posible adeudo 
        if mensaje_ahorro is not None:
            messagebox.showwarning("Precaucion", mensaje_ahorro)
        
        messagebox.showinfo("Éxito", "El registro se ha hecho correctamente")
        #Guardara las modificaciones que se hicieron en ahorro
        Ahorro.guardar_ahorros()
        #Actualiza mi tabla de la pestaña donde se muestran Ingresos y Egresos del periodo
        self.actualizar_lista_ingegr()
        #Limpia los campos donde el usuario dio los datos para el registro
        self.limpiar_campos_ingegr()

        #Actualizara en la pestaña ingreso, la cantidad de ahorro del periodo con las modificaciones
        self.ahorro_actual_label.config(text=str(Ahorro.impr_ahorro(PERIODO_ACTUAL)))

        #Actualizara en la pestaña Ahorro, la cantidad de ahorro del periodo con las modificaciones
        self.ahorro_label.config(text=f"Importe ($): {Ahorro.impr_ahorro(PERIODO_ACTUAL)}")
    
    #Cuando el usuario haga el corte de mes, ahora podra hacer registro de los ingresos y egresos
    def corte_mes(self):
        global PERIODO_ACTUAL
        Ahorro.cierra_periodo(PERIODO_ACTUAL)
        temp_fecha = date(int(PERIODO_ACTUAL[0:4]), int((PERIODO_ACTUAL[4:6])),1)
        temp_fecha = temp_fecha + relativedelta(months=1)
        siguiente_periodo = str(temp_fecha.year * 100 + temp_fecha.month)

        aho1 = Ahorro(siguiente_periodo, 0)
        PERIODO_ANTERIOR = PERIODO_ACTUAL
        PERIODO_ACTUAL = siguiente_periodo
        Ahorro.inserta_aho(aho1)

        #Actualizara de la pestaña ahorro y ingegr, el ahorro visible
        #y la sugerencia de ahorro se volvera el ahorro que quedo en el perido en el que hizo el corte
        self.ahorro_per_label.config(text=f"Período: {PERIODO_ACTUAL}")
        self.ahorro_label.config(text=f"Importe ($): {Ahorro.impr_ahorro(PERIODO_ACTUAL)}")
        self.sugerencia_ahorro_label.config(text=str(Ahorro.impr_ahorro(PERIODO_ANTERIOR)))
        self.ahorro_actual_label.config(text=str(Ahorro.impr_ahorro(PERIODO_ACTUAL)))
        self.actualizar_lista_ingegr()
        
        messagebox.showinfo("Éxito", "Ha hecho el corte de mes")

    
    #Busqueda avanzada, recibe la informacion de los 
    #campos que se dieron en la pestaña busqueda
    def validar_busqueda(self):
        categoria = self.categoria_bus_combobox.get()or None
        tipo = self.tipo_bus_entry.get()or None
        cantidad1 = self.cantidad1_bus_entry.get()or None
        cantidad2 = self.cantidad2_bus_entry.get()or None
        fecha1 = self.fecha1_bus_entry.get()or None
        fecha2 = self.fecha2_bus_entry.get()or None

        if tipo is None:
            messagebox.showerror("Error", "Falta dar el tipo E/I")
            return


        if not any([categoria, cantidad1, cantidad2, fecha1, fecha2]):
            messagebox.showerror("Error", "Es necesario dar más parámetros de búsqueda")
            return

        if (cantidad1 is None) ^ (cantidad2 is None):
            messagebox.showerror("Error", "Falta otro intervalo de cantidad")
            return

        if (fecha1 is None) ^ (fecha2 is None):
            messagebox.showerror("Error", "Falta otro intervalo de fecha")
            return
        
        if cantidad1 is not None and cantidad2 is not None:
            try:
                cantidad1 = int(cantidad1) if cantidad1 else None
                cantidad2 = int(cantidad2) if cantidad2 else None
            except ValueError:
                messagebox.showerror("Error", "Ingrese correctamente intervalo 1")
                return
        
        if fecha1 is not None and fecha2 is not None:
            try:
                fecha1 = datetime.strptime(fecha1, "%Y-%m-%d").date()
                fecha2 = datetime.strptime(fecha2, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto usa YYYY-MM-DD.")
                return
            
        #Despues de pasar las validaciones llama a la 
        #funcion busqueda para hacer la impresion de Egresos o Ingresos segun sus parametros
        self.busqueda(categoria, tipo, cantidad1, cantidad2, fecha1, fecha2)      
    
    #De acuerdo a los paratemtros dados en la validacion se hara la busqueda en las lista IngEgr.list_ingegr
    #para imprimir los Ingresos o Egresos
    def busqueda(self, categoria = None, tipo = None, cantidad1 = None, cantidad2 = None, fecha1 = None, fecha2 = None):
        for item in self.tree_busqueda.get_children():
                self.tree_busqueda.delete(item)

        if categoria and tipo and not any([cantidad1, cantidad2, fecha1, fecha2]):
            for cat in IngEgr.list_ingegr:
                if cat.categoria == categoria and cat.tipo == tipo:
                    self.tree_busqueda.insert("", "end", values=(
                        cat.categoria,
                        "Egreso" if cat.tipo == "E" else "Ingreso",
                        cat.cantidad,
                        cat.fecha.isoformat(),
                        cat.periodo))
        elif cantidad1 is not None and cantidad2 is not None and tipo and not any([categoria, fecha1, fecha2]):
            for can in IngEgr.list_ingegr:
                if cantidad1 <= can.cantidad <= cantidad2 and can.tipo == tipo:
                    self.tree_busqueda.insert("", "end", values=(
                        can.categoria,
                        "Egreso" if can.tipo == "E" else "Ingreso",
                        can.cantidad,
                        can.fecha.isoformat(),
                        can.periodo))
        elif fecha1 and fecha2 and tipo and not any([categoria, cantidad1, cantidad2]):
            for fech in IngEgr.list_ingegr:
                if fecha1 <= fech.fecha <= fecha2 and fech.tipo == tipo:
                    self.tree_busqueda.insert("", "end", values=(
                        fech.categoria,
                        "Egreso" if fech.tipo == "E" else "Ingreso",
                        fech.cantidad,
                        fech.fecha.isoformat(),
                        fech.periodo))
                    

        if categoria and tipo:
            if cantidad1 is not None and cantidad2 is not None and fecha1 is None and fecha2 is None:
                for catcan in IngEgr.list_ingegr:
                    if (catcan.categoria == categoria) and (catcan.tipo == tipo) and (cantidad1 <= catcan.cantidad <= cantidad2):
                        self.tree_busqueda.insert("", "end", values=(
                        catcan.categoria,
                        "Egreso" if catcan.tipo == "E" else "Ingreso",
                        catcan.cantidad,
                        catcan.fecha.isoformat(),
                        catcan.periodo))
            elif fecha1 and fecha2 and cantidad1 is None and cantidad2 is None:
                for catfech in IngEgr.list_ingegr:
                    if (catfech.categoria == categoria) and (catfech.tipo == tipo) and (fecha1 <= catfech.fecha <= fecha2):
                        self.tree_busqueda.insert("", "end", values=(
                        catfech.categoria,
                        "Egreso" if catfech.tipo == "E" else "Ingreso",
                        catfech.cantidad,
                        catfech.fecha.isoformat(),
                        catfech.periodo))
            elif cantidad1 is not None and cantidad2 is not None and fecha1 and fecha2:
                for catcanfech in IngEgr.list_ingegr:
                    if (catcanfech.categoria == categoria) and (catcanfech.tipo == tipo) and (cantidad1 <= catcanfech.cantidad <= cantidad2) and (fecha1 <= catcanfech.fecha <= fecha2):
                        self.tree_busqueda.insert("", "end", values=(
                        catcanfech.categoria,
                        "Egreso" if catcanfech.tipo == "E" else "Ingreso",
                        catcanfech.cantidad,
                        catcanfech.fecha.isoformat(),
                        catcanfech.periodo))

        if cantidad1 is not None and cantidad2 is not None and fecha1 and fecha2 and tipo:
            for canfech in IngEgr.list_ingegr:
                if (cantidad1 <= canfech.cantidad <= cantidad2) and (canfech.tipo == tipo) and (fecha1 <= canfech.fecha <= fecha2):
                    self.tree_busqueda.insert("", "end", values=(
                        canfech.categoria,
                        "Egreso" if canfech.tipo == "E" else "Ingreso",
                        canfech.cantidad,
                        canfech.fecha.isoformat(),
                        canfech.periodo))
    
    #Recibira y hara la validacion del periodo dado en el campo de la pestaña reporte
    def generar_reporte(self):
        per = self.periodo_entry.get()
        
        if not per:
            messagebox.showerror("Error", "Ingresa el periodo")
            return
        
        self.reporte(per)
        #self.limpiar_campos_reporte()

    #De acuerdo a periodo dado en generar_reporte hara la suma de gastos de acuerdo a su categoria
    #Guardar las alertas si es que hubo en el periodo
    #Mostrara el ahorro del periodo
    def reporte(self, periodo):
        alerta_ahorro = 0
        suma_toting = 0
        suma_totegr = 0
        suma_porcategoria = {}
        alertas_por_categoria = {}
        tipo_por_categoria = {}
    
        for aux in IngEgr.list_ingegr:
            if aux.periodo == periodo:
                if aux.tipo == "E":
                    suma_totegr += aux.cantidad

        for aux in Ahorro.list_ahorro:
            if aux.periodo == periodo:
                suma_toting = aux.cantidad
                alerta_ahorro = aux.alerta
        
        for aux in IngEgr.list_ingegr:
            if aux.periodo == periodo and aux.categoria in suma_porcategoria:
                suma_porcategoria[aux.categoria] += aux.cantidad
            elif aux.periodo == periodo:
                suma_porcategoria[aux.categoria] = aux.cantidad

            if aux.tipo is not None:
                tipo_por_categoria[aux.categoria] = aux.tipo

            if aux.alerta is not None:
                alertas_por_categoria[aux.categoria] = aux.alerta

        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)

        for categoria, suma in suma_porcategoria.items():
            tipo = tipo_por_categoria.get (categoria, "")
            alerta = alertas_por_categoria.get(categoria, "")
            self.tree_reporte.insert("", "end", values=(
                                        categoria,
                                        "Egreso" if tipo == "E" else "Ingreso",
                                        alerta,
                                        suma,
                                    ))
        self.tree_reporte.insert("", "end", values=(
                                        "AHORRO DEL PERIODO",
                                        "",
                                        alerta_ahorro,
                                        suma_toting,
                                        suma_toting
                                    ))

    #Actualizara la informacion en la tabla de la pestaña categorias
    def actualizar_lista_categorias(self):
        for item in self.tree_categoria.get_children():
            self.tree_categoria.delete(item)
        for data in Catelim.list_catelim:
            self.tree_categoria.insert("", "end", values=(
                data.categoria,  
                "Egreso" if data.tipo == "E" else "Ingreso", 
                data.lim_inf,
                data.lim_sup,
                data.descripcion
            ))
    
    #Actualizara la informacion en la tabla de la pestaña ingegr
    def actualizar_lista_ingegr(self):
        for item in self.tree_ingegr.get_children():
            self.tree_ingegr.delete(item)
        for data in IngEgr.list_ingegr:
            if data.periodo == PERIODO_ACTUAL:
                self.tree_ingegr.insert("", "end", values=(
                    data.categoria, 
                    "Egreso" if data.tipo == "E" else "Ingreso", 
                    data.cantidad,
                    data.fecha.strftime("%Y-%m-%d"),
                    data.periodo,
                    data.alerta
                ))

    # Limpia mis campos de entrada de la pestaña categoria
    def limpiar_campos_categorias(self):
        self.categoria_entry.delete(0, 'end')
        self.tipo_combobox.set('')
        self.lim_inf_entry.delete(0, 'end')
        self.lim_sup_entry.delete(0, 'end')
    
    # Limpia mis campos de entrada de la pestaña ingegr
    def limpiar_campos_ingegr(self):
        self.categoria_bus_combobox.set('')
        self.cantidad_entry.delete(0, 'end')

if __name__ == "__main__":
    ventanainicio()
