from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState


class ReloadModel(Operation):
    """
    Work around a Django bug by reloading a model manually.

    If a migration changes only model A that is related to models B, C, and
    D by successive foreign keys, and then a later data migration tries to
    delete model C in its reverse operation, then the deletion raises
    `ValueError: Cannot query "C (...)": Must be "C" instance` when trying
    to handle the foreign key from D to C because the migration engine's
    idea of the state of model D now refers to an old version of model C
    that hasn't been reloaded.  To work around that, the migration that
    changes model A can manually reload model D by including something like
    `ReloadModel(("db", "d"))` in its operations.

    This is probably related to https://code.djangoproject.com/ticket/27737.
    """

    def __init__(self, model_key: tuple[str, str]) -> None:
        """Construct the operation."""
        self.model_key = model_key

    def state_forwards(
        self,
        app_label: str,  # noqa: U100
        state: ProjectState,
    ) -> None:
        """Tell Django to reload the given model."""
        state.reload_model(*self.model_key)

    def database_forwards(
        self,
        app_label: str,  # noqa: U100
        schema_editor: BaseDatabaseSchemaEditor,  # noqa: U100
        from_state: ProjectState,  # noqa: U100
        to_state: ProjectState,  # noqa: U100
    ) -> None:
        """No schema change."""

    def database_backwards(
        self,
        app_label: str,  # noqa: U100
        schema_editor: BaseDatabaseSchemaEditor,  # noqa: U100
        from_state: ProjectState,  # noqa: U100
        to_state: ProjectState,  # noqa: U100
    ) -> None:
        """No schema change."""
