# Import all modules
import pygame
import random
import sys
import math
from pygame.locals import *
# Initialize pygame:
pygame.init()

# Set Frames per second:
FPS = 30
fpsClock = pygame.time.Clock()
screen_dim = (1200, 600)

# Create Screen:
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption('Creation of Life')

#Setting the boundries
left_bound = pygame.Rect(0, 0, 1, screen_dim[1])
right_bound = pygame.Rect(screen_dim[0] - 1, 0, 1, screen_dim[1])
top_bound = pygame.Rect(0, 0, screen_dim[0], 1)
bottom_bound = pygame.Rect(0, screen_dim[1] - 1, screen_dim[0], 1)

# Creat Particle class
class Particle(pygame.sprite.Sprite):
   
    def __init__(self, image_file, name):
        super().__init__()
       
        # Add image:
        self.image = pygame.image.load((image_file))
        self.image = pygame.transform.scale(self.image, (20,20))
       
        # Sprite rectangle:
        spacing = 15
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(spacing, screen_dim[0] - spacing)
        self.rect.centery = random.randint(spacing, screen_dim[1] - spacing)
        self.theta = random.random() * 2 * math.pi
        self.r = 2
        self.name = name
        self.mol = "None"

    # Update: Takes self as a parameter, chooses a random number and randomly choses to move in the positive or negative direction, then updates the center of the particle's center to get a new random coordinate.
    def update(self, r_multiplier):
        if right_bound.colliderect(self.rect) or self.rect.centerx > 1200:
            self.rect.centerx -= 2
            self.theta = math.pi - self.theta
        elif left_bound.colliderect(self.rect) or self.rect.centerx <0:
            self.rect.centerx += 2
            self.theta = math.pi - self.theta
        if bottom_bound.colliderect(self.rect)  or self.rect.centery > 600:
            self.rect.centery -= 2
            self.theta = 2 * math.pi - self.theta
        elif top_bound.colliderect(self.rect) or self.rect.centery <0:
            self.rect.centery += 2
            self.theta = 2 * math.pi - self.theta
        self.rect.centerx += self.r * r_multiplier * math.cos(self.theta)
        self.rect.centery += self.r * r_multiplier * math.sin(self.theta)
        
    #Allows particle to change image.
    def change_image(self, new_image, width, length):
        self.image = pygame.image.load((new_image))
        self.image = pygame.transform.scale(self.image, (width,length))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(15, screen_dim[0] - 15)
        self.rect.centery = random.randint(15, screen_dim[1] - 15)
    def change_mol(self, new_name):
        self.mol = new_name
    def change_name(self, new_name):
        self.name = new_name
        
    #Methods to get the attributes:
    def get_x(self):
        return self.rect.centerx
    def get_y(self):
        return self.rect.centerx
    def get_name(self):
        return self.name
    
    #Change speed of particles
    def stop_moving(self):
        self.r = 0
    def start_moving(self):
        self.r = 2
    def decrease_speed(self):
        self.r -= 2
    def increase_speed(self):
        self.r += 2

#Define counters:
carb_count = 0
protein_count = 0
DNA_count = 0
total_count = 0
screens = 0        
        
#Create all Sprite Groups:
# Create Carbon group:
carbon_particles = pygame.sprite.Group()
list_carbon_particles = [Particle("Carbon.png", "C") for i in range(15)]

for particle in list_carbon_particles:
    carbon_particles.add(particle)

# Create Hydrogen group:
hydrogen_particles = pygame.sprite.Group()
list_hydrogen_particles = [Particle("Hydrogen.png", "H") for i in range(15)]

for particle in list_hydrogen_particles:
    hydrogen_particles.add(particle)

#Create Oxygen Group:
oxygen_particles = pygame.sprite.Group()
list_oxygen_particles = [Particle("Oxygen.png", "O") for i in range(15)]

for particle in list_oxygen_particles:
    oxygen_particles.add(particle)
    
#Create Nitrogen Group:
nitrogen_particles = pygame.sprite.Group()
list_nitrogen_particles = [Particle("Nitrogen.png", "N") for i in range(15)]

for particle in list_nitrogen_particles:
    nitrogen_particles.add(particle)

#Create Phosphorus Group:
phosphorus_particles = pygame.sprite.Group()
list_phosphorus_particles = [Particle("Phosphorus.png", "P") for i in range(15)]

for particle in list_phosphorus_particles:
    phosphorus_particles.add(particle)

#Create Water Group:
water_particles = pygame.sprite.Group()
list_water_particles = [Particle("water.png", "W") for i in range(70)]

for particle in list_water_particles:
    water_particles.add(particle)

