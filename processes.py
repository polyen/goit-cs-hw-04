import os.path
from multiprocessing import Queue, Process, current_process
import time

PROCESSES = 4


def search_text(keywords, files, q):
    results = []
    try:
        for file in files:
            with open(file, 'r') as f:
                content = f.read()
                for text in keywords:
                    if text in content:
                        results.append((text, file.split('/')[-1]))

        q.put(results)

    except Exception as e:
        print(f'{current_process().name} - {e}')


def parse_result(q):
    d = {}
    while not q.empty():
        arr = q.get()
        for text, file in arr:
            if text in d:
                d[text].append(file)
            else:
                d[text] = [file]
    return d


def main(keywords, directory):
    q = Queue()
    try:
        files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]
    except Exception as e:
        print('Error reading directory: ', e)
        return

    processes = []

    for i in range(PROCESSES):
        p = Process(target=search_text, args=(keywords, files[i::PROCESSES], q))
        processes.append(p)
        p.start()

    [p.join() for p in processes]

    return parse_result(q)


if __name__ == "__main__":
    keywords = ['by', 'so']
    directory = os.path.normpath(os.path.join(os.getcwd(), 'data'))
    start = time.time()
    result = main(keywords, directory)
    print('Time taken: ', time.time() - start)
    print(result)
