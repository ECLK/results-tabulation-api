from sqlalchemy import bindparam
from sqlalchemy.orm import aliased

from app import db
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META as SOURCE_META, \
    TALLY_SHEET_COLUMN_SOURCE_CONTENT as SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_QUERY as SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.CANDIDATE_TYPE import CANDIDATE_TYPE_NORMAL, \
    CANDIDATE_TYPE_NATIONAL_LIST
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201 import \
    ExtendedTallySheet_CE_201
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201_PV import \
    ExtendedTallySheet_CE_201_PV
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_42 import \
    ExtendedTallySheet_PCE_42
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_31 import \
    ExtendedTallySheet_PCE_31
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_35 import \
    ExtendedTallySheet_PCE_35
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_34 import \
    ExtendedTallySheet_PCE_34
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_CO_PR_4 import \
    ExtendedTallySheet_PCE_CE_CO_PR_4
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_1 import \
    ExtendedTallySheet_PCE_CE_RO_PR_1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_2 import \
    ExtendedTallySheet_PCE_CE_RO_PR_2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_3 import \
    ExtendedTallySheet_PCE_CE_RO_PR_3
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V1 import \
    ExtendedTallySheet_PCE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V2 import \
    ExtendedTallySheet_PCE_CE_RO_V2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_R2 import \
    ExtendedTallySheet_PCE_R2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.META_DATA_KEY import \
    META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED, META_DATA_KEY_ELECTION_NUMBER_OF_BONUS_SEATS_ALLOCATED, \
    META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TALLY_SHEET_CODES import CE_201, CE_201_PV, \
    PCE_31, PCE_34, PCE_35, PCE_42, PCE_CE_CO_PR_1, PCE_CE_CO_PR_2, PCE_CE_CO_PR_3, PCE_CE_CO_PR_4, PCE_CE_RO_PR_1, \
    PCE_CE_RO_PR_2, PCE_CE_RO_PR_3, PCE_CE_RO_V1, PCE_CE_RO_V2, PCE_R1, PCE_R1_PV, PCE_R2, PROVINCIAL_RESULT_CANDIDATES, \
    PROVINCIAL_RESULT_PARTY_WISE, PROVINCIAL_RESULT_PARTY_WISE_POSTAL, PROVINCIAL_RESULT_PARTY_WISE_WITH_SEATS
from constants.VOTE_TYPES import NonPostal, PostalAndNonPostal
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, \
    TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE, \
    TEMPLATE_ROW_TYPE_NATIONAL_LIST_SEATS_ALLOCATED
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, WORKFLOW_ACTION_TYPE_EDIT, \
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_PRINT, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_PRINT_LETTER, \
    WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY, WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, \
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, WORKFLOW_STATUS_TYPE_SUBMITTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, \
    WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED, WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED
from ext.ExtendedElection.util import get_rows_from_csv
from orm.entities import Candidate, Template, Party, Meta, Workflow, TallySheet
from orm.entities.Area import AreaMap
from orm.entities.Area.Electorate import Country, Province, AdministrativeDistrict, PollingDivision, PollingDistrict
from orm.entities.Area.Office import PollingStation, CountingCentre, DistrictCentre, ElectionCommission
from orm.enums import AreaTypeEnum

role_based_access_config = RoleBasedAccess.role_based_access_config


