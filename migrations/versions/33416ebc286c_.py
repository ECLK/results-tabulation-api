"""empty message

Revision ID: 33416ebc286c
Revises: 4908a7e83f30
Create Date: 2019-11-05 22:27:08.863313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33416ebc286c'
down_revision = '4908a7e83f30'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dashboard_status_CE_201',
    sa.Column('recordId', sa.Integer(), nullable=False),
    sa.Column('voteType', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('electionId', sa.Integer(), nullable=True),
    sa.Column('electoralDistrictId', sa.Integer(), nullable=True),
    sa.Column('pollingDivisionId', sa.Integer(), nullable=True),
    sa.Column('countingCentreId', sa.Integer(), nullable=True),
    sa.Column('pollingStationId', sa.Integer(), nullable=True),
    sa.Column('ballotCount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['countingCentreId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
    sa.ForeignKeyConstraint(['electoralDistrictId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['pollingDivisionId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['pollingStationId'], ['area.areaId'], ),
    sa.PrimaryKeyConstraint('recordId')
    )
    op.create_table('dashboard_status_PRE_34',
    sa.Column('recordId', sa.Integer(), nullable=False),
    sa.Column('voteType', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('electionId', sa.Integer(), nullable=True),
    sa.Column('electoralDistrictId', sa.Integer(), nullable=True),
    sa.Column('pollingDivisionId', sa.Integer(), nullable=True),
    sa.Column('countingCentreId', sa.Integer(), nullable=True),
    sa.Column('candidateId', sa.Integer(), nullable=True),
    sa.Column('secondPreferenceCount', sa.Integer(), nullable=False),
    sa.Column('thirdPreferenceCount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'], ),
    sa.ForeignKeyConstraint(['countingCentreId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
    sa.ForeignKeyConstraint(['electoralDistrictId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['pollingDivisionId'], ['area.areaId'], ),
    sa.PrimaryKeyConstraint('recordId')
    )
    op.create_table('dashboard_status_PRE_41',
    sa.Column('recordId', sa.Integer(), nullable=False),
    sa.Column('voteType', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('electionId', sa.Integer(), nullable=True),
    sa.Column('electoralDistrictId', sa.Integer(), nullable=True),
    sa.Column('pollingDivisionId', sa.Integer(), nullable=True),
    sa.Column('countingCentreId', sa.Integer(), nullable=True),
    sa.Column('pollingStationId', sa.Integer(), nullable=True),
    sa.Column('candidateId', sa.Integer(), nullable=True),
    sa.Column('voteCount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'], ),
    sa.ForeignKeyConstraint(['countingCentreId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
    sa.ForeignKeyConstraint(['electoralDistrictId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['pollingDivisionId'], ['area.areaId'], ),
    sa.ForeignKeyConstraint(['pollingStationId'], ['area.areaId'], ),
    sa.PrimaryKeyConstraint('recordId')
    )
    op.alter_column('election_candidate', 'qualifiedForPreferences',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('invoice', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('invoice', 'delete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('invoice_stationaryItem', 'received',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('proof', 'finished',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tallySheetVersion', 'isComplete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('proof', 'finished',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('invoice_stationaryItem', 'received',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('invoice', 'delete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('invoice', 'confirmed',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.alter_column('election_candidate', 'qualifiedForPreferences',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.drop_table('dashboard_status_PRE_41')
    op.drop_table('dashboard_status_PRE_34')
    op.drop_table('dashboard_status_CE_201')
    ### end Alembic commands ###
