#!/usr/bin/env python

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
			def operate(a, b):
				return a + b
		elif val == "-":
			def operate(a, b):
				return a - b
		elif val == "*":
			def operate(a, b):
				return a * b
		elif val == "/":
			def operate(a, b):
				return a / float(b)
		self.operate = operate
		

def construct_postfix(numbers, operators):
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
	
	return tuple(pfix_exp)

def eval_postfix(pfix):
	pfix = list(pfix)
	while len(pfix) > 1:
		for i in range(0, len(pfix)):
			if type(pfix[i]) is operator:
				try:
					result = pfix[i].operate(pfix.pop(i-2), pfix.pop(i-2))
				except ZeroDivisionError:
					return None
				
				pfix[i-2] = result
				break
	
	if not float(pfix[0]).is_integer():
		return None
	
	return int(pfix[0])

def postfix_to_infix(pfix):
	pass

def operator_combinations(num):
	operators = itertools.product(operator.__members__.values(),[True,False])
	operator_combinations = itertools.product(operators, repeat=num)
	pfix_tests = set()
	for ops in operator_combinations:
		test_pfix = construct_postfix([1] * (num + 1), ops)
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
		yield construct_postfix(nums,ops)

nums = [ int(i) for i in sys.argv[1:] ]
target = nums.pop(len(nums)-1)

op_combs = operator_combinations(len(nums) - 1)
num_combs = number_combinations(nums)
exps = expression_combinations(num_combs, op_combs)

count = 0
for e in exps:
	count += 1
	result = eval_postfix(e)
	if result == target:
		print("%s = %s" % (str(e),result))
		break

print(count)