class ExtendedElectionProvincialCouncilElection2021(ExtendedElection):
    def __init__(self, election):
        super(ExtendedElectionProvincialCouncilElection2021, self).__init__(
            election=election,
            role_based_access_config=role_based_access_config
        )

    def get_area_map_query(self):
        from orm.entities import Election, Area
        from orm.entities.Area import AreaAreaModel
        from orm.enums import AreaTypeEnum

        country = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.Country).subquery()
        administrative_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.AdministrativeDistrict).subquery()
        polling_division = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingDivision).subquery()
        polling_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingDistrict).subquery()
        polling_station = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingStation).subquery()
        counting_centre = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.CountingCentre).subquery()
        district_centre = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.DistrictCentre).subquery()
        election_commission = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.ElectionCommission).subquery()

        country__administrative_district = aliased(AreaAreaModel)
        administrative_district__polling_division = aliased(AreaAreaModel)
        polling_division__polling_district = aliased(AreaAreaModel)
        polling_district__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        district_centre__counting_centre = aliased(AreaAreaModel)
        election_commission__district_centre = aliased(AreaAreaModel)

        # For postal vote counting centres.
        administrative_district__counting_centre = aliased(AreaAreaModel)

        query_args = [
            country.c.areaId.label("countryId"),
            country.c.areaName.label("countryName"),
            administrative_district.c.areaId.label("administrativeDistrictId"),
            administrative_district.c.areaName.label("administrativeDistrictName"),
            counting_centre.c.areaId.label("countingCentreId"),
            counting_centre.c.areaName.label("countingCentreName"),
            Election.Model.voteType,
            Election.Model.electionId
        ]

        query_filter = [
            country__administrative_district.parentAreaId == country.c.areaId,
            country__administrative_district.childAreaId == administrative_district.c.areaId,

            district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
            district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

            election_commission__district_centre.parentAreaId == election_commission.c.areaId,
            election_commission__district_centre.childAreaId == district_centre.c.areaId,

            Election.Model.electionId == counting_centre.c.electionId
        ]

        if self.election.voteType != NonPostal:
            query_args += [
                bindparam("pollingDivisionId", None),
                bindparam("pollingDivisionName", None),
                bindparam("pollingDistrictId", None),
                bindparam("pollingDistrictName", None),
                bindparam("pollingStationId", None),
                bindparam("pollingStationName", None)
            ]
            query_filter += [
                administrative_district__counting_centre.parentAreaId == administrative_district.c.areaId,
                administrative_district__counting_centre.childAreaId == counting_centre.c.areaId
            ]
        else:
            query_args += [
                polling_division.c.areaId.label("pollingDivisionId"),
                polling_division.c.areaName.label("pollingDivisionName"),
                polling_district.c.areaId.label("pollingDistrictId"),
                polling_district.c.areaName.label("pollingDistrictName"),
                polling_station.c.areaId.label("pollingStationId"),
                polling_station.c.areaName.label("pollingStationName")
            ]
            query_filter += [
                administrative_district__polling_division.parentAreaId == administrative_district.c.areaId,
                administrative_district__polling_division.childAreaId == polling_division.c.areaId,

                polling_division__polling_district.parentAreaId == polling_division.c.areaId,
                polling_division__polling_district.childAreaId == polling_district.c.areaId,

                polling_district__polling_station.parentAreaId == polling_district.c.areaId,
                polling_district__polling_station.childAreaId == polling_station.c.areaId,

                counting_centre__polling_station.parentAreaId == counting_centre.c.areaId,
                counting_centre__polling_station.childAreaId == polling_station.c.areaId
            ]

        query = db.session.query(*query_args).filter(*query_filter)

        return query

    def get_extended_tally_sheet_class(self, templateName):
        EXTENDED_TEMPLATE_MAP = {
            CE_201: ExtendedTallySheet_CE_201,
            CE_201_PV: ExtendedTallySheet_CE_201_PV,
            PCE_31: ExtendedTallySheet_PCE_31,
            PCE_34: ExtendedTallySheet_PCE_34,
            PCE_35: ExtendedTallySheet_PCE_35,
            PCE_42: ExtendedTallySheet_PCE_42,
            PCE_CE_CO_PR_4: ExtendedTallySheet_PCE_CE_CO_PR_4,
            PCE_CE_RO_PR_1:ExtendedTallySheet_PCE_CE_RO_PR_1,
            PCE_CE_RO_PR_2: ExtendedTallySheet_PCE_CE_RO_PR_2,
            PCE_CE_RO_PR_3: ExtendedTallySheet_PCE_CE_RO_PR_3,
            PCE_CE_RO_V1: ExtendedTallySheet_PCE_CE_RO_V1,
            PCE_CE_RO_V2: ExtendedTallySheet_PCE_CE_RO_V2,
            PCE_R2: ExtendedTallySheet_PCE_R2,
            PROVINCIAL_RESULT_CANDIDATES: "",
            PROVINCIAL_RESULT_PARTY_WISE: "",
            PROVINCIAL_RESULT_PARTY_WISE_POSTAL: "",
            PROVINCIAL_RESULT_PARTY_WISE_WITH_SEATS: "",

        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return super(ExtendedElectionProvincialCouncilElection2021, self).get_extended_tally_sheet_class(
                templateName=templateName
            )

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None, number_of_seats_dataset_file=None):

        root_election = self.election

        workflow_data_entry: Workflow = Workflow.create(
            workflowName="Data Entry",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_SUBMITTED,
                WORKFLOW_STATUS_TYPE_VERIFIED
            ],
            actionsMap={
                WORKFLOW_STATUS_TYPE_EMPTY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_EMPTY},
                    {"name": "Enter", "type": WORKFLOW_ACTION_TYPE_SAVE, "toStatus": WORKFLOW_STATUS_TYPE_SAVED}
                ],
                WORKFLOW_STATUS_TYPE_SAVED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_SAVE, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Submit", "type": WORKFLOW_ACTION_TYPE_SUBMIT, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED}
                ],
                WORKFLOW_STATUS_TYPE_SUBMITTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                ],
                WORKFLOW_STATUS_TYPE_VERIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
                ],
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                ]
            }
        )

        workflow_report: Workflow = Workflow.create(
            workflowName="Report",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_VERIFIED
            ],
            actionsMap={
                WORKFLOW_STATUS_TYPE_EMPTY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_SAVED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_VERIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
                ],
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ]
            }
        )

        workflow_released_report: Workflow = Workflow.create(
            workflowName="Released Report",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_RELEASED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_VERIFIED,
                WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                WORKFLOW_STATUS_TYPE_CERTIFIED,
                WORKFLOW_STATUS_TYPE_RELEASED
            ],
            actionsMap={
                WORKFLOW_STATUS_TYPE_EMPTY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_SAVED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_VERIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print Letter", "type": WORKFLOW_ACTION_TYPE_PRINT_LETTER,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Move to Certify", "type": WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                ],
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Upload Certified Documents", "type": WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Certify", "type": WORKFLOW_ACTION_TYPE_CERTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_CERTIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Notify Release", "type": WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Release", "type": WORKFLOW_ACTION_TYPE_RELEASE,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_RELEASED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED}
                ]
            }
        )

        workflow_edit_allowed_released_report: Workflow = Workflow.create(
            workflowName="Edit Allowed Released Report",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_RELEASED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_SUBMITTED,
                WORKFLOW_STATUS_TYPE_VERIFIED,
                WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                WORKFLOW_STATUS_TYPE_CERTIFIED,
                WORKFLOW_STATUS_TYPE_RELEASED
            ],
            actionsMap={
                WORKFLOW_STATUS_TYPE_EMPTY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_SAVE, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                ],
                WORKFLOW_STATUS_TYPE_SAVED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_SAVE, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Submit", "type": WORKFLOW_ACTION_TYPE_SUBMIT, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                ],
                WORKFLOW_STATUS_TYPE_SUBMITTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                    {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_VERIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Print Letter", "type": WORKFLOW_ACTION_TYPE_PRINT_LETTER,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                    {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Move to Certify", "type": WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                ],
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                    {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                ],
                WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Upload Certified Documents", "type": WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT,
                     "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                    {"name": "Certify", "type": WORKFLOW_ACTION_TYPE_CERTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_CERTIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                    {"name": "Notify Release", "type": WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                    {"name": "Release", "type": WORKFLOW_ACTION_TYPE_RELEASE,
                     "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                ],
                WORKFLOW_STATUS_TYPE_RELEASED: [
                    {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                    {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                     "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED}
                ]
            }
        )

        if not party_candidate_dataset_file:
            party_candidate_dataset_file = root_election.partyCandidateDataset.fileContent

        if not polling_station_dataset_file:
            polling_station_dataset_file = root_election.pollingStationsDataset.fileContent

        if not postal_counting_centers_dataset_file:
            postal_counting_centers_dataset_file = root_election.postalCountingCentresDataset.fileContent

        if not number_of_seats_dataset_file:
            number_of_seats_dataset_file = root_election.numberOfSeatsDataset.fileContent

        if not invalid_vote_categories_dataset_file:
            invalid_vote_categories_dataset_file = root_election.invalidVoteCategoriesDataset.fileContent

        tally_sheet_template_ce_201 = Template.create(
            templateName=CE_201,
            templateRowTypesMap={
                "BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_BALLOTS_RECEIVED": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_BALLOTS_SPOILT": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_BALLOTS_ISSUED": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_BALLOTS_UNUSED": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_PAPER_ACCOUNT": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
            }
        )

        tally_sheet_template_ce_201_pv = Template.create(
            templateName=CE_201_PV,
            templateRowTypesMap={
                "SITUATION": {
                    "hasMany": False,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "TIME_OF_COMMENCEMENT": {
                    "hasMany": False,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "ballotBoxId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A": {
                    "hasMany": False,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B": {
                    "hasMany": False,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

        tally_sheet_template_pce_35 = Template.create(
            templateName=PCE_35,
            templateRowTypesMap={
                "PARTY_WISE_VOTE": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "strValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                "REJECTED_VOTE": {
                    "hasMany": False,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

        tally_sheet_template_pce_ce_ro_v1 = Template.create(
            templateName=PCE_CE_RO_V1,
            templateRowTypesMap={
                "PARTY_WISE_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_35, "templateRowType": "PARTY_WISE_VOTE"}
                    ]
                },
                "REJECTED_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_35, "templateRowType": "REJECTED_VOTE"}
                    ]
                }
            }
        )

        # tally_sheet_template_polling_division_results = Template.create(
        #     templateName=POLLING_DIVISION_RESULTS,
        #     templateRowTypesMap={
        #         "PARTY_WISE_VOTE": {
        #             "hasMany": True,
        #             "isDerived": True,
        #             "columns": [
        #                 {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
        #             ],
        #             "derivativeRows": [
        #                 {"templateName": PCE_CE_RO_V1, "templateRowType": "PARTY_WISE_VOTE"}
        #             ]
        #         },
        #         "REJECTED_VOTE": {
        #             "hasMany": True,
        #             "isDerived": True,
        #             "columns": [
        #                 {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
        #             ],
        #             "derivativeRows": [
        #                 {"templateName": PCE_CE_RO_V1, "templateRowType": "REJECTED_VOTE"}
        #             ]
        #         }
        #     }
        # )

        tally_sheet_template_pce_ce_ro_v2 = Template.create(
            templateName=PCE_CE_RO_V2,
            templateRowTypesMap={
                "PARTY_WISE_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_V1, "templateRowType": "PARTY_WISE_VOTE"}
                    ]
                },
                "REJECTED_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_V1, "templateRowType": "REJECTED_VOTE"}
                    ]
                }
            }
        )

        tally_sheet_template_pce_r2 = Template.create(
            templateName=PCE_R2,
            templateRowTypesMap={
                "PARTY_WISE_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_V2, "templateRowType": "PARTY_WISE_VOTE"}
                    ]
                },
                "REJECTED_VOTE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_V2, "templateRowType": "REJECTED_VOTE"}
                    ]
                },
                TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

        tally_sheet_template_pce_co_pr_4 = Template.create(
            templateName=PCE_CE_CO_PR_4,
            templateRowTypesMap={
                "CANDIDATE_FIRST_PREFERENCE": {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": False, "func": None, "source": SOURCE_META},
                        {"columnName": "candidateId", "grouped": False, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "numValue", "grouped": False, "func": None, "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

        tally_sheet_template_pce_ce_ro_pr_1 = Template.create(
            templateName=PCE_CE_RO_PR_1,
            templateRowTypesMap={
                "CANDIDATE_FIRST_PREFERENCE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_CO_PR_4, "templateRowType": "CANDIDATE_FIRST_PREFERENCE"}
                    ]
                }
            }
        )

        tally_sheet_template_pce_ce_ro_pr_2 = Template.create(
            templateName=PCE_CE_RO_PR_2,
            templateRowTypesMap={
                "CANDIDATE_FIRST_PREFERENCE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_PR_1, "templateRowType": "CANDIDATE_FIRST_PREFERENCE"}
                    ]
                }
            }
        )

        tally_sheet_template_pce_ce_ro_pr_3 = Template.create(
            templateName=PCE_CE_RO_PR_3,
            templateRowTypesMap={
                "CANDIDATE_FIRST_PREFERENCE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_PR_2, "templateRowType": "CANDIDATE_FIRST_PREFERENCE"}
                    ]
                }
            }
        )

        # tally_sheet_template_pce_ai_sa = Template.create(
        #     templateName=PCE_AI_SA,
        #     templateRowTypesMap={
        #         "PARTY_WISE_VOTE": {
        #             "hasMany": True,
        #             "isDerived": True,
        #             "columns": [
        #                 {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
        #             ],
        #             "derivativeRows": [
        #                 {"templateName": PCE_AI_ED, "templateRowType": "PARTY_WISE_VOTE"}
        #             ]
        #         },
        #         "REJECTED_VOTE": {
        #             "hasMany": True,
        #             "isDerived": True,
        #             "columns": [
        #                 {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
        #             ],
        #             "derivativeRows": [
        #                 {"templateName": PCE_AI_ED, "templateRowType": "REJECTED_VOTE"}
        #             ]
        #         },
        #         TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
        #             "hasMany": True,
        #             "isDerived": True,
        #             "columns": [
        #                 {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
        #                 {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
        #                 {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
        #                 {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
        #             ],
        #             "derivativeRows": [
        #                 {"templateName": PCE_R2, "templateRowType": TEMPLATE_ROW_TYPE_SEATS_ALLOCATED}
        #             ]
        #         }
        #     }
        # )

        tally_sheet_template_pce_ce_ro_pr_3 = Template.create(
            templateName=PCE_CE_RO_PR_3,
            templateRowTypesMap={
                "CANDIDATE_FIRST_PREFERENCE": {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_CE_RO_PR_2, "templateRowType": "CANDIDATE_FIRST_PREFERENCE"}
                    ]
                },
                TEMPLATE_ROW_TYPE_SEATS_ALLOCATED: {
                    "hasMany": True,
                    "isDerived": True,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_QUERY},
                        {"columnName": "numValue", "grouped": False, "func": "sum", "source": SOURCE_QUERY}
                    ],
                    "derivativeRows": [
                        {"templateName": PCE_R2, "templateRowType": TEMPLATE_ROW_TYPE_SEATS_ALLOCATED}
                    ]
                },
                TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_CONTENT}
                    ]
                },
                TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE: {
                    "hasMany": True,
                    "isDerived": False,
                    "columns": [
                        {"columnName": "electionId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "areaId", "grouped": True, "func": None, "source": SOURCE_META},
                        {"columnName": "partyId", "grouped": True, "func": None, "source": SOURCE_CONTENT},
                        {"columnName": "candidateId", "grouped": True, "func": None, "source": SOURCE_CONTENT}
                    ]
                }
            }
        )

        data_entry_store = {
            AreaTypeEnum.Country: {},
            AreaTypeEnum.Province: {},
            AreaTypeEnum.AdministrativeDistrict: {},
            AreaTypeEnum.PollingDivision: {},
            AreaTypeEnum.PollingDistrict: {},
            AreaTypeEnum.PollingStation: {},
            AreaTypeEnum.CountingCentre: {},
            AreaTypeEnum.DistrictCentre: {},
            AreaTypeEnum.ElectionCommission: {},
        }

        province_election_store = {}
        administrative_district_election_store = {}
        administrative_district_sub_election_store = {}
        party_store = {}

        def _get_candidate(row):
            candidate_type = row["Candidate Type"]

            party = _get_party(row)

            candidate = Candidate.create(
                candidateName=row["Candidate Name"], candidateNumber=row["Candidate Number"],
                candidateType=candidate_type)

            root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

            if candidate_type == CANDIDATE_TYPE_NORMAL:
                administrative_district_election = _get_administrative_district_election(row)
                administrative_district_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)
                for administrative_district_sub_election in administrative_district_election.subElections:
                    administrative_district_sub_election.add_candidate(candidateId=candidate.candidateId,
                                                                       partyId=party.partyId)

            return candidate

        def _get_party(row):
            candidate_type = row["Candidate Type"]

            party_name = row["Party Name (Unique)"]
            party_name_unique = row["Party Name (Unique)"]
            party_symbol = row["Party Symbol (Text)"]
            party_abbreviation = row["Party Abbreviation"]

            if party_name_unique not in party_store:
                party = Party.create(
                    partyName=party_name,
                    partySymbol=party_symbol,
                    partyAbbreviation=party_abbreviation
                )

                party_store[party_name_unique] = party

            party = party_store[party_name_unique]

            root_election.add_party(partyId=party.partyId)

            if candidate_type == CANDIDATE_TYPE_NORMAL:
                administrative_district_election = _get_administrative_district_election(row)
                administrative_district_election.add_party(partyId=party.partyId)
                for administrative_district_sub_election in administrative_district_election.subElections:
                    administrative_district_sub_election.add_party(partyId=party.partyId)

            return party_store[party_name_unique]

        def _get_administrative_district_sub_election_map(row):
            administrative_district_name = row["Administrative District"]

            return administrative_district_sub_election_store[administrative_district_name]

        def _get_administrative_district_sub_election(row, vote_type):
            administrative_district_name = row["Administrative District"]
            administrative_district_election = _get_administrative_district_election(row)
            election_map = _get_administrative_district_sub_election_map(row)

            if vote_type not in election_map:
                sub_election = administrative_district_election.add_sub_election(
                    electionName="%s - %s - %s" % (root_election.electionName, administrative_district_name, vote_type),
                    voteType=vote_type, isListed=False
                )
                election_map[vote_type] = sub_election
                for party in administrative_district_election.parties:
                    sub_election.add_party(partyId=party.partyId)
                    for candidate in party.candidates:
                        sub_election.add_candidate(partyId=party.partyId, candidateId=candidate.candidateId)

                if vote_type is not NonPostal:
                    _get_sub_administrative_district_entry(row, vote_type=vote_type)
            else:
                sub_election = election_map[vote_type]

            return sub_election

        def _get_province_election(row):
            province_name = row["Province"]

            if province_name not in province_election_store:
                election = root_election.add_sub_election(
                    electionName="%s - %s" % (root_election.electionName, province_name),
                    voteType=PostalAndNonPostal, isListed=True
                )
                province_election_store[province_name] = election
            else:
                election = province_election_store[province_name]

            return election

        def _get_administrative_district_election(row):
            administrative_district_name = row["Administrative District"]
            province_election = _get_province_election(row)

            if administrative_district_name not in administrative_district_election_store:
                election = province_election.add_sub_election(
                    electionName="%s - %s" % (root_election.electionName, administrative_district_name),
                    voteType=PostalAndNonPostal, isListed=True
                )
                administrative_district_election_store[administrative_district_name] = election
                administrative_district_sub_election_store[administrative_district_name] = {}
            else:
                election = administrative_district_election_store[administrative_district_name]

            return election

        def _get_area_entry(election, area_class, area_name, area_key, create_tally_sheets_callback=None):

            area_type = area_class.Model.__mapper_args__["polymorphic_identity"]

            if area_key in data_entry_store[area_type]:
                area = data_entry_store[area_type][area_key]
            else:
                area = area_class.create(area_name, electionId=election.electionId)

                data_entry_store[area_type][area_key] = area

                if create_tally_sheets_callback is not None:
                    tally_sheet_mappings = create_tally_sheets_callback(area)

                    for tally_sheet_mapping_key in tally_sheet_mappings.keys():
                        tally_sheet_mapping_value = tally_sheet_mappings[tally_sheet_mapping_key]
                        setattr(area, tally_sheet_mapping_key, tally_sheet_mapping_value)

            return area

        def _get_country_entry(row):
            area_class = Country
            area_name = row["Country"]
            area_key = area_name

            def _create_country_tally_sheets(area):
                pce_ai_2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_2, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]
                pce_ai_1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_1, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]
                pce_ai_nl_2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_nl_2, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_2_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]
                pce_ai_nl_1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_nl_1, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_nl_2_tally_sheet_list, *pce_ai_1_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]
                pce_ai_sa_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_sa, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_1_tally_sheet_list],
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]
                pce_ai_ed_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ai_ed, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_sa_tally_sheet_list, *pce_ai_nl_1_tally_sheet_list,
                                       *pce_ai_1_tally_sheet_list],
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                return {
                    "pce_ai_ed_tally_sheet_list": pce_ai_ed_tally_sheet_list,
                    "pce_ai_sa_tally_sheet_list": pce_ai_sa_tally_sheet_list,
                    "pce_ai_nl_1_tally_sheet_list": pce_ai_nl_1_tally_sheet_list,
                    "pce_ai_nl_2_tally_sheet_list": pce_ai_nl_2_tally_sheet_list,
                    "pce_ai_1_tally_sheet_list": pce_ai_1_tally_sheet_list,
                    "pce_ai_2_tally_sheet_list": pce_ai_2_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             _create_country_tally_sheets)

            return data_entry_obj

        def _get_province_entry(row):
            area_class = Province
            area_name = row["Province"]
            area_key = area_name

            def _create_province_tally_sheets(area):
                return None

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             None)

            return data_entry_obj

        def _get_sub_administrative_district_entry(row, vote_type=None):
            administrative_district = _get_administrative_district_entry(row)
            administrative_district_sub_election = _get_administrative_district_sub_election(row, vote_type=vote_type)

            polling_division_results_tally_sheet = TallySheet.create(
                template=tally_sheet_template_polling_division_results,
                electionId=administrative_district_sub_election.electionId,
                areaId=administrative_district.areaId,
                metaId=Meta.create({
                    "areaId": administrative_district.areaId,
                    "electionId": administrative_district_sub_election.electionId
                }).metaId,
                workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
            )
            administrative_district.polling_division_results_tally_sheet_list.append(
                polling_division_results_tally_sheet)
            pce_ce_ro_v1_tally_sheet = TallySheet.create(
                template=tally_sheet_template_pce_ce_ro_v1, electionId=administrative_district_sub_election.electionId,
                areaId=administrative_district.areaId,
                metaId=Meta.create({
                    "areaId": administrative_district.areaId,
                    "electionId": administrative_district_sub_election.electionId
                }).metaId,
                parentTallySheets=[polling_division_results_tally_sheet,
                                   *administrative_district.pce_ce_ro_v2_tally_sheet_list],
                workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
            )
            administrative_district.pce_ce_ro_v1_tally_sheet_list.append(pce_ce_ro_v1_tally_sheet)
            administrative_district.pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map[vote_type] = [
                pce_ce_ro_v1_tally_sheet]

            for party in administrative_district_sub_election.parties:
                pce_ce_ro_pr_1_tally_sheet = TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_pr_1,
                    electionId=administrative_district_sub_election.electionId,
                    areaId=administrative_district.areaId,
                    metaId=Meta.create({
                        "areaId": administrative_district.areaId,
                        "partyId": party.partyId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    parentTallySheets=[
                        *administrative_district.pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId]],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )
                administrative_district.pce_ce_ro_pr_1_tally_sheet_list.append(pce_ce_ro_pr_1_tally_sheet)

                party_id_and_vote_typce_key = "%s%s" % (party.partyId, vote_type)
                if party_id_and_vote_typce_key not in administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map:
                    administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[
                        party_id_and_vote_typce_key] = [pce_ce_ro_pr_1_tally_sheet]
                else:
                    administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[
                        party_id_and_vote_typce_key].append(pce_ce_ro_pr_1_tally_sheet)

        def _get_administrative_district_entry(row):
            administrative_district_election = _get_administrative_district_election(row)

            country = _get_country_entry(row)

            area_class = AdministrativeDistrict
            area_name = row["Administrative District"]
            area_key = area_name

            def _create_administrative_district_tally_sheets(area):
                pce_ai_ed_tally_sheet_list = country.pce_ai_ed_tally_sheet_list
                pce_ai_sa_tally_sheet_list = country.pce_ai_sa_tally_sheet_list
                pce_ai_1_tally_sheet_list = country.pce_ai_1_tally_sheet_list
                pce_ai_2_tally_sheet_list = country.pce_ai_2_tally_sheet_list

                pce_21_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_21, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_2_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]

                pce_r2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_r2, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_21_tally_sheet_list, *pce_ai_sa_tally_sheet_list, *pce_ai_1_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_v2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_v2, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_r2_tally_sheet_list, *pce_ai_ed_tally_sheet_list],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                polling_division_results_tally_sheet_list = []
                pce_ce_ro_v1_tally_sheet_list = []
                pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map = {}

                pce_ce_ro_pr_1_tally_sheet_list = []
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map = {}
                pce_ce_ro_pr_2_tally_sheet_list = []
                pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map = {}
                pce_ce_ro_pr_3_tally_sheet_list = []
                pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_election.parties:
                    pce_ce_ro_pr_3_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_3,
                        electionId=administrative_district_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_election.electionId
                        }).metaId,
                        parentTallySheets=pce_21_tally_sheet_list,
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_3_tally_sheet_list.append(pce_ce_ro_pr_3_tally_sheet)
                    if party.partyId not in pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map:
                        pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_ro_pr_3_tally_sheet]
                    else:
                        pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_ro_pr_3_tally_sheet)

                    pce_ce_ro_pr_2_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_2,
                        electionId=administrative_district_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId]],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_2_tally_sheet_list.append(pce_ce_ro_pr_2_tally_sheet)
                    if party.partyId not in pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map:
                        pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_ro_pr_2_tally_sheet]
                    else:
                        pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_ro_pr_2_tally_sheet)

                return {
                    "pce_ce_ro_v1_tally_sheet_list": pce_ce_ro_v1_tally_sheet_list,
                    "pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map": pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                    "pce_r2_tally_sheet_list": pce_r2_tally_sheet_list,
                    "pce_ce_ro_v2_tally_sheet_list": pce_ce_ro_v2_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list": pce_ce_ro_pr_1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map": pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map,
                    "pce_ce_ro_pr_2_tally_sheet_list": pce_ce_ro_pr_2_tally_sheet_list,
                    "pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map": pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map,
                    "pce_ce_ro_pr_3_tally_sheet_list": pce_ce_ro_pr_3_tally_sheet_list,
                    "pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map": pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map
                }

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key,
                                             _create_administrative_district_tally_sheets)

            return data_entry_obj

        def _get_polling_division_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)

            area_class = PollingDivision
            area_name = row["Polling Division"]
            area_key = area_name

            def _create_polling_division_tally_sheets(area):
                pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map = administrative_district.pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map
                pce_ce_ro_v2_tally_sheet_list = administrative_district.pce_ce_ro_v2_tally_sheet_list

                polling_division_results_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_polling_division_results,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_v1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_v1,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=[*polling_division_results_tally_sheet_list, *pce_ce_ro_v2_tally_sheet_list],
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_pr_1_tally_sheet_list = []
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map = {}
                for party in administrative_district_ordinary_election.parties:
                    pce_ce_ro_pr_1_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_1,
                        electionId=administrative_district_ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId]],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_1_tally_sheet_list.append(pce_ce_ro_pr_1_tally_sheet)

                    party_id_and_vote_typce_key = "%s%s" % (party.partyId, NonPostal)
                    if party_id_and_vote_typce_key not in pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map:
                        pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[party_id_and_vote_typce_key] = [
                            pce_ce_ro_pr_1_tally_sheet]
                    else:
                        pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[
                            party_id_and_vote_typce_key].append(pce_ce_ro_pr_1_tally_sheet)

                return {
                    "pce_ce_ro_v1_tally_sheet_list": pce_ce_ro_v1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list": pce_ce_ro_pr_1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map": pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                }

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key,
                                             _create_polling_division_tally_sheets)

            return data_entry_obj

        def _get_polling_district_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = PollingDistrict
            area_name = row["Polling District"]
            area_key = "%s-%s-%s" % (administrative_district.areaName, polling_division.areaName, area_name)

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_polling_station_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)
            polling_district = _get_polling_district_entry(row)

            area_class = PollingStation
            area_name = row["Polling Station"]
            area_key = "%s-%s-%s-%s" % (
                administrative_district.areaName, polling_division.areaName, polling_district.areaName, area_name
            )

            area = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key)

            area._registeredVotersCount = row["Registered Normal Voters"]
            area._registeredPostalVotersCount = row["Registered Postal Voters"]
            area._registeredQuarantineVotersCount = row["Registered Quarantine Voters"]
            area._registeredDisplacedVotersCount = row["Registered Displaced Voters"]

            return area

        def _get_counting_centre_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = CountingCentre
            area_name = row["Counting Centre"]
            area_key = "%s-%s" % (administrative_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pce_ce_ro_v1_tally_sheet_list = polling_division.pce_ce_ro_v1_tally_sheet_list
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map = polling_division.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map

                pce_27_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_35,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=pce_ce_ro_v1_tally_sheet_list,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                # pce_39_tally_sheet_list = [TallySheet.create(
                #     template=tally_sheet_template_pce_39, electionId=administrative_district_ordinary_election.electionId,
                #     areaId=area.areaId,
                #     metaId=Meta.create({
                #         "areaId": area.areaId,
                #         "electionId": administrative_district_ordinary_election.electionId
                #     }).metaId,
                #     workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                # )]
                # pce_22_tally_sheet_list = [TallySheet.create(
                #     template=tally_sheet_template_pce_22, electionId=administrative_district_ordinary_election.electionId,
                #     areaId=area.areaId,
                #     metaId=Meta.create({
                #         "areaId": area.areaId,
                #         "electionId": administrative_district_ordinary_election.electionId
                #     }).metaId,
                #     workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                # )]

                pce_4_tally_sheet_list = []
                pce_4_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_ordinary_election.parties:
                    pce_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_4,
                        electionId=administrative_district_ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[
                            "%s%s" % (party.partyId, NonPostal)]],
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pce_4_tally_sheet_list.append(pce_4_tally_sheet)

                    if party.partyId not in pce_4_tally_sheet_list_party_id_wise_map:
                        pce_4_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_4_tally_sheet]
                    else:
                        pce_4_tally_sheet_list_party_id_wise_map[party.partyId].append(pce_4_tally_sheet)

                pce_ce_201_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pce_27_tally_sheet_list": pce_27_tally_sheet_list,
                    # "pce_39_tally_sheet_list": pce_39_tally_sheet_list,
                    # "pce_22_tally_sheet_list": pce_22_tally_sheet_list,
                    "pce_4_tally_sheet_list": pce_4_tally_sheet_list,
                    "pce_4_tally_sheet_list_party_id_wise_map": pce_4_tally_sheet_list_party_id_wise_map,
                    "pce_ce_201_tally_sheet_list": pce_ce_201_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_administrative_district_counting_centre_entry(row):
            area_class = CountingCentre
            area_name = row["Counting Centre"]
            vote_type = row["Vote Type"]

            administrative_district_sub_election = _get_administrative_district_sub_election(row, vote_type=vote_type)
            administrative_district = _get_administrative_district_entry(row=row)

            area_key = "%s-%s" % (administrative_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map = administrative_district.pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map = administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map

                pce_27_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_35, electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    parentTallySheets=pce_ce_ro_v1_tally_sheet_list_vote_typce_wise_map[vote_type],
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                # pce_39_tally_sheet_list = [TallySheet.create(
                #     template=tally_sheet_template_pce_39, electionId=administrative_district_sub_election.electionId,
                #     areaId=area.areaId,
                #     metaId=Meta.create({
                #         "areaId": area.areaId,
                #         "electionId": administrative_district_sub_election.electionId
                #     }).metaId,
                #     workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                # )]
                #
                # pce_22_tally_sheet_list = [TallySheet.create(
                #     template=tally_sheet_template_pce_22, electionId=administrative_district_sub_election.electionId,
                #     areaId=area.areaId,
                #     metaId=Meta.create({
                #         "areaId": area.areaId,
                #         "electionId": administrative_district_sub_election.electionId
                #     }).metaId,
                #     workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                # )]

                pce_4_tally_sheet_list = []
                pce_4_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_sub_election.parties:
                    pce_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_4, electionId=administrative_district_sub_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_sub_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_typce_wise_map[
                            "%s%s" % (party.partyId, vote_type)]],
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pce_4_tally_sheet_list.append(pce_4_tally_sheet)

                    if party.partyId not in pce_4_tally_sheet_list_party_id_wise_map:
                        pce_4_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_4_tally_sheet]
                    else:
                        pce_4_tally_sheet_list_party_id_wise_map[party.partyId].append(pce_4_tally_sheet)

                pce_ce_201_pv_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201_pv, electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pce_27_tally_sheet_list": pce_27_tally_sheet_list,
                    # "pce_39_tally_sheet_list": pce_39_tally_sheet_list,
                    # "pce_22_tally_sheet_list": pce_22_tally_sheet_list,
                    "pce_4_tally_sheet_list": pce_4_tally_sheet_list,
                    "pce_4_tally_sheet_list_party_id_wise_map": pce_4_tally_sheet_list_party_id_wise_map,
                    "pce_ce_201_pv_tally_sheet_list": pce_ce_201_pv_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(administrative_district_sub_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_district_centre_entry(row):
            administrative_district_election = _get_administrative_district_election(row)

            area_class = DistrictCentre
            area_name = row["District Centre"]
            area_key = area_name

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_election_commission_entry(row):
            administrative_district_election = _get_administrative_district_election(row)

            area_class = ElectionCommission
            area_name = row["Election Commission"]
            area_key = area_name

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key)

            return data_entry_obj

        # def extract_csv_files():
        for row in get_rows_from_csv(party_candidate_dataset_file):
            _get_candidate(row)

        for row in get_rows_from_csv(polling_station_dataset_file):
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"
            row["Polling Station"] = row["Polling Station (English)"]

            country = _get_country_entry(row=row)
            province = _get_province_entry(row=row)
            administrative_district = _get_administrative_district_entry(row=row)
            polling_division = _get_polling_division_entry(row=row)
            polling_district = _get_polling_district_entry(row=row)
            election_commission = _get_election_commission_entry(row=row)
            district_centre = _get_district_centre_entry(row=row)
            counting_centre = _get_counting_centre_entry(row=row)
            polling_station = _get_polling_station_entry(row=row)

            country.add_child(province.areaId)
            province.add_child(administrative_district.areaId)
            administrative_district.add_child(polling_division.areaId)
            polling_division.add_child(polling_district.areaId)
            polling_district.add_child(polling_station.areaId)
            election_commission.add_child(district_centre.areaId)
            district_centre.add_child(counting_centre.areaId)
            counting_centre.add_child(polling_station.areaId)

            # AreaMap.create(
            #     electionId=root_election.electionId,
            #     voteType=NonPostal,
            #     pollingStationId=polling_station.areaId,
            #     countingCentreId=counting_centre.areaId,
            #     districtCentreId=district_centre.areaId,
            #     electionCommissionId=election_commission.areaId,
            #     pollingDistrictId=polling_district.areaId,
            #     pollingDivisionId=polling_division.areaId,
            #     administrativeDistrictId=administrative_district.areaId,
            #     provinceId=province.areaId,
            #     countryId=country.areaId
            # )

        for row in get_rows_from_csv(postal_counting_centers_dataset_file):
            vote_type = row["Vote Type"]
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"

            country = _get_country_entry(row=row)
            province = _get_province_entry(row=row)
            administrative_district = _get_administrative_district_entry(row=row)
            election_commission = _get_election_commission_entry(row=row)
            district_centre = _get_district_centre_entry(row=row)
            postal_vote_counting_centre = _get_administrative_district_counting_centre_entry(row=row)

            country.add_child(province.areaId)
            province.add_child(administrative_district.areaId)
            election_commission.add_child(district_centre.areaId)
            district_centre.add_child(postal_vote_counting_centre.areaId)
            administrative_district.add_child(postal_vote_counting_centre.areaId)

            # AreaMap.create(
            #     electionId=root_election.electionId,
            #     voteType=vote_type,
            #     countingCentreId=postal_vote_counting_centre.areaId,
            #     districtCentreId=district_centre.areaId,
            #     electionCommissionId=election_commission.areaId,
            #     administrativeDistrictId=administrative_district.areaId,
            #     provinceId=province.areaId,
            #     countryId=country.areaId
            # )

        for row in get_rows_from_csv(number_of_seats_dataset_file):
            province_election = _get_province_election(row)
            province_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_BONUS_SEATS_ALLOCATED,
                metaDataValue=row["Bonus seats"]
            )

            administrative_district_election = _get_administrative_district_election(row)
            administrative_district_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED,
                metaDataValue=row["Number of seats"]
            )
            administrative_district_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION,
                metaDataValue=0.05
            )

        # extract_csv_files()

        db.session.commit()

        return root_election
