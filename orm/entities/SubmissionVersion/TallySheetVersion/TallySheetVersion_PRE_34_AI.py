from flask import render_template, url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_, or_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference
from util import to_comma_seperated_num, sqlalchemy_num_or_zero, convert_image_to_data_uri
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_34_AI_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_AI_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_AI
    }

    def add_row(self, preferenceNumber, preferenceCount, candidateId, electionId):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference

        TallySheetVersionRow_PRE_34_preference.create(
            tallySheetVersionId=self.tallySheetVersionId,
            electionId=electionId,
            preferenceNumber=preferenceNumber,
            preferenceCount=preferenceCount,
            candidateId=candidateId
        )

    @hybrid_property
    def content(self):

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber,
            TallySheetVersionRow_PRE_34_preference.Model.preferenceCount,
            TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId,
            TallySheetVersionRow_PRE_34_preference.Model.electionId
        ).join(
            TallySheetVersionRow_PRE_34_preference.Model,
            and_(
                TallySheetVersionRow_PRE_34_preference.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId == self.tallySheetVersionId,
            ),
            isouter=True
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
            isouter=True
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId,
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId.in_(self.submission.election.mappedElectionIds),
            ElectionCandidate.Model.qualifiedForPreferences == True
        ).all()

    def html_letter(self):

        stamp = self.stamp
        tallySheetContent = self.content

        content = {
            "election": {
                "electionName": self.submission.election.get_official_name(),
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "date": stamp.createdAt.strftime("%d/%m/%Y"),
            "time": stamp.createdAt.strftime("%H:%M:%S %p"),
            "data": [
            ],
            "validVoteCounts": [0, 0],
            "rejectedVoteCounts": [0, 0],
            "totalVoteCounts": [0, 0],
            "registeredVoters": [
                to_comma_seperated_num(self.submission.area.registeredVotersCount),
                100
            ],
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": self.submission.area.areaName
        }

        temp_data = {}
        for candidateIndex in range(len(tallySheetContent)):
            candidate = tallySheetContent[candidateIndex]
            temp_data[candidate.candidateId] = {
                "number": len(temp_data) + 1,
                "name": candidate.candidateName,
                "firstPreferenceCount": "",
                "secondPreferenceCount": "",
                "thirdPreferenceCount": "",
                "total": 0
            }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.preferenceCount is not None:

                if row.preferenceNumber == 1:
                    preference = "firstPreferenceCount"
                elif row.preferenceNumber == 2:
                    preference = "secondPreferenceCount"
                elif row.preferenceNumber == 3:
                    preference = "thirdPreferenceCount"
                else:
                    preference = ""

                temp_data[row.candidateId]['name'] = row.candidateName
                temp_data[row.candidateId][preference] = row.preferenceCount
                temp_data[row.candidateId]["total"] = temp_data[row.candidateId]["total"] + row.preferenceCount

        for i in temp_data:
            content['data'].append(temp_data[i])

        content["logo"] = convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png")

        html = render_template(
            'PRE-34-AI-LETTER.html',
            content=content
        )

        return html

    def html(self):
        stamp = self.stamp
        tallySheetContent = self.content

        content = {
            "tallySheetCode": "PRE-34-AI",
            "election": {
                "electionName": self.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "data": []
        }

        temp_data = {}
        for candidateIndex in range(len(tallySheetContent)):
            candidate = tallySheetContent[candidateIndex]
            temp_data[candidate.candidateId] = {
                "number": len(temp_data) + 1,
                "name": candidate.candidateName,
                "firstPreferenceCount": "",
                "secondPreferenceCount": "",
                "thirdPreferenceCount": "",
                "total": 0
            }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.preferenceCount is not None:

                if row.preferenceNumber == 1:
                    preference = "firstPreferenceCount"
                elif row.preferenceNumber == 2:
                    preference = "secondPreferenceCount"
                elif row.preferenceNumber == 3:
                    preference = "thirdPreferenceCount"
                else:
                    preference = ""

                temp_data[row.candidateId]['name'] = row.candidateName
                temp_data[row.candidateId][preference] = row.preferenceCount
                temp_data[row.candidateId]["total"] = temp_data[row.candidateId]["total"] + row.preferenceCount

        for i in temp_data:
            content['data'].append(temp_data[i])

        html = render_template(
            'PRE-34-AI.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_34_AI_Model
