import os
from threading import Thread

THREADS = 4


def search_text(keywords, files, result):
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result.append((keyword, file.split('/')[-1]))
        except Exception as e:
            print('Error handling file: ', file, e)


def parse_result(result):
    d = {}
    for text, file in result:
        if text in d:
            d[text].append(file)
        else:
            d[text] = [file]
    return d


def main(keywords, directory):
    result = []
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.txt')]

    files_for_threads = [files[i::THREADS] for i in range(THREADS)]
    threads = []

    for files_for_thread in files_for_threads:
        thread = Thread(target=search_text, args=(keywords, files_for_thread, result))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]

    return parse_result(result)


if __name__ == "__main__":
    keywords = ['by', 'so']
    directory = os.path.normpath(os.path.join(os.getcwd(), 'data'))
    result = main(keywords, directory)

    print(result)
