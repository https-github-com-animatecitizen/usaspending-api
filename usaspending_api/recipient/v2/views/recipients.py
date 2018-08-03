import logging
import uuid
import time

from rest_framework.response import Response
from django.db.models import F, Sum

from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.common.exceptions import InvalidParameterException
from usaspending_api.common.views import APIDocumentationView

from usaspending_api.awards.v2.filters.view_selector import recipient_totals
from usaspending_api.recipient.models import DUNS, RecipientProfile, RecipientLookup
from usaspending_api.recipient.v2.helpers import validate_year, reshape_filters
from usaspending_api.references.models import RefCountryCode, LegalEntity

logger = logging.getLogger(__name__)

# Recipient Levels
#   - P = Parent Recipient, There is at least one child recipient that lists this recipient as a parent
#   - C = Child Recipient, References a parent recipient
#   - R = Recipient, No parent info provided
RECIPIENT_LEVELS = ['P', 'C', 'R']

# Special Cases - Recipients that cover a group of recipients
SPECIAL_CASES = [
    'MULTIPLE RECIPIENTS',
    'REDACTED DUE TO PII',
    'MULTIPLE FOREIGN RECIPIENTS',
    'PRIVATE INDIVIDUAL',
    'INDIVIDUAL RECIPIENT'
]


def validate_recipient_id(recipient_id):
    """ Validate [duns+name]-[recipient_type] hash

        Args:
            hash: str of the hash+duns to look up

        Returns:
            uuid of hash
            recipient level

        Raises:
            InvalidParameterException for invalid hashes
    """
    if '-' not in recipient_id:
        raise InvalidParameterException('ID (\'{}\') doesn\'t include Recipient-Level'.format(hash))
    recipient_level = recipient_id[recipient_id.rfind('-') + 1:]
    if recipient_level not in RECIPIENT_LEVELS:
        raise InvalidParameterException('Invalid Recipient-Level: \'{}\''.format(recipient_level))
    recipient_hash = recipient_id[:recipient_id.rfind('-')]
    try:
        uuid.UUID(recipient_hash)
    except ValueError:
        raise InvalidParameterException('Recipient Hash not valid UUID: \'{}\'.'.format(recipient_hash))
    return recipient_hash, recipient_level


def extract_name_duns_from_hash(recipient_hash):
    """ Extract the name and duns from the recipient hash

        Args:
            recipient_hash: uuid of the hash+duns to look up

        Returns:
            duns and name
    """
    name_duns_qs = RecipientLookup.objects.filter(recipient_hash=recipient_hash).values('duns', 'legal_business_name')
    if not name_duns_qs:
        return None, None
    else:
        return name_duns_qs[0]['duns'], name_duns_qs[0]['legal_business_name']


def extract_parent_from_hash(recipient_hash):
    """ Extract the parent name and parent duns from the recipient hash

        Args:
            recipient_hash: uuid of the hash+duns to look up

        Returns:
            parent_duns
            parent_name
    """
    duns = None
    name = None
    parent_id = None
    affiliations = RecipientProfile.objects.filter(recipient_hash=recipient_hash, recipient_level='C')\
        .values('recipient_affiliations')
    if not affiliations:
        return duns, name, parent_id
    duns = affiliations[0]['recipient_affiliations'][0]

    parent = RecipientLookup.objects.filter(duns=duns).values('recipient_hash', 'legal_business_name')
    if parent:
        name = parent[0]['legal_business_name']
        parent_id = '{}-P'.format(parent[0]['recipient_hash'])
    return duns, name, parent_id


def extract_location(recipient_hash, extract_country_name=True):
    """ Extract the location data via the recipient hash

        Args:
            recipient_hash: uuid of the hash+duns to look up

        Returns:
            dict of location info
    """
    location = {
        'address_line1': None,
        'address_line2': None,
        'address_line3': None,
        'foreign_province': None,
        'city_name': None,
        'county_name': None,
        'state_code': None,
        'zip': None,
        'zip4': None,
        'foreign_postal_code': None,
        'country_name': None,
        'country_code': None,
        'congressional_code': None
    }
    duns = RecipientLookup.objects.filter(recipient_hash=recipient_hash).values('duns')
    duns_obj = DUNS.objects.filter(awardee_or_recipient_uniqu=duns[0]['duns']) if duns else None
    if duns_obj:
        duns_obj = duns_obj[0]
        if extract_country_name:
            country_name = RefCountryCode.objects.filter(country_code=duns_obj.country_code).values('country_name')
        else:
            country_name = None
        location.update({
            'address_line1': duns_obj.address_line_1,
            'address_line2': duns_obj.address_line_2,
            'city_name': duns_obj.city,
            'state_code': duns_obj.state,
            'zip': duns_obj.zip,
            'zip4': duns_obj.zip4,
            'country_name': country_name[0]['country_name'] if country_name else None,
            'country_code': duns_obj.country_code,
            'congressional_code': duns_obj.congressional_district
        })
    else:
        # Extract the location from the latest legal entity
        duns, name = extract_name_duns_from_hash(recipient_hash)
        legal_entity = LegalEntity.objects.filter(recipient_name=name,
                                                  recipient_unique_id=duns).\
            order_by('-update_date')\
            .values(
                address_line1=F('location__address_line1'),
                address_line2=F('location__address_line2'),
                address_line3=F('location__address_line3'),
                foreign_province=F('location__foreign_province'),
                city_name=F('location__city_name'),
                county_name=F('location__county_name'),
                state_code=F('location__state_code'),
                zip=F('location__zip4'),
                zip4=F('location__zip_4a'),
                foreign_postal_code=F('location__foreign_postal_code'),
                country_name=F('location__country_name'),
                country_code=F('location__location_country_code'),
                congressional_code=F('location__congressional_code')
        )
        if legal_entity:
            location.update(legal_entity[0])
    return location


