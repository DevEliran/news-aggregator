import os
from argparse import Namespace

import pytest
from pytest_mock import MockerFixture

from src.main import normalize_config


def test_reddit_source_with_no_sub() -> None:
    config = Namespace(
        reddit=True,
        metric='hot',
        sub=None
    )

    with pytest.raises(ValueError) as exc_info:
        normalize_config(config)

    assert str(exc_info.value) == "bad config"


def test_reddit_source_with_no_credentials(mocker: MockerFixture) -> None:
    config = Namespace(
        reddit=True,
        metric='hot',
        sub='programming',
        reddit_id=None,
        reddit_secret='secret',
        medium=False,
        tag=''
    )

    mocker.patch.dict('os.environ', {})

    with pytest.raises(ValueError) as exc_info:
        normalize_config(config)

    assert str(exc_info.value) == "bad config"

