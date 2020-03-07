import subprocess
import shlex
import sys
import time
import os
import errno

class _TaggerProgram:
    """Creates a process instatiatinmg the tagger .jar program."""
    cmd = 'java -XX:ParallelGCThreads=2 -Xmx500m -jar' # taken from original runtagger script
    only_tokenise = False # fault will return tagged items

    def __init__(self, path):
        # ensure input file path points to the tagger program and not just containing dir
        if path[-23:] != 'ark-tweet-nlp-0.3.2.jar':
            path = os.path.join(path, 'ark-tweet-nlp-0.3.2.jar')

        # check the tagger prgram exists
        if not os.path.isfile(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        # build commmand to run the tagger program
        self.args = shlex.split(self.cmd)
        self.args.append(path)


    def kill(self):
        # kills the tweet tagger program instance
        self.process.kill()


class Twagger(_TaggerProgram):
    """Tag tweets with the tagger program."""
    def __init__(self, path, conll=True):
        _TaggerProgram.__init__(self, path)
        self.conll = conll # output format

        # start tagger program
        self.process = subprocess.Popen(self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def tag(self, tweet):
        # remove newlines from tweet, and append newline at end
        tweet = tweet.replace('\r', '')
        tweet = tweet.replace('\n', ' ') + '\n'

        # send tweet to tagger program
        self.process.stdin.write(tweet.encode())
        self.process.stdin.flush()

        # recieve and parse the tagged tweet from program output
        out = self.process.stdout.readline()
        print(out)
        text, tags, confidence = [lst.split(' ') for lst in out.decode().split('\t')][:-1]
        confidence = [float(c) for c in confidence]

        if self.conll:
            return list(zip(text, tags, confidence))
        else:
            return text, tags, confidence



class Twokeniser(_TaggerProgram):
    """Only tokenise docuemnts with the tagger program."""
    def __init__(self, path):
        _TaggerProgram.__init__(self, path)

        # append tag to only tokenise
        self.args.append('--just-tokenize')

        # start tagger program
        self.process = subprocess.Popen(self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def tokenise(self, tweet):
        # remove newlines/carrige returns from tweet, and append newline at end
        tweet = tweet.replace('\r', '')
        tweet = tweet.replace('\n', ' ') + '\n'

        # send tweet to tokeniser program
        self.process.stdin.write(tweet.encode())
        self.process.stdin.flush()

        # recieve the tagged tweet from program output
        out = self.process.stdout.readline()
        return out.decode().split('\t')[0].split(' ')

if __name__ == '__main__':
    T = Twagger('ark-tweet-nlp-0.3.2.jar')
    output = T.tag('First case of covid in Colombia')
