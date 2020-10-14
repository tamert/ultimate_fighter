import arcade
import random
import os
cwd = os.getcwd()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
TITLE = "Ultimate Fighter"

SCALE = 0.5

class Fighter(arcade.Sprite):
    def __init__(self, role):
        super().__init__()
        self.cur = 0
        self.textures = []
        if role == 'P':
            texture = arcade.load_texture(os.path.join(cwd, 'res/still1.png'))
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/still2.png'))
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/punch1.png'))
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/punch2.png'))
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/defend.png'))
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/ko.png'))
            self.textures.append(texture)
            self.texture = self.textures[self.cur]
            self.right = 315
        else:
            texture = arcade.load_texture(os.path.join(cwd, 'res/still1R.png'), mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/still2R.png'), mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/punch1R.png'), mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/punch2R.png'), mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/defendR.png'), mirrored=True,)
            self.textures.append(texture)
            texture = arcade.load_texture(os.path.join(cwd, 'res/koR.png'))
            self.textures.append(texture)
            self.texture = self.textures[self.cur]
            self.left = 325
        self.center_y = 250
        self.scale = 1
        self.life = 100
        self.energy = 5

    def update(self, obj):
        if self.life == 0:
            self.texture = self.textures[5]
        else:
            if self.cur <= 1:
                self.cur = (self.cur+1)%2
                self.texture = self.textures[self.cur%2]
            elif self.cur == 4:
                self.energy -= 1
                self.energy = max(0, self.energy)
                self.texture = self.textures[self.cur]
                self.cur = 0
            else:
                self.energy -= 1
                self.energy = max(0, self.energy)
                if obj.cur != 4:
                    obj.life -= 10
                    obj.life = max(0, obj.life)
                self.center_x += -5
                self.texture = self.textures[self.cur]
                self.cur = 0


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.player = None
        self.enemy = None
        self.energy = None
        self.bg = None

    def setup(self):
        self.frame = 0
        self.game = None
        self.fighter_list = arcade.SpriteList()
        self.player = Fighter('P')
        self.enemy = Fighter('E')
        self.energy = arcade.Sprite(os.path.join(cwd, 'res/energy.png'), 0.2)
        self.energy.bottom = 560
        self.energy.left = 10
        self.bg = arcade.load_texture(os.path.join(cwd, 'res/BG.png'))
        self.punch_sound = arcade.load_sound(os.path.join(cwd, 'res/punch.wav'))
        self.grunt_sound = arcade.load_sound(os.path.join(cwd, 'res/grunt.mp3'))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,640,640,self.bg)
        self.player.draw()
        self.enemy.draw()
        self.energy.draw()
        arcade.draw_text('YOU',10,610,arcade.color.BLUE,14,bold=True)
        arcade.draw_text('OPPONENT',530,610,arcade.color.ROSE,14,bold=True)
        arcade.draw_xywh_rectangle_filled(10,590,self.player.life,10,arcade.color.BLUE)
        arcade.draw_xywh_rectangle_filled(630-self.enemy.life,590,self.enemy.life,10,arcade.color.ROSE)
        arcade.draw_text(str(self.player.energy),30,560,arcade.color.BLACK,18,bold=True)
        if self.game == 'Lose':
            texture = arcade.load_texture(os.path.join(cwd, 'res/lose.png'))
            arcade.draw_lrwh_rectangle_textured(192,80,256,128,texture)
        if self.game == 'Won':
            texture = arcade.load_texture(os.path.join(cwd, 'res/won.png'))
            arcade.draw_lrwh_rectangle_textured(192,80,256,128,texture)


    def on_update(self, delta_time):
        if self.game is not None:
            if self.player.life < 1:
                self.player.update(self.enemy)
                self.game = 'Lose'
            elif self.enemy.life < 1:
                self.enemy.update(self.player)
                self.game = 'Won'
            else:
                self.frame += 1
                if self.frame % 10 == 0:
                    if random.randint(0,1) == 1:
                        if self.enemy.energy >0:
                            self.enemy.center_x += 5
                            self.enemy.cur = random.randint(2,3)
                            arcade.play_sound(self.punch_sound)
                    self.player.update(self.enemy)
                    self.enemy.update(self.player)
                if self.frame % 120 == 0:
                    self.player.energy += 1
                    self.player.energy = min(5, self.player.energy)
                    self.enemy.energy += 1
                    self.enemy.energy = min(5, self.enemy.energy)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player.energy > 0:
            self.player.center_x += 5
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.cur = 3
                if self.enemy.energy > 0:
                    self.enemy.cur = random.choice([0,1,4])
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.player.cur = 2
                if self.enemy.energy > 0:
                    self.enemy.cur = random.choice([0,1,4])
            arcade.play_sound(self.punch_sound)

    def on_key_press(self, symbol, modifiers):
        if self.player.energy > 0:
            if symbol == arcade.key.SPACE:
                self.player.cur = 4
                arcade.play_sound(self.grunt_sound)
        if symbol == arcade.key.ENTER:
            self.game = 'Run'

def main():
    window  = MyGame()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
