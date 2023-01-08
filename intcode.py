import operator
import os

class HaltExecution(Exception):
    pass


class BlockedOnInput(Exception):
    pass


POS, IMM, REL = range(3)
class Op:
    opcode = None
    n_args = 0
    n_outputs = 0

    def __init__(self, process, mode_mask, args):
        self.process = process
        self.args = args
        self.modes = self.parse_modes(mode_mask)

    def parse_modes(self, mode_mask):
        modes = []
        i = 0
        for _ in range(len(self.args)):
            mode_mask, mode = divmod(mode_mask, 10)
            modes.append(mode)
        return modes

    def input(self, i):
        v = self.args[i]
        if self.modes[i] == IMM:
            return v
        if self.modes[i] == REL:
            v += self.process.rel_base
        return self.process.mem.get(v, 0)

    def format_arg(self, i):
        v = self.args[i]
        if self.modes[i] == IMM:
            return str(v)
        if self.modes[i] == POS:
            s = "r%d" % v
        else:
            s = "r(%d+%d=%d)" % (v, self.process.rel_base, v + self.process.rel_base)
            v += self.process.rel_base
        if i < (self.n_args - self.n_outputs):
            s += "(%d)" % self.process.mem.get(v, 0)

    def output(self, i, val):
        assert self.modes[i] != IMM
        addr = self.args[i]
        if self.modes[i] == REL:
            addr += self.process.rel_base
        self.process.mem[addr] = val

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


class Input(Op):
    opcode = 3
    n_args = 1
    n_outputs = 1

    def run(self):
        if not self.process.inputs:
            raise BlockedOnInput()
        self.output(0, self.process.inputs.pop(0))

    def __repr__(self):
        return "%s = INPUT" % (self.format_arg(0),)


class Output(Op):
    opcode = 4
    n_args = 1

    def run(self):
        self.process.outputs.append(self.input(0))

    def __repr__(self):
        return "OUTPUT %s" % (self.format_arg(0),)


class JmpT(Op):
    opcode = 5
    n_args = 2

    def run(self):
        if self.input(0):
            self.process.ctr = self.input(1) - 1 - self.n_args

    def __repr__(self):
        return "JMP(%s) if %s" % (self.format_arg(1), self.format_arg(0))


class JmpF(Op):
    opcode = 6
    n_args = 2

    def run(self):
        if not self.input(0):
            self.process.ctr = self.input(1) - 1 - self.n_args

    def __repr__(self):
        return "JMP(%s) if not %s" % (self.format_arg(1), self.format_arg(0))


class LT(Infix):
    opcode = 7
    fn = operator.lt
    symbol = '<'


class EQ(Infix):
    opcode = 8
    fn = operator.eq
    symbol = '=='


class RelAdj(Op):
    opcode = 9
    n_args = 1

    def run(self):
        self.process.rel_base += self.input(0)

    def __repr__(self):
        return "RELADJ(%s)" % (self.format_arg(0),)


class Halt(Op):
    opcode = 99

    def run(self):
        raise HaltExecution()

    def __repr__(self):
        return "HALT"


class Process:
    _idx = 0

    def __init__(self, mem, inputs=None):
        self.idx = self._idx
        type(self)._idx += 1
        self.verbose = os.environ.get('V')
        self.inputs = inputs or []
        self.outputs = []
        self.mem = mem
        self.ctr = 0
        self.rel_base = 0
        self.state = 'new'

    def __repr__(self):
        return "%s(%d, c=%d, state=%r)" % (type(self).__name__, self.idx, self.ctr, self.state)

    def dbg(self, *args):
        if self.verbose:
            print(' '.join([str(arg) for arg in [self] + list(args)]))

    def write_stdin(self, text):
        self.inputs += [ord(c) for c in text]

    def read_stdout(self):
        text = ''.join(map(chr, self.outputs))
        self.outputs.clear()
        return text

    def run(self, inputs=None):
        if isinstance(inputs, int):
            self.inputs.append(inputs)
        elif inputs:
            if isinstance(inputs, str):
                inputs = [ord(c) for c in inputs]
            self.inputs += inputs
        if self.state == 'new':
            self.dbg("start")
        self.state = 'running'
        while True:
            mode_mask, opcode = divmod(self.mem[self.ctr], 100)
            op_type = Op.get(opcode)
            args = [self.mem[self.ctr + 1 + i] for i in range(op_type.n_args)]
            op = op_type(self, mode_mask, args)
            self.dbg(op)
            try:
                op.run()
            except HaltExecution:
                self.state = 'done'
                break
            except BlockedOnInput:
                self.dbg("blocked on input")
                break
            self.ctr += 1 + op_type.n_args


def run(mem, inputs=None):
    proc = Process(mem, inputs)
    proc.run()
    return proc.outputs


def load(path):
    data = [int(x) for x in open(path).read().split(',')]
    return dict(enumerate(data))
