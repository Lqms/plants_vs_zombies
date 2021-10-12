import arcade
import time
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Plants VS Zombies"

TIMER_OF_RESPAWN_SUNS=15 #как часто спавнятся солнышки (15)
FREQ_OF_SHOOTING=2 #как часто стреляет горохошутер (2)
TIMER_OF_RESPAWN_ZOMBIES=20 #как часто спавнятся зомби (20). Если делать меньше или больше 20, то нужно менять логику спавна зомби и победы, ибо там на 20 завязано

TIMER_OF_DESPAWN_SUNS=3 #удаление солнышка спустя 3 сек появления

DAMAGE_OF_PEAS = 1 #дамаг горошин (1)
FIRE_PEA_DAMAGE = 3 #под огнем дамаг горошин (3)
DESPAWN_TIME_OF_SUNS=3 #солнышки исчезают через это время (3)

START_VALUE=2500 #стартовые солнышки (300)

ZOMBIE_SPEED=0.2 #скорость движения зомби (0.2)

FREEZING_TIME=20 #насколько замораживает заморозка (20 - примерно 4 секунды)
DD_TIME=40 #сколько действует дд (40 - 8 сек)
SPEED_UP_TIME=40 #сколько действует спидап(40 - 8 сек)

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game = True
        
        self.back = arcade.load_texture("background.jpg")
        self.menu = arcade.load_texture("menu_vertical.png")
        self.h_menu=arcade.load_texture("h_menu.png")
        
        self.plants = arcade.SpriteList()
        self.peas = arcade.SpriteList()
        self.spawns_suns = arcade.SpriteList()
        self.zombies = arcade.SpriteList()
        
        self.zombie_spawn = time.time()
        self.end_game = arcade.load_texture("end.png")
        
        self.seed = None
        self.lawns = []
        self.sun = START_VALUE
        self.killed_zombies = 0
        self.attack_time=TIMER_OF_RESPAWN_ZOMBIES
        
        self.show_menu=False
        self.show_menu_click=0
        self.speed_upgrade=5
        self.damage_upgrade=4
        self.kill_all_upgrade=3
        self.freeze_upgrade=2
        self.money_upgrade=1

        self.freezing = False
        self.time_of_freeze = 0

        self.double_damage = 1
        self.time_of_dd = 0

        self.speed_up=0
        self.time_of_speed_up=0

        self.pick_seed_sound=arcade.load_sound("seed.mp3")
        self.sunspawn_sound=arcade.load_sound("sunspawn.mp3")
        self.peaspawn_sound=arcade.load_sound("peaspawn.mp3")
        self.hit_sound=arcade.load_sound("hit.mp3")
        self.main_theme_sound=arcade.load_sound("grasswalk.mp3")



    # начальные значения
    def setup(self):
        #arcade.play_sound(self.main_theme_sound)
        pass

    # отрисовка
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.back)
        arcade.draw_texture_rectangle(60, 300, 130, 600, self.menu)

        if self.show_menu:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2+50, SCREEN_HEIGHT-35, 900, 70, self.h_menu)
            arcade.draw_text(f"{self.damage_upgrade}", 150, 530, arcade.color.BROWN,50)
            arcade.draw_text(f"{self.speed_upgrade}", 320, 530, arcade.color.BROWN,50)
            arcade.draw_text(f"{self.kill_all_upgrade}", 500, 530, arcade.color.BROWN,50)
            arcade.draw_text(f"{self.freeze_upgrade}", 670, 530, arcade.color.BROWN,50)
            arcade.draw_text(f"{self.money_upgrade}", 850, 530, arcade.color.BROWN,50)
        
        arcade.draw_text(f"{self.sun}", 30, 490, arcade.color.BROWN, 30)
        
        self.plants.draw()
        self.spawns_suns.draw()
        self.peas.draw()
        self.zombies.draw()
        
        if self.seed != None: 
            self.seed.draw()

        if self.game == False:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 500, 400, self.end_game) 

    # игровая логика
    def update(self, delta_time):
        if self.game: 
            self.plants.update_animation()
            self.plants.update()
            self.peas.update()
            self.spawns_suns.update()
            
            self.zombies.update()
            self.zombies.update_animation()
            
            if (time.time() - self.zombie_spawn > self.attack_time) and (self.killed_zombies < 20):
                
                center_y, line = lawn_y(random.randint(30, 520))
                
                #выбор зомбя#
                zombie_type = random.randint(1, 3) 
                if zombie_type == 1: 
                    zombie = OrdinaryZombie(line) 
                elif zombie_type == 2: 
                    zombie = ConeheadZombie(line)
                else: 
                    zombie = BuckheadZombie(line)
                #выбор зомбя#

                zombie.center_y = center_y
                self.zombies.append(zombie)
                self.zombie_spawn = time.time()

        if self.killed_zombies >= 20 and len(self.zombies) == 0: 
            self.end_game = arcade.load_texture("logo.png")
            self.game = False

        if self.time_of_freeze>0:
            self.time_of_freeze-=0.1
        if self.time_of_freeze<=0:
            self.time_of_freeze=0
            self.freezing=False

        if self.time_of_dd>0:
            self.time_of_dd-=0.1
        if self.time_of_dd<=0:
            self.time_of_dd=0
            self.double_damage=1

        if self.time_of_speed_up>0:
            self.time_of_speed_up-=0.1
        if self.time_of_speed_up<=0:
            self.speed_up=0
            self.time_of_speed_up=0

    # нажатить кнопку мыши
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game:
            
            if 10 < x < 110 and 510 < y < 600:
                print("Sun")
                if self.show_menu_click==0:
                    self.show_menu=True
                    self.show_menu_click=1
                else:
                    self.show_menu_click=0
                    self.show_menu=False
            
            if 10 < x < 110 and 370 < y < 480:
                print("SunFlower")
                self.seed = SunFlower()
                arcade.play_sound(self.pick_seed_sound)
                
            if 10 < x < 110 and 255 < y < 365: 
                print("PeaShooter")
                self.seed = PeaShooter()
                arcade.play_sound(self.pick_seed_sound)
                
            if 10 < x < 110 and 140 < y < 250: 
                print("WallNut")
                arcade.play_sound(self.pick_seed_sound)
                self.seed = WallNut()
                
            if 10 < x < 110 and 25 < y < 135: 
                print("Torchwood")
                arcade.play_sound(self.pick_seed_sound)
                self.seed = Torchwood()

            if self.seed != None:  
                self.seed.center_x = x  
                self.seed.center_y = y
                self.seed.alpha = 150

            if (190 < x < 270 and 540 < y < 600) and self.show_menu:
                print("damage")
                if self.damage_upgrade>0 and self.double_damage<2:
                    self.damage_upgrade-=1
                    self.double_damage=2
                    self.time_of_dd=DD_TIME

            if (360 < x < 450 and 540 < y < 600) and self.show_menu:
                print("Speed")
                if self.speed_upgrade>0:
                    self.speed_upgrade-=1
                    self.speed_up=1
                    self.time_of_speed_up=SPEED_UP_TIME

            if (540 < x < 640 and 540 < y < 600) and self.show_menu:
                print("kill_all")
                if self.kill_all_upgrade>0:
                    self.kill_all_upgrade-=1
                    for zombie in self.zombies:
                        zombie.kill()

            if (710 < x < 810 and 540 < y < 600) and self.show_menu:
                print("freeze")
                if self.freeze_upgrade>0 and self.freezing==False:
                    self.freeze_upgrade-=1
                    self.freezing=True
                    self.time_of_freeze=FREEZING_TIME

            if (900 < x < 990 and 540 < y < 600) and self.show_menu:
                print("money")
                if self.money_upgrade>0:
                    self.money_upgrade-=1
                    self.sun+=500
                    
                

        for sun in self.spawns_suns: 
            if sun.left < x < sun.right and sun.bottom < y < sun.top: 
                sun.kill()
                self.sun += 25
                


            

    # движение мыши
    def on_mouse_motion(self, x, y, dx, dy):
        if self.seed != None:  
            self.seed.center_x = x
            self.seed.center_y = y 

    # отпустить кнопку мыши
    def on_mouse_release(self, x, y, button, modifiers):
        if (self.seed != None) and (250 < x < 960) and (30 < y < 526):
            center_x, column = lawn_x(x) 
            center_y, line = lawn_y(y)
            cost = self.seed.cost  
            if (line, column) not in self.lawns and self.sun >= cost:
                self.sun -= cost
                self.lawns.append((line, column)) 
                self.seed.planting(center_x, center_y, line,column)
                self.seed.alpha = 255
                self.plants.append(self.seed) 
                self.seed = None
        elif self.seed is not None and 0 < x < 130: #чтобы отпустить цветок в меню
            self.seed = None
                



