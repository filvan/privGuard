import datetime
from datetime import timedelta


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    user_id = kwargs.get('extra_args').get('user_id')
    # saving of user based on previous research if user already exists
    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    time_range = datetime.datetime.today() - timedelta(minutes=5)
    libretaxi_posts = libretaxi_posts[libretaxi_posts.Date >= str(time_range)]
    libretaxi_posts = libretaxi_posts[libretaxi_posts.DataSubjectID == user_id]
    return libretaxi_posts.count()
