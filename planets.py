import pygame
import math
pygame.init()

WIN=pygame.display.set_mode((800,800))
pygame.display.set_caption("Planet Simulation")


YELLOW=(255,255,0)
BLUE=(100,149,237)
RED=(188,39,50)
DARK_GREY=(80,78,81)
WHITE=(255,255,255)
FONT=pygame.font.SysFont("comicsans",30)

class Planet:
    AU= 146.6e6*1000
    G= 6.67428e-11
    SCALE=250/AU 
    TIMESTEP=3600*12 #originally*24

    def __init__(self,x,y,radius,color,mass,name,isSun=False):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.mass=mass
        self.x_velocity=0
        self.y_velocity=0
        self.isSun=isSun
        self.name=name

        self.distToSun=0
        self.orbit=list()
    
    def draw(self,win):
        x=self.x*self.SCALE+800/2
        y=self.y*self.SCALE+800/2

        if len(self.orbit)>2:

            updatedPoints=[]

            for point in self.orbit:
                x,y=point
                x=x*self.SCALE+400
                y=y*self.SCALE+400
                updatedPoints.append((x,y))
            pygame.draw.lines(WIN,self.color,False,updatedPoints,1)

        pygame.draw.circle(WIN,self.color,(x,y),self.radius) #surface,color,position,rad
        if not self.isSun:
            distance_text=FONT.render(f"{round(self.distToSun/1000,1)} km",1,WHITE)
            planet_text=FONT.render(f"{self.name}",1,WHITE)
            WIN.blit(planet_text,(x-planet_text.get_width()/2,y-planet_text.get_width()/2-20))
    
    def attraction(self,otherPlanet):
        distX=otherPlanet.x-self.x
        distY=otherPlanet.y-self.y
        distance=math.sqrt(distX**2+distY**2)
        if otherPlanet.isSun:
            self.distToSun=distance
        
        force=(self.G*self.mass*otherPlanet.mass)/(distance**2)
        theta=math.atan2(distY,distX)
        forceX=force*math.cos(theta)
        forceY=force*math.sin(theta)

        return forceX,forceY 
    
    def updatePos(self,planets):
        total_fx=total_fy=0
        for planet in planets:
            if planet==self:
                continue
            fx,fy=self.attraction(planet)
            total_fx+=fx
            total_fy+=fy
        
        self.x_velocity+=total_fx/self.mass*self.TIMESTEP
        self.y_velocity+=total_fy/self.mass*self.TIMESTEP

        self.x+=self.x_velocity*self.TIMESTEP
        self.y+=self.y_velocity*self.TIMESTEP
        self.orbit.append((self.x,self.y))


class PlanetList:
    def __init__(self):
        self.planets=[]


def drawStars(win):
    for i in range(40,800,50):
        for j in range(40,800,60):
            pygame.draw.circle(win,WHITE,(j,i),1)

        

def main():
    clock=pygame.time.Clock()

    run=True

    planetList=PlanetList()

    sun=Planet(0,0,23,YELLOW,1.98892*10**30,"Sun",True)
    planetList.planets.append(sun)
    earth=Planet(-1*Planet.AU,0,9,BLUE,5.9742*10**24,"Earth")
    earth.y_velocity=29.783*1000
    planetList.planets.append(earth)
    mars=Planet(-1.524*Planet.AU,0,8,RED,6.39*10**23,"Mars")
    mars.y_velocity=24.077*1000
    planetList.planets.append(mars)
    mercury=Planet(0.387*Planet.AU,0,7,DARK_GREY,0.33*10**24,"Mercury")
    mercury.y_velocity=-47.4*1000
    planetList.planets.append(mercury)
    venus=Planet(0.723*Planet.AU,0,8.5,WHITE,4.8685*10**24,"Venus")
    venus.y_velocity=-35.02*1000
    planetList.planets.append(venus)

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        textStartX=20
        textStartY=100
        Distances_title=FONT.render("Distance From Sun",1,YELLOW)
        WIN.blit(Distances_title,(20,50))
        drawStars(WIN)
        for planet in planetList.planets:
            planet.updatePos(planetList.planets)
            planet.draw(WIN)
            if not planet.isSun:
                distanceText=FONT.render(f"{planet.name}: {planet.distToSun} km",1,planet.color)
                WIN.blit(distanceText,(textStartX,textStartY))
                textStartY+=50


        pygame.display.update()

    pygame.quit()


if __name__== "__main__":
    main()