class Plant(arcade.AnimatedTimeSprite): 
    def __init__(self, health, cost): 
        super().__init__(0.12) 

        self.health = health
        self.cost = cost 
        self.line = 0 
        self.column = 0
        
    def update(self): 
        if self.health <= 0: 
            self.kill()
            window.lawns.remove((self.line, self.column))

    def planting(self, center_x, center_y, line, column):
        self.center_x = center_x 
        self.center_y = center_y 
        self.line = line 
        self.column = column


class SunFlower(Plant): 
    def __init__(self): 
        super().__init__(health=80, cost=50) 
        self.texture = arcade.load_texture("sun1.png") 
        for i in range(3):
            self.textures.append(arcade.load_texture("sun1.png")) 
        for i in range(3):
            self.textures.append(arcade.load_texture("sun2.png"))
        self.sun_spawn = time.time()

    def update(self): 
        super().update()
        if time.time() - self.sun_spawn >= TIMER_OF_RESPAWN_SUNS:  
            sun = Sun(self.center_x + 20, self.center_y + 30)
            window.spawns_suns.append(sun)
            self.sun_spawn = time.time()
            arcade.play_sound(window.sunspawn_sound)


class Sun(arcade.Sprite): 
    def __init__(self, position_x, position_y): 
        super().__init__("sun.png", 0.12) 
        self.center_x = position_x 
        self.center_y = position_y
        self.despawn_time=time.time()
    def update(self): 
        self.angle += 1
        if time.time()-self.despawn_time>=DESPAWN_TIME_OF_SUNS:
            self.kill()


