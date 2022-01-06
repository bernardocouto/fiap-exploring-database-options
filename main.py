import pandas as pd


def main():
    df = pd.read_json('./sample/test.json')
    data = df.to_json(lines=True, orient='records')
    data = data.split('\n')
    print(data)
    for item in data:
        print(item)
        print(type(item))


if __name__ == '__main__':
    main()
