from typing import TextIO
from random import randint
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class Sequences:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = self.read_file()
        self.df_file = pd.DataFrame()

        self.number_of_characters = None
        self.number_of_amino = None
        self.number_of_gaps = None
        self.number_of_sequences = None

        self.avg_len_of_sequence = None
        self.avg_n_gaps_in_sequence = None
        self.len_sequences = None

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

    @staticmethod
    def read_file_from_request(stream_data: str):
        list_stream = stream_data.split('\n')
        sequences_list = []
        for i in range(0, len(list_stream), 2):
            if list_stream[i] == '': break
            sequences_list.append({
                'Name': list_stream[i],
                'Value': list_stream[i + 1].strip()
            })
            i += 1
        return sequences_list

    @staticmethod
    def clear_sequences(sequences: list):
        clean_sequences = []

        for sequence in sequences:
            seq_value = sequence['Value'].replace('-', ' ')
            clean_sequences.append({
                'Name': sequence['Name'],
                'Value': seq_value.strip().replace(' ', '-')
            })
        return clean_sequences

    @staticmethod
    def get_unique_characters(sequences: list):
        all_seqs_concat = ""
        for sequence in sequences:
            all_seqs_concat = all_seqs_concat+sequence['Value']
        return list(set(all_seqs_concat))

    @staticmethod
    def сalculate_number_of_characters(sequences: list):
        count = 0
        for sequence in sequences:
            count += len(sequence['Value'])
        return count

    @staticmethod
    def сalculate_number_of_amino(sequences: list):
        count = 0
        for sequence in sequences:
            count += len(sequence['Value'].replace('-', ''))
        return count

    @staticmethod
    def сalculate_number_of_gaps(sequences: list):
        count = 0
        for sequence in sequences:
            count += sequence['Value'].count('-')
        return count

    @staticmethod
    def сalculate_number_of_sequences(sequences: list):
        return len(sequences)

    @staticmethod
    def сalculate_len_sequences(sequences: list):
        return len(sequences[0]['Value'])

    def calculate_base_statistics(self, seqs):
        self.number_of_characters = self.сalculate_number_of_characters(seqs)
        self.number_of_amino = self.сalculate_number_of_amino(seqs)
        self.number_of_gaps = self.сalculate_number_of_gaps(seqs)
        self.number_of_sequences = self.сalculate_number_of_sequences(seqs)
        self.len_sequences = self.сalculate_len_sequences(seqs)

        self.avg_len_of_sequence = self.number_of_characters / self.number_of_sequences
        self.avg_n_gaps_in_sequence = self.number_of_gaps / self.number_of_sequences

        return {"number_of_characters": self.number_of_characters,
                "number_of_amino": self.number_of_amino,
                "number_of_gaps": self.number_of_gaps,
                "number_of_sequences": self.number_of_sequences,
                "avg_len_of_sequence": self.avg_len_of_sequence,
                "avg_n_gaps_in_sequence": self.avg_n_gaps_in_sequence,
                "len_sequences": self.len_sequences,
                }

    @staticmethod
    def calculate_base_statistics(seqs):
        number_of_characters = Sequences.сalculate_number_of_characters(seqs)
        number_of_amino = Sequences.сalculate_number_of_amino(seqs)
        number_of_gaps = Sequences.сalculate_number_of_gaps(seqs)
        number_of_sequences = Sequences.сalculate_number_of_sequences(seqs)
        len_sequences = Sequences.сalculate_len_sequences(seqs)

        avg_len_of_sequence = number_of_characters / number_of_sequences
        avg_n_gaps_in_sequence = number_of_gaps / number_of_sequences

        return {"number_of_characters": number_of_characters,
                "number_of_amino": number_of_amino,
                "number_of_gaps": number_of_gaps,
                "number_of_sequences": number_of_sequences,
                "avg_len_of_sequence": avg_len_of_sequence,
                "avg_n_gaps_in_sequence": avg_n_gaps_in_sequence,
                "len_sequences": len_sequences,
                }

    @staticmethod
    def get_percent_gaps_in_columns(data, element='-'):
        """ Create data in valid format for heatmap
            :param data: result from read_file()
            :param element: char in sequenses for calkulate percent in columns
        """
        df_file = Sequences.file_to_DataFrame(data)
        len_column = len(df_file)
        prcent_list = []
        for s in df_file:
            if s != int:
                prcent_list.append(len(df_file[s].loc[df_file[s] == element]) / len_column)
        return prcent_list

    @staticmethod
    def get_heatmap_full_data(x, y, data):
        """ Create data in valid format for heatmap
        :param data: result from read_file()
        """
        output = []
        for idy, seq in enumerate(data[y[0]:y[1]]):
            for idx, simbol in enumerate(seq['Value'][x[0]:x[1]]):
                output.append(
                    {
                        "x": idx + x[0],
                        "y": idy + y[0],
                        "value": randint(0, 100),
                        "name": f"{simbol}",
                        # "color": "#FFFFFF",
                        "accessibility": {
                            "description": seq['Name']}
                    }
                )
        return output

    def file_to_DataFrame(self):
        split_seq = []
        for seq in self.file:
            split_seq.append([seq['Name']] + list(seq['Value']))
        df = pd.DataFrame(split_seq)
        df = df.rename(columns={0: "Seq_name"})
        df.index += 1
        self.df_file = df
        return df

    @staticmethod
    def file_to_DataFrame(data):
        split_seq = []
        for seq in data:
            split_seq.append([seq['Name']] + list(seq['Value']))
        df = pd.DataFrame(split_seq)
        df = df.rename(columns={0: "Seq_name"})
        df.index += 1
        # self.df_file = df
        return df

