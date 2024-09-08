import argparse
import json
import os
import re

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--path', type=str, default='messages')
    p.add_argument('--outfile', type=str, default='messages.txt')

    args = p.parse_args()
    if not os.path.exists(args.path):
        p.error(f'Path {args.path} does not exist')
    return args

def strip_mentions(text: str) -> str:
    matches = re.findall('@<(\d+)>', text)
    for match in matches:
        text = text.replace(f'@<{match}>', '')
    return text

def strip_links(text: str) -> str:
    matches = re.findall('''(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])
''', text)
    for match in matches:
        text = text.replace(match, '')
    return text

def main():
    args = parse_args()
    messages = []

    for folder in os.listdir(args.path):
        try:
            if not os.path.isfile(os.path.join(args.path, folder, 'messages.json')):
                print(f'{folder} is not a file, skipping')
                continue
            with open(os.path.join(args.path, folder, 'messages.json'), 'rb') as f:
                content = json.loads(f.read().decode('utf-8','ignore'))

            for msg in content:
                if (text := msg.get('Contents')):
                    stripped = strip_links(
                        strip_mentions(text)
                    )
                    messages.append(stripped)
        except Exception as e:
            print(f'Error in {folder}: {e}')

    with open(args.outfile, 'w', encoding="utf-8") as f:
        f.write('\n'.join(messages))
    print('Written results to', args.outfile)
    print('Total lines:', len(messages))

if __name__ == '__main__':
    main()