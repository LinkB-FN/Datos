import matplotlib.pyplot as plt
import os
from datetime import datetime
import networkx as nx
import tkinter as tk
from tkinter import ttk

# Paleta de colores por rango
COLORES_POR_RANGO = {
    "0-9": "#FF9999",
    "10-19": "#FFCC99",
    "20-29": "#FFFF99",
    "30-39": "#CCFF99",
    "40-49": "#99FFCC",
    "50-59": "#99FFFF",
    "60-69": "#99CCFF",
    "70-79": "#9999FF",
    "80-89": "#CC99FF",
    "90-99": "#FF99CC"
}

def agrupar_similitudes(similitudes):
    rangos = {f"{i}-{i+9}": [] for i in range(0, 100, 10)}
    for doc1, doc2, sim in similitudes:
        porcentaje = sim * 100
        for rango in rangos.keys():
            inicio, fin = map(int, rango.split('-'))
            if inicio <= porcentaje < fin:
                rangos[rango].append((doc1, doc2, porcentaje))
                break
    return rangos

def mostrar_tabla(documentos):
    ventana = tk.Tk()
    ventana.title("Documentos Comparados")
    ventana.geometry("700x400")

    # Filtros
    frame_filtros = tk.Frame(ventana)
    frame_filtros.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_filtros, text="Buscar documento:").pack(side="left")
    entrada_busqueda = tk.Entry(frame_filtros)
    entrada_busqueda.pack(side="left", padx=5)

    tk.Label(frame_filtros, text="Similitud mínima (%):").pack(side="left")
    entrada_similitud = tk.Entry(frame_filtros, width=5)
    entrada_similitud.insert(0, "0")
    entrada_similitud.pack(side="left", padx=5)

    # Tabla
    tabla = ttk.Treeview(ventana, columns=("doc1", "doc2", "sim"), show="headings")
    tabla.heading("doc1", text="Documento 1")
    tabla.heading("doc2", text="Documento 2")
    tabla.heading("sim", text="Similitud (%)")
    tabla.pack(expand=True, fill="both")

    def aplicar_filtro():
        filtro_doc = entrada_busqueda.get().lower()
        try:
            filtro_sim = float(entrada_similitud.get())
        except ValueError:
            filtro_sim = 0

        for row in tabla.get_children():
            tabla.delete(row)

        for doc1, doc2, sim in documentos:
            if filtro_doc in doc1.lower() or filtro_doc in doc2.lower():
                if sim >= filtro_sim:
                    tabla.insert("", "end", values=(doc1, doc2, f"{sim:.2f}"))

    boton_filtrar = tk.Button(frame_filtros, text="Filtrar", command=aplicar_filtro)
    boton_filtrar.pack(side="left", padx=10)

    aplicar_filtro()
    ventana.mainloop()

def seleccionar_visualizacion(rangos_disponibles):
    root = tk.Tk()
    root.title("Opciones de visualización")
    
    # Frame para selección de visualización
    frame_vis = tk.Frame(root)
    frame_vis.pack(pady=10)
    
    tk.Label(frame_vis, text="Tipo de visualización:").pack()
    tipo_vis = tk.StringVar(value='heatmap')
    tk.Radiobutton(frame_vis, text="Mapa de calor", variable=tipo_vis, value='heatmap').pack(anchor='w')
    tk.Radiobutton(frame_vis, text="Grafo", variable=tipo_vis, value='grafo').pack(anchor='w')

    # Frame para selección de rangos
    frame_rangos = tk.Frame(root)
    frame_rangos.pack(pady=10)
    
    tk.Label(frame_rangos, text="Seleccionar rangos de similitud:").pack()
    vars_rangos = []
    for rango in rangos_disponibles:
        var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(frame_rangos, text=rango, variable=var)
        chk.pack(anchor='w')
        vars_rangos.append(var)

    # Frame para límite de documentos
    frame_limite = tk.Frame(root)
    frame_limite.pack(pady=10)
    
    tk.Label(frame_limite, text="Límite de documentos (0=todos):").pack()
    limite_docs = tk.IntVar(value=0)
    tk.Entry(frame_limite, textvariable=limite_docs, width=5).pack()

    def aceptar():
        root.resultado = {
            'tipo': tipo_vis.get(),
            'rangos': [r for i, r in enumerate(rangos_disponibles) if vars_rangos[i].get()],
            'limite': limite_docs.get()
        }
        root.destroy()

    tk.Button(root, text="Generar visualización", command=aceptar).pack(pady=10)
    root.mainloop()
    return getattr(root, 'resultado', None)

