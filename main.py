import render
import solution
import pieces
import datetime

def solve_puzzle(y=2025,m=8,d=16):
    '''solve the puzzle with DFS'''
    solver = solution.Solution()
    solver.init_state()
    solver.setup_target_date(y,m, d)
    q = solver.DFS()
    cstr = "" if q else "not "
    print(f"[*]{cstr} find solution")
    return solver

def test(y,m,d):
    '''test the solution'''
    import time
    start_time = time.perf_counter()
    solver = solve_puzzle(y, m, d)
    end_time = time.perf_counter()
    print(f"total {solver.cnt} steps, cost {end_time - start_time:.4f} seconds")
    solver.show_state()

    screen = render.Render()
    screen.newline()
    screen.display_state(solver.state)

def main(argv=None):
    '''main function to run the solution'''
    tdate = datetime.date.today()
    y,m,d = tdate.year, tdate.month, tdate.day
    try:
        if len(argv) == 1:
            args = argv[0].split('-')
            if len(args) == 2:
                m, d = map(int, args)
                y = 2025
            elif len(args) == 3:
                y, m, d = map(int, args)
            else:   
                y, m, d = 2025, 8, 16
        print(f"Solving puzzle for {y}-{m:02d}-{d:02d}")
        test(y, m, d)
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        print('''Usage: python main.py [[year-]month-day]
              e.g. python main.py 2025-8-16, or 
                   python main.py 8-16  (default year is 2025), or
                   python main.py       (default date is taday)''')
    

if __name__ == '__main__':
    import sys
    main(sys.argv[1:] )