from main import math, pygame, WIDTH, HEIGHT, screen, DICT, DARKENING_FACTOR, RENDER_DISTANCE_FAR, RENDER_DISTANCE_BEHIND, RENDER_DISTANCE_RIGHT, RENDER_DISTANCE_LEFT

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
