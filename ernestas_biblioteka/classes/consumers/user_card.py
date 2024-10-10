import random
import os
import pickle
from ernestas_biblioteka.constants import CARD_NUM_FILE


class UserCard:
    def __init__(self):
        self.card_number = self.__generate_number()

    def __generate_number(self) -> str:
        num_set = self.__load_cards_num()
        print(num_set)
        while True:
            card_number = ''.join(
                [str(random.randint(0, 9)) for _ in range(8)])
            if card_number not in num_set:
                num_set.add(card_number)
                # self.card_number = card_number
                self.__save_new_number(num_set)
                return card_number

    def __load_cards_num(self) -> set:
        if os.path.exists(CARD_NUM_FILE):
            try:
                with open(CARD_NUM_FILE, 'rb') as file:
                    data_set = pickle.load(file)
                    return data_set
            except Exception as err:
                print(err)
        return set()

    def __save_new_number(self, num_set) -> None:
        try:
            with open(CARD_NUM_FILE, 'wb') as file:
                pickle.dump(num_set, file)
        except Exception as err:
            print(err)
        print('Korteles nr išsaugota sekmingai')
