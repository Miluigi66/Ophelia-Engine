import main
from main import math, pygame, threeDModles
from core_vars import WIDTH, HEIGHT, DARKENING_FACTOR, RENDER_DISTANCE_FAR, RENDER_DISTANCE_BEHIND, RENDER_DISTANCE_LEFT, RENDER_DISTANCE_RIGHT
from main_loop import screen

def project(x, y, z, scale, distance, aspect_ratio):
    factor = scale / (distance + z)
    return int(x * factor * aspect_ratio + WIDTH // 2), int(-y * factor + HEIGHT // 2)

def calculate_position(obj_class, angle_x, angle_y, angle_z, pos_x, pos_y, pos_z):
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)

    pivot_x, pivot_y, pivot_z = obj_class.pivot
    transformed_vertices = []

    for x, y, z in obj_class.vertices:
        # Translate to pivot
        x -= pivot_x
        y -= pivot_y
        z -= pivot_z

        # Rotate around axes
        y, z = y * cos_x - z * sin_x, z * cos_x + y * sin_x
        x, z = x * cos_y - z * sin_y, z * cos_y + x * sin_y
        x, y = x * cos_z - y * sin_z, y * cos_z + x * sin_z

        # Apply position offsets
        x += pivot_x + pos_x
        y += pivot_y + pos_y
        z += pivot_z + pos_z

        transformed_vertices.append((x, y, z))

    obj_class.update_object(transformed_vertices, obj_class.edges, obj_class.faces, (pivot_x + pos_x, pivot_y + pos_y, pivot_z + pos_z))
    return transformed_vertices

def sort_high_to_low(all_vertices, all_faces):
    sorted_faces = [
        (sum(all_vertices[idx][2] for idx in face[0]) / len(face[0]), face)
        for face in all_faces
        if all(RENDER_DISTANCE_BEHIND <= all_vertices[idx][2] <= RENDER_DISTANCE_FAR for idx in face[0]) and
           RENDER_DISTANCE_LEFT <= all_vertices[face[0][0]][0] <= RENDER_DISTANCE_RIGHT
    ]
    return sorted(sorted_faces, reverse=True, key=lambda x: x[0])

def check_collision(obj1, obj2):
    box1 = obj1.get_bounding_box()
    box2 = obj2.get_bounding_box()
    return all(box1[i][0] <= box2[i][1] and box1[i][1] >= box2[i][0] for i in range(3))

def transfrom_image(points, sides):
    if sides == 4:
        image = pygame.image.load("man.jpg")
        new_width = max(abs(points[i][0] - points[j][0]) for i in range(4) for j in range(i + 1, 4))
        new_height = max(abs(points[i][1] - points[j][1]) for i in range(4) for j in range(i + 1, 4))
        image = pygame.transform.scale(image, (new_width, new_height))
        screen.blit(image, (min(p[0] for p in points), min(p[1] for p in points)))

def texturing(darkened_color, points):
    pygame.gfxdraw.filled_polygon(screen, points, darkened_color)

def draw_faces(all_vertices, sorted_faces, aspect_ratio):
    for depth, face in sorted_faces:
        vertices_indices, color = face[0], face[1]
        points = [project(*all_vertices[i], 400, 4, aspect_ratio) for i in vertices_indices]
        darken_factor = max(0, min(1, 1 - depth / DARKENING_FACTOR))
        darkened_color = tuple(int(c * darken_factor) for c in color)
        if all(c >= 0 for c in darkened_color):
            try:
                texturing(darkened_color, points)
            except Exception as e:
                print(f"Error drawing polygon with points: {points}, error: {e}")

normal_render = True
def get_all_faces(cam_pos):
    all_vertices = []
    all_faces = []
    vertex_offset = 0

    for obj in threeDModles.values():
        if not obj['render']:
            continue

        obj_class = obj['object_class']
        pivot_x, pivot_z = obj_class.pivot[0], obj_class.pivot[2]
        bounding_box = obj_class.bounding_box

        if not (bounding_box[0][0] - RENDER_DISTANCE_FAR < cam_pos[0] - pivot_x < bounding_box[0][1] + RENDER_DISTANCE_FAR and
                bounding_box[2][0] - abs(RENDER_DISTANCE_LEFT) < cam_pos[2] - pivot_z < bounding_box[2][1] + RENDER_DISTANCE_RIGHT):
            continue

        vertices = obj_class.vertices
        all_vertices.extend(vertices)

        for face in obj_class.faces:
            adjusted_indices = [index + vertex_offset for index in face[0]]
            all_faces.append((adjusted_indices, face[1]))

        vertex_offset += len(vertices)

    return all_vertices, all_faces
