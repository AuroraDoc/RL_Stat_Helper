# to get the stats of a replay we need the replay id
# we can use the post requests output of the id to then put into the get request
import json
import requests

token = "Your API token here"


class Replay:
    def __init__(self, file):
        self.replay_id = None
        self.replay_name = None
        self.file = file

    def post_id(self):
        if not self.replay_id:
            uploads_url = 'https://ballchasing.com/api/v2/upload?visibility=private'
            files = {'file': open(self.file, "rb")}
            res = requests.post(uploads_url, headers={
                "Authorization": token}, files=files)
            res_json = res.json()
            self.replay_id = res_json['id']
        return self.replay_id

    def get_stats(self):
        game_id = self.post_id()
        stats_url = 'https://ballchasing.com/api/replays/'
        res = requests.get(stats_url + game_id, headers={
            "Authorization": token})
        return res.json()

    def make_json(self):
        data = self.get_stats()
        self.replay_name = data["title"]
        self.replay_id = data["id"]
        with open(f'{self.replay_name}({self.replay_id}).json', 'w') as f:
            json.dump(data, f)
        return data

    def important_stats(self):
        data = self.make_json()
        link = data["link"]
        game_mode = data["playlist_id"]
        team_size = data["team_size"]

        blue_team = {}
        orange_team = {}
# might want to add in the ball stat later if we can get possession and pressure percentages
        for idx in range(0, team_size-1):
            player = {}
            player.update({"name": data["blue"]["players"][idx]["name"]}) 
            # update creates a new dictionary everytime. So initialize it once and predefine all the stats as keys and put the json in the val
            # Core
            player.update({"core_stats": data["blue"]["players"][idx]["stats"]["core"]})
            # Boost
            player.update({"bpm": data["blue"]["players"][idx]["stats"]["boost"]["bpm"]})
            player.update({"amount_used_while_supersonic": data["blue"]["players"][idx]["stats"]["boost"]["amount_used_while_supersonic"]})
            player.update({"count_collected_big": data["blue"]["players"][idx]["stats"]["boost"]["count_collected_big"]})
            player.update({"count_collected_small": data["blue"]["players"][idx]["stats"]["boost"]["count_collected_small"]})
            # Movement
            player.update({"avg_speed": data["blue"]["players"][idx]["stats"]["movement"]["avg_speed"]})
            # Position
            player.update({"percent_defensive_half": data["blue"]["players"][idx]["stats"]["positioning"]["percent_defensive_half"]})
            player.update({"percent_offensive_half": data["blue"]["players"][idx]["stats"]["positioning"]["percent_offensive_half"]})
            blue_team.update(player)
            player.clear()

        for idx in range(0, team_size-1):
            player = {}
            player.update({"name": data["orange"]["players"][idx]["name"]})
            # Core
            player.update({"core_stats": data["orange"]["players"][idx]["stats"]["core"]})
            # Boost
            player.update({"bpm": data["orange"]["players"][idx]["stats"]["boost"]["bpm"]})
            player.update({"amount_used_while_supersonic": data["orange"]["players"][idx]["stats"]["boost"]["amount_used_while_supersonic"]})
            player.update({"count_collected_big": data["orange"]["players"][idx]["stats"]["boost"]["count_collected_big"]})
            player.update({"count_collected_small": data["orange"]["players"][idx]["stats"]["boost"]["count_collected_small"]})
            # Movement
            player.update({"avg_speed": data["orange"]["players"][idx]["stats"]["movement"]["avg_speed"]})
            # Position
            player.update({"percent_defensive_half": data["orange"]["players"][idx]["stats"]["positioning"]["percent_defensive_half"]})
            player.update({"percent_offensive_half": data["orange"]["players"][idx]["stats"]["positioning"]["percent_offensive_half"]})
            orange_team.update(player)
            player.clear()
        game = {}
        game.update({"blue": blue_team})
        game.update({"orange": orange_team})
        return game
def main():
    file = Replay("Path to file you want to use!")
    stats = file.important_stats()
    print(stats)


if __name__ == '__main__':
    main()
