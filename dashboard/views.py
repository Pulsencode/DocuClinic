def dashboard_callback(request, context):
    context.update(
        {
            "custom_variable": "value",
        }
    )

    return context
