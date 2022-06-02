import pytest

from fregepoc.analyzers.core import AnalyzerFactory
from fregepoc.analyzers.tests.rust.constants import MOCKED_RUST_FILES
from fregepoc.repositories.constants import ProgrammingLanguages
from fregepoc.repositories.factories import RepositoryFileFactory


@pytest.mark.django_db
class TestRustAnalyzerLinesOfCode:
    @pytest.mark.parametrize(
        ["repo_file_params", "expected_average_loc"],
        [
            (
                {"repo_relative_file_path": "iban.rs"},
                32.0,
            ),
            (
                {"repo_relative_file_path": "perlin_noise.rs"},
                8.20,
            ),
            (
                {"repo_relative_file_path": "radix_search.rs"},
                6.33,
            ),
        ],
    )
    def test_count_loc(
        self, repo_file_params, expected_average_loc, settings, dummy_repo
    ):
        settings.DOWNLOAD_PATH = MOCKED_RUST_FILES
        analyzers = AnalyzerFactory.make_analyzers(ProgrammingLanguages.RUST)
        repo_file = RepositoryFileFactory(
            repository=dummy_repo,
            language=ProgrammingLanguages.RUST,
            **repo_file_params,
        )
        for analyzer in analyzers:
            actual = analyzer.analyze(repo_file)
            assert actual["average_lines_of_code"] == pytest.approx(
                expected_average_loc, 0.01
            )
