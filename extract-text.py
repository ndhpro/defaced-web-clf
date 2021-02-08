import sys
from glob import glob
from urllib.request import urlopen
from bs4 import BeautifulSoup
from multiprocessing import cpu_count
from joblib import Parallel, delayed
from tqdm import tqdm


def html2text(path, encoding):
    text_path = path.replace('data/', 'text/').replace('.html', '.txt')
    if glob(text_path):
        return

    with open(path, 'r', encoding=encoding) as f:
        try:
            html = f.read()
        except:
            return -1

    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    with open(text_path, 'w') as f:
        f.write(text)
    return 0


if __name__ == '__main__':
    html_paths = glob('data/*/*.html')

    encoding = sys.argv[1]

    print(f'Extracting text ({encoding})...')
    output = Parallel(n_jobs=cpu_count())(delayed(html2text)(path, encoding=encoding)
                                          for path in tqdm(html_paths))

    print(f'Done ({output.count(0)}')
