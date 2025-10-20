from glob import glob
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

from anticipation.convert import midi_to_compound
from anticipation.config import PREPROC_WORKERS

# https://github.com/jthickstun/anticipation/blob/main/train/midi-preprocess.py

def convert_midi(filename, debug=False):
    try:
        tokens = midi_to_compound(filename, debug=debug)
    except Exception:
        if debug:
            print('Failed to process: ', filename)
            print(traceback.format_exc())

        return 1

    with open(f"./text/{filename.split('/')[-1]}.compound.txt", 'w') as f:
        f.write(' '.join(str(tok) for tok in tokens))

    return 0

def main():
    curr_dir = input("Enter absolute or relative path: ")
    filenames = glob(curr_dir + '/**/*.mid', recursive=True) \
        + glob(curr_dir + '/**/*.midi', recursive=True)

    print(f'Preprocessing {len(filenames)} files with {PREPROC_WORKERS} workers')
    with ProcessPoolExecutor(max_workers=PREPROC_WORKERS) as executor:
        results = list(tqdm(executor.map(convert_midi, filenames), desc='Preprocess', total=len(filenames)))

    discards = round(100*sum(results)/float(len(filenames)),2)
    print(f'Successfully processed {len(filenames) - sum(results)} files (discarded {discards}%)')

if __name__ == '__main__':
    main()
