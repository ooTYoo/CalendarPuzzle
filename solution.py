# this part is the algorithm to solve the puzzle
import config
import pieces
import copy
from queue import  Queue
from datetime import date, timedelta
import time


class Solution:
    def __init__(self):
        self.w = config.width
        self.h = config.height
        self.step = -1
        self.state = []
        self.next_pos = None
        self.cnt = 0
        self.sol = []

    def init_state(self):
        self.state = [[-3 for _ in range(self.w)]
                      for _ in range(self.h)]
        for r,c in config.frame_constrain:
            self.state[r-1][c-1] = -2 # not fillable
        self.step = 0
        self.sol = []
        self.cnt = 0
        self.next_pos = self.next_position()

    def setup_target_date(self, y=2025, m=8, d=1):
        target = config.get_date_constrain(y, m, d)
        for r,c in target:
            self.state[r-1][c-1] = -1 # target
        self.next_pos = self.next_position()

    @staticmethod
    def shift_config(r,c,config_t):
        '''re calculate new pixels, (r,c) is the coordinate of left-top cornor
            If the Frame are out of Box, return None'''
        rn, cn, ps = config_t
        if r < 3 and  (cn + c ) > config.width:
            return None
        if (cn + c - 1 > config.width) or ( c < 1)  or (rn + r - 1 > config.height):
            return None
        result = [(a + r - 1, b + c -1) for a,b in ps]
        return rn, cn, result

    def is_placing_ok(self, config_t):
        self.cnt += 1
        for r,c in config_t[2]:
            if r-1 <0 or  c-1 < 0:
                return False
            if self.state[r-1][c-1] != -3:
                return False
        return True

    def update_state(self, config_t):
        for ps in config_t[2]:
            self.state[ps[0]-1][ps[1]-1] = self.step
        self.step += 1

    def next_position(self):
        for r in range(config.height):
            for c in range(config.width):
                if self.state[r][c] == -3:
                    return r + 1, c + 1
        return None

    def get_allowed_config_and_offset(self, r, c, shape:pieces.Block):
        allowed_index = [] # (config_index, off_set)
        confs = shape.get_config_space()
        for i in range(len(confs)):
            k = confs[i][2][0][1] - 1
            tmp = Solution.shift_config(r,c-k, confs[i])
            if tmp is None:
                continue
            if self.is_placing_ok(tmp):
                allowed_index.append((i, k))
        return allowed_index

    def get_allowed_config_and_offset_2(self, r, c, shape:pieces.Block):
        allowed_index = [] # (config_index, off_set)
        for i, conf in enumerate(shape.get_config_space()):
            cn = conf[1]
            for k in range(cn):
                tmp = Solution.shift_config(r,c-k, conf)
                if tmp is None:
                    continue
                if self.is_placing_ok(tmp):
                    allowed_index.append((i, k))
        return allowed_index

    def update_sol(self, r, c, i_shape, i_conf, offset):
        config_space = pieces.blocks[i_shape].get_config_space()
        config_t = config_space[i_conf]
        tmp = Solution.shift_config(r, c-offset, config_t)
        assert tmp is not None
        self.update_state(tmp)
        self.sol.append((i_shape, i_conf, offset))
        self.next_pos = self.next_position()

    def pack_state(self):
        pack = {"step": self.step,
                "sol": copy.deepcopy(self.sol),
                "state": copy.deepcopy(self.state),
                "next_pos": self.next_pos
                }
        return pack

    def load_state(self,pack):
        self.step = pack['step']
        self.sol = copy.deepcopy(pack['sol'])
        self.state = copy.deepcopy(pack['state'])
        self.next_pos  = pack['next_pos']

    def BFS(self):
        q = Queue()
        q.put(self.pack_state())
        while True:
            if q.qsize() == 0:
                print("[!] No solution found, quit")
                return 0
            node =  q.get()
            if node['step'] == 10:
                q.put(node)
                return q
            used_shape = [a[0] for a in node['sol']]
            for i_shape in range(10):
                if i_shape in used_shape:
                    continue
                self.load_state(node)
                shape = pieces.blocks[i_shape]
                r,c = self.next_pos
                allowed_config_and_offset = self.get_allowed_config_and_offset(r,c, shape)
                load_state_flag = True
                for i_conf, offset in allowed_config_and_offset:
                    if not load_state_flag:
                        self.load_state(node)
                    self.update_sol(r, c, i_shape, i_conf, offset)
                    # self.show_state()
                    q.put(self.pack_state())
                    load_state_flag = False

    def DFS_recursive(self, shape_index_array):
        # self.show_state()
        if len(shape_index_array)==0:
            return True

        packed = None
        for i, i_shape in enumerate(shape_index_array):
            shape = pieces.blocks[i_shape]
            confs = shape.get_config_space()
            # store for recovery
            packed1 = self.pack_state()
            if i == 0:
                remain_shape_array = shape_index_array[1:]
            elif i==len(shape_index_array)-1:
                remain_shape_array = shape_index_array[:i-1]
            else:
                remain_shape_array = shape_index_array[0:i] + shape_index_array[i+1:]

            for i_config in range(len(confs)):
                if self.step == 10:
                    break
                r, c = self.next_pos
                conf = confs[i_config]
                offset = conf[2][0][1] - 1
                #check if current config ok
                tmp = Solution.shift_config(r, c - offset, conf)
                if tmp and self.is_placing_ok(tmp):
                    packed2 = self.pack_state()
                    self.update_sol(r,c, i_shape, i_config, offset)
                    self.DFS_recursive(remain_shape_array)
                    if self.step == 10:
                        return 0
                    self.load_state(packed2)

            if self.step == 10:
                return 1
            #backtracing
            self.load_state(packed1)
            self.next_pos = self.next_position()

    def DFS(self):
        self.DFS_recursive([i for i in range(10)])
        return self.next_position() is None

    def show_state(self):
        print()
        sym = ["D", "X", " "]
        for a in self.state:
            for b in a:
                c = b
                if b < 0:
                    c = sym[-1-b]
                print(f"[{c}]",end="")
            print()



