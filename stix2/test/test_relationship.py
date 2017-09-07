import datetime as dt

import pytest
import pytz

import stix2

from .constants import (FAKE_TIME, INDICATOR_ID, MALWARE_ID, RELATIONSHIP_ID,
                        RELATIONSHIP_KWARGS)


EXPECTED_RELATIONSHIP = """{
    "type": "relationship",
    "id": "relationship--00000000-1111-2222-3333-444444444444",
    "created": "2016-04-06T20:06:37.000Z",
    "modified": "2016-04-06T20:06:37.000Z",
    "relationship_type": "indicates",
    "source_ref": "indicator--01234567-89ab-cdef-0123-456789abcdef",
    "target_ref": "malware--fedcba98-7654-3210-fedc-ba9876543210"
}"""


def test_relationship_all_required_properties():
    now = dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)

    rel = stix2.Relationship(
        type='relationship',
        id=RELATIONSHIP_ID,
        created=now,
        modified=now,
        relationship_type='indicates',
        source_ref=INDICATOR_ID,
        target_ref=MALWARE_ID,
    )
    assert str(rel) == EXPECTED_RELATIONSHIP


def test_relationship_autogenerated_properties(relationship):
    assert relationship.type == 'relationship'
    assert relationship.id == 'relationship--00000000-0000-0000-0000-000000000001'
    assert relationship.created == FAKE_TIME
    assert relationship.modified == FAKE_TIME
    assert relationship.relationship_type == 'indicates'
    assert relationship.source_ref == INDICATOR_ID
    assert relationship.target_ref == MALWARE_ID

    assert relationship['type'] == 'relationship'
    assert relationship['id'] == 'relationship--00000000-0000-0000-0000-000000000001'
    assert relationship['created'] == FAKE_TIME
    assert relationship['modified'] == FAKE_TIME
    assert relationship['relationship_type'] == 'indicates'
    assert relationship['source_ref'] == INDICATOR_ID
    assert relationship['target_ref'] == MALWARE_ID


def test_relationship_type_must_be_relationship():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.Relationship(type='xxx', **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.prop_name == "type"
    assert excinfo.value.reason == "must equal 'relationship'."
    assert str(excinfo.value) == "Invalid value for Relationship 'type': must equal 'relationship'."


def test_relationship_id_must_start_with_relationship():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.Relationship(id='my-prefix--', **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.prop_name == "id"
    assert excinfo.value.reason == "must start with 'relationship--'."
    assert str(excinfo.value) == "Invalid value for Relationship 'id': must start with 'relationship--'."


def test_relationship_required_property_relationship_type():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.Relationship()
    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.properties == ["relationship_type", "source_ref", "target_ref"]


def test_relationship_missing_some_required_properties():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.Relationship(relationship_type='indicates')

    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.properties == ["source_ref", "target_ref"]


def test_relationship_required_properties_target_ref():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.Relationship(
            relationship_type='indicates',
            source_ref=INDICATOR_ID
        )

    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.properties == ["target_ref"]


def test_cannot_assign_to_relationship_attributes(relationship):
    with pytest.raises(stix2.exceptions.ImmutableError) as excinfo:
        relationship.relationship_type = "derived-from"

    assert str(excinfo.value) == "Cannot modify 'relationship_type' property in 'Relationship' after creation."


def test_invalid_kwarg_to_relationship():
    with pytest.raises(stix2.exceptions.ExtraPropertiesError) as excinfo:
        stix2.Relationship(my_custom_property="foo", **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.Relationship
    assert excinfo.value.properties == ['my_custom_property']
    assert str(excinfo.value) == "Unexpected properties for Relationship: (my_custom_property)."


def test_create_relationship_from_objects_rather_than_ids(indicator, malware):
    rel = stix2.Relationship(
        relationship_type="indicates",
        source_ref=indicator,
        target_ref=malware,
    )

    assert rel.relationship_type == 'indicates'
    assert rel.source_ref == 'indicator--00000000-0000-0000-0000-000000000001'
    assert rel.target_ref == 'malware--00000000-0000-0000-0000-000000000002'
    assert rel.id == 'relationship--00000000-0000-0000-0000-000000000003'


def test_create_relationship_with_positional_args(indicator, malware):
    rel = stix2.Relationship(indicator, 'indicates', malware)

    assert rel.relationship_type == 'indicates'
    assert rel.source_ref == 'indicator--00000000-0000-0000-0000-000000000001'
    assert rel.target_ref == 'malware--00000000-0000-0000-0000-000000000002'
    assert rel.id == 'relationship--00000000-0000-0000-0000-000000000003'


@pytest.mark.parametrize("data", [
    EXPECTED_RELATIONSHIP,
    {
        "created": "2016-04-06T20:06:37Z",
        "id": "relationship--00000000-1111-2222-3333-444444444444",
        "modified": "2016-04-06T20:06:37Z",
        "relationship_type": "indicates",
        "source_ref": "indicator--01234567-89ab-cdef-0123-456789abcdef",
        "target_ref": "malware--fedcba98-7654-3210-fedc-ba9876543210",
        "type": "relationship"
    },
])
def test_parse_relationship(data):
    rel = stix2.parse(data)

    assert rel.type == 'relationship'
    assert rel.id == RELATIONSHIP_ID
    assert rel.created == dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)
    assert rel.modified == dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)
    assert rel.relationship_type == "indicates"
    assert rel.source_ref == "indicator--01234567-89ab-cdef-0123-456789abcdef"
    assert rel.target_ref == "malware--fedcba98-7654-3210-fedc-ba9876543210"
