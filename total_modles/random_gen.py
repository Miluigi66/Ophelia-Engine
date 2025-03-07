import random
chance_of_hills = 35
max_height = 10
min_height = 1
max_width = 75
min_width = -max_width
max_length = 75
min_length = -max_length

generate_model_after = {
    'hills': {
        # Cube vertices
        "vertices": [],

        # Pivot point
        "pivot": (0, 0, 0),  # Pivot point
        
        # Cube edges
        "edges": [],
        
        # Cube faces
        "faces": []
    }
}

def custom_random_height():
    # Generate a random number between 0 and 1
    r = random.random()
    # Raise the random number to the power of 3 to skew the distribution towards lower values
    return min_height + (max_height - min_height) * (r ** chance_of_hills)

def generate_hills_vertices():
    for i in range(min_width, max_width):
        for j in range(min_length, max_length):
            height = round(custom_random_height(), 5)
            generate_model_after['hills']['vertices'].append((i, height, j))

def generate_hills_faces():
    for i in range(min_width, max_width - 1):
        for j in range(min_length, max_length - 1):
            v1 = (i - min_width) + (j - min_length) * (max_width - min_width)
            v2 = (i - min_width + 1) + (j - min_length) * (max_width - min_width)
            v3 = (i - min_width + 1) + (j - min_length + 1) * (max_width - min_width)
            v4 = (i - min_width) + (j - min_length + 1) * (max_width - min_width)
            generate_model_after['hills']['faces'].append(([v1, v2, v3, v4], (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

generate_hills_vertices()
generate_hills_faces()