# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_document(conn, document):
    """Write document to database.

    Args:
        conn (dict): connection dict
        document (dict): normalized document data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    obj = None

    # Get slug/read object
    if document.get('id'):
        obj = conn['database']['documents'].find_one(id=document['id'])
    else:
        # (trial_id, url, file_id, fda_approval_id) must be unique
        obj = conn['database']['documents'].find_one(
            trial_id=document.get('trial_id'),
            url=document.get('url'),
            file_id=document.get('file_id'),
            fda_approval_id=document.get('fda_approval_id')
        )

    # Create object
    if not obj:
        obj = {
            'id': document.get('id', uuid.uuid1().hex),
        }
        create = True

    # Update object
    obj.update({
        'source_id': document.get('source_id'),
        'name': document['name'],
        'type': document['type'],
        'trial_id': document.get('trial_id'),
        'fda_approval_id': document.get('fda_approval_id'),
        'file_id': document.get('file_id'),
        'url': document.get('url'),
    })

    # Validate object
    if not helpers.validate_remote_url(obj['url']):
        logger.warning(
            'Document %s wasn\'t %s because its "%s" field is invalid: %s',
            obj['name'][0:50],
            'created' if create else 'updated',
            'url',
            obj['url']
        )
        return None

    # Write object
    conn['database']['documents'].upsert(obj, ['id'], ensure=False)

    # Log debug
    logger.debug(
        'Document - %s: %s',
        'created' if create else 'updated',
        document['name'][0:50]
    )

    return obj['id']
