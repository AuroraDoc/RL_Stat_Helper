import json
import requests
import sys

token = "API Ballchasing Token"

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
        url_response = requests.get(stats_url + game_id, headers={
            "Authorization": token})
        return url_response.json()

    def make_json(self):
        data = self.get_stats()
        self.replay_name = data["title"]
        self.replay_id = data["id"]
        #with open(f'{self.replay_name}({self.replay_id}).json', 'w') as f:
            #json.dump(data, f) (We dont need to dump the json into a file since its being handled by the node server)
        return data

    def important_stats(self):
        data = self.make_json()
        link = data["link"]
        gameMode = data["playlist_id"]
        team_size = data["team_size"]

        game = [{"Name": gameMode,
               "Team_Size": team_size,}]

# might want to add in the ball stat later if we can get possession and pressure percentages
        for idx in range(team_size):
            player = {"Name": data["blue"]["players"][idx]["name"],
                     "Team_Color": "Blue",
                     "Core_Stats": data["blue"]["players"][idx]["stats"]["core"],
                     "BPM": data["blue"]["players"][idx]["stats"]["boost"]["bpm"],
                     "Boost_Used_While_Supersonic": data["blue"]["players"][idx]["stats"]["boost"]["amount_used_while_supersonic"],
                     "Big_Pads_Collected": data["blue"]["players"][idx]["stats"]["boost"]["count_collected_big"],
                     "Small_Pads_Collected": data["blue"]["players"][idx]["stats"]["boost"]["count_collected_small"],
                     "Average_Speed": data["blue"]["players"][idx]["stats"]["movement"]["avg_speed"],
                     "Percent_Defensive_Half": data["blue"]["players"][idx]["stats"]["positioning"]["percent_defensive_half"],
                     "Percent_Offensive_Half": data["blue"]["players"][idx]["stats"]["positioning"]["percent_offensive_half"]}
            game.append(player.copy())
            player.clear()

        for idx in range(team_size):
            player = {"Name": data["orange"]["players"][idx]["name"],
                     "Team_Color": "Orange",
                     "Core_Stats": data["orange"]["players"][idx]["stats"]["core"],
                     "BPM": data["orange"]["players"][idx]["stats"]["boost"]["bpm"],
                     "Boost_Used_While_Supersonic": data["orange"]["players"][idx]["stats"]["boost"]["amount_used_while_supersonic"],
                     "Big_Pads_Collected": data["orange"]["players"][idx]["stats"]["boost"]["count_collected_big"],
                     "Small_Pads_Collected": data["orange"]["players"][idx]["stats"]["boost"]["count_collected_small"],
                     "Average_Speed": data["orange"]["players"][idx]["stats"]["movement"]["avg_speed"],
                     "Percent_Defensive_Half": data["orange"]["players"][idx]["stats"]["positioning"]["percent_defensive_half"],
                     "Percent_Offensive_Half": data["orange"]["players"][idx]["stats"]["positioning"]["percent_offensive_half"]}
            game.append(player.copy())
            player.clear()

         # like this with the players
        return game

def main():
    try:
        file = Replay(sys.argv[1])
        stats = file.important_stats() 
        print(stats)
        sys.stdout.flush()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
