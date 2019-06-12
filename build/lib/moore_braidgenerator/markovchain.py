import random
import copy
import pandas as pd
import functools
from copy import copy, deepcopy
from moore_braidgenerator.braidword import BraidWord
from moore_braidgenerator.decorators.markovchain import checkparams_markovchain


class MarkovChain:
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
        """Function to dynamically create log of move @mstep"""
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
        Method to clear braid instance.
        i.e. clears braidagg
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
        '''
        # Check if is braidword
        if not isinstance(braidword, BraidWord):
            # Check if is list
            if not isinstance(braidword, list):
                msg = 'First argument must be BraidWord or list.'
                raise ValueError(msg)
            else:
                self.braid = BraidWord(braidword)
        else:
            self.braid = braidword


    def aggregate(self):
        '''
        Method to return MarkovChain instance aggregate.
        '''
        return deepcopy(self.braidagg)

    def logs(self):
        '''
        Method to return MarkovChain instance logs
        '''
        return deepcopy(self.braidagg['logs'])

    def isomorphs(self, as_word=False):
        '''
        Method to return MarkovChain instance isomorphs
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
        '''
        # DEFAULT set to isomorphs and logs
        # If True, then will only export isomorphs

        isos = self.isomorphs(as_word=True)
        logs = self.logs()
        dat = ({'Isomorphs': isos} if only_isomorphs
               else {'Isomorphs': isos, "Logs": logs})
        df = pd.DataFrame(dat, index=[i for i in range(len(isos))])
        return df.copy()

    def tocsv(self, path_or_filename="", only_isomorphs=False):
        '''
        Method to export logs, isomorphs to csv.
        '''
        # DEFAULT set to isomorphs and logs
        # If True, then will only export isomorphs

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
        Method to export logs, isomorphs to txt
        '''
        # DEFAULT set to only isomorphs
        # If True, then will only export isomorphs

        # Set path_or_filename if not given
        if not path_or_filename:
            path_or_filename = ("Isomorphs.txt" if only_isomorphs
                                else "Isomorphs_and_Logs.txt")

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
