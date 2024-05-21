import csv
import re
from collections import defaultdict

# Función para parsear las posiciones de las ovejas
def parse_positions(data):
    positions = re.findall(r'(\d\s*\d\s*\d\s*a\s*h)\s*:\s*\(\s*([-.\d\s]+)\s*;\s*([-.\d\s]+)\s*\)', data)
    return [(ov[0].replace(' ', ''), round(float(ov[1].replace(' ', '')), 2), round(float(ov[2].replace(' ', '')), 2)) for ov in positions]

if __name__ == '__main__':
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

    # Mostrar los datos almacenados
    for sheep_id, positions in sheep_positions.items():
        print(f"Oveja {sheep_id}:")
        print(f"  x: {positions['x']}")
        print(f"  y: {positions['y']}")


