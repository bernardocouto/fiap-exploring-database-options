import pandas as pd


def main():
    df = pd.read_parquet('./sample/test.parquet')
    print(df)


if __name__ == '__main__':
    main()
