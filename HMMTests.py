import unittest

from plotly.graph_objs.bar import Selected

from HMM import HMM, Sequence


class MyTestCase(unittest.TestCase):

    def test_load(self):
        h = HMM()
        h.load('cat')
        transitions = {'#': {'happy': '0.5', 'grumpy': '0.5', 'hungry': '0'},
         'happy': {'happy': '0.5', 'grumpy': '0.1', 'hungry': '0.4'},
         'grumpy': {'happy': '0.6', 'grumpy': '0.3', 'hungry': '0.1'},
         'hungry': {'happy': '0.1', 'grumpy': '0.6', 'hungry': '0.3'}}
        emissions = {'happy': {'silent': '0.2', 'meow': '0.3', 'purr': '0.5'},
         'grumpy': {'silent': '0.5', 'meow': '0.4', 'purr': '0.1'},
         'hungry': {'silent': '0.2', 'meow': '0.6', 'purr': '0.2'}}
        self.assertEqual(h.transitions, transitions)
        self.assertEqual(h.emissions, emissions)

        """
        see if all the values sum to one in load
        """

        h1 = HMM()
        h1.load('partofspeech')


    def test_generate(self):
        h = HMM()
        h.load('cat')
        print(h.generate(20))

        h1 = HMM()
        h1.load('partofspeech')
        print(h1.generate(20))

    def test_forward(self):
        h = HMM()
        h.load('cat')
        s = Sequence(["grumpy", "happy", "grumpy"], ["purr", "silent", "silent", "meow", "meow"])
        print(h.forward(s))
        #
        h1 = HMM()
        h1.load('lander')
        s1 = Sequence([], ["1,1", "2,2", "2,2", "3,3", "4,3"])
        print(h1.forward(s1))

        h2 = HMM()
        h2.load('partofspeech')
        s2 = Sequence([], ["this", "is", "a", "light", "blanket", "."])
        print(h2.forward(s2))

    def test_viterbi(self):
        h = HMM()
        h.load('cat')
        s = Sequence(["grumpy", "happy", "grumpy"], ["purr", "silent", "silent", "meow", "meow"])
        print(h.viterbi(s))
        #
        h1 = HMM()
        h1.load('lander')
        s1 = Sequence(['1,1', '2,2', '3,2', '4,3', '5,3'], ["1,1", "2,2", "2,2", "3,3", "4,3"])
        print(h1.viterbi(s1))

        h2 = HMM()
        h2.load('partofspeech')
        s2 = Sequence([], ["this", "is", "a", "light", "blanket", "."])
        print(h2.viterbi(s2))

if __name__ == '__main__':
    unittest.main()
