# MIT License

# Copyright (c) 2021 sunblaze-ucb

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" PrivAnalyzer. """

import os
import sys

privguard_path = os.getcwd()
sys.path.append(os.path.join(privguard_path, 'parser'))
sys.path.append(os.path.join(privguard_path, "stub_libraries"))
from importlib.util import spec_from_file_location, module_from_spec
import json
from shutil import copyfile
import argparse

from attribute import Satisfied
from policy_tree import Policy

import stub_pandas
import stub_numpy
import stub_numpy.random as stub_random
import stub_lightgbm
import stub_xgboost
import stub_statsmodels.tsa.arima.model as stub_arima
import stub_sklearn.cross_validation as stub_cross_validation
import stub_sklearn.metrics as stub_metrics
import stub_sklearn.model_selection as stub_model_selection
from examples.program.Libretaxi.locales import english, es, fa, pt_br, pt_pt, ru
program_map = {
    0: "./examples/program/ehr_example.py",
    # 1: "./examples/program/1_fraud_detection.py",
    # 2: "./examples/program/2_fraud_detection.py",
    # 3: "./examples/program/3_merchant_recommendation.py",
    4: "./examples/program/4_customer_satisfaction_prediction.py",
    5: "./examples/program/5_customer_transaction_prediction.py",
    6: "./examples/program/6_customer_transaction_prediction.py",
    7: "./examples/program/extra_examples/bank_customer_classification.py",
    # 8: "./examples/program/8_bank_customer_segmentation.py",
    # 9: "./examples/program/9_credit_risk_analysis.py",
    # 10: "./examples/program/10_customer_churn_prediction.py",
    # 11: "./examples/program/11_heart_disease_causal_inference.py",
    # 12: "./examples/program/12_classify_forest_categories.py",
    # 13: "./examples/program/13_simple_lstm.py",
    # 14: "./examples/program/14_solve_titanic.py",
    # 15: "./examples/program/15_earthquake_prediction.py",
    # 16: "./examples/program/16_display_advertising.py",
    # 17: "./examples/program/17_fraud_detection.py",
    # 18: "./examples/program/18_restaurant_revenue_prediction.py",
    # 19: "./examples/program/19_nfl_analytics.py",
    # 20: "./examples/program/20_ncaa_prediction.py",
    # 21: "./examples/program/21_home_value_prediction.py",
    # 22: "./examples/program/22_malware_prediction.py",
    23: "./examples/program/23_web_traffic_forecasting.py",
    24: "./examples/program/cpra_example.py",


    25: "./examples/program/Libretaxi/libretaxi_example.py",
    26: "./examples/program/Libretaxi/repository/libretaxi_saveUser.py",
    27: "./examples/program/Libretaxi/libretaxi_ModifyUser.py",
    28: "./examples/program/Libretaxi/libretaxi_callback.py",
    29: "./examples/program/Libretaxi/libretaxi_validation.py",
    30: "./examples/program/Libretaxi/repository/libretaxi_savePost.py",
    31: "./examples/program/Libretaxi/repository/libretaxi_findUserAround.py",
    32: "./examples/program/Libretaxi/repository/libretaxi_recentPosts.py",
    33: "./examples/program/Libretaxi/menu/libretaxi_ask_location.py",
    34: "./examples/program/Libretaxi/menu/libretaxi_feed_menu.py",
    35: "./examples/program/Libretaxi/menu/libretaxi_init_menu.py",
    36: "./examples/program/Libretaxi/menu/libretaxi_menu.py",
    37: "./examples/program/Libretaxi/menu/libretaxi_post_menu.py",
    38: "./examples/program/Libretaxi/repository/libretaxi_findPost.py",
    39: "./examples/program/Libretaxi/repository/libretaxi_findUser.py",
    40: "./examples/program/Libretaxi/libretaxi_locale.py",
    41: "./examples/program/extra_examples/bank_customer_churn_prediction.py",
    42: "./examples/program/extra_examples/bank_customer_classification.py",
    #selfmailbot
    50: "./examples/program/selfmailbot/app/confirm_email.py",
    51: "./examples/program/selfmailbot/app/resend.py",
    52: "./examples/program/selfmailbot/app/reset_email.py",
    53: "./examples/program/selfmailbot/app/send_confirmation.py",
    54: "./examples/program/selfmailbot/app/send_photo.py",
    55: "./examples/program/selfmailbot/app/send_text_message.py",
    56: "./examples/program/selfmailbot/app/start.py",

    57: "./examples/program/selfmailbot/celery/send_confirmation_mail.py",
    58: "./examples/program/selfmailbot/celery/send_file.py",
    59: "./examples/program/selfmailbot/celery/send_text.py",

    60: "./examples/program/selfmailbot/mail/send_confirmation_mail.py",
    61: "./examples/program/selfmailbot/mail/send_mail.py",
    62: "./examples/program/selfmailbot/models/get_user_by_confirmation_link.py",
    63: "./examples/program/selfmailbot/models/get_user_instance.py",
    64: "./examples/program/selfmailbot/web.py",

}

