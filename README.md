# Markov Chain and Braids

A project from the University of California, Davis' Department of Mathematics, to be used to generate braid isomorphisms from a given braid. The project was born when researchers at UC Davis attempted to use Machine Learning techniques on braids but found the data to be too small. This should help others generate data to help better understand the topology of knots.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

If downloading through pip then only _Pandas_ is required. Otherwise, consider the list below.

- markovchain.py (repository)
- braidword.py (repository)
- decorators/braidword.py (repository)
- decorators/markovchain.py (repository)
- pandas

### Installation and setup

#### Installation with pip

Need to upload to piplib

#### Importing modules from repository

To use the following scripts straight from the github repository, it is necessary to pull the modules listed in **prerequisites** into your current directory. Once this is done, the _markovchain_ script can be imported into any script that exists in the current directory. Note that the method `topandas` in _markovchain_ requires _pandas_.

To create a Markov Chain, simply call MarkovChain with at least the `braidword` argument given. The Markov Chain initializor has default values of
nine and ten for the `maxgen` and `maxlen` parameters, respectively.

```
from markovchain import MarkovChain
import pandas as pd

mc = MarkovChain(braidword=[1, 2, 3], maxgen=9, maxlen=10)

```

Alternatively, the Markov Chain can be initialized with a `BraidWord` instead of a list. The BraidWord is wrapped around a list (the _word_).

```
from markovchain import MarkovChain
from braidword import BraidWord
import pandas as pd

mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)
```

> Note that if the Markov Chain is initialized with a list instead of a BraidWord, it will be processed into a BraidWord behind the scenes.

To create isomorphisms it suffices to call the `model` method. `model` takes two parameters,
`num_isomorphs` and `msteps`, where `num_isomorphs` is the number of isomorphs that are to be generated and `msteps` is the amount of Markov Moves to apply to the BraidWord for each isomorphism. Default values are one and 100, respectively.

```
mc.model(num_isomorphs=10, msteps=50)
```

Once the modelling is complete, the isomorphs and/or logs can be accessed via the following getter methods:

- `MarkovChain.aggregate`
- `MarkovChain.logs`
- `MarkovChain.isomorphs`
- `MarkovChain.topandas`
- `MarkovChain.tocsv`
- `MarkovChain.totxt`

#### `MarkovChain.aggregate`

The `aggregate` method will return a dictionary with two keys: _isomorphs_ and _logs_, whereby _isomorphs_ is a list that contains the generated isomorphs and _logs_ is a list that contains the relevant Markov Moves per iteration and if they were successful or not.

> This aggregate dictionary is mainly a container for the relevant data and while this getter method is available, it is not recommended for retrieving the data. Better alternative methods exist for this.

```
agg = mc.aggregate()

agg

> {'isomorphs': [], 'logs': []}
```

#### `MarkovChain.logs`

The `logs` method returns only the logs in the list format. Each element of the log is itself a dictionary that represents all the Markov Moves for each isomorph created. Thus, the size of _isomorphs_ and _logs_ will be the same, but each entry will contain a larger set of logs. The example below shows a MarkovChain's logs with `num_isomorphs=1` and `msteps=5`

```
logs = mc.logs()

logs[0]

> {0: 'MoveType: 5, Attempted stabilize: stabilize Succeeded.',
1: 'MoveType: 0, Attempted conjugate: conjugate Succeeded.',
2: 'MoveType: 6, Attempted destabilize: destabilize Failed.',
3: 'MoveType: 3, Attempted transpose: transpose Failed.',
4: 'MoveType: 4, Attempted flip: flip Failed.'}
```

#### `MarkovChain.isomorphs`

The `isomorphs` method will return the list with the generated isomorphs. This method takes an optional parameter `as_word` which is set to `False` by default. If left as `False` then it will return a list of BraidWords, otherwise it will return a list of words (i.e. of type list).

```
# As BraidWords with as_word set to False (default)

mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

isomorphs_asBraidWord = mc.isomorphs()

isomorphs_asBraidWord

> [<braidword.BraidWord at 0x114dbe7b8>,
 <braidword.BraidWord at 0x114dbe7f0>,
 <braidword.BraidWord at 0x114dbe588>]
```

```
# As words with as_word set to True

mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

isomorphs_asword = mc.isomorphs(as_word=True)

isomorphs_asword

> [[1, 2, 3], [2, 3, 1], [1, 2]]
```

> Note that the Braid that was fed into the model is not included. The first word of the second example above is a coincidence resulting from one successful destabilize and one successful stabilize.

#### `MarkovChain.topandas`

The logs and isomorphs can be most easily accessed via the `topandas` method. To use it, simply import _pandas_ into the script and call the `topandas` method. The method takes one optional argument, `only_isomorphs`, which is set to `False` by defualt. If set to `True` then the resulting dataframe will only include the isomorphs in word form. Otherwise, each entry will comprise of both the isomorph and the logs associated with it.

```
# only_isomorphs set to False (default)
import pandas as pd

mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

df = mc.topandas()
df.columns

> Index(['Isomorphs', 'Logs'], dtype='object')
```

