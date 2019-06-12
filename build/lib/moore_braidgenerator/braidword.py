#!/usr/bin/env python
# BraidWord.py
import random
from copy import copy, deepcopy
from moore_braidgenerator.decorators.braidword import checkparams_braidword

class BraidWord():
	"""Class for working with braids"""
	@checkparams_braidword
	def __init__(self, initword: list):
		"""Construct a BraidWord object using an initial word"""
		self.word = initword
		# self.length = self.wordlength()
		self.largestGenerator = max(list(map(abs, initword)))
		# NOTE genCount[0] will be 1, since there
		# are no generators 0
		self.genCount = self.calcGenCount(initword)

	@staticmethod
	def calcGenCount(generators: list) -> list:
		# NOTE we consider gen and -gen as abs(gen)
		temp = generators.copy()
		temp = list(map(abs, temp))
		genCount = [0] * max(temp)
		for i in temp:
			genCount[i - 1] += 1
		return genCount

	def length(self) -> int:
		"""Returns length of word"""
		return len(self.word)

	def canCancel(self, index) -> bool:
		"""returns a boolean stating if self.cancel(index) is a valid move"""
		word = self.word
		nextIdx = (index + 1) % len(word)
		indexes = [ word[index], word[nextIdx] ]
		if (indexes[0] == -indexes[1]):
			return True
		else:
			return False

	def canTranspose(self, index) -> bool:
		"""returns a boolean stating if self.transpose(index) is a valid move"""
		word = self.word
		indexes = list(map(abs, [word[index], word[(index + 1) % len(word)]]))
		if ( abs(indexes[0] - indexes[1]) > 1 ):
			return True
		else:
			return False

	def canFlip(self, index: int) -> bool:
		"""returns a boolean stating if self.flip(index) is a valid move"""
		l = self.word.copy()
		# positive moves
		condP1 = ( l[index] == l[(index+2) % len(l)] )
		condP2 = abs(l[index] - l[(index+1) % len(l)]) == 1
		# check conditions
		cRight = condP1 and condP2

		if (cRight):
			return True
		else:
			return False

	def canDestabilize(self) -> bool:
		"""returns a boolean stating if self.destabilize() is a valid move.
		For consistent Markov probabilities we only consider end of word.
		"""
		# Make sure only one of the largestGenerator exists
		if self.genCount[-1] > 1:
			return False
		else:
			# If largest generator exists at end
			# return True. Else, return False
			'''
				NOTE if (self.word)[-1] != self.largestGenerator,
				the operation is technically still valid,
				but is not the inverse of @stabilize!
			'''
			if (self.word)[-1] == self.largestGenerator:
				return True
			else:
				return False

	def conjugate(self, idx) -> bool:
		"""conjugate the word by amount"""
		self.word = self.word[idx:] + self.word[:idx]
		return True

	def cancel(self, index) -> bool:
		"""performs a cancelation of the generators at index and (index+1)%length and decreases self.length by 2"""
		if self.canCancel(index):
			word = self.word
			indexes = [index, (index + 1) % len(word)]
			temp = [val for idx, val in enumerate(word) if idx not in indexes]
			self.word = temp
			# Modify genCount
			# NOTE word is used since is unmodified self.word
			self.genCount[abs(word[index]) - 1] -= 2
			return True
		else:
			return False

	def insert(self, index, generator) -> bool:
		"""inserts a generator and its inverse at index and increases self.length by 2"""
		# generator must be | generator| <= |self.largestGenerator|
		if (abs(generator) > abs(self.largestGenerator)):
			raise ValueError("""Absolute value of Generator must be less
			than or equal to self.largestGenerator.""")
		# create gen & inv
		genInsert = [-generator, generator]
		# create object to be returned
		self.word = self.word[:index] + genInsert + self.word[index:]
		# Modify genCount
		self.genCount[generator - 1] += 2
		return True

	def transpose(self, index) -> bool:
		"""transposes generators at index and (index+1)%length"""
		if self.canTranspose(index):
			word = self.word
			nextIdx = (index + 1) % len(word)
			word[index], word[nextIdx] = word[nextIdx], word[index]
			return True
		else:
			return False

	def flip(self, index: int) -> bool:
		"""flips generators at index, (index+1)%length, and (index+2)%length"""
		l = self.word
		idx0 = index
		idx1 = (index+1)%len(l)
		idx2 = (index+2)%len(l)

		if ( self.canFlip(index) ):
			# Perform flip
			l[idx0], l[idx1], l[idx2] = l[idx1], l[idx0], l[idx1]

			# Modify genCount
			# NOTE genCount[l[idx0]] == genCount[l[idx2]]
			# NOTE idx0 and idx1 do not change, but l[idx0]
			# and l[idx1] do change
			# NOTE abs() handles negative generators
			self.genCount[abs(l[idx1])-1] -= 1
			self.genCount[abs(l[idx0])-1] += 1
			return True
		else:
			return False


	def stabilize(self) -> bool:
		"""stabilize the braid word, increase self.length by 1, and increase self.largestGenerator"""
		self.largestGenerator += 1
		(self.word).append(self.largestGenerator)
		# Modify genCount
		(self.genCount).append(1)

		return True

	def destabilize(self) -> bool:
		"""destabilize the braid word and decrease self.length by 1, and possibly decrease self.largestGenerator"""
		'''NOTE
		Destabilization can leave a hidden largest generator,
		i.e. when there is a split link with an unknotted component.
		'''
		if self.canDestabilize():
			# Pop largest generator and decrement self.largestGenerator
			(self.word).pop()
			self.largestGenerator -= 1
			# Modify genCount
			(self.genCount).pop()
			return True
		else:
			return False

	def __str__(self):
		return str(self.word)

	def __copy__(self):
		cls = self.__class__
		result = cls.__new__(cls)
		result.__dict__.update(self.__dict__)
		return result

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		for k, v in self.__dict__.items():
			setattr(result, k, deepcopy(v, memo))
		return result