data_map = {
    0: "./examples/data/ehr_example/",
    # 1: "./examples/data/fraud_detection_1/",
    # 2: "./examples/data/fraud_detection_1/",
    # 3: "./examples/data/merchant_recommendation/",
    4: "./examples/data/customer_satisfaction_prediction/",
    5: "./examples/data/customer_transaction_prediction/",
    6: "./examples/data/customer_transaction_prediction/",
    7: "./examples/data/bank_customer_churn/",
    # 8: "./examples/data/bank_customer_segmentation/",
    # 9: "./examples/data/credit_risk_analysis/",
    # 10: "./examples/data/customer_churn_prediction/",
    # 11: "./examples/data/heart_disease_causal_inference/",
    # 12: "./examples/data/classify_forest_categories/",
    # 13: "./examples/data/simple_lstm/",
    # 14: "./examples/data/solve_titanic/",
    # 15: "./examples/data/earthquake_prediction/",
    # 16: "./examples/data/display_advertising/",
    # 17: "./examples/data/fraud_detection_2/",
    # 18: "./examples/data/restaurant_revenue_prediction/",
    # 19: "./examples/data/nfl_analytics/",
    # 20: "./examples/data/ncaa_prediction/",
    # 21: "./examples/data/home_value_prediction/",
    # 22: "./examples/data/malware_prediction/",
    23: "./examples/data/web_traffic_forecasting/",
    24: "./examples/data/cpra/",
    25: "./examples/data/libretaxi_cpra/",
    26: "./examples/data/libretaxi_cpra/",
    27: "./examples/data/libretaxi_cpra/",
    28: "./examples/data/libretaxi_cpra/",
    29: "./examples/data/libretaxi_cpra/",
    30: "./examples/data/libretaxi_cpra/",
    31: "./examples/data/libretaxi_cpra/",
    32: "./examples/data/libretaxi_cpra/",
    33: "./examples/data/libretaxi_cpra/",
    34: "./examples/data/libretaxi_cpra/",
    35: "./examples/data/libretaxi_cpra/",
    36: "./examples/data/libretaxi_cpra/",
    37: "./examples/data/libretaxi_cpra/",
    38: "./examples/data/libretaxi_cpra/",
    39: "./examples/data/libretaxi_cpra/",
    40: "./examples/data/libretaxi_cpra/",
    41: "./examples/data/bank_customer_churn/",
    42: "./examples/data/bank_customer_churn/",
    50: "./examples/data/selfmailbot/",
    51: "./examples/data/selfmailbot/",
    52: "./examples/data/selfmailbot/",
    53: "./examples/data/selfmailbot/",
    54: "./examples/data/selfmailbot/",
    55: "./examples/data/selfmailbot/",
    56: "./examples/data/selfmailbot/",
    57: "./examples/data/selfmailbot/",
    58: "./examples/data/selfmailbot/",
    59: "./examples/data/selfmailbot/",
    60: "./examples/data/selfmailbot/",
    61: "./examples/data/selfmailbot/",
    62: "./examples/data/selfmailbot/",
    63: "./examples/data/selfmailbot/",
    64: "./examples/data/selfmailbot/",

}