def test_DFS_over_year(year=2025):
    sol = Solution()
    sol.init_state()

    day_begin = date.fromisoformat(f"{year}-01-01")
    day_cnt = date.fromisoformat(f"{year}-12-31")
    day_range = day_cnt.timetuple().tm_yday
    delta = timedelta(days=1)
    day_test = day_begin
    for i in range(day_range):
        sol.init_state()
        sol.setup_target_date(m=day_test.month, d=day_test.day)
        if not sol.DFS():
            print("\n[!] DFS solver fails for date-", day_test.strftime("%y-%m-%d"))
        else:
            print(".",end="")
        if i%15==0:
            print()
        day_test += delta

def test_BFS():
    solver = Solution()
    solver.init_state()
    solver.setup_target_date(m=8, d=9)
    solver.show_state()
    start_time = time.perf_counter()
    # BFS
    q = solver.BFS()
    end_time = time.perf_counter()
    print(f"total {q.qsize()} solutions, cost {end_time - start_time}")
    solver.show_state()


def test_DFS():
    solver = Solution()
    solver.init_state()
    solver.setup_target_date(m=8, d=9)
    solver.show_state()
    start_time = time.perf_counter()
    q = solver.DFS()
    end_time = time.perf_counter()
    print(f"total {solver.cnt} steps, cost {end_time - start_time}")
    rslt = "can" if q else "can not"
    print(f"[!] DFS Algorithm {rslt} find answer")
    solver.show_state()


if __name__ == "__main__":
    print("Testing DFS") 
    test_DFS()
    print("Testing BFS") 
    test_BFS()
    print("Tes ting over year 2025") 
    test_DFS_over_year(2025)