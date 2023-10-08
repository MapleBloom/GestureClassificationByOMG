import requests
import json

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import os
import datetime
from zipfile import ZipFile


class PathNoStringError(Exception):
    pass


class bcolors:
    OKG = '\033[92m'
    OKB = '\033[94m'
    FR = '\033[91m'
    END = '\033[0m'


# Create gestures dictionary
GEST = {
    0: "open",
    1: "little",
    2: "ring",
    3: "middle",
    4: "gun",
    5: "index",
    6: "thumb",
    7: "ОК",
    8: "grab",
}

SENS = 40  # number of sensors


def check_exit(inp):
    '''If input == 'q' then exit program'''
    if inp == 'q':
        print(f'{bcolors.END}Exit.\n')
        exit()


def plot_omg_and_gestures(omg: pd.DataFrame, classes: pd.Series = None, i: int = None) -> None:
    """Plot omg data at one subplot and predicted gesture labels below in the file

    Args:
        omg (pd.DataFrame): omg data.
        classes (pd.Series): predicted gesture labels. Defaults to None.
        i (int, optional): number of sample plotted. Defaults to None.
    """
    fig, axx = plt.subplots(2, 1, sharex=True, figsize=(16, 8))

    axx[0].plot(omg)
    axx[0].set_title('OMG')

    if classes is not None:
        axx[1].plot(classes)
        axx[1].set_title('Gestures predicted')
    else:
        axx[1].set_title('No gestures predicted')
    axx[1].set_xlabel('Timestamp')
    axx[1].set_yticks(list(GEST.keys()), labels=list(GEST.values()))

    stitle = 'OMG and gestures predicted.'
    if i is not None:
        stitle += f' TEST SAMPLE {i}'
    plt.suptitle(stitle)
    plt.tight_layout()
    plt.savefig('result/plot_gesture.png')
    plt.close();


def main():
    # Read test data
    while True:
        try:
            print(f"{bcolors.OKG}\nOMG sensors data should be stored in 'X_test.npy' compressed to .zip file or not,\n",
                  "and contain 40 sensors data.")
            print(
                f"X_test shape: np.array( number of samples, number of sensors (=40) , number of time ticks in one sample )")
            inp = input(
                f"{bcolors.OKB}\nEnter path to .zip with OMG sensors data or press ENTER for default path 'data/X_test.zip': ")
            if inp == '':
                inp = 'data/X_test.zip'
            if not isinstance(inp, str):
                raise PathNoStringError
            if inp.strip()[-4:] == '.zip':
                with ZipFile(inp) as myzip:
                    X_test = np.load(myzip.open('X_test.npy'))
                break
            elif inp.strip()[-10:] == 'X_test.npy':
                X_test = np.load(f'{inp}')
                break
            else:
                raise FileNotFoundError
        except PathNoStringError:
            inp = input(f"{bcolors.FR}Path to the file should be a string. Enter any key to continue or 'q' to exit: ")
        except FileNotFoundError:
            inp = input(
                f"{bcolors.FR}File 'X_test.npy' at this path doesn't exist. Enter any key to continue or 'q' to exit: ")
        finally:
            check_exit(inp)

    TS_SAMP = X_test.shape[0]  # samples in the test data
    TS_TICKS = X_test.shape[2]  # time ticks at one sample
    # check number of sensors in the test data
    assert SENS == X_test.shape[1], f'{bcolors.FR}Test data should contain {SENS} OMG sensors{bcolors.END} '

    # Reshape X_test
    X_test = X_test.transpose((0, 2, 1)).reshape((TS_SAMP * TS_TICKS, SENS))
    X_df_test = pd.DataFrame(X_test, columns=[f'sens_{s}' for s in range(SENS)])
    X_df_test['sample'] = X_df_test.apply(lambda x: x.name // TS_TICKS, axis=1)
    X_df_test['timestamp'] = X_df_test.apply(lambda x: x.name % TS_TICKS, axis=1)

    # Get prediction from model and save in X_df_test
    r = requests.post('http://localhost/predict', json=json.dumps(X_test.reshape(-1).tolist()))
    print(f'\nStatus code: {r.status_code}')
    if r.status_code != 200:
        print(f'{bcolors.FR}Response: {r.text}')
        print(f'{bcolors.END}Something went wrong. Try later.\nExit.\n')
        exit()

    X_df_test['predicted'] = r.json()['prediction']

    # Save prediction in .csv
    if not os.path.exists('result'):
        os.mkdir('result')
    save_time = datetime.datetime.utcnow().strftime('%y.%m.%d_%H.%M')
    X_df_test[['sample', 'timestamp', 'predicted']].to_csv(f'result/prediction_{save_time}.csv', index=False)

    # Visualization
    i = 0
    print(
        f"{bcolors.OKG}\nOpen 'result/plot_gesture.png' file to see one by one visualization of the samples prediction.\n")
    while True:
        plot_omg_and_gestures(X_df_test.iloc[TS_TICKS * i:TS_TICKS * (i + 1), :SENS],
                              X_df_test.loc[TS_TICKS * i:TS_TICKS * (i + 1), 'predicted'],
                              i=i)
        i += 1
        if i == TS_SAMP:
            print(f'{bcolors.END}\nAll samples have been shown. Exit.\n')
            exit()
        inp = input(f"{bcolors.OKB}Enter any key to continue or 'q' to exit: ")
        check_exit(inp)


if __name__ == '__main__':
    main()
