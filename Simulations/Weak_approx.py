class FloatNum:
    def __init__(self,number,exp_bits=8,man_bits=23):

        self.bias = (2**(exp_bits-1)) - 1
        self.sign = int(number<0)
        self.man_bits = man_bits
        self.exp_bits = exp_bits

        exp = 0
        mod_number = number if number>0 else number*-1
        if(mod_number>1):
            while(mod_number>=2):
                mod_number = mod_number/2
                exp = exp+1
        elif(mod_number==0):
            exp= -1 * self.bias
        else:
            while(mod_number<1):
                if(exp==-126):
                    exp = exp-1
                    break
                mod_number = mod_number*2
                exp = exp-1

        man = mod_number-1 if mod_number>1 else mod_number
        self.mantissa = 0
        for i in range(man_bits):
            self.mantissa = (self.mantissa<<1)+int(man*2)
            man = man*2 - int(man*2)

        self.exp = exp + self.bias

    def add(self,number):
        exp1 = self.exp
        exp2 = number.exp
        d = exp1-exp2
        exp = exp1

        man1 = self.mantissa | (int(exp1>0))<<(self.man_bits)
        man2 = number.mantissa | int(exp2>0)<<(number.man_bits)

        if(d>0):
            man2 = man2>>d
        else:
            d = -1*d
            man1 = man1>>(d)
            exp = exp2
        man = man1+man2
        if(man & 2<<(self.man_bits) != 0):
            man = man>>1
            exp = exp+1
        man = man - (1<<self.man_bits)
        return(self.sign,exp,man)

    def subtract(self,number):
        exp1 = self.exp
        exp2 = number.exp
        d = exp1-exp2
        exp = exp1
        sign = self.sign

        man1 = self.mantissa | int(exp1>0)<<(self.man_bits)
        man2 = number.mantissa | int(exp2>0)<<(number.man_bits)

        if(d>0):
            man2 = man2>>d
        elif(d<0):
            sign = number.sign
            d = -1*d
            man1 = man1>>(d)
            exp = exp2

        if(man2>man1):
            sign = number.sign
            tmp = man1
            man1 = man2
            man2 = tmp

        man = man1-man2
        if(man==0):
            return(sign,0,0)
        for i in range(1,self.man_bits+1):
            if(man & 1<<(self.man_bits-i) != 0):
                man = man<<i
                exp = exp-i
                break            
        man = man - (1<<self.man_bits)
        return(sign,exp,man)

    def multiply(self,number,tuning):
        exp1 = self.exp
        exp2 = number.exp
        exp3 = exp1+exp2-self.bias

        man1 = self.mantissa & (-1<<16)
        man2 = number.mantissa & (-1<<16)

        man3 = (man1+man2)
        if(man3 & 1<<(self.man_bits)):
            exp3 = exp3+1
            man3 = (man3 ^ 1<<(self.man_bits))

        return(self.sign^number.sign,exp3,man3)

    def signed_add(self,number):
        if(self.sign != number.sign):
            return(self.subtract(number))
        else:
            return(self.add(number))

    def SignToBin(self):
        return(self.sign)

    def SignToBin(self):
        return(self.sign)

    def show_num(self,to_print=True):
        num = (2**(self.exp-self.man_bits-self.bias)*(self.mantissa | ((1<<(self.man_bits))*int(self.exp!=0))) * (pow(-1,self.sign)))
        if(self.exp==0):
            num=num*2
        if(to_print==True):
            print(num,end=' ')
        return(num)

    def re_init_num(self,sign,exp,mantissa):
        self.sign = sign
        self.mantissa = mantissa
        self.exp = exp

    def __str__(self):
        return(str(self.show_num(False)))

    def __add__(self,other):
        if(type(other) != FloatNum):
            raise TypeError
        Z = FloatNum(0,self.exp_bits,self.man_bits)
        s,e,m = self.signed_add(other)
        Z.re_init_num(s,e,m)
        return(Z)

    def __sub__(self,other):
        if(type(other) != FloatNum):
            raise TypeError
        Z = FloatNum(0,self.exp_bits,self.man_bits)
        X = FloatNum(0,self.exp_bits,self.man_bits)
        X.re_init_num(other.sign,other.exp,other.mantissa)
        X.sign = 1^X.sign
        s,e,m = self.signed_add(X)
        Z.re_init_num(s,e,m)
        return(Z)        

    def __mul__(self,other):
        if(type(other) != FloatNum):
            raise TypeError
        Z = FloatNum(0,self.exp_bits,self.man_bits)
        s,e,m = self.multiply(other,1)
        Z.re_init_num(s,e,m)
        return(Z)

    def __lt__(self,other):
        Z = self - other
        if(Z.exp==0 and Z.mantissa==0):
            return(False)
        return(bool(Z.sign))

    def __gt__(self,other):
        Z = self - other
        if(Z.exp==0 and Z.mantissa==0):
            return(False)
        return(not bool(Z.sign))

    def __eq__(self,other):
        if(type(self) != type(other)):
            return(False)
        Z = self - other
        if(Z.exp==0 and Z.mantissa==0):
            return(True)
        return(False)

import random
for i in range(1000):
    FpErr = []
    for i in range(0,1000):
        num = random.uniform(0,1000000)
        num2 = random.uniform(0,1000000)
        X = FloatNum(num).multiply(FloatNum(num2))
        num3 = num*num2

        errorX = 100*(num3 - X.show_num(False))/num3
        FpErr.append(abs(errorX))
        if(errorX<0):
            Y = FloatNum(num*num2)
            print(num2,num,Y,Y.mantissa,X,X.mantissa)
            X.mantissa = X.mantissa>>1
            print(X)

    print("Avg:",sum(FpErr)/len(FpErr))
    print("Max:",max(FpErr))

import matplotlib.pyplot as plt

# plt.hist(FpErr)
# plt.show()
