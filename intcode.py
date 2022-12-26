import operator
import os

class HaltExecution(Exception):
    pass


class Op:
    opcode = None
    n_args = 0
    n_outputs = 0

    def __init__(self, process, args):
        self.process = process
        self.args = args

    def input(self, i):
        return self.process.mem[self.args[i]]

    def format_arg(self, i):
        v = self.args[i]
        s = "r%d" % v
        if i < (self.n_args - self.n_outputs):
            s += "(%d)" % self.process.mem[v]
        return s

    def output(self, i, val):
        self.process.mem[self.args[i]] = val

    def run(self):
        raise NotImplementedError()

    @classmethod
    def opcodes(self):
        opcodes = {}
        for cls in self.__subclasses__():
            if cls.opcode:
                opcodes[cls.opcode] = cls
            opcodes.update(cls.opcodes())
        return opcodes

    @classmethod
    def get(cls, opcode):
        return cls.opcodes()[opcode]


class Infix(Op):
    n_args = 3
    n_outputs = 1
    fn = None
    symbol = None

    def run(self):
        self.output(2, int(self.fn(self.input(0), self.input(1))))

    def __repr__(self):
        return "%s = %s %s %s" % (
            self.format_arg(2),
            self.format_arg(0),
            self.symbol,
            self.format_arg(1),
        )


class Add(Infix):
    opcode = 1
    fn = operator.add
    symbol = '+'


class Mul(Infix):
    opcode = 2
    fn = operator.mul
    symbol = '*'


class Halt(Op):
    opcode = 99

    def run(self):
        raise HaltExecution()

    def __repr__(self):
        return "HALT"


class Process:
    _idx = 0

    def __init__(self, mem, inputs=None, output=None):
        self.idx = self._idx
        type(self)._idx += 1
        self.verbose = os.environ.get('V')
        self.mem = mem
        self.ctr = 0

    def __repr__(self):
        return "%s(%d, c=%d)" % (type(self).__name__, self.idx, self.ctr)

    def dbg(self, *args):
        if self.verbose:
            print(' '.join([str(arg) for arg in [self] + list(args)]))

    def run(self):
        self.dbg("start")
        while True:
            op_type = Op.get(self.mem[self.ctr])
            args = [self.mem[self.ctr + 1 + i] for i in range(op_type.n_args)]
            op = op_type(self, args)
            self.dbg(op)
            try:
                op.run()
            except HaltExecution:
                break
            self.ctr += 1 + op_type.n_args


def run(mem):
    Process(mem).run()


def load(path):
    data = [int(x) for x in open(path).read().split(',')]
    return dict(enumerate(data))
