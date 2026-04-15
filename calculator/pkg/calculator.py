class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        output_queue = []
        operator_stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                output_queue.append(float(token))
            elif token in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], 0) >= self.precedence.get(token, 0)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                else:
                    raise ValueError("Mismatched parentheses")
            else:
                raise ValueError(f"Unknown token: {token}")
            i += 1

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output_queue.append(operator_stack.pop())

        return self._evaluate_rpn(output_queue)

    def _evaluate_rpn(self, rpn_tokens):
        operand_stack = []
        for token in rpn_tokens:
            if isinstance(token, float):
                operand_stack.append(token)
            else:
                operator = token
                if len(operand_stack) < 2:
                    raise ValueError("Invalid RPN expression: not enough operands for operator")
                b = operand_stack.pop()
                a = operand_stack.pop()
                result = self.operators[operator](a, b)
                operand_stack.append(result)
        if len(operand_stack) != 1:
            raise ValueError("Invalid RPN expression: too many operands")
        return operand_stack[0]
