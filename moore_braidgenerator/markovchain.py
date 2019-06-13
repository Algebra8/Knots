import random
import copy
import pandas as pd
import functools
from copy import copy, deepcopy
from moore_braidgenerator.braidword import BraidWord
from moore_braidgenerator.decorators.markovchain import checkparams_markovchain


class MarkovChain:
    """MarkovChain is an encapsulation of the Markov Chain.
    It takes a BraidWord and allows modelling, which creates
    a specified number of isomorphs along with the logs pertaining
    to that isomorph (i.e. which Markov Move was made at some iteration).

    Args:
        braidword (BraidWord): A BraidWord to have isomorphs generated
        from it. Note that a simple Python list can be given as a
        parameter as well, which will be converted to a BraidWord behind
        the scenes.

        maxgen (int): The maximum absolute value a generator can be in the
        BraidWord and its subsequent isomorphisms.

        maxlen (int): The maxmimum length of that any subsequent isomorphs
        can reach.

    Attributes:
        word (list): A list containing generators.
        largestGenerator (int): The largest generator of the absolute value
		of generators in the word.
		genCount (list): A list containing quantities of generators that
		exist in word, indexed from generator number minus one.

	Examples:
		>>> mc = MarkovChain(braidword=[1, 2, 3], maxgen=9, maxlen=10)
        >>> mc.braid.word
		[1, 2, 3]

		>>> mc.maxgen
		9

		>>> mc.maxlen
		10
    """
    @checkparams_markovchain
    def __init__(self, braidword: BraidWord,
                 maxgen: int = 9, maxlen: int = 10):
        # braidword
        self.braid = braidword
        # max generators
        self.maxgen = maxgen
        # max length of braidword
        self.maxlen = maxlen
        # braid aggregate
        self.braidagg = {
            # list of isomorphs
            'isomorphs': [],
            # list of logs
            'logs': []  # holds dict
        }

    @staticmethod
    def log_message(movetype: int, name: str, result: bool) -> str:
        """Function to dynamically create log of move @mstep

        Args:
            movetype (int): Markov Move[i] for i in [0, 6], inclusive. There
            are 7 Markov Moves that determine the braid-to-isomorph modification.

            name (str): The name of the Markov Move.

            result (bool): Boolean representing whether the move was successfully
            executed or not.

        Returns:
            String of log for BraidWord.word at Markov Move [i] for
            i in [0, 6], inclusive.

        """
        beg = f"MoveType: {str(movetype)}, "
        tmp = f"Attempted {name}: "
        if result == True:
            tmp += name + " Succeeded."
        else:
            tmp += name + " Failed."

        return beg + tmp

    def model(self, num_isomorphs: int = 1, msteps: int = 100):
        '''
        Method to model the BraidWord and generate isomorphs and logs.

        A random number is picked between (0, 6), inclusive, determining the
        Markov Move to perform.

        Another random number is picked from range(len(BraidWord.word)) that
        represents the index of BraidWord.word to perform the Markov Move on.

        The isomorph is generated by picking a random index from the set
        of possible indices for BraidWord.word and a random Markov Move that
        acts on BraidWord.word at the given index.

        Args:
            num_isomorphs (int): Number of isomorphs to be modeled from
            the BraidWord given to the Markov Chain.

            msteps (int): The number of steps to be taken until an isomorph
            is considered to be complete. That is, msteps many iterations
            of the model process take place on a given BraidWord.

        Returns:
            Appends isomorph and log to self.braidagg.
        '''
        # msteps: number of markov steps per iteration
        # num_isomorphs: number of isomorphisms (iterations) to create
        rr = random.randrange  # Consider resetting seed
        for _ in range(num_isomorphs):
            braid = self.braid  # Not copied purposefully
            log = {}
            # Perform markov moves on braid
            for step in range(msteps):
                movetype = rr(7)
                index = rr(braid.length())
                if movetype == 0:
                    if braid.conjugate(index):
                        # append logs success
                        log[step] = self.log_message(movetype, braid.conjugate.__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, braid.conjugate.__name__, False)

                elif movetype == 1:
                    # Do not cancel if braid length is 2: unknot
                    if braid.length() == 2 and braid.canCancel(index):
                        log[step] = self.log_message(movetype, (braid.cancel).__name__, False)
                        log[step] += 'Unknot'
                        continue
                    elif braid.cancel(index):
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.cancel).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.cancel).__name__, False)

                elif movetype == 2:
                    if (braid.length() <= self.maxlen-2
                        and braid.insert(index, rr(braid.largestGenerator + 1))):
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.insert).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.insert).__name__, False)

                elif movetype == 3:
                    if braid.transpose(index):
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.transpose).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.transpose).__name__, False)

                elif movetype == 4:
                    if braid.flip(index):
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.flip).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.flip).__name__, False)

                elif movetype == 5:
                    if (braid.length() <= self.maxlen-1
                        and braid.largestGenerator < self.maxgen
                        and braid.stabilize()):
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.stabilize).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.stabilize).__name__, False)

                elif movetype == 6:
                    # Do not destabilize if braid length is 1: unknot
                    if braid.length() == 1 and braid.canDestabilize():
                        log[step] = self.log_message(movetype, (braid.destabilize).__name__, False)
                        log[step] += 'Unknot'
                        continue
                    elif braid.destabilize():
                        # append logs success
                        log[step] = self.log_message(movetype, (braid.destabilize).__name__, True)
                    else:
                        # append logs fail
                        log[step] = self.log_message(movetype, (braid.destabilize).__name__, False)
                else:
                    # should not get to this point
                    continue

            # Append new isomorphism and log
            self.braidagg['isomorphs'] += [deepcopy(braid)]
            self.braidagg['logs'].append(log)

        return

    def clear_model(self):
        '''
        Method to clear braid instance. That is, it clears self.braidagg.
        '''
        self.braidagg = {
            # list of isomorphisms
            'isomorphs': [],
            # list of logs
            'logs': []  # holds dict
        }

    def new_braidword(braidword: BraidWord):
        '''
        Method to set a new BraidWord.

        Args:
            braidword (BraidWord): The new BraidWord to replace the old
            BraidWord.

        Returns:
            Replaces self.braid with braidword.
        '''
        # Check if is braidword
        if not isinstance(braidword, BraidWord):
            # Check if is list
            if not isinstance(braidword, list):
                msg = 'First argument must be BraidWord or list.'
                raise ValueError(msg)
            else:
                self.braid = BraidWord(deepcopy(braidword))

        else:
            self.braid = deepcopy(braidword)

    def aggregate(self):
        '''
        Method to return a dictionary of MarkovChain instance's
        isomorphs and logs, both contained in their respective lists.
        That is, returns self.braidagg.
        '''
        return deepcopy(self.braidagg)

    def logs(self):
        '''
        Method to return MarkovChain instance logs in a list.

        Note that the length of the list is equal to the number of
        isomorphisms requested in the num_isomorphs argument of model.

        Each log represents the logs undergone to create a specific
        isomorphism and is held in a dictionary. The size of the
        dictionary is equal to the argument passed for msteps in model.
        '''
        return deepcopy(self.braidagg['logs'])

    def isomorphs(self, as_word=False):
        '''
        Method to return MarkovChain instance isomorphs in a list.

        Args:
            as_word (bool): Determines if isomorphs should be returned
            as words or BraidWords.

        Returns:
            If True returns isomorphs as words (list).
            Otherwise returns them as BraidWords (of class BraidWord).
        '''
        isos = (self.braidagg['isomorphs']).copy()
        if as_word:
            # Return list of words
            isos = [i.word for i in isos]
            return isos

        elif not as_word:
            # Return list of BraidWords
            return isos

        else:
            raise ValueError("as_word argument must be boolean.")
            return

    def topandas(self, only_isomorphs=False):
        '''
        Method to export logs, isomorphs to pandas df.

        Args:
            only_isomorphs (bool): Determines if only isomorphs
            should be returned or both isomorphs and logs.

        Returns:
            If only_isomorphs=True returns a pandas dataframe of
            only isomorphs. Otherwise will return a pandas dataframe
            with both isomorphs and logs.
        '''
        isos = self.isomorphs(as_word=True)
        logs = self.logs()
        dat = ({'Isomorphs': isos} if only_isomorphs
               else {'Isomorphs': isos, "Logs": logs})
        df = pd.DataFrame(dat, index=[i for i in range(len(isos))])

        return df.copy()

    def tocsv(self, path_or_filename="", only_isomorphs=False):
        '''
        Method to export logs, isomorphs to csv.

        If path_or_filename not given, will export the csv to
        current directory with the name `Isomorphs.csv` or
        `Isomorphs_and_Logs.csv`. The name is implicitly determined
        by the parameter passed to only_isomorphs.

        Args:
            path_or_filename (str): Path or filename to store csv.

            only_isomorphs (bool): Determines if only isomorphs
            should be returned or both isomorphs and logs.

        Returns:
            A csv file containing a dataframe with either only
            isomorphs or both isomorphs and logs, depending on parameter
            passed to only_isomorphs.
        '''
        # Set path_or_filename if not given
        if not path_or_filename:
            path_or_filename = ("Isomorphs.csv" if only_isomorphs
                                else "Isomorphs_and_Logs.csv")
        # Get pandas df
        df = self.topandas(only_isomorphs)
        # Export df to csv file on current directory
        df.to_csv(path_or_filename, sep='\t')

        return

    def totxt(self, path_or_filename="", only_isomorphs=False):
        '''
        Method to export logs, isomorphs to a txt file.

        If path_or_filename not given, will export the csv to
        current directory with the name `Isomorphs.txt` or
        `Isomorphs_and_Logs.txt`. The name is implicitly determined
        by the parameter passed to only_isomorphs.

        The format in the .txt is vertical, as follows:

        isomorph[1]
        isomorph[2]
        .
        .
        .
        isomorph[n]

        log[1]
        log[2]
        .
        .
        .
        log[n]

        Args:
            path_or_filename (str): Path or filename to store txt.
            only_isomorphs (bool): Determines if only isomorphs
            should be returned or both isomorphs and logs.

        Returns:
            A txt file containing a either only isomorphs or both isomorphs
            and logs, depending on parameter passed to only_isomorphs.
        '''
        # Set path_or_filename if not given
        if not path_or_filename:
            path_or_filename = ("Isomorphs.txt" if only_isomorphs
                                else "Isomorphs_and_Logs.txt")

        # Write to txt
        with open(path_or_filename, 'w') as file:
            for braid in self.isomorphs(as_word=True):
                file.write(' '.join(str(gen) for gen in braid))
                file.write('\n')
            file.write('\n')
        if not only_isomorphs:
            with open(path_or_filename, 'a') as file:
                for log in self.logs():
                    file.write(str(log))
                    file.write('\n')
                file.write('\n')

        return
