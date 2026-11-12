"""Teste do desempate do ranking de hotéis."""

from helpers import run_cli


def test_top_hotels_tie_breaks_by_hotel_id_ascending(tmp_path):
    """Hotéis com o mesmo total devem ser ordenados pelo ID crescente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "amount": "1000.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "1000.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "amount": "900.00"},
        ],
        top=3,
    )

    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02", "H03"]
