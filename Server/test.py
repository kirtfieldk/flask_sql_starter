import unittest
import os
from flask import json
from project import app, db
####################################
# IF DOCKER CONTAINER WILL NOT RUN #
# COMMENT THE unittest.main() ON ###
# BOTTOM OF FILE ###################
####################################

#################
###TEST CASES####
#################
TEST_DB = "applicants-collection"


class TestCase(unittest.TestCase):
     # executed prior to each test
    with app.app_context():
        db.drop_all()
        db.create_all()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #     os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev intern', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='Ryan', last_name="Kirtfield",
                                 school='Penn State', position='dev intern', degree='mathematics')),
            content_type='application/json',
            follow_redirects=True
        )
        self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='Little', last_name="John",
                                 school='VT', position='dev intern', degree='Health')),
            content_type='application/json',
            follow_redirects=True
        )
        self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='Lion', last_name="Welsh",
                                 school='Harvard', position='dev intern', degree='good')),
            content_type='application/json',
            follow_redirects=True
        )
    ####################
    ##POSTING ENTRIES###
    ####################

    def test_post_app1(self):
        tester = app.test_client(self)
        res = self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev intern', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 201)

    def test_post_missing_fields(self):
        tester = app.test_client(self)
        res = self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(
                school='VCU', position='dev intern', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 400)

    def test_post_invalid_position(self):
        tester = app.test_client(self)
        res = self.app.post(
            '/api/v1/applicants',
            data=json.dumps(dict(
                school='VCU', position='cat caller', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 400)

    ####################
    ##Testing Routes####
    ####################

    def test_index(self):
        tester = app.test_client(self)
        res = tester.get('/api/v1/applicants', content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_index_without_json(self):
        tester = app.test_client(self)
        res = tester.get('/api/v1/applicants', content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_fetch_application(self):
        tester = app.test_client(self)
        res = tester.get('/api/v1/applicants/2',
                         content_type='application/json')
        self.assertEqual(res.status_code, 200)

    ####################
    ##FETCHING DATA#####
    ####################
    def test_fetch_application_nonexist(self):
        tester = app.test_client(self)
        res = tester.get('/api/v1/applicants/200',
                         content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_delete_nonexisting_index(self):
        tester = app.test_client(self)
        res = tester.delete('/api/v1/applicants/200 ',
                            content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_delete_exists_index(self):
        tester = app.test_client(self)
        res = tester.delete('/api/v1/applicants/1',
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_fetch_application_nonexist_after_delete(self):
        tester = app.test_client(self)
        res = tester.get('/api/v1/applicants/1',
                         content_type='application/json')
        self.assertEqual(res.status_code, 404)
    ####################
    ##Updating ENTRIES##
    ####################

    def test_update_some_prop(self):
        tester = app.test_client(self)
        res = self.app.put(
            '/api/v1/applicants/2',
            data=json.dumps(dict(first_name='bar')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)

    def test_update_all_prop(self):
        tester = app.test_client(self)
        res = self.app.put(
            '/api/v1/applicants/2',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev engineer', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)

    ###########################
    ##TEST POST IN PUT METHOD##
    ###########################
    def test_wrong_method(self):
        tester = app.test_client(self)
        res = self.app.post(
            '/api/v1/applicants/7',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev engineer', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 405)
    ###########################
    ##TEST POST IN GET METHOD##
    ###########################

    def test_wrong_method_post_in_get(self):
        tester = app.test_client(self)
        res = self.app.post(
            '/api/v1/applicants/7',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev engineer', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 405)
    ###########################
    ##TEST PUT IN GET METHOD###
    ###########################

    def test_wrong_method_put_in_get(self):
        tester = app.test_client(self)
        res = self.app.put(
            '/api/v1/applicants',
            data=json.dumps(dict(first_name='bar', last_name="Kirtfield",
                                 school='VCU', position='dev engineer', degree='eyesight')),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 405)

    ###########################
    ##TEST PUT WITH EMPTY######
    ###########################

    def test_wrong_method_put_empty(self):
        tester = app.test_client(self)
        res = self.app.put(
            '/api/v1/applicants',
            data=json.dumps(dict()),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 405)

    ###########################
    ##TEST SEARCH METHODS######
    ###########################
    def test_search_school(self):
        tester = app.test_client(self)
        res = self.app.get(
            '/api/v1/applicants/school/vcu',
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)

    def test_search_school_no_results(self):
        tester = app.test_client(self)
        res = self.app.get(
            '/api/v1/applicants/school/lslslsls',
            data=json.dumps(dict()),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)

    def test_seach_name(self):
        tester = app.test_client(self)
        res = self.app.get(
            '/api/v1/applicants/lastname/kirtfield',
            data=json.dumps(dict()),
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)

    def test_search_name_no_results(self):
        tester = app.test_client(self)
        res = self.app.get(
            '/api/v1/applicants/lastname/jwoefjei',
            data=json.dumps(dict()),
            follow_redirects=True
        )
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
