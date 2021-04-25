import pandas as pd
from surprise import dump


def get_user_rec_activities(user_id, club_path, weights_path, min, max):
    club = pd.read_csv(club_path)
    algorithm = dump.load(weights_path)
    top_n = sorted([(i[1]["item"], algorithm.predict(str(user_id), str(i[1]["item"]))[3]) for i in club.iterrows() if
                    not type(i[1]["Наименование_услуги"]) == float], key=lambda x: -x[1])[min:max]
    top_n = list(map(lambda x: x[0], top_n))
    return top_n