class PeaShooter(Plant): 
    def __init__(self): 
        super().__init__(health=100, cost=100)
        
        self.texture = arcade.load_texture("pea1.png") 
        for i in range(2): 
            self.textures.append(arcade.load_texture("pea1.png")) 
        for i in range(2): 
            self.textures.append(arcade.load_texture("pea2.png")) 
        for i in range(2): 
            self.textures.append(arcade.load_texture("pea3.png"))
            self.pea_spawn = time.time()

    def update(self): 
        super().update()

        if window.double_damage>1:
            self.angle=-15
        else:
            self.angle=0
        #не стреляем пока нет зомби#
        zombie_on_line = False
        for zombie in window.zombies: 
            if zombie.line == self.line:
                zombie_on_line = True
            
        if time.time() - self.pea_spawn >= (FREQ_OF_SHOOTING-window.speed_up)  and zombie_on_line:  
            pea = Pea(self.center_x + 10, self.center_y + 10) 
            window.peas.append(pea)
            arcade.play_sound(window.hit_sound)
            self.pea_spawn = time.time() 

class Pea(arcade.Sprite): 
    def __init__(self, position_x, position_y): 
        super().__init__("bul.png", 0.12)
        
        self.center_x = position_x
        self.center_y = position_y
        self.damage = DAMAGE_OF_PEAS * window.double_damage 
        self.change_x = 7
        
    def update(self): 
        self.center_x += self.change_x
        
        hits = arcade.check_for_collision_with_list(self, window.zombies)
        if len(hits) > 0: 
            for zombie in hits:  
                zombie.health -= self.damage 
                self.kill()
        
        if self.center_x > SCREEN_WIDTH: 
            self.kill()

        

