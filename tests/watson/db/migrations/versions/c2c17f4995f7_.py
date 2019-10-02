"""empty message

Revision ID: c2c17f4995f7
Revises: None
Create Date: 2019-10-02 15:48:32.285000

"""

# revision identifiers, used by Alembic.
revision = 'c2c17f4995f7'
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

