from colored import Fore, Back, Style
import random
import datetime
# Frame info
width = 7
height = 8
frame_constrain = [(1, 7), (2, 7), (8, 1), (8, 2), (8, 3), (8, 4)]

def gen_calendar_constrain(m,d,wd):
    c_m = (m//6 + 1,m%6)
    c_d = (d//7 + 3, d%7)
    if wd < 4:
        c_wd = (7, 4 + wd)
    else:
        c_wd = (8, wd+1)
    return [c_m, c_d, c_wd]

def get_date_constrain(y=2025, m=8, d=1):
    dd = datetime.date(y,m,d)
    return gen_calendar_constrain(dd.month, dd.day, dd.weekday())

puzzle_grid = [
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'xxx'],
    ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'xxx'],
    [f' 0{i + 7*0}'[:3] for i in range(7)],
    ['08 ', ' 09', ' 10', ' 11', ' 12', ' 13', ' 14'],
    [f' {i + 7*2}' for i in range(7)],
    [f' {i + 7*3}' for i in range(7)],
    [' 29', ' 30', ' 31', 'Mon', 'Tue', 'Wed', 'Thu'],
    ['xxx', 'xxx', 'xxx', 'xxx', 'Fri', 'Sat', 'Sun']
]

if __name__ == '__main__':
    print(gen_calendar_constrain(8,1,0))

    import pprint
    pprint.pp(puzzle_grid)