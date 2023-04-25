import pygame
import numpy as np

class WorldTest:
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Define the points
    points = [(10, 10), (150, 200), (200, 400)]

    # Define the initial zoom level and circle size
    zoom_level = 1.0
    circle_size = 10

    # Define the initial pan position
    panning = False
    last_x, last_y = 0, 0

    # Define the zoom matrix
    zoom_matrix = np.eye(3)
    pan_matrix = np.eye(3)

    # Initialize Pygame
    pygame.init()

    # Set the window size
    screen_size = (800.0, 600.0)
    screen = pygame.display.set_mode(screen_size)

    center_x, center_y = screen_size[0] / 2, screen_size[1] / 2
    motion_x, motion_y = 0, 0

    # Set the window title
    pygame.display.set_caption("My Game")

    # Set the clock
    clock = pygame.time.Clock()

    # Load a custom font
    font_path = "eurostile.TTF"  # replace with your own font file path
    font = pygame.font.Font(font_path, 20)

    # Main game loop
    done = False


    while not done:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    panning = True
                    last_x, last_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left mouse button
                    panning = False
            elif event.type == pygame.MOUSEMOTION:
                if panning:
                    motion_x += event.pos[0] - last_x
                    motion_y += event.pos[1] - last_y
                    
                    last_x, last_y = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                zoom_amount = event.y * 1.1
                zoom_scale = np.exp(zoom_amount / 10)
        
                zoom_matrix *= zoom_scale

                # Get the new zoom level and circle size
                zoom_level = zoom_matrix[0, 0]

                # mouse_pos = pygame.mouse.get_pos()
                # norm_mouse_pos = (mouse_pos[0] / screen_size[0], mouse_pos[1] / screen_size[1])

                # center_x = norm_mouse_pos[0] * screen_size[0]
                # center_y = norm_mouse_pos[1] * screen_size[1]

        # Clear the screen
        screen.fill(WHITE)

        #print(":", norm_mouse_pos[0], norm_mouse_pos[1])

        zoom_matrix[0, 2] = center_x
        zoom_matrix[1, 2] = center_y

        # Update the pan matrix
        pan_matrix[0, 2] = motion_x / zoom_level
        pan_matrix[1, 2] = motion_y / zoom_level

        mat_result = zoom_matrix @ pan_matrix

        # Draw the points
        for point in points:
            position = np.array([point[0], point[1], 1])

            position = np.matmul(mat_result, position)

            x = int(position[0])
            y = int(position[1])

            #pygame.draw.circle(screen, RED, (x, y), circle_size * zoom_level)

            circle_size_zoom = circle_size * zoom_level


            
            circle_surface = pygame.Surface((circle_size_zoom*2, circle_size_zoom*2), pygame.SRCALPHA)

            # Draw the circle on the new surface
            pygame.draw.circle(circle_surface, RED, (circle_size_zoom, circle_size_zoom), circle_size_zoom)

            # Blit the circle surface onto the main screen surface at the desired position
            screen.blit(circle_surface, (x - circle_size_zoom, y - circle_size_zoom))



        # Display frame rate on screen
        fps = round(clock.get_fps(), 2)
        text = font.render(str(fps), True, BLACK)
        screen.blit(text, (10, 10))

        # Update the screen
        pygame.display.flip()

        # Wait for a little bit to control the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
