
from rest_framework import serializers
from .models import DraftType, Draft
from drafting.fact_definitions import FACT_SCHEMAS
from drafting.workflow import DraftStatus
from datetime import datetime

def get_fact_schema_for_draft(draft):
    return FACT_SCHEMAS.get(draft.draft_type.code, [])
def get_schema_by_key(schema, key):
    for item in schema:
        if item["key"] == key:
            return item
    return None
def coerce_value(value, expected_type):
    if expected_type == "string":
        return str(value)

    if expected_type == "text":
        return str(value)

    if expected_type == "number":
        try:
            return int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                f"Expected number, got '{value}'"
            )

    if expected_type == "boolean":
        if isinstance(value, bool):
            return value
        if str(value).lower() in ["true", "1", "yes"]:
            return True
        if str(value).lower() in ["false", "0", "no"]:
            return False
        raise serializers.ValidationError(
            f"Expected boolean, got '{value}'"
        )

    if expected_type == "date":
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            raise serializers.ValidationError(
                f"Expected date YYYY-MM-DD, got '{value}'"
            )

    if expected_type == "list":
        if isinstance(value, list):
            return value
        raise serializers.ValidationError(
            f"Expected list, got '{value}'"
        )

    raise serializers.ValidationError(
        f"Unsupported fact type '{expected_type}'"
    )

class DraftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftType
        fields = ["id", "code", "name", "description"]

class DraftCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ["id", "title", "draft_type"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        return Draft.objects.create(
            user=user,
            status="CREATED",
            **validated_data
        )

class DraftFactSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

class DraftFactIntakeSerializer(serializers.Serializer):
    facts = DraftFactSerializer(many=True)

    def validate(self, data):
        draft = self.context["draft"]
        incoming_facts = data["facts"]

        schema = get_fact_schema_for_draft(draft)
        allowed_keys = {f["key"] for f in schema}
        required_keys = {f["key"] for f in schema if f["required"]}

        received_keys = {f["key"] for f in incoming_facts}

        # 1. Block unknown facts
        unknown = received_keys - allowed_keys
        if unknown:
            raise serializers.ValidationError(
                f"Unknown fact keys: {unknown}"
            )

        # 2. Block missing required facts
        missing = required_keys - received_keys
        if missing:
            raise serializers.ValidationError(
                f"Missing required facts: {missing}"
            )

        # 3. Type validation + coercion
        cleaned_facts = []

        for fact in incoming_facts:
            schema_item = get_schema_by_key(schema, fact["key"])
            expected_type = schema_item["type"]

            coerced_value = coerce_value(
                fact["value"],
                expected_type
            )

            cleaned_facts.append({
                "key": fact["key"],
                "value": coerced_value
            })

        data["facts"] = cleaned_facts
        return data