from main import math, pygame, sys
from objects import threeDModles
class Cam:
    def __init__(self, pos):
        # ALL WHEN FACING DEGREE (_,0,_)
        # x = left and right
        # y = up and down
        # z = front and back
        self.pos = list(pos)
        self.rot = [0, 0, 0]  # Pitch, yaw, roll
        # Define a simple hitbox for the camera (a small cube around the position)
        self.hitbox = (-1, 1), (-1, 1), (-1, 1)
    
        
    def mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200
            y /= 200
            self.rot[0] -= y
            self.rot[1] += x
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                direction = [
                        math.sin(self.rot[1]) * math.cos(self.rot[0]),
                        math.sin(self.rot[0]),
                        math.cos(self.rot[1]) * math.cos(self.rot[0])
                    ]
                for obj in threeDModles.values():
                    if hasattr(obj, 'intersects_ray') and obj.intersects_ray(self.pos, direction, legnth=3):
                        if hasattr(obj, 'color_change'):
                            obj.color_change((255, 0, 0))
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            None     
    
    def update(self, key):
                
        # Make sure the camera is always in range of 360 degrees for yaw
        self.rot[1] %= 2 * math.pi        
                
        if key[pygame.K_LSHIFT]:
            s = .5
        elif key[pygame.K_LCTRL]:
            s = .01
        else:
            s = .1
        # Camera movement z
        if key[pygame.K_c]:
            self.pos[1] -= s
        if key[pygame.K_SPACE]:
            self.pos[1] += s
        
        # Camera rotation
        if key[pygame.K_UP]:
            self.rot[0] = max(-1.58, min(1.58, self.rot[0] + 0.1))  # Clamp pitch rotation
        if key[pygame.K_DOWN]:
            self.rot[0] = max(-1.58, min(1.58, self.rot[0] - 0.1))  # Clamp pitch rotation
        if key[pygame.K_LEFT]:
            self.rot[1] -= 0.1
        if key[pygame.K_RIGHT]:
            self.rot[1] += 0.1
        # No..., but here if needed
        """if key[pygame.K_q]:
            self.rot[2] -= 0.1  # Roll left
        if key[pygame.K_e]:
            self.rot[2] += 0.1  # Roll right"""
        
        x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])

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
        cos_z, sin_z = math.cos(self.rot[2]), math.sin(self.rot[2])  # Add z-axis rotation

        for x, y, z in vertices:
            x -= self.pos[0]
            y -= self.pos[1]
            z -= self.pos[2]

            # Rotate around y-axis
            x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y

            # Rotate around x-axis
            y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

            # Rotate around z-axis
            x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
            
            transformed_vertices.append((x, y, z))
        return transformed_vertices
