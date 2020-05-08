# User

# 执行方式
# python manage.py shell
# %run 此文件的绝对路径

# eg:  
# %run  /Users/jiangjiebai/Desktop/gen_fake_data.py 

import datetime
from assets.models import Asset, AdminUser
from users.models import User, UserGroup
from terminal.models import Session, Terminal
from orgs.models import Organization
from orgs.utils import set_to_default_org

prefix = 'fake1-'

def create_users(start, end):
    for i in range(start, end):
        try:
            name = '{}-{}'.format(prefix, i)
            user = User.objects.create(username=name, name=name, email="{}@{}".format(name, 'jms.com'))
        except Exception as e:
            print('create user error: {}'.format(str(e)))
        else:
            print('create user: {}'.format(user))


# UserGroup


def create_user_groups(start, end):
    for i in range(start, end):
        try:
            name = '{}-{}'.format(prefix, i)
            user_group = UserGroup.objects.create(name=name)
        except Exception as e:
            print('create user group error: {}'.format(str(e)))
        else:
            print('create user group: {}'.format(user_group))

# AdminUser


def create_admin_users(start, end):
    for i in range(start, end):
        try:
            name = '{}-{}'.format(prefix, i)
            admin_user = AdminUser.objects.create(username=name, name=name)
        except Exception as e:
            print('create admin user error: {}'.format(str(e)))
        else:
            print('create admin user: {}'.format(admin_user))


# Asset

def create_assets(start, end):
    admin_user = AdminUser.objects.first()
    for i in range(start, end):
        try:
            name = '{}-{}'.format(prefix, i)
            asset = Asset.objects.create(hostname=name, ip=name, admin_user=admin_user)
        except Exception as e:
            print('create asset error: {}'.format(str(e)))
        else:
            print('create asset: {}'.format(asset))


# Session

def get_last_30_days_datetimes(start, end):
    now = datetime.datetime.utcnow()
    datetimes = [now - datetime.timedelta(days=i) for i in range(start, end)]
    return datetimes


def create_session(datetimes, start, end, is_finished):
    terminal = Terminal.objects.first()
    for date_start in datetimes:
        for i in range(start, end):
            try:
                name = '{}-{}'.format(prefix, i)
                session = Session.objects.create(user=name, user_id=name, asset=name, asset_id=name, system_user=name, system_user_id=name, terminal=terminal, is_finished=is_finished, date_start=date_start)
            except Exception as e:
                print('create session error: {}'.format(str(e)))
            else:
                print('create session: {}'.format(session))


# Org

def create_orgs(start, end):
    users = User.objects.all()

    for i in range(start, end):
        try:
            name = '{}-{}'.format(prefix, i)
            org = Organization.objects.create(name=name)
            org.users.set(users)
            org.admins.set(users[:50])
            org.auditors.set(users[50:70])
        except Exception as e:
            print('create org error: {}'.format(e))
        else:
            print('create org: {}'.format(org))


# -------- Create  --------


def create_fake_bulk():
    global prefix
    prefix = 'fake-bulk-'

    set_to_default_org()

    create_users(1, 10000)

    create_user_groups(1, 500)

    create_admin_users(1, 300)

    create_assets(1, 50000)

    create_orgs(1, 10)

    datetimes = get_last_30_days_datetimes(1, 30)
    create_session(datetimes, 1, 10000, True)
    create_session(datetimes, 1, 10000, False)

    datetimes = get_last_30_days_datetimes(1, 7)
    create_session(datetimes, 1, 20000, True)
    create_session(datetimes, 1, 20000, False)


def create_fake_test():
    global prefix
    prefix = 'fake-test-'
    set_to_default_org()

    create_users(1, 10)

    create_user_groups(1, 5)

    create_admin_users(1, 3)

    create_assets(1, 5)

    create_orgs(1, 3)

    datetimes = get_last_30_days_datetimes(1, 30)
    create_session(datetimes, 1, 10, True)
    create_session(datetimes, 1, 10, False)

    datetimes = get_last_30_days_datetimes(1, 7)
    create_session(datetimes, 1, 20, True)
    create_session(datetimes, 1, 20, False)


# create_fake_bulk()
create_fake_test()

