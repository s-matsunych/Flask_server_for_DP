from typing import TextIO

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class Nucleotide:
    def __init__(self, coordinates, value):
        self.coordinates = coordinates
        self.value = value


    def get_nucleotide(self):
        return {
            'X': self.coordinates[0],
            'Y': self.coordinates[1],
            'Value': self.value
        }

class Sequences:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = self.read_file()
        self.clean_sequences = self.clear_sequences(self.file)
        self.df_file = pd.DataFrame()

        self.number_of_characters = self.сalculate_number_of_characters(self.clean_sequences)
        self.number_of_amino = self.сalculate_number_of_amino(self.clean_sequences)
        self.number_of_gaps = self.сalculate_number_of_gaps(self.clean_sequences)
        self.number_of_sequences = self.сalculate_number_of_sequences(self.clean_sequences)

        self.avg_len_of_sequence = self.number_of_characters / self.number_of_sequences
        self.avg_n_gaps_in_sequence = self.number_of_gaps / self.number_of_sequences

    def read_file(self):
        try:
            sequences_list = []
            with open(self.file_name, 'r') as file:
                file_list = file.readlines()
                for i in range(0, len(file_list), 2):
                    sequences_list.append({
                        'Name': file_list[i],
                        'Value': file_list[i + 1].strip()
                    })
                    i += 1
            return sequences_list
        except:
            Exception("| Ups => Exception (Maybe not existing file)")

    def clear_sequences(self, sequences: list):
        clean_sequences = []

        for sequence in sequences:
            seq_value = sequence['Value'].replace('-', ' ')
            clean_sequences.append({
                'Name': sequence['Name'],
                'Value': seq_value.strip().replace(' ', '-')
            })
        return clean_sequences

    def сalculate_number_of_characters(self, sequences: list):
        count = 0
        for sequence in sequences:
            count += len(sequence['Value'])
        return count

    def сalculate_number_of_amino(self, sequences: list):
        count = 0
        for sequence in sequences:
            count += len(sequence['Value'].replace('-', ''))
        return count

    def сalculate_number_of_gaps(self, sequences: list):
        count = 0
        for sequence in sequences:
            count += sequence['Value'].count('-')
        return count

    def сalculate_number_of_sequences(self, sequences: list):
        return len(sequences)

    def file_to_DataFrame(self, ):
        split_seq = []
        for seq in self.file:
            split_seq.append([seq['Name']] + list(seq['Value']))
        df = pd.DataFrame(split_seq)
        df = df.rename(columns={0: "Seq_name"})
        df.index += 1
        self.df_file = df
        return df

    def get_percent_gaps_in_columns(self):
        len_column = len(self.df_file)
        prcent_list = []
        for s in self.df_file:
            if s != int:
                prcent_list.append(len(self.df_file[s].loc[self.df_file[s] == '-']) / len_column)

        return prcent_list


if __name__ == '__main__':
    seq_oject = Sequences(file_name="sekvencie.txt")
    seq_oject.file_to_DataFrame()
    # seq_oject.df_file.to_csv("Seq_df.csv")
    pr_list = seq_oject.get_percent_gaps_in_columns()
    print(pr_list)
    print(seq_oject.number_of_sequences)
    plt.plot(pr_list)
    plt.show()
