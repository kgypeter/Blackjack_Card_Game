import datetime
import random


class Deck:
    def __init__(self, cards=[]):
        self.cards = cards

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def card_init(self):
        file = open("deck.txt")
        # Every line consists of: html code of the card, value -> hard (11), value -> soft(1) , what kind of card

        # The four aces
        for i in range(4):
            line = file.readline()
            html_code, hard, soft, face = line.rstrip().split(',')  # The values in a row are separated by a comma
            html_code = chr(int(html_code))
            hard = int(hard)
            soft = int(soft)
            card = AceCard(html_code, hard, soft, face)
            self.cards.append(card)

        # The twelve cards with value of 10
        for i in range(12):
            line = file.readline()
            html_code, hard, soft, face = line.rstrip().split(',')
            html_code = chr(int(html_code))
            hard = int(hard)
            soft = int(soft)
            card = FaceCard(html_code, hard, soft, face)
            self.cards.append(card)

        # the rest of the cards
        line = file.readline()
        while line != '':
            html_code, hard, soft, face = line.rstrip().split(',')
            html_code = chr(int(html_code))
            hard = int(hard)
            soft = int(soft)
            card = Karte(html_code, hard, soft, face)
            self.cards.append(card)
            line = file.readline()
        file.close()
        self.shuffle_cards()

    def next_card(self):
        card = self.cards[-1]
        self.cards.pop()
        return card

    def print_card(self):
        for card in self.cards:
            print(card, "  ", type(card))


class Karte:
    def __init__(self, html_code, hard, soft, face):
        self.html_code = html_code
        self.hard = hard
        self.soft = soft
        self.face = face

    def __repr__(self):
        return f'Card: {self.html_code} -> {self.face}, value = {self.hard}'


class FaceCard(Karte):
    def __init__(self, html_code, hard, soft, face):
        super().__init__(html_code, hard, soft, face)
        self.hard = self.soft = 10


class AceCard(FaceCard):
    def __init__(self, html_code, hard, soft, face):
        super().__init__(html_code, hard, soft, face)
        self.hard = 11
        self.soft = 1

    def __repr__(self):
        return super().__repr__() + f' or {self.soft}'


class Scores:

    def write_score(self, spieler):
        file = open("score.txt", "r")
        score = len(file.readlines()) + 1
        file.close()
        file = open("score.txt", "a")
        file.write(
            f'  {datetime.date.today()}, {score}. Spiel, Geld: {spieler.money}, Name: {spieler.name}\n')
        file.close()

    def read_data(self, spieler):
        f = open("score.txt", "r")
        scores = []
        for line in f:
            value = line.split(':')[1].strip()
            value = int(value.split(',')[0])
            scores.append(value)
        scores.sort(reverse=True)
        print('''   
                                    BLACKJACK SCORES:
        
              ''')
        nr = 1
        for score in scores:
            print(f'    {nr}. {score}')
            nr += 1
        f.close()


class Nutzer:
    def __init__(self, name, money=100):
        self.name = name
        self.money = money

    def __repr__(self):
        return f'   {self.name} hat {self.money}€'


class Dealer:
    def __init__(self, deck):
        self.deck = deck

    def naechste_karte_bekommen(self):
        return self.deck.next_card()

    def new_deck(self, neues_deck):
        self.deck = neues_deck


class Spiel:
    def __init__(self, dealer, spieler):
        self.dealer = dealer
        self.spieler = spieler


def test_exchange():
    liste = [Karte('127181', '10', '10', 'queen_of_diamonds'), Karte('127175', '7', '7', 'seven_of_diamonds'),
             Karte('127149', '10', '10', 'queen_of_spades')]
    deck1 = Deck(liste)
    deck1.shuffle_cards()
    veraendert = False
    for nr, karte in enumerate(deck1.cards):
        if karte != liste[nr]:
            veraendert = True
    return veraendert


