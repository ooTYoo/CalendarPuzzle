import render
import solution
import pieces

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import time
    solver = solution.Solution()
    solver.init_state()
    solver.setup_target_date(m=8, d=9)
    solver.show_state()
    start_time = time.perf_counter()
    # DFS
    q = solver.DFS(list(range(10)))
    end_time = time.perf_counter()
    print(f"total {solver.cnt} steps, cost {end_time - start_time}")
    solver.show_state()

    screen = render.Render()
    screen.newline()
    screen.display_state(solver.state)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/