def extract_business_categories(recipient_name, recipient_duns):
    """ Extract the business categories via the recipient hash

        Args:
            recipient_name: name of the recipient
            recipient_duns: duns of the recipient

        Returns:
            list of business categories
    """
    qs_business_cat = LegalEntity.objects.filter(recipient_name=recipient_name, recipient_unique_id=recipient_duns)\
        .order_by('-update_date').values('business_categories').first()
    return qs_business_cat['business_categories'] if qs_business_cat is not None else []


def obtain_recipient_totals(recipient_id, children=False, year='latest', subawards=False):
    """ Extract the total amount and transaction count for the recipient_hash given the timeframe

        Args:
            recipient_id: string of hash(duns, name)-[recipient-level]
            children: whether or not to group by children
            year: the year the totals/counts are based on
            subawards: whether to total based on subawards
        Returns:
            list of dictionaries representing hashes and their totals/counts
    """
    if year == 'latest' and children is False:
        # Simply pull the total and count from RecipientProfile
        recipient_hash = recipient_id[:-2]
        recipient_level = recipient_id[-1]
        results = list(RecipientProfile.objects.filter(recipient_hash=recipient_hash, recipient_level=recipient_level) \
                       .annotate(total=F('last_12_months'), count=F('last_12_months_count')) \
                       .values('recipient_hash', 'recipient_unique_id', 'recipient_name', 'total', 'count'))

    else:
        filters = reshape_filters(recipient_id=recipient_id, year=year)
        queryset, model = recipient_totals(filters)
        if children:
            # Group by the child recipients
            queryset = queryset.values('recipient_hash', 'recipient_unique_id', 'recipient_name') \
                .annotate(total=Sum('generated_pragmatic_obligation'), count=Sum('counts')) \
                .values('recipient_hash', 'recipient_unique_id', 'recipient_name', 'total', 'count')
            results = list(queryset)
        else:
            # Calculate the overall totals
            aggregates = queryset.aggregate(total=Sum('generated_pragmatic_obligation'), count=Sum('counts'))
            aggregates.update({'recipient_hash': recipient_id[:-2]})
            results = [aggregates]
    for result in results:
        result['count'] = result['count'] if result['count'] else 0
        result['total'] = result['total'] if result['total'] else 0
    return results


class RecipientOverView(APIDocumentationView):

    @cache_response()
    def get(self, request, recipient_id):
        get_request = request.query_params
        year = validate_year(get_request.get('year', 'latest'))
        recipient_hash, recipient_level = validate_recipient_id(recipient_id)
        recipient_duns, recipient_name = extract_name_duns_from_hash(recipient_hash)
        special_case = (recipient_name in SPECIAL_CASES and recipient_duns is None)

        if recipient_level != 'R':
            parent_duns, parent_name, parent_id = extract_parent_from_hash(recipient_hash)
        else:
            parent_duns, parent_name, parent_id = None, None, None
        location = extract_location(recipient_hash) if not special_case else {}
        business_types = extract_business_categories(recipient_name, recipient_duns) if not special_case else []
        results = obtain_recipient_totals(recipient_id, year=year, subawards=False)
        # subtotal, subcount = obtain_recipient_totals(recipient_hash, recipient_level, year=year, subawards=False)

        result = {
            'name': recipient_name,
            'duns': recipient_duns,
            'recipient_id': recipient_id,
            'recipient_level': recipient_level,
            'parent_id': parent_id,
            'parent_name': parent_name,
            'parent_duns': parent_duns,
            'business_types': business_types,
            'location': location,
            'total_transaction_amount': results[0]['total'] if results else 0,
            'total_transactions': results[0]['count'] if results else 0,
            # 'total_sub_transaction_amount': subtotal,
            # 'total_sub_transaction_total': subcount
        }
        return Response(result)


def extract_hash_name_from_duns(duns):
    """ Extract the all the names and hashes associated with the DUNS provided

        Args:
            duns: duns to find the equivalent hash and name

        Returns:
            list of dictionaries containing hashes and names
    """
    qs_hash = RecipientLookup.objects.filter(duns=duns).values('recipient_hash', 'legal_business_name')
    if not qs_hash:
        return None, None
    else:
        return qs_hash[0]['recipient_hash'], qs_hash[0]['legal_business_name']


class ChildRecipients(APIDocumentationView):

    @cache_response()
    def get(self, request, duns):
        get_request = request.query_params
        year = validate_year(get_request.get('year', 'latest'))
        parent_hash, parent_name = extract_hash_name_from_duns(duns)
        if not parent_hash:
            raise InvalidParameterException('DUNS not found: \'{}\'.'.format(duns))

        totals = list(obtain_recipient_totals('{}-P'.format(parent_hash), children=True, year=year, subawards=False))

        # Get child info for each child DUNS
        results = []
        for total in totals:
            results.append({
                'recipient_id': '{}-C'.format(total['recipient_hash']),
                'name': total['recipient_name'],
                'duns': total['recipient_unique_id'],
                'amount': total['total'],
                # Commenting out until location data is included in a quick matview
                # 'state_province': total['state_province']
            })
        return Response(results)
