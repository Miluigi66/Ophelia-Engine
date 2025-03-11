import pygame
import sys
import math
import pygame.gfxdraw
import numpy as np #MAKES IT SLOWER!!!
import time
import cProfile


# models
print("Importing models.... (Might take a while)")
from total_modles.model import MODLES
from total_modles.custom_model import BOB
from total_modles.random_gen import generate_model_after
print("DONE!")
# models

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
fullscreen = False
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("3D Rendering Engine")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Darkening effect higher value = less darkening
DARKENING_FACTOR = 60
# Rendering distance
RENDER_DISTANCE_FAR = DARKENING_FACTOR
RENDER_DISTANCE_BEHIND = 0
RENDER_DISTANCE_RIGHT = 50
RENDER_DISTANCE_LEFT = -RENDER_DISTANCE_RIGHT

# % of object to split
split_whole_value = .1
SPLIT_PERCENT = split_whole_value / 100
class Object:
    # Initialize vertices, edges, and faces
    def __init__(self, froms, shape):
        self.name = shape
        print("intializing object: " + shape)
        self.vertices = froms[shape]["vertices"]
        self.edges = froms[shape]["edges"]
        self.faces = froms[shape]["faces"]
        self.pivot = froms[shape]["pivot"]
        self.get_bounding_box()
        self.split_objects_each_faces = list(self.split_object_each_face())
        self.split_objects_smaller_percent = list(self.split_object_smaller_percent())

        
    def __str__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

    def __repr__(self):
        return f"Object({self.vertices}, {self.edges}, {self.faces}, {self.pivot})"

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
        self.get_bounding_box()
        
    def update_object(self, vertices, edges, faces, pivot):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.pivot = pivot
    
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

# So this works like how I want the spliting objects into smnaller objects works but mayby to fix the other thing maybe take legnth and with then split the object into smaller objects based on that
"""DICT = {}
# Additional objects using a loop
for i in range(1, 6):
    DICT[f'gen_modle_{i}'] = {
        'type': 'terrain',
        'object_class': Object(generate_model_after, 'hills'),
        'render': True,
        'move': True,
        'collision': True,
        'start_pos': (0, -2, -150 + i * 50),
        'scale': 1
    }
"""