```
# only_isomorphs set to True
import pandas as pd

mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

df = mc.topandas(only_isomorphs=True)
df.columns

> Index(['Isomorphs'], dtype='object')
```

#### `MarkovChain.tocsv`

The `tocsv` method exports the dataframe to a .csv file. The parameters include `path_or_filename` and `only_isomorphs`, respectively. Similar to the `topandas` method, `only_isomorphs` is set to `False` by default. The `path_or_filename` parameter is more interesting. If a path is not specified, the method will export the requested information to the current directory with either the name _Isomorphs.csv_
or _Isomorphs_and_Logs.csv_, which it will implicitly interpret from the argument passed to `only_isomorphs`.

```
mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

path = 'some/path/onyourpc.csv'
mc.tocsv(path_or_filename=path, only_isomorphs=False)
```

#### `MarkovChain.totxt`

The `totxt` method is similar to the `topandas` and `tocsv` difference being that it exports the data to a _.txt_ file in the following format:

```
isomorph[1]
.
.
.
isomorph[n]

log[1]
.
.
.
log[n]
```

As is with to `tocsv`, the `totxt` has the two parameters
`path_or_filename` and `only_isomorphs`, respectively.

### Clearing the model and setting a new BraidWord

If it is desired to use the same model to create a new set of isomoprhs, the `clear_model` method is required. This method clears the _braidagg_ container.

```
mc = MarkovChain(braidword=BraidWord([1, 2, 3]), maxgen=9, maxlen=10)

mc.model(num_isomorphs=3, msteps=5)

mc.clear_model()

mc.aggregate()

> {'isomorphs': [], 'logs': []}
```

> Note that if not changed, the subsequent BraidWord will have been mutated. This functionality is left in as it may seem desirable for some situations and is simple enough to undo (i.e. replace the BraidWord with the `new_braidword` method).

In the event that it is desirable to set a new _BraidWord_ into an already existing method, the `new_braidword` method can be used. A list or `BraidWord` object can be passed as an argument.

```
mc.new_braidword([1, 1, 2])
```

```
mc.new_braidword(BraidWord([1, 2, 3]))
```

> As is the case with the initializor, if a list is passed in as an argument it will be converted to a BraidWord behind the scenes.

## Running the tests

Tests for these scripts are included in the github repository under the paths shown below.

```
Repo
│
└───tests
        test_braidword.py
        test_markovchain.py
```

### Breakdown of tests

The given tests use Pythons UnitTest package for testing.
**test_braidword.py** contains over 350 lines of tests with 30+ test cases (at the time of writting this readme). The test cases contain suites that test for initialization, boolean helper functions (such as `canDestabilize`, `canFlip`, etc...), and the **BraidWord** methods (such as `Destabilize`, `Flip`, etc...). Examples of **test_braidword.py** include:

```
def test_init_pathfail_0(self):
    '''
    Should raise TypeError if initword
    is not a list (args)
    '''
    with self.assertRaises(TypeError) as te:
        bw = BraidWord(1)
```

```
def test_canCancel_pathfail(self):
    """Should return False when adjacent
    generators are not inverses of one other"""
    bw = BraidWord([1, 2, 3, -3])
    # Execution path False
    self.assertFalse(bw.canCancel(0))
```

```
def test_cancel_pathsuccess(self):
    """Should successfully cancel gen @idx 3
    and should modify word"""
    bw = BraidWord([-1, 2, 3, 1])
    # Execution path True
    self.assertTrue(bw.cancel(3))
    # Word modification
    self.assertEqual(bw.word, [2, 3])
```

**test_markovchain.py** contains roughly 200 lines of tests with 18+ test cases (at the time of writing this readme). The test cases contain suites that test mainly for initialization and that containers, such as _logs_, _isomorphisms_, and _braidagg_, vis-a-vis the `aggregate`, `logs`, and `isomorphs` methods, as well as exporting methods, such as `tocsv`, `topandas`, and `totxt`, are valid (i.e. not empty). The lack of automated tests for said script is due to the probabilistic nature of the results of the `model` method. Results for this method are tested by hand by Professor Moore. Examples of **test_markovchain.py** include:

```
def test_init_pathfail_0(self):
    """Should throw error if BraidWord not given"""
    with self.assertRaises(Exception) as te:
        MarkovChain()
```

```
def test_aggregate(self):
    '''
    Should return non-empty self.braidagg
    '''
    mc = MarkovChain(BraidWord([1, 2, 3]))
    mc.model(num_isomorphs=1, msteps=10)
    # Check if non-empty
    self.assertTrue(mc.aggregate())
```

```
def test_logs(self):
    '''
    Should return non-empty self.braidagg.logs
    '''
    mc = MarkovChain(BraidWord([1, 2, 3]))
    mc.model(num_isomorphs=1, msteps=10)
    # Check if non-empty
    self.assertTrue(mc.logs())
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Professor Allison Moore** - _Initial work_ - [allisonhmoore](https://github.com/allisonhmoore)
- **Milad Michael Nasrollahi** - _Initial work_ - [Algebra8](https://github.com/Algebra8)
- **Shawn Witte, PhD Candidate** - _Initial work_ - [Minirogue](https://github.com/Minirogue)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc

```

```