lib_map = {
    0: {'numpy':stub_numpy, 'pandas':stub_pandas},
    4: {'cross_validation': stub_cross_validation, 'metrics': stub_metrics, 'numpy': stub_numpy, 'pandas': stub_pandas, 'xgboost': stub_xgboost},
    5: {'lgb':stub_lightgbm, 'metrics': stub_metrics, 'model_selection':stub_model_selection, 'numpy':stub_numpy, 'pandas':stub_pandas, 'random':stub_random},
    6: {'numpy':stub_numpy, 'pandas':stub_pandas},

    7: {'numpy': stub_numpy, 'pandas': stub_pandas,'lgb':stub_lightgbm, 'metrics': stub_metrics, 'model_selection':stub_model_selection},

    23: {'numpy':stub_numpy, 'pandas':stub_pandas, 'arima': stub_arima},
    24: {'numpy':stub_numpy, 'pandas':stub_pandas},
    25: {'numpy': stub_numpy, 'pandas': stub_pandas},
    26: {'numpy': stub_numpy, 'pandas': stub_pandas},
    27: {'numpy': stub_numpy, 'pandas': stub_pandas},
    28: {'numpy': stub_numpy, 'pandas': stub_pandas},
    29: {'numpy': stub_numpy, 'pandas': stub_pandas},
    30: {'numpy': stub_numpy, 'pandas': stub_pandas},
    31: {'numpy': stub_numpy, 'pandas': stub_pandas},
    32: {'numpy': stub_numpy, 'pandas': stub_pandas},
    33: {'numpy': stub_numpy, 'pandas': stub_pandas},
    34: {'numpy': stub_numpy, 'pandas': stub_pandas},
    35: {'numpy': stub_numpy, 'pandas': stub_pandas},
    36: {'numpy': stub_numpy, 'pandas': stub_pandas},
    37: {'numpy': stub_numpy, 'pandas': stub_pandas},
    38: {'numpy': stub_numpy, 'pandas': stub_pandas},
    39: {'numpy': stub_numpy, 'pandas': stub_pandas},
    40: {'numpy': stub_numpy, 'pandas': stub_pandas},
    41: {'numpy': stub_numpy, 'pandas': stub_pandas},
    42: {'numpy': stub_numpy, 'pandas': stub_pandas,'cross_validation': stub_cross_validation},
    50: {'pandas': stub_pandas},
    51: {'pandas': stub_pandas},
    52: {'pandas': stub_pandas},
    53: {'pandas': stub_pandas},
    54: {'pandas': stub_pandas},
    55: {'pandas': stub_pandas},
    56: {'pandas': stub_pandas},
    57: {'pandas': stub_pandas},
    58: {'pandas': stub_pandas},
    59: {'pandas': stub_pandas},
    60: {'pandas': stub_pandas},
    61: {'pandas': stub_pandas},
    62: {'pandas': stub_pandas},
    63: {'pandas': stub_pandas},
    64: {'pandas': stub_pandas},

}

locales = {
    'english': english,
    'spanish': es,
    'portugese': pt_pt,
    'portugese_brasil':pt_br,
    'russian': ru
}
def analyze(module, data_folder, lib_list):
    return module.run(data_folder, lightgbm=stub_lightgbm, **lib_list)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--example_id', help='The example program ID', type=int, default=6)
    parser.add_argument('--post_report', help='Post action', type=str, default='REPORT_POST')
    parser.add_argument('--lat', help="Latitude for user", type=str, default="")
    parser.add_argument('--lon', help="Longitude for user", type=str, default="")
    parser.add_argument('--user_id', help='User to find', type = str, default='n_consumer')
    parser.add_argument('--consent_use', help='Consent use data', type = str, default='N')
    parser.add_argument('--consent_share', help='Consent share data', type = str, default='N')
    parser.add_argument('--consent_sell', help='Consent sell data', type = str, default='N')
    parser.add_argument('--consent_collection', help='Consent collection data', type = str, default='N')
    parser.add_argument('--consent_retention', help='Consent retention data', type = str, default='N')
    parser.add_argument('--guardian_consent', help='Consent from guardians data', type = str, default='N')
    parser.add_argument('--request_deletion', help='Request deletion of data from user', type = str, default='N')
    parser.add_argument('--request_disclosure', help='Request disclosure of data from user', type = str, default='N')
    parser.add_argument('--request_inaccurate', help='Request modification of data from user because inaccurate', type = str, default='N')
    parser.add_argument('--limit_use', help='User request limit use', type = str, default='N')
    parser.add_argument('--age', help='User age', type = int, default=16)
    parser.add_argument('--menu_id', help='Menu ID associated to user', type = str, default="")
    parser.add_argument('--username', help='User username', type = str, default="")
    parser.add_argument('--first_name', help='User first name', type = str, default="")
    parser.add_argument('--last_name', help='User last name', type = str, default="")
    parser.add_argument('--language_code', help='User language code', type = str, default="")
    parser.add_argument('--report_cnt', help='User report count', type = int, default=0)
    parser.add_argument('--shadow_banned', help='User is shadow banned', type = str, default="N")
    parser.add_argument('--text', help='User text message', type = str, default="")
    parser.add_argument('--post_id', help='Id of post', type = str, default="")
    parser.add_argument('--locales', help = 'Language code', type = str, default='english')

    parser.add_argument('--attachment', help = 'Attachment email', type = int, default=None)
    parser.add_argument('--attachment_name', help = 'Attachment name for email', type = str, default='')
    parser.add_argument('--email', help = 'Attachment name for email', type = str, default='')
    parser.add_argument('--subject', help = 'Subject for email', type = str, default='')
    parser.add_argument('--link', help = 'Confirmation link', type = str, default='')

    parser.add_argument('--key',help ='Confirmation key for email', type = str, default = '')
    args = parser.parse_args()
    user = {'ConsumerID':args.user_id,
            'ConsentUse':args.consent_use,
            'ConsentShare':args.consent_share,
            'ConsentSell': args.consent_sell,
            'ConsentCollection': args.consent_collection,
            'ConsentRetention': args.consent_retention,
            'GuardianConsent': args.guardian_consent,
            'RequestDeletion': args.request_deletion,
            'RequestDisclosure': args.request_disclosure,
            'RequestInaccurate': args.request_inaccurate,
            'LimitUse': args.limit_use,
            'MenuID': args.menu_id,
            'Username': args.username,
            'FirstName': args.first_name,
            'LastName': args.last_name,
            'Longitude': args.lon,
            'Latitude': args.lat,
            'LanguageCode':args.language_code,
            'ReportCnt':args.report_cnt,
            'ShadowBanned': args.shadow_banned
            }

    extra_args = {
        'post_report': args.post_report,
        'lat': args.lat,
        'lon':args.lon,
        'user_id': args.user_id,
        'user':user,
        'text':args.text,
        'post_id': args.post_id,
        'report_cnt': args.report_cnt,
        'menu_id': args.menu_id,
        'first_name': args.first_name,
        'last_name': args.last_name,
        'shadow_banned': args.shadow_banned,
        'language_code': args.language_code,
        'key': args.key,
        'email': args.email,
        'attachment': args.attachment,
        'attachment_name': args.attachment_name,
        'subject': args.subject,
        'link': args.link
    }
    lib_map[args.example_id].__setitem__('locales',locales[args.locales])
    return program_map[args.example_id], data_map[args.example_id], lib_map[args.example_id], extra_args

if __name__ == '__main__':

    script, data_folder, lib_list, extra_args = parse()

    spec = spec_from_file_location("default_module", script)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    lib_list.__setitem__('extra_args',extra_args)
    result = analyze(module, data_folder, lib_list)
    result = analyze(module, data_folder, lib_list)
    print("\nResidual policy of the output:" + str(result))

