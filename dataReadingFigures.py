import csv
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Función para parsear las posiciones de las ovejas
def parse_positions(data):
    positions = re.findall(r'(\d\s*\d\s*\d\s*a\s*h)\s*:\s*\(\s*([-.\d\s]+)\s*;\s*([-.\d\s]+)\s*\)', data)
    return [(ov[0].replace(' ', ''), round(float(ov[1].replace(' ', '')), 2), round(float(ov[2].replace(' ', '')), 2)) for ov in positions]

def readAndFigures():
    try:
        # Crear una carpeta para guardar las imágenes
        folder_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(folder_name, exist_ok=True)

        # Inicializar diccionario para las posiciones de las ovejas
        sheep_positions = defaultdict(lambda: {'x': [], 'y': []})

        # Leer el archivo CSV
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # El primer campo es la fecha y hora, el resto contiene información de las ovejas
                timestamp = row[0]
                sheep_data = ' '.join(row[1:]).replace('"', '').replace(':', ' : ')
                
                # Parsear posiciones de las ovejas
                parsed_data = parse_positions(sheep_data)
                
                # Guardar posiciones en arreglos separados
                for sheep_id, x, y in parsed_data:
                    sheep_positions[sheep_id]['x'].append(x)
                    sheep_positions[sheep_id]['y'].append(y)

        # Graficar las curvas de las ovejas
        for sheep_id, positions in sheep_positions.items():
            # Crear un nuevo plot para cada oveja
            plt.figure()
            plt.plot(positions['x'], positions['y'])
            plt.plot(positions['x'][0], positions['y'][0], 'ro')  # Círculo azul en el punto inicial
            plt.plot(positions['x'][-1], positions['y'][-1], 'ro', fillstyle='none')  # Círculo rojo vacío en el punto final

            # Añadir etiquetas y título
            plt.xlabel('X axis')
            plt.ylabel('Y axis')
            plt.title(f'Sheep {sheep_id} tracking')

            # Guardar la imagen en un archivo PNG en la carpeta
            plt.savefig(os.path.join(folder_name, f'sheep_{sheep_id}.png'))
            plt.close()

        # Mostrar el gráfico con todas las ovejas
        plt.figure(figsize=(10, 6))  # Ajustar el tamaño de la figura
        for sheep_id, positions in sheep_positions.items():
            plt.plot(positions['x'], positions['y'], label=f'Sheep {sheep_id}')
            plt.plot(positions['x'][0], positions['y'][0], 'ro')  # Círculo azul en el punto inicial
            plt.plot(positions['x'][-1], positions['y'][-1], 'ro', fillstyle='none')  # Círculo rojo vacío en el punto final

        # Añadir etiquetas y leyenda
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.title('Sheep Tracking')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        # Guardar la imagen con todas las ovejas en un archivo PNG en la carpeta
        plt.savefig(os.path.join(folder_name, 'all_sheeps.png'), bbox_inches='tight')
        plt.close()

        # Mostrar el gráfico con todas las ovejas
        print("Successful image generation")
        #plt.show()
    except Exception as e:
        print("There was an issue while generating tracking images:")
        print(e)
