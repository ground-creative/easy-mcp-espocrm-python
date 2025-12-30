from core.utils.env import EnvConfig

SERVICES = [
    "core.services.server_info",    # server info html page
]

# Optional, add configuration for the info server
INFO_SERVICE_CONFIG = {
    "service_uri": "/", # the uri for the info service page
    "site_url": EnvConfig.get("SITE_URL"),
    "site_name": EnvConfig.get("SITE_NAME"),
    "show_tools_specs": True,   # show specs for tools (name, description, parameters)
    #"notes": [], # a list of notes for the server information
    "header_params": {
        "X-API-KEY": "(Required) Your EspoCRM API key for authentication.",
        "X-API-ADDRESS": "(Required) The URL of EspoCRM API."
    },
    "privacy_policy_url": f"{EnvConfig.get('SITE_URL')}/en/privacy-policy",
    "terms_of_service_url": f"{EnvConfig.get('SITE_URL')}/en/terms-of-service",
}

MIDDLEWARE = {"mcp": [{"middleware": "app.middleware.AuthenticationMiddleware", "priority": 1}]}