def test_one_and_only():
    liste = [Karte('127181', '10', '10', 'queen_of_diamonds'), Karte('127175', '7', '7', 'seven_of_diamonds'),
             Karte('127149', '10', '10', 'queen_of_spades')]
    deck1 = Deck(liste)
    dealer = Dealer(deck1)
    initial_len = len(deck1.cards)
    dealer.naechste_karte_bekommen()
    set_von_karten = set(deck1.cards)
    assert len(deck1.cards) == initial_len - 1 and len(deck1.cards) == len(set_von_karten)


def test_card_value():
    c1 = Karte('127175', '7', '7', 'seven_of_diamonds')
    c2 = AceCard('127169', '11', '1', 'ace_of_diamonds')
    c3 = FaceCard('127149', '10', '10', 'queen_of_spades')
    assert c1.hard == c1.soft and c2.hard == 11 and c2.soft == 1 and c3.hard == c3.soft == 10


def main():
    player_deck = Deck()
    player_deck.card_init()
    dealer_deck = Deck()
    dealer_deck.card_init()
    dealer = Dealer(player_deck)
    name = input("\tName: ")
    spieler = Nutzer(name)
    rund = 1

    while rund < 6:
        if spieler.money == 0:
            print("\tSorry! You lose all of your money!.")
            Scores.write_score(Scores, spieler)
            break
        print("\tRound ", rund)
        value = int(input(f'\tYou have {spieler.money}€. Your bet = '))
        if value > spieler.money:
            raise ValueError("\tNot enough money...")
        karte = dealer.naechste_karte_bekommen()

        test_one_and_only()

        print('\t', karte)
        if isinstance(karte, AceCard):
            kartenwert = int(input('\tSoft or Hard? (1 or 11):'))
            if kartenwert == 1:
                s = karte.soft
            elif kartenwert == 11:
                s = karte.hard
        else:
            s = karte.hard

        option = None
        rund += 1
        while option != 'no':
            option = input("\tDo you want a new card? (yes/no): ")
            if option == 'yes':
                karte = dealer.naechste_karte_bekommen()
                print('\t', karte)
                if isinstance(karte, AceCard):
                    kartenwert = int(input('\tSoft or Hard? (1 or 11): '))
                    if kartenwert == 1:
                        s = karte.soft
                    elif kartenwert == 11:
                        s = karte.hard
                else:
                    s += karte.hard
            if s == 21:
                spieler.money += value
                print(f'\tCongrats! You won {spieler.money}€.')

                break
            if s > 21:
                spieler.money -= value
                print(f'\tGame over, you went beyond 21. You have now {spieler.money}€.')

                break
        if s >= 21:
            continue

        print('''
                DEALER: 
        ''')
        dealer.deck = dealer_deck
        dealer.deck.shuffle_cards()
        karte = dealer.naechste_karte_bekommen()
        print('\t', karte)
        sum_cardValue = karte.hard
        if isinstance(karte, AceCard):
            print(f'\t{karte.hard} chosen')
        while sum_cardValue < s and sum_cardValue < 21:
            karte = dealer.naechste_karte_bekommen()
            print('\t', karte)
            if isinstance(karte, AceCard):
                if 11 + sum_cardValue <= 21:
                    sum_cardValue += karte.hard
                    print(f'\t{karte.hard} chosen')
                else:
                    sum_cardValue += karte.soft
                    print(f'\t{karte.soft} chosen')
            else:
                sum_cardValue += karte.hard

        if sum_cardValue == s:
            print(f'\tThe amount of money did not change. You have now {spieler.money}€.')
        elif sum_cardValue < s < 21 or sum_cardValue > 21:
            spieler.money += value
            print(f'\tCongrats! You have {spieler.money}€.')
        else:
            spieler.money -= value
            print(f'\tYou lost {value}€ . You have now {spieler.money}€.')

        dealer.deck = player_deck
        dealer.deck.shuffle_cards()

    if spieler.money != 0:
        Scores.write_score(Scores, spieler)
    Scores.read_data(Scores, spieler)
    test_exchange()
    test_card_value()


main()