#Create one big list of ALL the particles on the screen:
list_all_particles = list_carbon_particles + list_hydrogen_particles + list_oxygen_particles + list_nitrogen_particles + list_phosphorus_particles + list_water_particles


#Detecting collisions:
def init_collision():
    scanned_particles = []
    global total_count
    for particle_1 in list_all_particles:
        scanned_particles.append(particle_1)
        for particle_2 in list_all_particles:
            if particle_2 in scanned_particles:
                continue
            if particle_1.rect.colliderect(particle_2.rect):
                particle_1_name = particle_1.get_name()
                particle_2_name = particle_2.get_name()
                #Initial collisions:
                if (particle_1_name == "C" and particle_2_name == "H") or (particle_1_name == "H" and particle_2_name == "C"):
                    particle_1.change_image("carbon_hydrogen.png", 50, 20)
                    particle_1.change_name("CH")
                    total_count += 1
                    particle_2.kill()
               
                elif (particle_1_name == "O" and particle_2_name == "H") or (particle_1_name == "H" and particle_2_name == "O"):
                    particle_1.change_image("Hydrogen_Oxygen.png", 50, 20)
                    particle_1.change_name("OH")
                    total_count += 1
                    particle_2.kill()
                   
                elif (particle_1_name == "O" and particle_2_name == "C") or (particle_1_name == "C" and particle_2_name == "O"):
                    particle_1.change_image("Carbon_Oxygen.png",50, 20)
                    particle_1.change_name("CO")
                    total_count += 1
                    particle_2.kill()
                else:
                    particle_1.theta, particle_2.theta = particle_2.theta, particle_1.theta
                    particle_1.r, particle_2.r = particle_2.r, particle_1.r
                    scanned_particles.append(particle_2)
                    particle_1.update(1)
                    particle_2.update(1)
                    
#detecting secondary collisions (carbohydrate)
def detect_carb():
    init_collision()
    global total_count
    global carb_count
    scanned_particles = []
    for particle_1 in list_all_particles:
        scanned_particles.append(particle_1)
        for particle_2 in list_all_particles:
            if particle_2 in scanned_particles:
                continue
            if particle_1.rect.colliderect(particle_2.rect):
                particle_1_name = particle_1.get_name()
                particle_2_name = particle_2.get_name()
                #Initial collisions:
                if (particle_1_name == "CH" and particle_2_name == "O") or (particle_1_name == "O" and particle_2_name == "CH"):
                    particle_1.change_image("carb.png", 70, 30)
                    particle_1.change_name("CHO")
                    particle_1.change_mol("Carb")
                    total_count += 1
                    carb_count += 1
                    particle_2.kill()
                elif (particle_1_name == "OH" and particle_2_name == "C") or (particle_1_name == "C" and particle_2_name == "OH"):
                    particle_1.change_image("carb.png", 70, 30)
                    particle_1.change_name("CHO")
                    particle_1.change_mol("Carb")
                    total_count += 1
                    carb_count += 1
                    particle_2.kill()
                elif (particle_1_name == "CO" and particle_2_name == "H") or (particle_1_name == "H" and particle_2_name == "CO"):
                    particle_1.change_image("carb.png", 70,30)
                    particle_1.change_name("CHO")
                    particle_1.change_mol("Carb")
                    total_count += 1
                    carb_count += 1
                    particle_2.kill()
                else:
                    particle_1.theta, particle_2.theta = particle_2.theta, particle_1.theta
                    particle_1.r, particle_2.r = particle_2.r, particle_1.r
                    scanned_particles.append(particle_2)
                    particle_1.update(1)
                    particle_2.update(1)
                    
#Detect tertiary collisions (Proteins) 
def detect_protein():
    detect_carb()
    global total_count
    global protein_count
    scanned_particles = []
    
    for particle_1 in list_all_particles:
        scanned_particles.append(particle_1)
        for particle_2 in list_all_particles:
            if particle_2 in scanned_particles:
                continue
            if particle_1.rect.colliderect(particle_2.rect):
                particle_1_name = particle_1.get_name()
                particle_2_name = particle_2.get_name()
                #Initial collisions:
                if (particle_1_name == "CHO" and particle_2_name == "N") or (particle_1_name == "N" and particle_2_name == "CHO"):
                    particle_1.change_image("protein.png", 90, 40)
                    particle_1.change_name("CHON")
                    particle_1.change_mol("Protein")
                    total_count += 1
                    protein_count += 1
                    particle_2.kill()
                else:
                    particle_1.theta, particle_2.theta = particle_2.theta, particle_1.theta
                    particle_1.r, particle_2.r = particle_2.r, particle_1.r
                    scanned_particles.append(particle_2)
                    particle_1.update(1)
                    particle_2.update(1)
                    
