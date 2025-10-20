from multiprocessing import Pool, RLock
from glob import glob
from tqdm import tqdm

from anticipation.config import *
from anticipation.tokenize import tokenize, tokenize_ia
import anticipation.tokenize as tok

tok.MIN_TRACK_LENGTH = 0
tok.MIN_TRACK_EVENTS = 0

# https://github.com/jthickstun/anticipation/blob/main/train/tokenize-lakh.py

def tokenization(curr_dir):
    encoding = 'arrival' # can also be interarrival
    augment = 1

    print('Tokenization parameters:')
    print(f'  anticipation interval = {DELTA}s')
    print(f'  augment = {augment}x')
    print(f'  max track length = {MAX_TRACK_TIME_IN_SECONDS}s')
    print(f'  min track length = {MIN_TRACK_TIME_IN_SECONDS}s')
    print(f'  min track events = {MIN_TRACK_EVENTS}')

    files = glob(curr_dir + '/**/*.compound.txt', recursive=True)
    outputs = [f"./tokens/{f.split('/')[-1].split('.')[0]}.tokenized-events.txt" for f in files]

    func = tokenize_ia if encoding == 'interarrival' else tokenize
    arguments = [([files[i]], outputs[i], augment, i) for i in range(len(files))]
    with Pool(processes=PREPROC_WORKERS, initargs=(RLock(),), initializer=tqdm.set_lock) as pool:
        print(arguments)
        results = pool.starmap(func, arguments)

    seq_count, rest_count, too_short, too_long, too_manyinstr, discarded_seqs, truncations \
            = (sum(x) for x in zip(*results))
    rest_ratio = round(100*float(rest_count)/(seq_count*M),2)

    trunc_type = 'interarrival' if encoding == 'interarrival' else 'duration'
    trunc_ratio = round(100*float(truncations)/(seq_count*M),2)

    print('Tokenization complete.')
    print(f'  => Processed {seq_count} training sequences')
    print(f'  => Inserted {rest_count} REST tokens ({rest_ratio}% of events)')
    print(f'  => Discarded {too_short+too_long} event sequences')
    print(f'      - {too_short} too short')
    print(f'      - {too_long} too long')
    print(f'      - {too_manyinstr} too many instruments')
    print(f'  => Discarded {discarded_seqs} training sequences')
    print(f'  => Truncated {truncations} {trunc_type} times ({trunc_ratio}% of {trunc_type}s)')

    print('Remember to shuffle the training split!')

def main():
    curr_dir = input("Enter absolute or relative path: ")
    tokenization(curr_dir)

if __name__ == '__main__':
    main()
