from solich.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "solich_crumbs.context_processors.breadcrumbs",
)