def generar_grafo(similitudes):
    rangos = agrupar_similitudes(similitudes)
    rangos_disponibles = [r for r, docs in rangos.items() if docs]
    if not rangos_disponibles:
        print("No hay documentos suficientes para graficar.")
        return

    opciones = seleccionar_visualizacion(rangos_disponibles)
    if not opciones:
        return

    # Filtrar similitudes por rangos seleccionados
    similitudes_filtradas = []
    for doc1, doc2, sim in similitudes:
        porcentaje = sim * 100
        for rango in opciones['rangos']:
            inicio, fin = map(int, rango.split('-'))
            if inicio <= porcentaje < fin:
                similitudes_filtradas.append((doc1, doc2, sim))
                break

    # Aplicar límite de documentos si se especificó
    if opciones['limite'] > 0:
        documentos = sorted(list({doc for pair in similitudes_filtradas for doc in pair[:2]}))
        if len(documentos) > opciones['limite']:
            documentos = documentos[:opciones['limite']]
            similitudes_filtradas = [pair for pair in similitudes_filtradas 
                                   if pair[0] in documentos and pair[1] in documentos]

    if opciones['tipo'] == 'heatmap':
        # Crear matriz de similitud
        documentos = sorted(list({doc for pair in similitudes for doc in pair[:2]}))
        matriz = [[0]*len(documentos) for _ in range(len(documentos))]
        
        doc_index = {doc: i for i, doc in enumerate(documentos)}
        for doc1, doc2, sim in similitudes:
            i, j = doc_index[doc1], doc_index[doc2]
            matriz[i][j] = matriz[j][i] = sim * 100  # Convertir a porcentaje

        # Crear heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        cax = ax.matshow(matriz, cmap='YlOrRd', vmin=0, vmax=100)
        
        # Configurar ejes
        ax.set_xticks(range(len(documentos)))
        ax.set_yticks(range(len(documentos)))
        ax.set_xticklabels(documentos, rotation=90)
        ax.set_yticklabels(documentos)
        
        # Añadir barra de color
        fig.colorbar(cax, label='Porcentaje de similitud')
        
        # Añadir valores en las celdas
        for i in range(len(documentos)):
            for j in range(len(documentos)):
                if matriz[i][j] > 0:
                    ax.text(j, i, f'{matriz[i][j]:.0f}%', ha='center', va='center', color='black')

        plt.title('Mapa de calor de similitud entre documentos')
        plt.tight_layout()

    else:  # Grafo original
        rangos = agrupar_similitudes(similitudes)
        rangos_disponibles = [r for r, docs in rangos.items() if docs]
        if not rangos_disponibles:
            print("No hay documentos suficientes para graficar.")
            return

        rangos_seleccionados = seleccionar_rangos_disponibles(rangos_disponibles)
        G = nx.Graph()

        for rango in rangos_seleccionados:
            docs = rangos[rango]
            if docs:
                G.add_node(rango, size=len(docs), docs=docs)

        pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42)
        sizes = [G.nodes[n]['size'] * 150 for n in G.nodes]
        colors = [COLORES_POR_RANGO.get(n, '#cccccc') for n in G.nodes]

        fig, ax = plt.subplots(figsize=(12, 8))
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color=colors, alpha=0.8)
        nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, alpha=0.5)
        labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold', font_family='sans-serif')

        def on_click(event):
            if event.inaxes == ax:
                x, y = event.xdata, event.ydata
                for node, (nx_pos, ny_pos) in pos.items():
                    dx, dy = x - nx_pos, y - ny_pos
                    dist = (dx**2 + dy**2)**0.5
                    if dist < 0.05:
                        mostrar_tabla(G.nodes[node]['docs'])
                        break

        fig.canvas.mpl_connect('button_press_event', on_click)
        ax.set_title("Similitud de documentos agrupados por porcentaje")
        plt.axis('off')

    # Guardar y mostrar
    os.makedirs('resultados/graficos', exist_ok=True)
    tipo_nombre = opciones['tipo']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/{tipo_nombre}_similitudes_{timestamp}.png'

    plt.savefig(filename)
    plt.show()
