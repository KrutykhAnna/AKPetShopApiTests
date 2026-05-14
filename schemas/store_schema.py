INVENTORY_STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "placed": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        }
    },
    "required": ["approved", "placed", "delivered"],
    "additionalProperties": False
}

STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["approved", "placed", "delivered"]
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity", "status", "complete"],
    "additionalProperties": False
}
