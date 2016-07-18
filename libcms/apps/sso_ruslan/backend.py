# encoding: utf-8
import logging
import json
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User

from ruslan import connection_pool, humanize, grs
from .models import RuslanUser
from sso import models as sso_models

RUSLAN = getattr(settings, 'RUSLAN', {})

API_ADDRESS = RUSLAN.get('api_address', 'http://localhost/')
API_USERNAME = RUSLAN.get('username')
API_PASSWORD = RUSLAN.get('password')
RUSLAN_USERS_DATABASE = RUSLAN.get('users_database', 'allusers')

AUTH_SOURCE = 'ruslan'

logger = logging.getLogger('django.request')


class RuslanAuthBackend(object):
    def authenticate(self, username=None, password='', need_check_password=True):
        if username:
            username = username.strip()

        if password:
            password = password.strip()

        if not username:
            return None

        portal_client = connection_pool.get_client(API_ADDRESS, API_USERNAME, API_PASSWORD)

        if need_check_password:
            try:
                reader_id = username.replace('\\', '\\\\').replace('"', '\\"')
                password = password.replace('\\', '\\\\').replace('"', '\\"')
                sru_response = portal_client.search(
                    query='@attrset bib-1 @attr 1=100 "%s"' % (reader_id,),
                    database=RUSLAN_USERS_DATABASE,
                    maximum_records=1
                )
                sru_records = humanize.get_records(sru_response)

                if not sru_records:
                   return None

            except Exception as e:
                logger.exception(e)
                return None

        sru_reps = portal_client.get_user(username, database=RUSLAN_USERS_DATABASE)
        records = humanize.get_records(sru_reps)

        if not records:
            return None
        # 101 - фамилия
        # 102 - имя
        # 103 - отчество
        grs_record = grs.Record.from_dict(humanize.get_record_content(records[0]))
        user_password = password

        if need_check_password and user_password != password:
            return None

        return self.get_or_create_user(username, password, grs_record)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @transaction.atomic()
    def get_or_create_user(self, username, password, grs_record):

        first_name = grs_record.get_field_value('102')[:30]
        last_name = grs_record.get_field_value('101')[:30]
        email = grs_record.get_field_value('122')[:75]
        groups = ['users']

        user = sso_models.create_or_update_external_user(
            external_username=username,
            auth_source=AUTH_SOURCE,
            first_name=first_name,
            last_name=last_name,
            email=email,
            groups=groups,
            is_active=True
        ).user

        try:
            ruslan_user = RuslanUser.objects.get(user=user)
            need_update = False
            if ruslan_user.username != username:
                ruslan_user.username = username
                need_update = True
            if ruslan_user.password != password:
                ruslan_user.password = password
                need_update = True

            if need_update:
                ruslan_user.save()
        except RuslanUser.DoesNotExist:
            ruslan_user = RuslanUser(user=user, username=username, password=password)
            ruslan_user.save()

        return user