class Cam:
    def __init__(self, pos):
        self.pos = list(pos)
        self.rot = [0, 0]
        self.hitbox = (-1, 1), (-1, 1), (-1, 1)
    
        
    def mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200
            y /= 200
            self.rot[0] -= y
            self.rot[1] += x
        if event.type == pygame.MOUSEBUTTONDOWN:
            None
        if event.type == pygame.MOUSEBUTTONUP:
            None
            
    def update(self, key):
        if key[pygame.K_LSHIFT]:
            s = .5
        else:
            s = .1
        # Camera movement z
        if key[pygame.K_c]:
            self.pos[1] -= s
        if key[pygame.K_SPACE]:
            self.pos[1] += s
        
        # Camera rotation
        if key[pygame.K_UP]:
            self.rot[0] += 0.1
        if key[pygame.K_DOWN]:
            self.rot[0] -= 0.1
        if key[pygame.K_LEFT]:
            self.rot[1] -= 0.1
        if key[pygame.K_RIGHT]:
            self.rot[1] += 0.1
        
        x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])

        # Checks to see if the camera is within the bounds of rotation 
        if self.rot[0] <= -1.58:
            self.rot[0] = -1.58

        if self.rot[0] >= 1.58:
            self.rot[0] = 1.58

        # Camera movement x, y
        if key[pygame.K_w]:
            self.pos[0] += x
            self.pos[2] += y
        if key[pygame.K_s]:
            self.pos[0] -= x
            self.pos[2] -= y
        if key[pygame.K_a]:
            self.pos[0] -= y
            self.pos[2] += x
        if key[pygame.K_d]:
            self.pos[0] += y
            self.pos[2] -= x
        

        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()  # Quits Game
        if key[pygame.K_f]:
            global fullscreen
            if not fullscreen:
                pygame.display.quit
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                fullscreen = True
            else:
                pygame.display.quit
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                fullscreen = False
        if key[pygame.K_p]:
            for obj_name, obj in DICT.items():
                print(f"{obj_name} split_objects_each_faces: {len(obj['object_class'].split_objects_each_faces)}")
                print(f"{obj_name} split_objects_smaller_percent: {len(obj['object_class'].split_objects_smaller_percent)}")
        if key[pygame.K_o]:
            tp_x = int(input("Enter x: "))
            tp_y = int(input("Enter y: "))
            tp_z = int(input("Enter z: "))
            self.pos = [tp_x, tp_y, tp_z]
            
    def check_collision_with_camera(self, obj):
        (min_x1, max_x1), (min_y1, max_y1), (min_z1, max_z1) = self.hitbox
        (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = obj.get_bounding_box()
        if (min_x1 <= max_x2 and max_x1 >= min_x2 and \
            min_y1 <= max_y2 and max_y1 >= min_y2 and \
            min_z1 <= max_z2 and max_z1 >= min_z2):
            print("Collision detected")
    
        

    def transform(self, vertices):
        transformed_vertices = []
        cos_y, sin_y = math.cos(self.rot[1]), math.sin(self.rot[1])
        cos_x, sin_x = math.cos(self.rot[0]), math.sin(self.rot[0])
        for x, y, z in vertices:
            x -= self.pos[0]
            y -= self.pos[1]
            z -= self.pos[2]

            # Rotate around y-axis
            x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y

            # Rotate around x-axis
            y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

            transformed_vertices.append((x, y, z))
        return transformed_vertices

def project(x, y, z, scale, distance, aspect_ratio):
    factor = scale / (distance + z)
    x = x * factor * aspect_ratio + WIDTH // 2
    y = -y * factor + HEIGHT // 2
    return int(x), int(y)


def calculate_position(obj_class, angle_x, angle_y, angle_z, pos_x, pos_y, pos_z,):
    cos_angle_x = math.cos(angle_x)
    sin_angle_x = math.sin(angle_x)
    cos_angle_y = math.cos(angle_y)
    sin_angle_y = math.sin(angle_y)
    cos_angle_z = math.cos(angle_z)
    sin_angle_z = math.sin(angle_z)

    transformed_vertices = []
    for x, y, z in obj_class.vertices:
        # Translate to pivot
        x -= obj_class.pivot[0]
        y -= obj_class.pivot[1]
        z -= obj_class.pivot[2]
        
        # Rotate around x-axis
        y, z = y * cos_angle_x - z * sin_angle_x, z * cos_angle_x + y * sin_angle_x
        # Rotate around y-axis
        x, z = x * cos_angle_y - z * sin_angle_y, z * cos_angle_y + x * sin_angle_y
        # Rotate around z-axis
        x, y = x * cos_angle_z - y * sin_angle_z, y * cos_angle_z + x * sin_angle_z
        
        # Apply position offsets
        x += obj_class.pivot[0] + pos_x
        y += obj_class.pivot[1] + pos_y
        z += obj_class.pivot[2] + pos_z
        
        # Update pivot's position
        pivot = (obj_class.pivot[0] + pos_x, obj_class.pivot[1] + pos_y, obj_class.pivot[2] + pos_z)
            
        transformed_vertices.append((x, y, z))
    
    obj_class.update_object(transformed_vertices, obj_class.edges, obj_class.faces, pivot)
    
    return transformed_vertices

def sort_high_to_low(all_vertices, all_faces):
    sorted_faces = []
    for face in all_faces:
        vertices_indices = face[0]
        depths = [all_vertices[index][2] for index in vertices_indices]
        avg_depth = sum(depths) / len(vertices_indices)

        if RENDER_DISTANCE_BEHIND < min(depths) < RENDER_DISTANCE_FAR and \
           RENDER_DISTANCE_BEHIND < max(depths) < RENDER_DISTANCE_FAR and \
           RENDER_DISTANCE_LEFT < all_vertices[vertices_indices[0]][0] < RENDER_DISTANCE_RIGHT:
            sorted_faces.append((avg_depth, face))

    sorted_faces.sort(reverse=True, key=lambda x: x[0])
    return sorted_faces


def check_collision(obj1, obj2):
    (min_x1, max_x1), (min_y1, max_y1), (min_z1, max_z1) = obj1.get_bounding_box()
    (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = obj2.get_bounding_box()

    return (min_x1 <= max_x2 and max_x1 >= min_x2 and
            min_y1 <= max_y2 and max_y1 >= min_y2 and
            min_z1 <= max_z2 and max_z1 >= min_z2)

def texturing(screen, darkened_color, points):
    pygame.gfxdraw.filled_polygon(screen, points, darkened_color)
    
    
    # draws the bounding boxes
    
    # Weird half arks
    #pygame.gfxdraw.bezier(screen, points, 2, darkened_color)
    # Connect the dots 
    #pygame.gfxdraw.circle(screen, points[0][0], points[0][1], 2, WHITE)
    # Black outline
    #pygame.gfxdraw.aapolygon(screen, points, (0, 0, 0))
    # Color outling
    #pygame.gfxdraw.trigon(screen, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], darkened_color)

    


def draw_faces(all_vertices, sorted_faces, aspect_ratio):
    for depth, face in sorted_faces:
        vertices_indices, color = face
        points = [project(all_vertices[i][0], all_vertices[i][1], all_vertices[i][2], 400, 4, aspect_ratio) for i in vertices_indices]
        
        # Darken the color based on depth
        darken_factor = max(0, min(1, 1 - depth / DARKENING_FACTOR))  # Adjust the divisor to control the darkening effect
        darkened_color = tuple(int(c * darken_factor) for c in color)
        if darkened_color[0] > 0 and darkened_color[1] > 0 and darkened_color[2] > 0:
            try:
                texturing(screen, darkened_color, points)
            except Exception as e:
                print(f"Error drawing polygon with points: {points}, error: {e}")

normal_render = True
def get_all_faces(cam_pos):
    all_vertices = []
    all_faces = []
    vertex_offset = 0
    for obj in DICT.values():
        if obj['render']:
            bounding_box = obj['object_class'].bounding_box
            if bounding_box[0][0] - RENDER_DISTANCE_FAR < cam_pos[0] - obj['object_class'].pivot[0] < bounding_box[0][1] + RENDER_DISTANCE_FAR and \
               bounding_box[2][0] - abs(RENDER_DISTANCE_LEFT) < cam_pos[2] - obj['object_class'].pivot[2] < bounding_box[2][1] + RENDER_DISTANCE_RIGHT:
                if normal_render:
                    # Used if you want to split the object into smaller objects
                    obj_class = obj['object_class']
                    vertices = obj_class.vertices
                    all_vertices.extend(vertices)
                    for face in obj['object_class'].faces:
                        vertices_indices, color = face
                        adjusted_indices = [index + vertex_offset for index in vertices_indices]
                        all_faces.append((adjusted_indices, color))
                    vertex_offset += len(vertices)
                else:
                    smaller_bounding_boxes = obj['object_class'].split_objects_smaller_percent
                    for vertices, smaller_bounding_box in smaller_bounding_boxes:
                        if smaller_bounding_box[0][0] - RENDER_DISTANCE_FAR < cam_pos[0] - obj['object_class'].pivot[0] < smaller_bounding_box[0][1] + RENDER_DISTANCE_FAR and \
                           smaller_bounding_box[2][0] - abs(RENDER_DISTANCE_LEFT) < cam_pos[2] - obj['object_class'].pivot[2] < smaller_bounding_box[2][1] + RENDER_DISTANCE_RIGHT:
                            # need to somehow state
                            # What ithe condition is before is: Hello yes this is in the bound of the smaller bounding box
                            # then need to say hi faces, what ones are tied into this smaller bounding box
                            # then says yes appendthem to a list :)
                            # then if that faces is split inbetween two smaller bounding boxes then it will not render the face (unless it works and causes no problem)
                            break
    
    return all_vertices, all_faces


def main():
    global screen
    clock = pygame.time.Clock()
    
    collisions_on = True
    running = True

    cam = Cam((0, 0, -5))
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)
    
    # Updates the start position of the objects
    for obj_name, obj in DICT.items():
        Object.scale(obj['object_class'], obj['scale'])
        calculate_position(obj['object_class'], 0, 0, 0, *obj['start_pos'])

    while running:
        start_time = time.time()
        # Single input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cam.mouse_event(event)
        

        keys = pygame.key.get_pressed()
        cam.update(keys)

        """for obj_name, obj in DICT.items():
            cam.check_collision_with_camera(obj['object_class'])"""
            
        screen.fill(BLACK)
        pygame.draw.rect(screen, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        # Draw blue sky
        sky_color = (135, 206, 235)  # Light blue color
        sky_height = int((1 - (1.58 - cam.rot[0]) / 3.16) * HEIGHT)
        pygame.draw.rect(screen, sky_color, (0, 0, WIDTH, sky_height))


        # Get all faces to render
        func_start_time = time.time()
        all_vertices, all_faces = get_all_faces(cam.pos)
        get_all_faces_time = time.time() - func_start_time

        # Transform vertices based on camera position and rotation
        func_start_time = time.time()
        transformed_vertices = cam.transform(all_vertices)
        transform_time = time.time() - func_start_time

        # Sort faces by dot product with camera's front vector
        func_start_time = time.time()
        sorted_faces = sort_high_to_low(transformed_vertices, all_faces)
        sort_time = time.time() - func_start_time
        
        # Calculate aspect ratio
        aspect_ratio = pygame.display.get_surface().get_width() / pygame.display.get_surface().get_height()

        # Draw all faces
        func_start_time = time.time()
        draw_faces(transformed_vertices, sorted_faces, aspect_ratio)
        draw_faces_time = time.time() - func_start_time

        end_time = time.time()
        processing_time = end_time - start_time
        
        # Display individual function processing times
        font = pygame.font.SysFont('Arial', 20)
        get_all_faces_surface = font.render(f"Get All Faces Time: {get_all_faces_time:.4f} s", False, WHITE)
        screen.blit(get_all_faces_surface, (0, 90))
        transform_surface = font.render(f"Transform Time: {transform_time:.4f} s", False, WHITE)
        screen.blit(transform_surface, (0, 120))
        sort_surface = font.render(f"Sort Time: {sort_time:.4f} s", False, WHITE)
        screen.blit(sort_surface, (0, 150))
        draw_faces_surface = font.render(f"Draw Faces + Textures Time: {draw_faces_time:.4f} s", False, WHITE)
        screen.blit(draw_faces_surface, (0, 180))
        
        
        # Display processing time
        font = pygame.font.SysFont('Arial', 30)
        processing_time_surface = font.render(f"Processing Time: {processing_time:.4f} s", False, WHITE)
        screen.blit(processing_time_surface, (0, 60))

        # See FPS
        fps = str(int(clock.get_fps()))
        font = pygame.font.SysFont('Arial', 30)
        fpssurface = font.render(fps, False, WHITE)
        screen.blit(fpssurface, (0, 0))

        # See position
        pos = str(cam.pos)
        font = pygame.font.SysFont('Arial', 30)
        possurface = font.render(pos, False, WHITE)
        screen.blit(possurface, (0, 30))
        
        # Draw small x, y, z axis in the middle of the screen
        axis_length = 10
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2

        # Draw small x, y, z axis in the middle of the screen based on camera rotation
        axis_length = 10
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        # Draw x-axis (red)
        end_x = center_x + axis_length * math.cos(cam.rot[1])
        end_y = center_y + axis_length * math.sin(cam.rot[1])
        pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (end_x, end_y), 2)
        # Draw y-axis (green)
        end_x = center_x
        end_y = center_y - axis_length
        pygame.draw.line(screen, (0, 255, 0), (center_x, center_y), (end_x, end_y), 2)
        # Draw z-axis (blue)
        end_x = center_x + axis_length * math.sin(cam.rot[1])
        end_y = center_y - axis_length * math.cos(cam.rot[1])
        pygame.draw.line(screen, (0, 0, 255), (center_x, center_y), (end_x, end_y), 2)

        
        pygame.display.flip()
        #pygame.display.update()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    #cProfile.run("main()")
    main()
