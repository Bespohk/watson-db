"""empty message

Revision ID: 26ad29083da5
Revises: None
Create Date: 2019-10-02 14:35:55.145728

"""

# revision identifiers, used by Alembic.
revision = '26ad29083da5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()['upgrade_{}'.format(engine_name)]()


def downgrade(engine_name):
    globals()['downgrade_{}'.format(engine_name)]()


# Upgrade/downgrade functions for default

def upgrade_default():
    pass


def downgrade_default():
    pass

