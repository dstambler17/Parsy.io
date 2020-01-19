"""empty message

Revision ID: 6a877258d70e
Revises:
Create Date: 2019-09-08 19:34:36.038774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6a877258d70e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report',
    sa.Column('reportid', sa.Integer(), nullable=False),
    sa.Column('courseID', sa.String(length=30), nullable=True),
    sa.Column('semester', sa.String(length=15), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('status', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('reportid')
    )
    '''op.drop_table('ta_oh')
    op.drop_table('location')
    op.drop_table('happens_in')
    op.drop_table('teaches')
    op.drop_table('works_for')
    op.drop_table('course')
    op.drop_table('ta')
    op.drop_table('professor')
    op.drop_table('prof_oh')
    op.drop_table('temp')
    op.drop_table('exam_data')
    op.drop_table('assignment_data')
    op.drop_table('help')
    op.drop_table('class_times')
    op.drop_table('has_help')'''
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('has_help',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('HelpID', mysql.VARCHAR(length=50), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('class_times',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('DayTime', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('LocID', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('TYPE', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('help',
    sa.Column('HelpID', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('Type', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('HName', mysql.VARCHAR(length=50), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('assignment_data',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('Date', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('Name', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('exam_data',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('Date', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('Time', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('Name', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('temp',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('LName', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('FName', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('Department', mysql.VARCHAR(length=40), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('prof_oh',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('DayTime', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('LocID', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('professor',
    sa.Column('ProfId', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('LName', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('FName', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('PEmail', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('Department', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('ProfId'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('ta',
    sa.Column('TEmail', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('LName', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('FName', mysql.VARCHAR(length=25), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('course',
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('CName', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('CNum', mysql.VARCHAR(length=15), nullable=True),
    sa.Column('Semester', mysql.VARCHAR(length=15), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('works_for',
    sa.Column('TEmail', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('teaches',
    sa.Column('ProfId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('happens_in',
    sa.Column('HelpID', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('DayTime', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('LocID', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('location',
    sa.Column('LocID', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('Building', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('Room', mysql.VARCHAR(length=10), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('ta_oh',
    sa.Column('TEmail', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('CSID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('DayTime', mysql.VARCHAR(length=300), nullable=True),
    sa.Column('LocID', mysql.VARCHAR(length=100), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('report')
    # ### end Alembic commands ###
