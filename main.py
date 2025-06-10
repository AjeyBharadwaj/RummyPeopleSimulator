import random
import matplotlib.pyplot as plt

class Person:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.games = []

    def __str__(self):
        return f"{self.name} has {self.money}"
    
    def add_game(self, game):
        self.games.append(game)

    def get_money(self):
        return self.money
    
    def reduce_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount
    

class Game:
    game_no = 0
    def __init__(self, players, game_fee, governemnt):
        self.players = players
        self.game_fee = game_fee
        self.governemnt = governemnt
        self.game_no = Game.game_no
        Game.game_no += 1

        for player in self.players:
            player.add_game(self)

    def play(self):
        
        total_money = self.game_fee*len(self.players)
        for player in self.players:
            player.reduce_money(self.game_fee)

        # Select random player
        import random
        self.winner = random.choice(self.players)
        self.remaining_money = self.governemnt.collect_tax(total_money)
        self.winner.add_money(self.remaining_money)

    def __str__(self):
        return f"Game {self.game_no} with players: {[player.name for player in self.players]} and game fee: {self.game_fee} won by {self.winner.name}"


class Government:
    def __init__(self, percentage):
        self.percentage = percentage
        self.total_tax_collected = 0

    def collect_tax(self, total_money):
        todeduct = total_money * self.percentage/100
        self.total_tax_collected += todeduct
        return total_money - todeduct

def split_into_random_lists(lst, n):
    """
    Split lst into sublists, each with n elements.
    The last sublist may have fewer than n elements if not enough remain.
    """
    random.shuffle(lst)
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def plot(iteration_player):
    plt.plot(iteration_player)
    plt.xlabel('Iteration')
    plt.ylabel('Number of Players')
    plt.title('Number of Players Over Iterations')
    plt.grid()
    plt.show()

def run_simulation(total_players, initial_amount, game_amount, players_per_game, max_iterations, governemnt):
    players = []
    games = []
    iteration_to_player = []
    player_name_start = "P"

    for i in range(total_players):
        players.append(Person(f"{player_name_start}{i}", initial_amount))

    original_players = players.copy()

    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        players = [player for player in players if player.get_money() >= game_amount]

        print(f"Iteration: {iteration} : {len(players)}")
        print(f"Total {sum(player.get_money() for player in players)} and tax collected {governemnt.total_tax_collected}")
        iteration_to_player.append(len(players))

        if len(players) == 1:
            return iteration_to_player, games, original_players, players

        games_players = split_into_random_lists(players, players_per_game)

        for game_player in games_players:
            game = Game(game_player, game_amount, governemnt)
            game.play()
            games.append(game)

    return iteration_to_player, games, original_players, players


total_players = 1000000
initial_amount = 1000
game_amount = 100
players_per_games = [100000]
max_iterations = 100
governemnt = Government(30)  # 10% tax

for players_per_game in players_per_games:
    iteration_to_player, games, original_players, players = run_simulation(total_players, initial_amount, game_amount, players_per_game, max_iterations, governemnt)
    print(f"After {len(iteration_to_player)} iterations, {len(players)} players remain out of {total_players} i.e {len(players)/total_players*100:.2f}%")
    print(f"Games played: {len(games)}")
    print(f"total Remaining money : {sum(player.get_money() for player in original_players)} and tax collected ({governemnt.percentage}): {governemnt.total_tax_collected}")
    print(f"total Remaining money with winners : {len(players)} : {sum(player.get_money() for player in players)}")
    # Find the winner
    if players:
        winner = max(players, key=lambda p: p.get_money())
        print(f"Winner: {winner.name} with {winner.get_money()} played {len(winner.games)} games")

    #plot(iteration_to_player)
    pass
