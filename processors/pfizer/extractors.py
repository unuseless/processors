# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'pfizer',
        'name': 'Pfizer',
        'type': 'register',
        'source_url': 'http://www.pfizer.com/research/clinical_trials',
        'terms_and_conditions_url': 'http://www.pfizer.com/general/terms',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_identifiers({
        'nct': record['nct_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['title'],
        record['nct_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Available': ['ongoing', 'unknown'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'No longer available': ['other', 'other'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Unknown': ['unknown', 'unknown'],
        'Withdrawn': ['withdrawn', 'other'],
    }
    status, recruitment_status = statuses[record.get('status')]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = None

    # Get age_range
    age_range = _extract_age_range(record)

    return {
        'identifiers': identifiers,
        'public_title': public_title,
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'],
        'gender': gender,
        'age_range': age_range,
        'has_published_results': has_published_results,
    }


def extract_conditions(record):
    conditions = []
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    return organisations


def extract_persons(record):
    persons = []
    return persons


def _extract_age_range(record):
    age = (record.get('age_range') or '').strip().lower()
    min_age, max_age = None, None
    if age.endswith(' and older'):
        min_age = age[:-len(' and older')]
        max_age = 'no limit'
    elif len(re.split('\s*-\s*', age)) == 2:
        min_age, max_age = re.split('\s*-\s*', age)

    return {
        'min_age': base.helpers.format_age(min_age),
        'max_age': base.helpers.format_age(max_age),
    }