class Zombie(arcade.AnimatedTimeSprite): 
    def __init__(self, health, line):  
        super().__init__(0.09)
        
        self.health = health 
        self.line = line 
        self.center_x = SCREEN_WIDTH 
        self.change_x = ZOMBIE_SPEED

    def update(self): 
        self.center_x -= self.change_x
        if self.health <= 0:
            self.kill()
            window.killed_zombies += 1
            window.attack_time -= 1 

        #ест растение#
        eating = False

        food = arcade.check_for_collision_with_list(self, window.plants)
        for plant in food:
            if self.line == plant.line: 
                plant.health -= 0.5  
                eating = True
                
        if eating or window.freezing: 
            self.change_x = 0 
            self.angle = 15
        else: 
            self.change_x = ZOMBIE_SPEED 
            self.angle = 0
        #ест растение#
            
        if self.center_x<=200:
            self.kill()
            window.game = False



class OrdinaryZombie(Zombie):
    def __init__(self, line):
        super().__init__(health=12, line=line)
        
        self.texture = arcade.load_texture("zom1.png") 
        for i in range(5):
            self.textures.append(arcade.load_texture("zom1.png"))
        self.textures.append(arcade.load_texture("zom2.png"))

class WallNut(Plant): 
    def __init__(self): 
        super().__init__(health=200, cost=50) 
        self.texture = arcade.load_texture("nut1.png") 
        for i in range(10):
            self.textures.append(arcade.load_texture("nut1.png"))
        self.textures.append(arcade.load_texture("nut2.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("nut3.png"))
        self.textures.append(arcade.load_texture("nut2.png"))

class ConeheadZombie(Zombie): 
    def __init__(self, line): 
        super().__init__(health=20, line=line) 
        self.texture = arcade.load_texture("cone1.png") 
        for i in range(5):
            self.textures.append(arcade.load_texture("cone1.png"))
        self.textures.append(arcade.load_texture("cone2.png"))

class Torchwood(Plant): 
    def __init__(self): 
        super().__init__(health=120, cost=175) 
        self.texture = arcade.load_texture("tree1.png")
        for i in range(2):
            self.textures.append(arcade.load_texture("tree1.png")) 
        for i in range(2): 
            self.textures.append(arcade.load_texture("tree2.png"))  
        for i in range(2):
            self.textures.append(arcade.load_texture("tree3.png")) 

    def update(self): 
        super().update() 
        fire_peas = arcade.check_for_collision_with_list(self, window.peas) 
        for pea in fire_peas:  
            pea.texture = arcade.load_texture("firebul.png") 
            pea.damage = FIRE_PEA_DAMAGE * window.double_damage 

class BuckheadZombie(Zombie): 
    def __init__(self, line): 
        super().__init__(health=32, line=line) 
        self.texture = arcade.load_texture("buck1.png") 
        for i in range(5): 
            self.textures.append(arcade.load_texture("buck1.png")) 
        self.textures.append(arcade.load_texture("buck2.png"))

def lawn_x(x): 
    if 250 < x < 326: 
        column = 1 
        center_x = 283 
    elif 326 < x < 400: 
        column = 2 
        center_x = 360 
    elif 400 < x < 485:
        column = 3 
        center_x = 440 
    elif 485 < x < 560: 
        column = 4 
        center_x = 520 
    elif 560 < x < 640: 
        column = 5 
        center_x = 600 
    elif 640 < x < 715: 
        column = 6 
        center_x = 675 
    elif 715 < x < 785: 
        column = 7 
        center_x = 750 
    elif 785 < x < 870: 
        column = 8 
        center_x = 830 
    elif 870 < x < 960: 
        column = 9 
        center_x = 915 
    return center_x, column 

def lawn_y(y): 
    if 29 < y <= 130: 
        line = 1 
        center_y = 80 
    elif 130 < y <= 220: 
        line = 2 
        center_y = 170 
    elif 220 < y <= 323: 
        line = 3 
        center_y = 270 
    elif 323 < y <= 424: 
        line = 4 
        center_y = 370 
    elif 424 < y <= 527: 
        line = 5 
        center_y = 470 
    return center_y, line 


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
