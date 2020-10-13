from typing import List

from django.db.models import F
from usaspending_api.accounts.models import TreasuryAppropriationAccount
from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.disaster.v2.views.disaster_base import (
    LoansPaginationMixin,
    LoansMixin,
    FabaOutlayMixin,
)
from usaspending_api.disaster.v2.views.elasticsearch_account_base import ElasticsearchAccountDisasterBase
from usaspending_api.search.v2.elasticsearch_helper import get_summed_value_as_float


class LoansViewSet(LoansMixin, LoansPaginationMixin, FabaOutlayMixin, ElasticsearchAccountDisasterBase):
    """ Returns loan disaster spending by federal account. """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/disaster/federal_account/loans.md"
    agg_key = "financial_accounts_by_award.federal_account_id"  # primary (tier-1) aggregation key
    nested_nonzero_fields = {"outlay": "gross_outlay_amount_by_award_cpe", "obligation": "transaction_obligated_amount"}
    query_fields = [
        "federal_account_symbol",
        "federal_account_symbol.contains",
        "federal_account_title",
        "federal_account_title.contains",
    ]
    sub_agg_key = "financial_accounts_by_award.treasury_account_id"
    sub_top_hits_fields = [
        "financial_accounts_by_award.treasury_account_symbol",
        "financial_accounts_by_award.treasury_account_title",
    ]
    top_hits_fields = [
        "financial_accounts_by_award.federal_account_symbol",
        "financial_accounts_by_award.federal_account_title",
    ]

    @cache_response()
    def post(self, request):
        self.filters.update({"award_type": ["07", "08"]})
        return self.perform_elasticsearch_search()

    def build_elasticsearch_result(self, info_buckets: List[dict]) -> List[dict]:
        results = []

        for bucket in info_buckets:
            result = self._build_json_result(bucket, True)
            child_info_buckets = bucket.get(self.sub_agg_group_name, {}).get("buckets", [])
            children = []
            for child_bucket in child_info_buckets:
                children.append(self._build_json_result(child_bucket, False))
            result["children"] = children
            results.append(result)

        return results

    def _build_json_result(self, bucket: dict, is_parent: bool):
        if is_parent:
            description_key = "federal_account_title"
            id_key = "federal_account_symbol"
        else:
            description_key = "treasury_account_title"
            id_key = "treasury_account_symbol"
        return {
            "id": bucket["key"],
            "code": bucket["dim_metadata"]["hits"]["hits"][0]["_source"][id_key],
            "description": bucket["dim_metadata"]["hits"]["hits"][0]["_source"][description_key],
            # the count of distinct awards contributing to the totals
            "award_count": int(bucket["count_awards_by_dim"]["award_count"]["value"]),
            **{key: get_summed_value_as_float(bucket, f"sum_{val}") for key, val in self.nested_nonzero_fields.items()},
            "face_value_of_loan": bucket["count_awards_by_dim"]["sum_loan_value"]["value"],
        }

    # def build_elasticsearch_result(self, info_buckets: List[dict]) -> List[dict]:
    #     temp_results = {}
    #     child_results = []
    #     for bucket in info_buckets:
    #         child = self._build_child_json_result(bucket)
    #         child_results.append(child)
    #     for child in child_results:
    #         result = self._build_json_result(child)
    #         child.pop("parent_data")
    #         if result["id"] in temp_results.keys():
    #             temp_results[result["id"]] = {
    #                 "id": int(result["id"]),
    #                 "code": result["code"],
    #                 "description": result["description"],
    #                 "award_count": temp_results[result["id"]]["award_count"] + result["award_count"],
    #                 # the count of distinct awards contributing to the totals
    #                 "obligation": temp_results[result["id"]]["obligation"] + result["obligation"],
    #                 "outlay": temp_results[result["id"]]["outlay"] + result["outlay"],
    #                 "face_value_of_loan": bucket["count_awards_by_dim"]["sum_loan_value"]["value"],
    #                 "children": temp_results[result["id"]]["children"] + result["children"],
    #             }
    #         else:
    #             temp_results[result["id"]] = result
    #     results = [x for x in temp_results.values()]
    #     return results
    #
    # def _build_json_result(self, child):
    #     return {
    #         "id": child["parent_data"][2],
    #         "code": child["parent_data"][1],
    #         "description": child["parent_data"][0],
    #         "award_count": child["award_count"],
    #         # the count of distinct awards contributing to the totals
    #         "obligation": child["obligation"],
    #         "outlay": child["outlay"],
    #         "face_value_of_loan": child["face_value_of_loan"],
    #         "children": [child],
    #     }
    #
    # def _build_child_json_result(self, bucket: dict):
    #     return {
    #         "id": int(bucket["key"]),
    #         "code": bucket["dim_metadata"]["hits"]["hits"][0]["_source"]["treasury_account_symbol"],
    #         "description": bucket["dim_metadata"]["hits"]["hits"][0]["_source"]["treasury_account_title"],
    #         # the count of distinct awards contributing to the totals
    #         "award_count": int(bucket["count_awards_by_dim"]["award_count"]["value"]),
    #         **{key: get_summed_value_as_float(bucket, f"sum_{val}") for key, val in self.nested_nonzero_fields.items()},
    #         "face_value_of_loan": bucket["count_awards_by_dim"]["sum_loan_value"]["value"],
    #         "parent_data": [
    #             bucket["dim_metadata"]["hits"]["hits"][0]["_source"]["federal_account_title"],
    #             bucket["dim_metadata"]["hits"]["hits"][0]["_source"]["federal_account_symbol"],
    #             bucket["dim_metadata"]["hits"]["hits"][0]["_source"]["federal_account_id"],
    #         ],
    #     }

    @property
    def queryset(self):
        query = self.construct_loan_queryset(
            "treasury_account__treasury_account_identifier", TreasuryAppropriationAccount, "treasury_account_identifier"
        )

        annotations = {
            "fa_code": F("federal_account__federal_account_code"),
            "award_count": query.award_count_column,
            "description": F("account_title"),
            "code": F("tas_rendering_label"),
            "id": F("treasury_account_identifier"),
            "fa_description": F("federal_account__account_title"),
            "fa_id": F("federal_account_id"),
            "obligation": query.obligation_column,
            "outlay": query.outlay_column,
            # hack to use the Dataclasses, will be renamed later
            "total_budgetary_resources": query.face_value_of_loan_column,
        }

        return query.queryset.annotate(**annotations).values(*annotations)
