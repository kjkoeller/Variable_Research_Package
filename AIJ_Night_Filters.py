"""
Author: Kyle Koeller
Created: 11/11/2020
Last Updated: 8/19/2022
Python Version 3.9

This program is meant to make the process of collecting the different filters from AIJ excel spreadsheets faster.
The user enters however many nights they have and the program goes through and checks those text files for the
different columns for,HJD, Amag, and Amag error for the B and V filters.

The program will also calculate the R magnitude from the rel flux of T1.

There are error catching statements within the program so if the user mistypes, the program will not crash and
close on them (hopefully)
"""

import pandas as pd
from os import path


def main(c):
    # warning prompts for the user to read to make sure this program works correctly
    if c == 0:
        # warning prompts for the user to read to make sure this program works correctly
        print()
        print("From each night, yous should have a file that is sort of like this: 2018.09.18.APASS.B_datasubset.dat."
              "This file has 5 columns and you will only need 3 of them.")
        print()
    else:
        print()

    while True:
        # checks to see whether you have entered a number and a correct filter letter
        try:
            num = int(input("Number of nights you have: "))
            print()
            break
        except ValueError:
            print("You have entered an invalid number for your number of nights. Please enter a number.")
            print()

    get_filters(num)


def get_filters(n):
    """
    Takes a number of nights for a given filter and takes out the HJD, either A_Mag1 or T1_flux, and
    error for mag or flux

    :param n: Number of observation nights
    :return: the output text files for each night in a given filter
    """
    total_hjd = []
    total_amag = []
    total_error = []
    # checks for either the b or v filter as either upper or lowercase will work
    # an example pathway for the files
    # E:\Research\Data\NSVS_254037\2018.10.12-reduced\Check\V\2018.09.18.APASS.B_datasubset.dat
    print("When entering a file path make sure to use files that are the same filter. So if you are going"
          " through the Johnson B files, then only use the file paths of the Johnson B and not V or R")
    for i in range(n):
        while True:
            # makes sure the file pathway is real and points to some file
            # (does not check if that file is the correct one though)
            try:
                file = input("Enter night %d file path: " % (i + 1))
                if path.exists(file):
                    break
                else:
                    continue
            except FileNotFoundError:
                print("Please enter a correct file path")

        # noinspection PyUnboundLocalVariable
        df = pd.read_csv(file, delimiter="\t")

        # set parameters to lists from the file by the column header
        hjd = []
        flux = []
        flux_error = []
        try:
            hjd = list(df["HJD"])
            flux = list(df["rel_flux_T1"])
            flux_error = list(df["rel_flux_err_T1"])
        except KeyError:
            print("The file you entered does not have the columns of HJD, Source_AMag_T1, or Source_AMag_Err_T1. "
                  "Please re-enter the file path and make sure its the correct file.")
            c = 1
            main(c)

        total_hjd.append(hjd)
        total_amag.append(flux)
        total_error.append(flux_error)

    # converts the Dataframe embedded lists into a normal flat list
    new_hjd = [item for elem in total_hjd for item in elem]
    new_flux = [item for elem in total_amag for item in elem]
    new_flux_error = [item for elem in total_error for item in elem]

    # outputs the new file to dataframe and then into a text file for use in Peranso or PHOEBE
    data = pd.DataFrame({
        "HJD": new_hjd,
        "rel flux": new_flux,
        "rel flux error": new_flux_error
    })
    print("")
    output = input("What is the file output name (with file extension .txt): ")

    data.to_csv(output, index=False, header=False, sep='\t')
    print("")
    print("Fished saving the file to the same location as this program.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count = 0
    main(count)
