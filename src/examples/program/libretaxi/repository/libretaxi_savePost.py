# function from repo.go to save a post
# Translated ina way that allow analysys with privguard. In the original code the post it is received as argument of the function. The last post is in the file and it is the last row. When returning it I manage and check the compliance with the policies


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    PostID = kwargs.get('extra_args').get('post_id')
    Text = kwargs.get('extra_args').get('text')
    lon = kwargs.get('extra_args').get('lon')
    lat = kwargs.get('extra_args').get('lat')
    ReportCnt = kwargs.get('extra_args').get('report_cnt')

    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    # add last new row
    if not libretaxi_posts[libretaxi_posts.PostID == PostID]:
        # get new id
        last_el = str(int(str(libretaxi_posts.iloc[-1:].postID)) + 1)

    return libretaxi_posts['PostID']
