from main import MODLES, BOB, generate_model_after
from core_vars import WHITE, SPLIT_PERCENT

class Object:
    # Initialize vertices, edges, and faces
    def __init__(self, froms, shape, type, image=None, scale=1):
        self.name = type
        self.vars_to_null
        print("intializing object: " + shape)
        if self.name[:3] == "ob:":
            self.vertices = froms[shape]["vertices"]
            self.edges = froms[shape]["edges"]
            self.faces = froms[shape]["faces"]
            self.pivot = froms[shape]["pivot"]
            self.scale(scale)
        elif self.name[:3] == "im:":
            #(x,y, z)
            #y is up and down
            self.vertices = [
                (0, 0, 0),
                (1, 0, 0),
                (1, -1, 0),
                (0, -1, 0)
            ]
            self.edges = []
            self.faces = [
                ((0, 1, 2, 3), (255, 255, 255), (image, ("all"))),
            ]
            self.image = image
            self.pivot = (0, 0, 0)
            self.scale(scale)
        else:
            print(f"{self.name} is not a valid object name")
            
    def __str__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

    def __repr__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

    def vars_to_null(self):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.pivot = (0, 0, 0)
        self.bounding_box = []
    
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
            vertices_indices = face[0]
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
        """
        So ummm this function does spit it but it renders the same amount of faces
        but it could be because the normal_render is on in main_functions_math.py
        """
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
        #print(f"Each bounding box is: ")
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
        print(f"Updated object: {self.name}")
    
    def intersects_ray(self, ray_origin, ray_direction, legnth):
        for _, bounding_box in self.split_objects_each_faces:
            (min_x, max_x), (min_y, max_y), (min_z, max_z) = bounding_box
            ray_x, ray_y, ray_z = ray_origin
            ray_rot_x, _, ray_rot_z = ray_direction
            for i in range(0, legnth, .1):
                if ray_rot_x >= 0:
                    ray_x += i * ray_rot_x
                else:
                    ray_x -= i * abs(ray_rot_x)
                if ray_rot_z >= 0:
                    ray_z += i * ray_rot_z
                else:
                    ray_z -= i * abs(ray_rot_z)
                if (min_x <= ray_x <= max_x and
                    min_y <= ray_y <= max_y and
                    min_z <= ray_z <= max_z):
                    return True
        return False
    
    def color_change(self, color):
        for i in range(len(self.faces)):
            self.faces[i] = (self.faces[i][0], color)
        self.update_bounding_boxs()
        print(f"Changed color of {self.name} to {color}")
    
threeDModles = {
    'square': {
        'type': 'ob:player',
        'object_class': Object(MODLES, 'square', "ob:player", None, 10),
        'render': True,
        'move': False,
        'collision': False,
        'start_pos': (0, 0, 0),
        'scale': 10,
        'general_color': WHITE
    },
    'bulbasaur': {
        'type': 'ob:player',
        'object_class': Object(MODLES, 'bulbasaur', 'ob:player'),
        'render': False,
        'move': False,
        'collision': False,
        'start_pos': (-5, 0, 0),
        'scale': 1,
        'general_color': WHITE
    },
    'octahedron': {
        'type': 'ob:player',
        'object_class': Object(MODLES, 'octahedron', 'ob:player'),
        'render': False,
        'move': False,
        'collision': False,
        'start_pos': (3, 0, 0),
        'scale': 1,
        'general_color': WHITE
    },
    'mountains': {
        'type': 'ob:terrain',
        'object_class': Object(BOB, 'mount', 'ob:terrain'),
        'render': False,
        'move': True,
        'collision': False,
        'start_pos': (-79, -6, 0),
        'scale': 1,
        'general_color': WHITE
    },
    'mountains2': {
        'type': 'ob:terrain',
        'object_class': Object(BOB, 'mount', 'ob:terrain'),
        'render': False,
        'move': True,
        'collision': False,
        'start_pos': (80, -6, 0),
        'scale': 1,
        'general_color': WHITE
    },
    'gen_modle': {
        'type': 'ob:terrain',
        'object_class': Object(generate_model_after, 'hills', 'ob:terrain'),
        'render': False,
        'move': True,
        'collision': True,
        'start_pos': (0, -2, -150),
        'scale': 1,
        'general_color': WHITE
    },
    'try_image': {
        'type': 'im:player',
        'object_class': Object("man.jpg", 'try_image', 'im:player', "man.jpg"),
        'render': True,
        'move': True,
        'collision': False,
        'start_pos': (0, 0, 0),
        'scale': 1,
        'general_color': WHITE
    },
}

import quick_import
print("Importing uncompressed modles.... (Might take a while)")
quick_import.what_file_type()
for new_object in quick_import.QUICK_IMPORT_DATA:
    threeDModles[new_object] = {
        'type': 'player',
        'object_class': Object(quick_import.QUICK_IMPORT_DATA, new_object),
        'render': True,
        'move': True,
        'collision': True,
        'start_pos': (0, 0, 0),
        'scale': 1,
        'general_color': WHITE
    }
print("DONE!")

print(f"The names of each object are: {threeDModles.keys()}")

for key, value in threeDModles.items():
    if value['type'][:3] == "ob:":
        obj = value['object_class']
        start_pos = value['start_pos']
        updated_vertices = [(v[0] + start_pos[0], v[1] + start_pos[1], v[2] + start_pos[2]) for v in obj.vertices]
        obj.update_object(updated_vertices, obj.edges, obj.faces, obj.pivot)
    elif value['type'][:3] == "im:":
        print()
    else:
        print(f"{value['type']} is not a valid object type")
