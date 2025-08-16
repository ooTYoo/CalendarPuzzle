from colored import Fore, Back, Style, back, fore, style
import random
from config import puzzle_grid
import config


def rand_rgb():
    return [random.randint(1,254) for _ in range(3)]
bgclc = [Back.rgb(*rand_rgb()) for _ in range(20)]
basic_style =   [ f"{Fore.rgb(0,0,0)}{Back.rgb(255,255,255)}",
                  f"{Fore.rgb(255,255,255)}{Back.rgb(0,0,0)}",
                  f"{Fore.rgb(0,0,0)}{Back.rgb(0,0,0)}",
                  f"{Fore.white}{Back.pink_1}"]

style_flag = 0

class Shape:
    def __init__(self,w,h,pixels, rev_flag=False):
        self.row = h
        self.col = w
        self.pixels = pixels
        if  rev_flag:
            self.pixels = []
            for i in range(self.row):
                for j in range(self.col):
                    if not (i+1, j+1) in pixels:
                        self.pixels += [(i+1, j+1)]
        self.bc = Back.red
        self.fc = Fore.white
        self.pixel = "[o]"

    def set_color(self,bg=Back.black, fc=Fore.white):
        self.bc = bg
        self.fc = fc

    def set_pixel(self, sym):
        self.pixel = sym


class Render ():
    def __init__(self, pixel="   ", bg=Back.black):
        self.pixel = pixel
        self.bc = bg
        print("")

    def set_color(self, bg:Back):
        self.bc = bg

    def set_pixel(self, sym):
        self.pixel = sym

    def print_shape(self, shape: Shape):
        p1 = f'{shape.fc}{shape.bc}{shape.pixel}{Style.reset}'
        p0 = f'{self.bc}{self.pixel}{Style.reset}'

        for i in range(shape.row):
            for j in range(shape.col):
                if (i+1,j+1) in shape.pixels:
                    print(p1, end="")
                else:
                    print(p0, end="")
            print("")

    def newline(self):
        print("")

    def display_state(self, state):
        global style_flag
        sym = ['xxx', 'DOD','   ']
        for r,a in enumerate(state):
            for c,b in enumerate(a):
                if b == -1:
                    print(f'{basic_style[3]}{puzzle_grid[r][c]}{Style.reset}',end="")
                elif b == -3:
                    print(f'{basic_style[style_flag]}{puzzle_grid[r][c]}{Style.reset}',end="")
                    style_flag = 1 - style_flag
                elif b == -2:
                    print(f'{basic_style[2]}{puzzle_grid[r][c]}{Style.reset}',end="")
                #if b < 0:
                #    c = sym[-1-b]
                #    print(f'{Fore.red}{Back.black}{c}{Style.reset}', end="")
                else:
                    c = f'[{b}]'
                    print(f'{Fore.red}{bgclc[b]}{c}{Style.reset}', end="")
            print()
        print()

    def display_grid(self,grid, constrain =None):
        global style_flag
        rn, cn = len(grid), len(grid[0])
        for r in range(rn):
            for c in range(cn):
                if constrain and ((r+1,c+1) in constrain):
                    sc = basic_style[2]
                else:
                    sc = basic_style[style_flag]
                print(f'{sc}{grid[r][c]}{Style.reset}', end='')
                style_flag = 1-style_flag
            print()
        print()

def test():
    '''test the Render class'''
    render = Render()
    basic_frame = Shape(w=config.width, h=config.height, pixels=config.frame_constrain, rev_flag=False)
    render.print_shape(shape=basic_frame)

    render.newline()
    basic_frame = Shape(w=config.width, h=config.height, pixels=config.frame_constrain, rev_flag=True)
    basic_frame.set_color(bg=Back.red)
    basic_frame.set_pixel("[x]")
    render.set_pixel("   ")
    render.print_shape(shape=basic_frame)

    render.display_grid(config.puzzle_grid, config.frame_constrain)


if __name__ == "__main__":
    test()