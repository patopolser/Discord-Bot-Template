import json

def read_data(db: str):
    with open(f"./bot/database/{db}.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
        f.close()

    return data
    
def edit_data(data: str):
    with open(f"./bot/database/db.json", "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4, sort_keys = True)

        f.close()


class Database:

    def __init__(self, user_id: int = None) -> None:
        self.user_id = str(user_id)
        self.create_data()
        
    @property
    def data(self):
        return read_data("db")