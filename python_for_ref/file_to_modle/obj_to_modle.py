def parse_obj_file(file_path, model_name):
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = tuple(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('f '):
                parts = line.strip().split()
                face = tuple(int(idx.split('/')[0]) - 1 for idx in parts[1:5])
                faces.append((face, (255, 255, 255)))  # Default color white

    model_dict = {
        model_name: {
            "vertices": vertices,
            "edges": [],
            "pivot": (0, 0, 0),
            "faces": faces
        }
    }

    return model_dict

# Example usage:
file_path = 'terrain.obj'
model_name = 'ter'
model_dict = parse_obj_file(file_path, model_name)

file = open('really_custom_model.py', 'a')
file.write(str(model_dict))