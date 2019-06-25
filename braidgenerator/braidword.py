import random
from copy import copy, deepcopy
from braidgenerator.decorators.braidword import checkparams_braidword

class BraidWord:
	r"""Encapsulation of a mathematical braid. BraidWord contains a word
	which consists of a list of generators and is a component to be
	used in the MarkovChain.

    Parameters
	----------
        initword : :obj:`list`
            List containing generators to be used as initial word.

    Attributes
	----------
        word : :obj:`list`
            `word` of BraidWord, made up of list containing integer generators

		largestGenerator : :obj:`int`
			Largest Generator in `word`.

		genCount : :obj:`list`
			Array of quantity of generators in `word`.

    """
	@checkparams_braidword
	def __init__(self, initword: list):
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
		r"""
        Dynamically returns the length of the `word`.

        Returns
		-------
            Length of `word`.

        """
		return len(self.word)

	def canCancel(self, index) -> bool:
		r"""
        Boolean stating if cancel at index is a valid move.

        Parameters
    	----------
            index : :obj:`int`
                Index where canCancel is to be checked.

        Returns
		-------
            True if successful, False otherwise.

        """
		word = self.word
		nextIdx = (index + 1) % len(word)
		indexes = [ word[index], word[nextIdx] ]
		if (indexes[0] == -indexes[1]):
			return True
		else:
			return False

	def canTranspose(self, index) -> bool:
		r"""
        Boolean stating if transpose at index is a valid move.

        Parameters
    	----------
            index : :obj:`int`
                Index where canTranspose is to be checked.


        Returns
		-------
            True if successful, False otherwise.

        """
		word = self.word
		indexes = list(map(abs, [word[index], word[(index + 1) % len(word)]]))
		if ( abs(indexes[0] - indexes[1]) > 1 ):
			return True
		else:
			return False

	def canFlip(self, index: int) -> bool:
		r"""
        Function that checks if flip can be performed at index.

        Parameters
    	----------
            index : :obj:`int`
                Index where canFlip is to be checked.


        Returns
		-------
            True if successful, False otherwise.

        """
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
		r"""
        Function to check if destabilize() is a valid move.

		Note
		----
		For consistent Markov probabilities, `largestGenerator` is only \
		checked for at the last index of `word`.


        Returns
		-------
            True if successful, False otherwise.

        """
		# Make sure only one of the largestGenerator exists
		if self.genCount[-1] > 1:
			return False
		else:
			# If largest generator exists at end
			# return True. Else, return False
			if (self.word)[-1] == self.largestGenerator:
				return True
			else:
				return False

	def conjugate(self, index) -> bool:
		r"""
        Method to conjugate the `word` at index.

        Parameters
    	----------
            index : :obj:`int`
                Index where conjugate is to be performed.


        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
		self.word = self.word[index:] + self.word[:index]
		return True

	def cancel(self, index) -> bool:
		r"""
        Performs cancellation of the genrators at index and (index+1) % length
		and decreases length of `word` by two.

        Parameters
    	----------
            index : :obj:`int`
                Index where cancel is to be performed.

            name : :obj:`str`
                The name of the Markov step.

            result : :obj:`bool`
                Boolean representing whether the move was successfully
                executed or not.

        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
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
		r"""
        Insert a generator and its inverse into word. Will insert the
		given generator and its inverse at index and increases `word`
		length by two.

        Parameters
    	----------
            index : :obj:`int`
                Index where insert is to be performed.

            generator : :obj:`int`
                Generator to be inserted into `word`.

        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
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
		r"""
        Transposes generators at index and (index+1) % length.

        Parameters
    	----------
            index : :obj:`int`
                Index where transpose is to be performed.


        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
		if self.canTranspose(index):
			word = self.word
			nextIdx = (index + 1) % len(word)
			word[index], word[nextIdx] = word[nextIdx], word[index]
			return True
		else:
			return False

	def flip(self, index: int) -> bool:
		r"""
        Flips generators at index, (index+1)%length, and (index+2)%length.

        Parameters
    	----------
            index : :obj:`int`
                Index where flip is to be performed.

        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
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
		r"""
        Stabilizes the `BraidWord`, increases `word` length by one,
		and increases `largestGenerator` by one if successful.

        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
		self.largestGenerator += 1
		(self.word).append(self.largestGenerator)
		# Modify genCount
		(self.genCount).append(1)

		return True

	def destabilize(self) -> bool:
		r"""
        Destabilizes the `BraidWord`, decreases `word` length by one,
		and decreases `largestGenerator` if successful.

        Returns
		-------
            Boolean that triggers state of Markov step in
			`logs`.

        """
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

	def crossing_change(self, *, random_index: bool = True, index: int = None):
		r"""
		Performs crossing change on braid. That is, returns a new BraidWord
		with generator at resulting index inverted.

		If random_index is set to True, will select a random index
		in [0, len(self.word)]. Else if random_index is set to False
		then `index` must be set manually.

        Returns
		-------
            BraidWord

        """
		if (random_index == False
			and type(index) != int):
			raise ValueError('crossing_change parameter index must be an '
				+ 'integer value if random_index is set to False.')
		newbraidword = self.word.copy()
		if random_index:
			# Get random index in range of word's length
			random_idx = random.randrange(self.length())
			# Set generator at random index to inverse
			newbraidword[random_idx] = -newbraidword[random_idx]
		else:
			# Set generator at manual index to inverse
			newbraidword[index] = -newbraidword[index]

		return BraidWord(newbraidword)

	def resolution(self, *, random_index: bool = True, index: int = None):
		r"""
		Performs resolution on braid. That is, returns a new BraidWord
		excluding the generator that existed at the resulting index.

		If random_index is set to True, will select a random index
		in [0, len(self.word)]. Else if random_index is set to False
		then `index` must be set manually.

        Returns
		-------
            BraidWord

        """
		if (random_index == False
			and type(index) != int):
			raise ValueError('resolution parameter index must be an '
				+ 'integer value if random_index is set to False.')
		if random_index:
			# Get random index in range of word's length
			random_idx = random.randrange(self.length())
			# Create new BraidWord without generator @ random index
			newbraidword = [gen for idx, gen in enumerate(self.word) if idx != random_idx]
		else:
			# Use input index to create new BraidWord wihtout generator @ index
			newbraidword = [gen for idx, gen in enumerate(self.word) if idx != index]

		return BraidWord(newbraidword)
