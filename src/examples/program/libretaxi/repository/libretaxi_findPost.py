def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    post_id = kwargs.get('extra_args').get('post_id')

    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    libretaxi_posts = libretaxi_posts[libretaxi_posts.PostID == post_id]

    return libretaxi_posts
