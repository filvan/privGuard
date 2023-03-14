#handle of callback.go
#we marshal the data for identifying how to act on post

import repository.libretaxi_findPost as find_post
import repository.libretaxi_findUser as find_user
import repository.libretaxi_saveUser as save_user
import repository.libretaxi_savePost as save_post

def run(data_folder, **kwargs):
    #pd = kwargs.get('pandas')
    action = kwargs.get('extra_args').get('action')

    if action == 'REPORT_POST':
        libretaxi_posts = find_post.run(data_folder,**kwargs)
        post_infos = libretaxi_posts.iloc[-1:]
        post_infos.ReportCnt = str(int(str(post_infos.ReportCnt)) + 1)
        kwargs.__setitem__('reportCnt',post_infos.ReportCnt)
        save_post(data_folder,**kwargs)
        return post_infos
    elif action == 'SHADOW_BAN':
        libretaxi_users = find_user.run(data_folder,**kwargs)
        user_infos = libretaxi_users.iloc[-1:]
        user_infos.ShadowBanned = 'Y'
        kwargs.__setitem__('shadow_banned',user_infos.ShadowBanned)
        save_user(data_folder,**kwargs)

        return libretaxi_users.iloc[-1:0].drop(['ConsentUse', 'ConsentShare', 'ConsentSell', 'ConsentRetetention', 'ConsentCollection', 'ConsentRetention','GuardianConsent', 'RequestDeletion', 'RequestDisclosure', 'RequestInaccurate'], axis=1)