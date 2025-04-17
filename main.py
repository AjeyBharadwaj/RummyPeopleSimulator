import random

class Person:
    def __init__(self, name, money):
        self.name = name
        self.money = money

    def __str__(self):
        return f"{self.name} has {self.money}"
    
    def get_money(self):
        return self.money
    
    def reduce_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount
    

class Game:
    def __init__(self, players, game_fee):
        self.players = players
        self.game_fee = game_fee

    def play(self):
        
        total_money = self.game_fee*len(self.players)
        for player in self.players:
            player.reduce_money(self.game_fee)

        # Select random player
        import random
        player = random.choice(self.players)
        player.add_money(total_money)

players = []
player_name_start = "P"
total_players = 10000
initial_amount = 100
game_amount = 90
players_per_game = 100

for i in range(total_players):
    players.append(Person(f"{player_name_start}{i}", initial_amount))

iteration = 0
last_iteration_players_count = len(players)
while True:
    iteration += 1

    if len(players) != last_iteration_players_count:
        print(f"Iteration: {iteration} : {len(players)}")
        last_iteration_players_count = len(players)

    eligible_players = [player for player in players if player.get_money() >= game_amount]
    players_for_this = random.sample(eligible_players, min(players_per_game, len(eligible_players)))

    game = Game(players, game_amount)
    game.play()

    for player in players:
        if player.get_money() < game_amount:
            print(f"{player.name} is out of the game.")

    players = [player for player in players if player.get_money() > 0]

    if len(players) == 1:
        print(f"After {iteration} iteration : {players[0].name} is the winner!")
        break
