#!/usr/bin/env python3

import sys
import itertools
import enum

class operator(enum.Enum):
	ADD      = "+"
	SUBTRACT = "-"
	MULTIPLY = "*"
	DIVIDE   = "/"
	def __init__(self, val):
		if val == "+":
			operate = lambda a, b : a + b
		elif val == "-":
			operate = lambda a, b : a - b
		elif val == "*":
			operate = lambda a, b : a * b
		elif val == "/":
			operate = lambda a, b : a / float(b)
		self.operate = operate
	
	def __str__(self):
		return self.value

class postfix:
	def __init__(self, numbers, operators):
		#
		# Postfix expression always starts with the first 2 numbers
		# Add the first number now and then we can add another number
		# for each operator
		#
		pfix_exp = numbers[:1]
		#
		# Now the rest of the expression will depend on the operators
		# Operators can be either between numbers or at the end
		#
		pfix_ops = []
		for idx in range(0, len(operators)):
			num = numbers[idx+1]
			op = operators[idx]
			pfix_exp.append(num)
			if op[1]:
				pfix_ops.append(op[0])
			else:
				pfix_exp.append(op[0])
		
		pfix_exp.extend(pfix_ops)
		
		self.contents = tuple(pfix_exp)
	
	def __str__(self):
		return " ".join([ str(elem) for elem in self.contents ])
	
	def evaluate(self):
		pfix = list(self.contents)
		pfix_len = len(pfix)
		start_index = 2
		while pfix_len > 2:
			for i in range(start_index, pfix_len):
				if type(pfix[i]) is operator:
					try:
						result = pfix[i].operate(pfix.pop(i-2), pfix.pop(i-2))
					except ZeroDivisionError:
						return None
					
					pfix[i-2] = result
					start_index = i - 1
					pfix_len -= 2
					break
		
		return pfix[0]
	
	def to_infix(self):
		infix = list(self.contents)
		for i in range(0, len(infix)):
			if type(infix[i]) is operator:
				infix[i] = infix[i].value
		return infix

def operator_combinations(num):
	operators = itertools.product(operator.__members__.values(),[True,False])
	operator_combinations = itertools.product(operators, repeat=num)
	pfix_tests = set()
	for ops in operator_combinations:
		test_pfix = postfix([1] * (num + 1), ops)
		if test_pfix not in pfix_tests:
			pfix_tests.add(test_pfix)
			yield(ops)

def number_combinations(numbers):
	coms = itertools.permutations(numbers)
	for com in coms:
		yield list(com)

def expression_combinations(num_combs, op_combs):
	exps = itertools.product(num_combs, op_combs)
	for nums,ops in exps:
		yield postfix(nums,ops)

nums = [ int(i) for i in sys.argv[1:] ]
target = nums.pop(len(nums)-1)

op_combs = operator_combinations(len(nums) - 1)
num_combs = number_combinations(nums)
exps = expression_combinations(num_combs, op_combs)

count = 0
for e in exps:
	count += 1
	#if count == 1000000:
	#	break
	result = e.evaluate()
	if result == target:
		print("%s = %s" % (e, result))
		break
else:
	print("No solution")
