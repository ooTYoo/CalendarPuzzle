from sympy.logic.boolalg import Boolean
from copy import deepcopy
from render import *

# define shape of each piece, starting from (1,1)
piece = dict()
piece["I"] = [(1, i+1) for i in range(4)]
piece["L1"] = [(1, i+1) for i in range(4)] + [(2,1)]
piece["L2"] = [(1, i+1) for i in range(3)] + [(2,1)]
piece["L3"] = [(1, i+1) for i in range(3)] + [(2,1),(3,1)]
piece["z1"] = [(1, i+1) for i in range(2)] + [(2,2),(2,3)]
piece["z2"] = [(1, i+1) for i in range(2)] + [(2,2),(2,3),(2,4)]
piece["z3"] = [(1, i+1) for i in range(2)] + [(2,2),(3,2),(3,3)]
piece["b"] = [(1, i+1) for i in range(3)] + [(2,1),(2,2)]
piece["T"] = [(1, i+1) for i in range(3)] + [(2,2),(3,2)]
piece["n"] = [(1, i+1) for i in range(3)] + [(2,1),(2,3)]

class Transform:
    @staticmethod
    def reflect_x(config_t):
        rn, cn, ps = config_t
        result = [(rn + 1 -a, b) for a,b in ps]
        result.sort(key=lambda x: x[0]*10 + x[1])
        return rn, cn, result

    @staticmethod
    def reflect_y(config_t):
        rn, cn, ps = config_t
        result = [(a, cn + 1 - b) for a, b in ps]
        result.sort(key=lambda x: x[0]*10 + x[1])
        return rn, cn, result

    @staticmethod
    def rotation90(config_t, times):
        rn, cn, ps = config_t
        for _ in range(times):
            rn, cn = cn, rn
        result = []
        for p in ps:
            aa, bb = p
            for _ in range(times):
                aa, bb = bb, -1*aa
            if aa < 0:
                aa += rn + 1
            if bb < 0:
                bb += cn + 1
            result.append((aa,bb))
        result.sort(key=lambda x: x[0]*10 + x[1])
        return rn, cn, result


class Block():
    def __init__(self, layout):
        self.core = layout
        self.row_num = max([a[0] for a in self.core])
        self.col_num = max([a[1] for a in self.core])
        self.cf = False # whether transform will modify private data
        self.config_space = [(self.row_num, self.col_num, layout)]
        self.all_config_available = False

    def set_changeF(self, f:bool):
        self.cf = f

    def to_shape(self):
        return Shape(w=self.col_num, h=self.row_num, pixels=self.core)

    def x_axis_reflect(self):
        ans = Transform.reflect_x((self.row_num, self.col_num, self.core))
        if self.cf:
            self.row_num, self.col_num, self.core = ans
        return ans

    def y_axis_reflect(self):
        ans = Transform.reflect_y((self.row_num, self.col_num, self.core))
        if self.cf:
            self.row_num, self.col_num, self.core = ans
        return ans

    def rotate(self, times):
        ans = Transform.rotation90((self.row_num, self.col_num, self.core),times)
        if self.cf:
            self.row_num, self.col_num, self.core = ans
        return ans

    def is_repeat_pattern(self, config_t):
        for c in self.config_space:
            if self.is_same_patten(config_t, c):
                    return True
        return False

    def is_same_patten(self, pattern1, pattern2):
        rn, cn, ps = pattern1
        rrn, ccn, pps = pattern2
        if rn != rrn or cn != ccn or len(ps) != len(pps):
            return False
        assert id(ps) != id(pps)
        for i in range(len(ps)):
            if ps[i] != pps[i]:
                return False
        return True

    def gen_all_configs(self):
        self.cf = False
        for i in [1,2,3]:
            ans = self.rotate(i)
            if not self.is_repeat_pattern(ans):
                self.config_space.append(ans)

        ref_c = self.x_axis_reflect()
        if not self.is_repeat_pattern(ref_c):
            self.config_space.append(ref_c)
            for i in [1,2,3]:
                ans = Transform.rotation90(ref_c,i)
                if not self.is_repeat_pattern(ans):
                    self.config_space.append(ans)

        self.all_config_available = True

    def gen_shape(self,i):
        assert -1 < i < len(self.config_space)
        rn, cn, ps = self.config_space[i]
        return Shape(w=cn, h=rn, pixels=ps)

    def get_config_num(self):
        return len(self.config_space)

    def get_config_space(self):
        if not self.all_config_available:
            self.gen_all_configs()
        return self.config_space

# gen all the blocks data
blocks = []
#for key in piece.keys():
for key in ["I", "L1", "L2", "L3", "z1", "z2", "z3", "b", "T", "n"]:
        blocks.append(Block(layout=piece[key]))
for b in blocks:
    b.set_changeF(False)
    b.gen_all_configs()

print(len(blocks))

if __name__ == "__main__":
    render = Render()
    for key in list(piece.keys()):
        print(f"-------------{key}---------------")
        b = Block(layout=piece[key])
        if False:
            render.print_shape(b.to_shape())
            render.newline()
            b.set_changeF(True)
            b.rotate(3)
            render.print_shape(b.to_shape())
            render.newline()
        b.gen_all_configs()
        for i in range(b.get_config_num()):
            render.print_shape(b.gen_shape(i))
            render.newline()

        #dbg
        if False:
            print(b.is_same_patten(b.config_space[0], b.config_space[1]))
            print(b.is_same_patten(b.config_space[0], b.config_space[2]))
            print(b.config_space[0])
            print(b.config_space[2])
            b.config_space[0][2].sort(key=lambda x: x[0] + 10*x[1])
            b.config_space[2][2].sort(key=lambda x: x[0] + 10*x[1])
            print(b.config_space[0])
            print(b.config_space[2])

