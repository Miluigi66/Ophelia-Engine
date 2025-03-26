import total_modles
from main import os 
from main import np

QUICK_IMPORT_DATA = {}


def what_file_type():
    for imported_file in os.listdir(total_modles.__path__[0]):
        if imported_file.endswith(".stl"):
            import stl
            # Load the STL file
            mesh_data = stl.mesh.Mesh.from_file(imported_file)
            
            # Extract vertices and faces
            vertices = mesh_data.vectors.reshape((-1, 3))
            faces = np.arange(len(vertices)).reshape((-1, 3))
            
            general_data_final(vertices, faces, imported_file) 
        elif imported_file.endswith(".obj"):
            with open(imported_file, 'r') as file:
                for line in file:
                    if line.startswith('v '):
                        parts = line.strip().split()
                        vertex = tuple(map(float, parts[1:4]))
                        vertices.append(vertex)
                    elif line.startswith('f '):
                        parts = line.strip().split()
                        face = tuple(int(idx.split('/')[0]) - 1 for idx in parts[1:5])
                        faces.append((face, (255, 255, 255)))  # Default color white
            general_data_final(vertices, faces, imported_file)
        else:
            print("The file type is not supported")

def general_data_final(vertices, faces, imported_file):
    imported_file = {
        "vertices": vertices.tolist(),
        "pivot": (0, 0, 0),
        "edges": [],
        "faces": [
            (face.tolist(), (255, 0, 0)) for face in faces
        ]
    }
    QUICK_IMPORT_DATA.append(imported_file)
    
