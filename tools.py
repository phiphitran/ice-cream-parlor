tools = [
    {
        "type": "function",
        "function": {
            "name": "check_menu",
            "description": "Retrieve the current menu of ice cream flavors.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Retrieve the current inventory of ice cream flavors.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "purchase_ice_cream",
            "description": "Purchase ice cream flavors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_flavor": {
                        "type": "string",
                        "description": "The flavor of ice cream to purchase.",
                    },
                    "input_quantity": {
                        "type": "integer",
                        "description": "The quantity of the flavor to purchase.",
                    }
                },
                "required": ["input_flavor", "input_quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restock_ice_cream",
            "description": "Restock ice cream flavors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restock_flavor": {
                        "type": "string",
                        "description": "The flavor of ice cream to restock.",
                    },
                    "restock_quantity": {
                        "type": "integer",
                        "description": "The quantity of ice cream flavor to restock.",
                    }
                },
                "required": ["restock_flavor", "restock_quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "give_user_feedback",
            "description": "Provide feedback of the ice creams.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_feedback": {
                        "type": "string",
                        "description": "The feedback of the ice cream.",
                    },
                    "user_rating": {
                        "type": "integer",
                        "description": "The rating of the ice cream.",
                    }
                },
                "required": ["user_feedback", "user_rating"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_feedback",
            "description": "Retrieve all the feedback from customers.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "feedback_report",
            "description": "Retrieve a report of feedback.",
            "parameters": {},
        },
    },
]