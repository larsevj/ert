import uuid
from typing import Dict

import pytest
from cloudevents.http.event import CloudEvent

from ert.ensemble_evaluator import identifiers as ids
from ert.ensemble_evaluator import state
from ert.ensemble_evaluator.snapshot import (
    Job,
    PartialSnapshot,
    RealizationSnapshot,
    Snapshot,
    SnapshotDict,
    Step,
)

from ..unit_tests.gui.conftest import (  # noqa  # pylint: disable=unused-import
    active_realizations_fixture,
    large_snapshot,
    mock_tracker,
    runmodel,
)
from ..unit_tests.gui.simulation.test_run_dialog import test_large_snapshot


@pytest.mark.parametrize(
    "ensemble_size, forward_models, memory_reports",
    [
        (10, 10, 1),
        (100, 10, 1),
        (10, 100, 1),
        (10, 10, 10),
    ],
)
def test_snapshot_handling_of_forward_model_events(
    benchmark, ensemble_size, forward_models, memory_reports
):
    benchmark(
        simulate_forward_model_event_handling,
        ensemble_size,
        forward_models,
        memory_reports,
    )


def test_gui_snapshot(
    benchmark,
    runmodel,  # noqa
    large_snapshot,  # noqa
    qtbot,
    mock_tracker,  # noqa
):
    # pylint: disable=redefined-outer-name
    infinite_timeout = 100000
    benchmark(
        test_large_snapshot,
        runmodel,
        large_snapshot,
        qtbot,
        mock_tracker,
        timeout_per_iter=infinite_timeout,
    )


def simulate_forward_model_event_handling(
    ensemble_size, forward_models, memory_reports
):
    reals: Dict[str, RealizationSnapshot] = {}
    for real in range(ensemble_size):
        reals[str(real)] = RealizationSnapshot(
            active=True,
            status=state.REALIZATION_STATE_WAITING,
        )
        reals[str(real)].steps["0"] = Step(status=state.STEP_STATE_UNKNOWN)
        for job_idx in range(forward_models):
            reals[f"{real}"].steps["0"].jobs[str(job_idx)] = Job(
                status=state.JOB_STATE_START,
                index=job_idx,
                name=f"FM_{job_idx}",
            )
    top = SnapshotDict(
        reals=reals, status=state.ENSEMBLE_STATE_UNKNOWN, metadata={"foo": "bar"}
    )

    snapshot = Snapshot(top.dict())

    partial = PartialSnapshot(snapshot)

    ens_id = "A"
    partial.from_cloudevent(
        CloudEvent(
            {
                "source": f"/ert/ensemble/{ens_id}",
                "type": ids.EVTYPE_ENSEMBLE_STARTED,
                "id": str(uuid.uuid1()),
            }
        )
    )

    for real in range(ensemble_size):
        partial.from_cloudevent(
            CloudEvent(
                {
                    "source": f"/ert/ensemble/{ens_id}/real/{real}/step/0",
                    "type": ids.EVTYPE_FM_STEP_WAITING,
                    "id": str(uuid.uuid1()),
                }
            )
        )

    for job_idx in range(forward_models):
        for real in range(ensemble_size):
            partial.from_cloudevent(
                CloudEvent(
                    attributes={
                        "source": f"/ert/ensemble/{ens_id}/"
                        f"real/{real}/step/0/job/{job_idx}",
                        "type": ids.EVTYPE_FM_JOB_START,
                        "id": str(uuid.uuid1()),
                    },
                    data={"stderr": "foo", "stdout": "bar"},
                )
            )
        for current_memory_usage in range(memory_reports):
            for real in range(ensemble_size):
                partial.from_cloudevent(
                    CloudEvent(
                        attributes={
                            "source": f"/ert/ensemble/{ens_id}/"
                            f"real/{real}/step/0/job/{job_idx}",
                            "type": ids.EVTYPE_FM_JOB_RUNNING,
                            "id": str(uuid.uuid1()),
                        },
                        data={
                            "max_memory_usage": current_memory_usage,
                            "current_memory_usage": current_memory_usage,
                        },
                    )
                )
        for real in range(ensemble_size):
            partial.from_cloudevent(
                CloudEvent(
                    attributes={
                        "source": f"/ert/ensemble/{ens_id}/"
                        f"real/{real}/step/0/job/{job_idx}",
                        "type": ids.EVTYPE_FM_JOB_SUCCESS,
                        "id": str(uuid.uuid1()),
                    },
                )
            )

    for real in range(ensemble_size):
        partial.from_cloudevent(
            CloudEvent(
                {
                    "source": f"/ert/ensemble/{ens_id}/real/{real}/step/0",
                    "type": ids.EVTYPE_FM_STEP_SUCCESS,
                    "id": str(uuid.uuid1()),
                }
            )
        )
