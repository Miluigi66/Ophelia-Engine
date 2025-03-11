from main import MODLES, BOB, generate_model_after
# % of object to split
split_whole_value = .1
SPLIT_PERCENT = split_whole_value / 100
class Object:
    # Initialize vertices, edges, and faces
    def __init__(self, froms, shape, scale=1):
        self.name = shape
        print("intializing object: " + shape)
        self.vertices = froms[shape]["vertices"]
        self.edges = froms[shape]["edges"]
        self.faces = froms[shape]["faces"]
        self.pivot = froms[shape]["pivot"]
        self.scale(scale)

    def __str__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

    def __repr__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

    def update_bounding_boxs(self):
        self.get_bounding_box()
        self.split_objects_each_faces = list(self.split_object_each_face())
        self.split_objects_smaller_percent = list(self.split_object_smaller_percent())
        
    def get_bounding_box(self):
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)
        min_z = min(v[2] for v in self.vertices)
        max_z = max(v[2] for v in self.vertices)
        self.bounding_box = (min_x, max_x), (min_y, max_y), (min_z, max_z)
        return self.bounding_box
    
    def split_object_each_face(self):
        split_objects_each_faces = []
        for face in self.faces:
            vertices_indices, color = face
            vertices = [self.vertices[i] for i in vertices_indices]
            min_x = min(v[0] for v in vertices)
            max_x = max(v[0] for v in vertices)
            min_y = min(v[1] for v in vertices)
            max_y = max(v[1] for v in vertices)
            min_z = min(v[2] for v in vertices)
            max_z = max(v[2] for v in vertices)
            bounding_box = (min_x, max_x), (min_y, max_y), (min_z, max_z)
            yield vertices, bounding_box
            split_objects_each_faces.append((vertices, bounding_box))
        return split_objects_each_faces
    
    # does this work???
    def split_object_smaller_percent(self):
        split_objects_each_faces = []
        num_faces = len(self.faces)
        split_count = int(num_faces * SPLIT_PERCENT)
        print(f"Splitting {self.name} into {split_count} smaller objects")
        for big_face in range(split_count):
            vertices_indices, color = self.faces[big_face]
            vertices = [self.vertices[i] for i in vertices_indices]
            min_x = min(v[0] for v in vertices)
            max_x = max(v[0] for v in vertices)
            min_y = min(v[1] for v in vertices)
            max_y = max(v[1] for v in vertices)
            min_z = min(v[2] for v in vertices)
            max_z = max(v[2] for v in vertices)
            bounding_box = (min_x, max_x), (min_y, max_y), (min_z, max_z)
            yield vertices, bounding_box
            split_objects_each_faces.append((vertices, bounding_box))
        print(f"Each bounding box is: ")
        for vertices, bounding_box in split_objects_each_faces:
            print(f"{bounding_box}")
        return split_objects_each_faces
        
    def scale(self, scale):
        for i in range(len(self.vertices)):
            self.vertices[i] = (self.vertices[i][0] * scale, self.vertices[i][1] * scale, self.vertices[i][2] * scale)
        self.update_bounding_boxs()
        
    def update_object(self, vertices, edges, faces, pivot):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.pivot = pivot
        self.update_bounding_boxs()
    
# Dictionary of objects
DICT = {
    'square': {
        'type': 'player',
        'object_class': Object(MODLES, 'square'),
        'render': False,
        'move': False,
        'collision': True,
        'start_pos': (0, 0, 0),
        'scale': 1
    },
    'bulbasaur': {
        'type': 'player',
        'object_class': Object(MODLES, 'bulbasaur'),
        'render': False,
        'move': False,
        'collision': False,
        'start_pos': (-5, 0, 0),
        'scale': 1
    },
    'octahedron': {
        'type': 'player',
        'object_class': Object(MODLES, 'octahedron'),
        'render': False,
        'move': False,
        'collision': False,
        'start_pos': (3, 0, 0),
        'scale': 1
    },
    'mountains': {
        'type': 'terrain',
        'object_class': Object(BOB, 'mount'),
        'render': True,
        'move': True,
        'collision': False,
        'start_pos': (-79, -6, 0),
        'scale': 1
    },
    'mountains2': {
        'type': 'terrain',
        'object_class': Object(BOB, 'mount'),
        'render': True,
        'move': True,
        'collision': False,
        'start_pos': (80, -6, 0),
        'scale': 1
    },
    'gen_modle': {
        'type': 'terrain',
        'object_class': Object(generate_model_after, 'hills'),
        'render': True,
        'move': True,
        'collision': True,
        'start_pos': (0, -2, -150),
        'scale': 1
    },
}

for key, value in DICT.items():
    obj = value['object_class']
    start_pos = value['start_pos']
    updated_vertices = [(v[0] + start_pos[0], v[1] + start_pos[1], v[2] + start_pos[2]) for v in obj.vertices]
    obj.update_object(updated_vertices, obj.edges, obj.faces, obj.pivot)
