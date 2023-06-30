#handle of callback.go
#we marshal the data for identifying how to act on post

from src.examples.program.Libretaxi.repository import libretaxi_findPost, libretaxi_findUser,libretaxi_saveUser, libretaxi_savePost

def run(data_folder, **kwargs):

    action = kwargs.get('extra_args').get('post_report')

    if action == 'REPORT_POST':
        libretaxi_posts = libretaxi_findPost.run(data_folder,**kwargs)
        post_infos = libretaxi_posts.iloc[-1:]
        post_infos.ReportCnt = str(int(str(post_infos.ReportCnt)) + 1)
        kwargs.__setitem__('report_cnt',post_infos.ReportCnt)
        libretaxi_savePost.run(data_folder,**kwargs)
        return post_infos
    elif action == 'SHADOW_BAN':
        libretaxi_users = libretaxi_findUser.run(data_folder,**kwargs)
        user_infos = libretaxi_users.iloc[-1:]
        user_infos.ShadowBanned = 'Y'
        kwargs.__setitem__('shadow_banned',user_infos.ShadowBanned)
        libretaxi_saveUser.run(data_folder,**kwargs)

        return libretaxi_users.iloc[-1:0].drop(['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)