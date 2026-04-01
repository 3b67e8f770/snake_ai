#!/usr/bin/python3
import pandas as pd
import matplotlib as plt

def plot_learning():
    df = pd.read_csv('stats.csv')
    plt.figure(figsize=(10,5))
    plt.plot(df['Game'], df['Score'], label ='Score per Game')
    plt.plot(df['Game'], df['Score'].rolling(window=10).mean(), label='Average (10 games)')
    plt.xlabel('Game Number')
    plt.ylabel('Score')
    plt.title('Snake AI Learning Process')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_learning()