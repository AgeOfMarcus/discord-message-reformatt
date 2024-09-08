import argparse
import json
import os

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--path', type=str, default='messages')
    p.add_argument('--outfile', type=str, default='messages.txt')

    args = p.parse_args()
    if not os.path.exists(args.path):
        p.error(f'Path {args.path} does not exist')
    return args

def main():
    args = parse_args()
    messages = []

    for folder in os.listdir(args.path):
        try:
            with open(os.path.join(args.path, folder), 'r') as f:
                content = json.loads(f.read())

            for msg in content:
                if (text := msg.get('Contents')):
                    messages.append(text)
        except Exception as e:
            print(f'Error in {folder}: {e}')

    with open(args.outfile, 'w') as f:
        f.write('\n'.join(messages))
    print('Written results to', args.outfile)
    print('Total lines:', len(messages))

if __name__ == '__main__':
    main()