#Detect last collision (DNA) & then stop simulator
def detect_DNA():
    detect_protein()
    global total_count
    global DNA_count
    scanned_particles = []
    
    for particle_1 in list_all_particles:
        scanned_particles.append(particle_1)
        for particle_2 in list_all_particles:
            if particle_2 in scanned_particles:
                continue
            if particle_1.rect.colliderect(particle_2.rect):
                particle_1_name = particle_1.get_name()
                particle_2_name = particle_2.get_name()
                #Initial collisions:
                if (particle_1_name == "CHON" and particle_2_name == "P") or (particle_1_name == "P" and particle_2_name == "CHON"):
                    particle_1.change_image("DNA.png", 100, 50)
                    particle_1.change_name("CHONP")
                    particle_1.change_mol("DNA")
                    total_count += 1
                    DNA_count += 1
                    particle_2.kill()
                else:
                    particle_1.theta, particle_2.theta = particle_2.theta, particle_1.theta
                    particle_1.r, particle_2.r = particle_2.r, particle_1.r
                    scanned_particles.append(particle_2)
                    particle_1.update(1)
                    particle_2.update(1)
  
 
end_game = False   


# Main loop
while True:
    if end_game == False:
        screens += 1
    #Fill Screen:
    screen.fill((255, 255, 255))
    #Quit Program:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #Adding Text and Counting Collisions:

    #Carbohydrate Collisions:
    carb_fontObj = pygame.font.Font('freesansbold.ttf', 32)
    carb_SurfaceObj = carb_fontObj.render("carbs:" + str(carb_count), True, (0,0,0), (255,255,255))
    carb_RectObj = carb_SurfaceObj.get_rect()
    carb_RectObj.center = (200, 500)     
    #Protein Collisions:
    protein_fontObj = pygame.font.Font('freesansbold.ttf', 32)
    protein_SurfaceObj = protein_fontObj.render("Proteins:" + str(protein_count), True, (0,0,0), (255,255,255))
    protein_RectObj = protein_SurfaceObj.get_rect()
    protein_RectObj.center = (200, 400)    
    #DNA Collisions:
    DNA_fontObj = pygame.font.Font('freesansbold.ttf', 32)
    DNA_SurfaceObj = DNA_fontObj.render("DNA:" + str(DNA_count), True, (0,0,0), (255,255,255))
    DNA_RectObj =DNA_SurfaceObj.get_rect()
    DNA_RectObj.center = (200, 300)    
    #Total Collisions:
    total_fontObj = pygame.font.Font('freesansbold.ttf', 32)
    total_SurfaceObj = total_fontObj.render("Total:" + str(total_count), True, (0,0,0), (255,255,255))
    total_RectObj = total_SurfaceObj.get_rect()
    total_RectObj.center = (200, 200) 
    #Time it took: 
    screens_fontObj = pygame.font.Font('freesansbold.ttf', 32)
    screens_SurfaceObj = screens_fontObj.render("Screens:" + str(screens), True, (0,0,0), (255,255,255))
    screens_RectObj = screens_SurfaceObj.get_rect()
    screens_RectObj.center = (200, 100)
    if end_game == True:
        screen.blit(carb_SurfaceObj, carb_RectObj)
        screen.blit(protein_SurfaceObj, protein_RectObj)
        screen.blit(DNA_SurfaceObj, DNA_RectObj)
        screen.blit(total_SurfaceObj, total_RectObj)
        screen.blit(screens_SurfaceObj, screens_RectObj)
        
    #Calling Detection function:
    detect_DNA()
               
               
    # using the update method in particle class to move objects
    carbon_particles.update(1)
    hydrogen_particles.update(1)
    oxygen_particles.update(1)
    nitrogen_particles.update(1)
    phosphorus_particles.update(1)
    water_particles.update(1)

    # Drawing the 2 particles
    carbon_particles.draw(screen)
    hydrogen_particles.draw(screen)
    oxygen_particles.draw(screen)
    nitrogen_particles.draw(screen)
    phosphorus_particles.draw(screen)
    water_particles.draw(screen)
    #Increase speeed using keys:
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        for particle in list_all_particles:
            particle.increase_speed()
            particle.update(1)
    elif key[pygame.K_DOWN]:
        for particle in list_all_particles:
            particle.decrease_speed()
            particle.update(1)
    elif key[pygame.K_SPACE]:
        for particle in list_all_particles:
            particle.stop_moving()
    elif key[pygame.K_BACKSPACE]:
        for particle in list_all_particles:
            particle.start_moving() 
    elif key[pygame.K_ESCAPE]:
        for particle in list_all_particles:
            particle.kill()
            end_game = True
    pygame.display.update()
    fpsClock.tick(FPS)