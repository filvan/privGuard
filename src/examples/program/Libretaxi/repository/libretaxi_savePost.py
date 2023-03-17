#function from repo.go to save a post
#Translated ina way that allow analysys with privguard. In the original code the post it is received as argument of the function. The last post is in the file and it is the last row. When returning it I manage and check the compliance with the policies
last_post_id = 0
def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    ConsumerID = kwargs.get('extra_args').get('user_id')
    MessageTxt = kwargs.get('extra_args').get('text')
    lon = kwargs.get('extra_args').get('lon')
    lat = kwargs.get('extra_args').get('lat')
    ReportCnt = kwargs.get('extra_args').get('report_cnt')

    libretaxi_posts = pd.read_csv(data_folder + "posts/data.csv")
    #add last new row
    global last_post_id
    last_el = last_post_id + 1
    last_post_id = last_el

    return libretaxi_posts['PostID']