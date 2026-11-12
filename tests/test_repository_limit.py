"""Teste de leitura integral do CSV de reservas."""

import csv

from onfly_report.repositories.csv_reservation_repository import CsvReservationRepository

from helpers import BASE, COLUMNS


def test_repository_reads_all_reservations(tmp_path):
    """Todas as reservas do arquivo devem ser carregadas, sem limite artificial."""
    input_path = tmp_path / "reservas.csv"
    rows = [{**BASE, "reservation_id": f"R-{index}"} for index in range(201)]

    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    reservations = CsvReservationRepository(input_path).read()

    assert len(reservations) == len(rows)
    assert reservations[-1].values["reservation_id"] == "R-200"
