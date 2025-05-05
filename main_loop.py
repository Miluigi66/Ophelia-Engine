from main import pygame, sys, math, time, camera
from core_vars import WIDTH, HEIGHT, BLACK, WHITE
import  main_functions_math
from objects import threeDModles

# the screen supper important 
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
def main_loop():
    
    # Initialize Pygame
    pygame.init()


    fullscreen = False
    
    pygame.display.set_caption("3D Rendering Engine")


    clock = pygame.time.Clock()

    collisions_on = True
    running = True

    cam = camera.Cam((0, 0, -5))
    pygame.event.get()
    pygame.mouse.get_rel()
    pygame.mouse.set_visible(0)
    pygame.event.set_grab(1)
    
    
    
    while running:
        start_time = time.time()
        # Single input
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
            
        keys = pygame.key.get_pressed()
        cam.update(keys)
        
        """if clock % 2 == 0:
            main_functions_math.calculate_position(DICT['mountains2']['BOB'], 0, 0, .1, 0, 0, 0)"""
        
        """for obj_name, obj in DICT.items():
            cam.check_collision_with_camera(obj['object_class'])"""
            
        screen.fill(BLACK)
        # Draw blue sky
        sky_color = (135, 206, 235)  # Light blue color
        sky_height = int((1 - (1.58 - cam.rot[0]) / 3.16) * HEIGHT)
        pygame.draw.rect(screen, sky_color, (0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(screen, sky_color, (0, 0, WIDTH, sky_height))
        # Draw green ground
        ground_height = HEIGHT - sky_height
        pygame.draw.rect(screen, (0, 0, 0), (0, sky_height, WIDTH, ground_height))


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
