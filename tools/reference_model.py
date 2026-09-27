#!/usr/bin/env python3
from dataclasses import dataclass, field
OP_NOP=0x0; OP_LDI=0x1; OP_ADDI=0x2; OP_SUBI=0x3
OP_XORI=0x4; OP_ANDI=0x5; OP_ORI=0x6; OP_STORE=0x7
OP_LOAD=0x8; OP_JMP=0x9; OP_JZ=0xA; OP_INC=0xB
OP_DEC=0xC; OP_SHL=0xD; OP_SHR=0xE; OP_HALT=0xF
@dataclass
class CPU:
    pc:int=0; acc:int=0; halted:int=0
    regs:list[int]=field(default_factory=lambda:[0]*4)
    prog:list[int]=field(default_factory=lambda:[0]*8)
    def step(self):
        if self.halted: return
        instr=self.prog[self.pc&7]; op=(instr>>4)&0xf; arg=instr&0xf; r=instr&3
        np=(self.pc+1)&7
        if op==OP_HALT: self.halted=1; return
        if op==OP_JMP: self.pc=arg&7; return
        if op==OP_JZ and self.acc==0: self.pc=arg&7; return
        if op==OP_STORE: self.regs[r]=self.acc; self.pc=np; return
        if op==OP_LDI: self.acc=arg
        elif op==OP_ADDI: self.acc=(self.acc+arg)&0xff
        elif op==OP_SUBI: self.acc=(self.acc-arg)&0xff
        elif op==OP_XORI: self.acc^=arg
        elif op==OP_ANDI: self.acc&=arg
        elif op==OP_ORI: self.acc|=arg
        elif op==OP_LOAD: self.acc=self.regs[r]
        elif op==OP_INC: self.acc=(self.acc+1)&0xff
        elif op==OP_DEC: self.acc=(self.acc-1)&0xff
        elif op==OP_SHL: self.acc=(self.acc<<1)&0xff
        elif op==OP_SHR: self.acc=(self.acc>>1)&0xff
        self.acc&=0xff; self.pc=np

def main():
    for acc in range(256):
        for arg in range(16):
            cases=[(OP_LDI,arg),(OP_ADDI,(acc+arg)&255),(OP_SUBI,(acc-arg)&255),
                   (OP_XORI,acc^arg),(OP_ANDI,acc&arg),(OP_ORI,acc|arg)]
            for op,expected in cases:
                c=CPU(acc=acc); c.prog[0]=(op<<4)|arg; c.step()
                assert c.acc==expected and c.pc==1
        for op,expected in [(OP_INC,(acc+1)&255),(OP_DEC,(acc-1)&255),
                            (OP_SHL,(acc<<1)&255),(OP_SHR,(acc>>1)&255)]:
            c=CPU(acc=acc); c.prog[0]=op<<4; c.step()
            assert c.acc==expected and c.pc==1
    for target in range(8):
        c=CPU(acc=1); c.prog[0]=(OP_JMP<<4)|target; c.step(); assert c.pc==target
        c=CPU(acc=0); c.prog[0]=(OP_JZ<<4)|target; c.step(); assert c.pc==target
        c=CPU(acc=1); c.prog[0]=(OP_JZ<<4)|target; c.step(); assert c.pc==1
    for r in range(4):
        c=CPU(acc=0x40+r); c.prog[0]=(OP_STORE<<4)|r; c.step(); assert c.regs[r]==0x40+r
        c=CPU(); c.regs[r]=0x90+r; c.prog[0]=(OP_LOAD<<4)|r; c.step(); assert c.acc==0x90+r
    print("FORGECPU-TT1 REFERENCE MODEL PASS")
if __name__=="__main__": main()
