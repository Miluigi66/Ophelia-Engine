import main
from main import math, pygame, threeDModles
from core_vars import WIDTH, HEIGHT, DARKENING_FACTOR, RENDER_DISTANCE_FAR, RENDER_DISTANCE_BEHIND, RENDER_DISTANCE_LEFT, RENDER_DISTANCE_RIGHT
from main_loop import screen
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
        min_depth = min(depths)
        max_depth = max(depths)
        
        if RENDER_DISTANCE_BEHIND <= min_depth <= RENDER_DISTANCE_FAR and \
           RENDER_DISTANCE_BEHIND <= max_depth <= RENDER_DISTANCE_FAR and \
           RENDER_DISTANCE_LEFT <= all_vertices[vertices_indices[0]][0] <= RENDER_DISTANCE_RIGHT:
            sorted_faces.append((avg_depth, face))
        if min_depth <= RENDER_DISTANCE_BEHIND <= max_depth <= RENDER_DISTANCE_FAR and \
           RENDER_DISTANCE_LEFT <= all_vertices[vertices_indices[0]][0] <= RENDER_DISTANCE_RIGHT:
            sorted_faces.append((avg_depth, face))
            
        # maybe try all places or try to find out how to not render if the point is behind a point or not seen
    sorted_faces.sort(reverse=True, key=lambda x: x[0])
    return sorted_faces


def check_collision(obj1, obj2):
    (min_x1, max_x1), (min_y1, max_y1), (min_z1, max_z1) = obj1.get_bounding_box()
    (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = obj2.get_bounding_box()

    return (min_x1 <= max_x2 and max_x1 >= min_x2 and
            min_y1 <= max_y2 and max_y1 >= min_y2 and
            min_z1 <= max_z2 and max_z1 >= min_z2)

def transfrom_image(points, sides):
    if sides == 4:
        image = pygame.image.load("man.jpg")
        # Calculate the width and height based on the points
        new_width = max(points[0][0] - points[1][0], points[1][0] - points[0][0], points[2][0] - points[3][0], points[3][0] - points[2][0])
        new_height = max(points[0][1] - points[3][1], points[3][1] - points[0][1], points[1][1] - points[2][1], points[2][1] - points[1][1])
        image = pygame.transform.scale(image, (new_width, new_height))
        
        # Calculate the top-left corner for positioning the image
        min_x = min(points[0][0], points[1][0], points[2][0], points[3][0])
        min_y = min(points[0][1], points[1][1], points[2][1], points[3][1])
        
        # Blit the image onto the screen at the calculated position
        screen.blit(image, (min_x, min_y))

def texturing(darkened_color, points):
    pygame.gfxdraw.filled_polygon(screen, points, darkened_color)
    transfrom_image(points, len(points))
    
    # draws the bounding boxes
    
    # Weird half arks
    #pygame.gfxdraw.bezier(screen, points, 2, darkened_color)
    # Connect the dots 
    ##pygame.gfxdraw.circle(screen, points[0][0], points[0][1], 2, (255, 255, 255))
    # Black outline
    ##pygame.gfxdraw.aapolygon(screen, points, (255, 255, 255))
    # Color outling
    #pygame.gfxdraw.trigon(screen, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], darkened_color)

    


def draw_faces(all_vertices, sorted_faces, aspect_ratio):
    for depth, face in sorted_faces:
        vertices_indices, color = face
        points = [project(all_vertices[i][0], all_vertices[i][1], all_vertices[i][2], 400, 4, aspect_ratio) for i in vertices_indices]
        # Darken the color based on depth
        darken_factor = max(0, min(1, 1 - depth / DARKENING_FACTOR))  # Adjust the divisor to control the darkening effect
        darkened_color = tuple(int(c * darken_factor) for c in color)
        if darkened_color[0] >= 0 and darkened_color[1] >= 0 and darkened_color[2] >= 0:
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


    
    # maybe try to seperate the rendering and the colision so colision is immaginary and the render is seprrate so the smaller chunks all have 
    # it own render 
    # also maybe move the orginiser from sort to here I need to change the process fo rendering so its quicker than this and i need to do a
    #flow chart to see how I render 
    # I also need to fix how i split the objecct so i need to do it in squares in process of x and z not y so it down then up 
    # and need to fox how stuff looks when i get close I just need to somehow say oh my its goinf to render behind me and in frount ok here:
    # render the spot it goes to at the bottom of the screen 
    return all_vertices, all_faces
