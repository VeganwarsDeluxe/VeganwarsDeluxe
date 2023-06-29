import math
from .Player import Player


class RatingManager:
    def __init__(self):
        pass

    def get_top(self):
        tts = ''
        _ = 9999999
        for user in Player.objects().order_by('-rating'):
            user.rating = int(user.rating)
            if _ < user.rating:
                continue
            _ = user.rating
            user.save()
            tts += f'{user.username} ({user.rating})\n'
        return tts

    def get_k(self, rating):
        if rating > 2400:
            return 10
        if 2400 > rating > 1100:
            return 20
        return 40

    def outcome(self, a, b, a_s, b_s):
        EWP_a = 1 / (1 + (10 ** ((b.rating - a.rating) / 400)))
        EWP_b = 1 / (1 + (10 ** ((a.rating - b.rating) / 400)))

        AWP_a = 0.5
        AWP_b = 0.5

        if a_s > b_s:
            AWP_a = 1
            AWP_b = 0
        elif b_s > a_s:
            AWP_a = 0
            AWP_b = 1

        K_a, K_b = self.get_k(a.rating), self.get_k(b.rating)

        R_a = a.rating + K_a * (AWP_a - EWP_a)
        R_b = b.rating + K_b * (AWP_b - EWP_b)

        return int(math.ceil(R_a)), int(math.ceil(R_b))

    def get_by_username(self, username):
        try:
            return Player.objects.get(username=username)
        except:
            pass

    def get_user(self, user_id, name, username):
        try:
            Player.objects(id=user_id).update_one(upsert=True, name=name, username=username)
            user = Player.objects.get(id=user_id)
        except:
            user = Player(id=user_id, name=name, username=username)
            user.save()
        return user

    def process_lambda(self, m):
        if not m.from_user:
            return
        self.get_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
