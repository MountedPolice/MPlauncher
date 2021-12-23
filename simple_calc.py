class operation:
    def __init__(self, operation):
        self.operation = operation.split()
        print(self.operation)
        if len(self.operation) == 3:
            if "=" not in self.operation:
                self.operand1 = self.operation[0]
                self.operator = self.operation[1]
                self.operand2 = self.operation[2]
                self.result = self._getResult()
            else:
                self.operand1 = operation[0]
                self.operator = operation[1]
                self.operand2 = operation[2]
                self.result = operation[4]
        elif len(self.operation) == 2:
            self.operand1 = operation[0]
            self.operator = operation[1]
            self.operand2 = 0
            self.result = self._getResult()
        elif len(self.operation) == 1:
            self.operand1 = operation[0]
            self.operator = "+"
            self.operand2 = 0
            self.result = operation[0]
        elif len(self.operation) == 0:
            self.operand1 = "0"
            self.operator = "+"
            self.operand2 = "0"
            self.result = "0"

    def _getResult(self):
        print('TIME TO MATH')
        print(self.operator)
        if self.operator == '+':
            print("OPERATION + ")
            return float(self.operand1) + float(self.operand2)
        elif self.operator == '-':
            return float(self.operand1) - float(self.operand2)
        elif self.operator == '*':
            return float(self.operand1) * float(self.operand2)
        elif self.operator == '/':
            return float(self.operand1) / float(self.operand2)

    def __str__(self):
        return self.operand1 + ' ' + self.operator + ' ' +self.operand2 + ' = ' + str(self.result)