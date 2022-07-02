class Security():
    def inputs(self,input):
        black=[">","<","{","}","&"]
        if len(input) < 64:
            for bc in black:
                if input.find(bc) >= 0:
                    return False
                else:
                    return True
        else:
            return False

