"""empty message

Revision ID: 4bf021abcee7
Revises: None
Create Date: 2019-10-02 15:41:28.431475

"""

# revision identifiers, used by Alembic.
revision = '4bf021abcee7'
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

