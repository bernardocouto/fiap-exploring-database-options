import pandas as pd


def main():
    df = pd.read_json('./sample/test.json')
    data = df.to_json(lines=True, orient='records')
    print(data)


if __name__ == '__main__':
    main()
