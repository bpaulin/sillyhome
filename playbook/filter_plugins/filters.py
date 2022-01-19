def appsForPortal(apps, groups, public, private):
    all_items = [
        item
        for sublist in [
            app_for_portal["portal"]
            for app_for_portal in apps
            if "portal" in app_for_portal.keys()
        ]
        for item in sublist
        if ((public and item["public"]) or (private and not item["public"]))
    ]
    all_groups = list(
        set(
            [app["group"] for app in all_items if "group" in app.keys()]
            + [group for group in groups.keys()]
        )
    )
    formatted = [
        {
            "name": group_name,
            "icon": groups[group_name]["icon"] if group_name in groups.keys() else "",
            "items": (
                groups[group_name]["items"] if group_name in groups.keys() else []
            )
            + [item for item in all_items if item["group"] == group_name],
        }
        for group_name in all_groups
    ]
    return [f for f in formatted if f["items"]]


class FilterModule(object):
    def filters(self):
        return {"apps_for_portal": appsForPortal}
