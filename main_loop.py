from main import pygame, sys, math, time, camera
from core_vars import WIDTH, HEIGHT, BLACK, WHITE
import  main_functions_math
from objects import threeDModles

# Initialize Pygame
pygame.init()

# The screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("Ophelia Engine")
#TRY THIS MAYBE to make icon :)
#pygame.display.set_icon(pygame.image.load(os.path.join("total_modles", "icon.png")))

# Preload fonts to avoid recreating them in the loop
font_small = pygame.font.SysFont('Arial', 20)
font_large = pygame.font.SysFont('Arial', 30)

def main_loop():
    fullscreen = False
    clock = pygame.time.Clock()
    collisions_on = True
    running = True

    cam = camera.Cam((0, 0, 0))
    # ALL WHEN FACING DEGREE (_,0,_)
    # x = left and right
    # y = up and down
    # z = front and back
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)
    
    while running:
        start_time = time.time()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                cam.mouse_event(event)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_0:
                    for obj in threeDModles.values():
                        if obj['type'] == 'ob:terrain':
                            obj['render'] = not obj['render']   
        
        # Update camera
        keys = pygame.key.get_pressed()
        cam.update(keys)
        
        """if clock.get_time() % 2 == 0:
            main_functions_math.calculate_position(threeDModles['square']['object_class'], 1, 0, 0, .1, 0, 0)"""
        
        """for obj_name, obj in DICT.items():
            cam.check_collision_with_camera(obj['object_class'])"""
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw blue sky and ground
        sky_color = (135, 206, 235)  # Light blue
        sky_height = int((1 - (1.58 - cam.rot[0]) / 3.16) * HEIGHT)
        pygame.draw.rect(screen, sky_color, (0, 0, WIDTH, sky_height))
        pygame.draw.rect(screen, (0, 0, 0), (0, sky_height, WIDTH, HEIGHT - sky_height))

        # Get all faces to render
        func_start_time = time.time()
        all_vertices, all_faces = main_functions_math.get_all_faces(cam.pos)
        get_all_faces_time = time.time() - func_start_time
        
        # Transform vertices based on camera position and rotation
        func_start_time = time.time()
        transformed_vertices = cam.transform(all_vertices)
        transform_time = time.time() - func_start_time

        # Sort faces by dot product with camera's front vector
        func_start_time = time.time()
        sorted_faces = main_functions_math.sort_high_to_low(transformed_vertices, all_faces)
        sort_time = time.time() - func_start_time
    
        # Calculate aspect ratio
        aspect_ratio = pygame.display.get_surface().get_width() / pygame.display.get_surface().get_height()

        # Draw all faces
        func_start_time = time.time()
        main_functions_math.draw_faces(transformed_vertices, sorted_faces, aspect_ratio)
        draw_faces_time = time.time() - func_start_time

        end_time = time.time()
        processing_time = end_time - start_time
        
        # Display performance metrics
        processing_time = time.time() - start_time
        metrics = [
            (f"FPS: {int(clock.get_fps())}", 0, 0),
            (f"Position: {cam.pos}", 0, 30),
            (f"Rotation: {tuple(round(math.degrees(angle), 2) for angle in cam.rot)}", 0, 60),
            (f"Processing Time: {processing_time:.4f} s", 0, 90),
            (f"Get All Faces Time: {get_all_faces_time:.4f} s", 0, 120),
            (f"Transform Time: {transform_time:.4f} s", 0, 150),
            (f"Sort Time: {sort_time:.4f} s", 0, 180),
            (f"Draw Faces Time: {draw_faces_time:.4f} s", 0, 240),
            (f"Total Faces: {len(all_faces)}", 0, 270),
            (f"Total Faces Rendered: {len(sorted_faces)}", 0, 300),
        ]
        max_time = max(get_all_faces_time, transform_time, sort_time, draw_faces_time)
        bottleneck = ["Get All Faces", "Transform", "Sort", "Draw Faces + Textures"][
            [get_all_faces_time, transform_time, sort_time, draw_faces_time].index(max_time)
        ]
        metrics.append((f"Bottleneck: {bottleneck} ({max_time:.4f} s)", 0, 210))

        for text, x, y in metrics:
            surface = font_small.render(text, False, WHITE)
            screen.blit(surface, (x, y))

        # Draw axes
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        axis_length = 10
        pygame.draw.line(screen, (255, 0, 0), (center_x, center_y),
                         (center_x + axis_length * math.cos(cam.rot[1]), center_y + axis_length * math.sin(cam.rot[1])), 2)
        pygame.draw.line(screen, (0, 255, 0), (center_x, center_y), (center_x, center_y - axis_length), 2)
        pygame.draw.line(screen, (0, 0, 255), (center_x, center_y),
                         (center_x + axis_length * math.sin(cam.rot[1]), center_y - axis_length * math.cos(cam.rot[1])), 2)

        # Update display
        #pygame.display.flip()
        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS