# Test GOES HERE
import unittest
from SI507F17_finalproject import InsUser, InsPost
from SI507F17_finalproject_oauth import get_from_cache, get_data_from_api, CACHE_DICTION
from SI507F17_finalproject_database import conn, cur, execute_and_print

print("BELOW IS TEST OUTPUT FOR PROJECT 2 SI 507 F17 *****\n\n")


class TestClass(unittest.TestCase):
    def setUp(self):
        self.ins_user_instance = InsUser({'username':'hy501test', 'id': '6737424442', 'profile_picture': "https://scontent.cdninstagram.com/t51.2885-19/s150x150/25018144_294893787685696_3529974367213584384_n.jpg"})
        self.ins_post_instance = InsPost({'id': '1669788584103954038_6737424442',
                                        'user':{'id':'6737424442'},
                                        'images':{'low_resolution':{'url': "https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/25014793_229149194290605_8418496965175672832_n.jpg"}},
                                        'likes':{'count':0},
                                        'link':"https://www.instagram.com/p/BcsR97NhMZ2/",
                                        'tags':['mutipletags', 'test']
                                        })

    def test_InsUser_vartype(self):
        self.assertEqual(type(self.ins_user_instance.name), type(u"s"), "Wrong Type! Should be string.")
        self.assertEqual(type(self.ins_user_instance.id), type(u"s"), "Wrong Type! Should be string.")
        self.assertEqual(type(self.ins_user_instance.profile_url), type(u"s"), "Wrong Type! Should be string.")

    def test_InsUser_constructor(self):
        self.assertEqual(self.ins_user_instance.name, "hy501test", "Wrong Value! Should be hy501test.")
        self.assertEqual(self.ins_user_instance.id, "6737424442", "Wrong Value! Should be 6737424442.")
        self.assertEqual(self.ins_user_instance.profile_url, "https://scontent.cdninstagram.com/t51.2885-19/s150x150/25018144_294893787685696_3529974367213584384_n.jpg", "Wrong Link!")

    def test_InsUser_repr(self):
        self.assertEqual(self.ins_user_instance.__repr__(),"name: hy501test, uid: 6737424442, profile: https://scontent.cdninstagram.com/t51.2885-19/s150x150/25018144_294893787685696_3529974367213584384_n.jpg","Wrong String!")

    def test_InsPost_vartype(self):
        self.assertEqual(type(self.ins_post_instance.num_of_likes), type(1), "Wrong Type! Should be int.")
        self.assertEqual(type(self.ins_post_instance.num_of_tags), type(1), "Wrong Type! Should be int.")
        self.assertEqual(type(self.ins_post_instance.tags), type([""]), "Wrong Type! Should be list.")
        self.assertEqual(type(self.ins_post_instance.id), type(u"s"), "Wrong Type! Should be string.")
        self.assertEqual(type(self.ins_post_instance.owner), type(u"s"), "Wrong Type! Should be string.")
        self.assertEqual(type(self.ins_post_instance.post_url), type(u"s"), "Wrong Type! Should be string.")
        self.assertEqual(type(self.ins_post_instance.img_url), type(u"s"), "Wrong Type! Should be string.")

    def test_InsPost_constructor(self):
        self.assertEqual(self.ins_post_instance.id, "1669788584103954038_6737424442", "Wrong Value! Should be 1669788584103954038_6737424442.")
        self.assertEqual(self.ins_post_instance.post_url, "https://www.instagram.com/p/BcsR97NhMZ2/", "Wrong Link! Should be https://www.instagram.com/p/BcsR97NhMZ2/")
        self.assertEqual(self.ins_post_instance.num_of_tags, 2, "Wrong Value! Should be 2.")

    def test_InsPost_repr(self):
        self.assertEqual(self.ins_post_instance.__repr__(),"post_url:https://www.instagram.com/p/BcsR97NhMZ2/, owner:6737424442, likes:0")

    def test_InsPost_contains(self):
        self.assertTrue("mutipletags" in self.ins_post_instance, "tag: mutipletags should be in this instance.")
        self.assertTrue("test" in self.ins_post_instance, "tag: test should be in this instance.")
        self.assertTrue("abcd" not in self.ins_post_instance, "tag: abcd should not be in this instance.")


class TestOauth(unittest.TestCase):
    def setUp(self):
        self.data_instance = get_data_from_api("hy501test", 'https://api.instagram.com/v1/users/self/media/recent/', {'count':20})['data']
        self.cache_instance = get_from_cache('hy501test', CACHE_DICTION)['data']

    def test_get_data_from_api(self):
        self.assertEqual(self.data_instance[0]['created_time'],'1513274332', "Wrong Value! created_time Should be 1513274332.")

    def test_get_from_cache(self):
        self.assertEqual(self.cache_instance[0]['created_time'],'1513274332', "Wrong Value! created_time Should be 1513274332.")


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.query_result1 = execute_and_print("SELECT name from Users WHERE id='1421109997'")
        self.query_result2 = execute_and_print("SELECT tags from Posts WHERE num_of_tags=3")
        self.query_result3 = execute_and_print("SELECT name, img_url, num_of_likes from Posts INNER JOIN Users ON Posts.owner = Users.id WHERE num_of_likes>15", 1)
        self.query_result4 = execute_and_print("SELECT count(*) from Users")
        self.query_result5 = execute_and_print("SELECT count(*) from Posts")

    def test_table_users(self):
        self.assertEqual(self.query_result1[0][0],"toaruc", "Wrong Name! Should be toaruc.")

    def test_table_posts(self):
        self.assertEqual(self.query_result2[0][0],"forfun;multipletags;test", "Wrong Value! Should be forfun;multipletags;test.")

    def test_table_inner_join(self):
        self.assertEqual(self.query_result3[0][0],"toaruc", "Wrong Name! Should be toaruc.")
        self.assertEqual(self.query_result3[0][1],"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/23161520_910591929094155_2281174366332911616_n.jpg", "Wrong LINK!")
        self.assertEqual(self.query_result3[0][2],17, "Wrong Value! Should be 17.")

    def test_table_counts(self):
        self.assertEqual(self.query_result4[0][0],5, "Wrong Value! Should be 5.")
        self.assertEqual(self.query_result5[0][0],100, "Wrong Value! Should be 100.")

    def test_table_columns_users(self):
        col_names_users = ['id', 'name', 'profile_url']
        cur.execute("SELECT * from Users")
        tmp = cur.fetchall()
        result_col_names = []
        for elt in cur.description:
            result_col_names.append(elt[0])
        self.assertEqual(result_col_names, col_names_users, "Wrong Column Names!")

    def test_table_columns_posts(self):
        col_names_posts = ['id', 'owner', 'img_url', 'num_of_likes', 'post_url', 'num_of_tags', 'tags']
        cur.execute("SELECT * from Posts")
        tmp = cur.fetchall()
        result_col_names = []
        for elt in cur.description:
            result_col_names.append(elt[0])
        self.assertEqual(result_col_names, col_names_posts, "Wrong Column Names!")

if __name__ == "__main__":
    unittest.main(verbosity=2)
