import argparse
import csv
import sys
from typing import Iterable, Optional, TextIO

from . import __plugins__version__
from .plugin import Plugin, PluginInfo, PluginInstance, SourcePropertyType, SourceRecord


class CSVPluginInstance(PluginInstance):
    def __init__(self, file: str, dialect: csv.Dialect) -> None:
        if file == "-":
            self.fd = sys.stdin

            def flush_stdout(out: TextIO) -> None:
                out.flush()

            self.on_stream_end = flush_stdout
        else:
            self.fd = open(file, "rt", encoding="utf8")

            def close_file(out: TextIO) -> None:
                out.close()

            self.on_stream_end = close_file
        self.reader = csv.DictReader(self.fd, dialect=dialect)
        assert self.reader.fieldnames
        self.props = set(self.reader.fieldnames)

    def get_property_type(self, prop_name: str) -> Optional[SourcePropertyType]:
        if prop_name in self.props:
            return SourcePropertyType.STR
        return None

    def values(self) -> Iterable[SourceRecord]:
        for row in self.reader:
            yield SourceRecord(row, source_id=self.reader.line_num)
        self.close()

    def close(self) -> None:
        self.on_stream_end(self.fd)


class excel_with_semi_colon(csv.excel):
    delimiter = ";"


csv.register_dialect("excel_with_semi-colon", excel_with_semi_colon)


class CSVPlugin(Plugin):
    def __init__(self) -> None:
        pass

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="csv",
            author="Pierre Souchay",
            description="Read CSV Files",
            version=__plugins__version__,
        )

    def register_in_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "csv_file",
            help="CSV file to inject in Notion, if '-' is set, read from stdin",
        )
        parser.add_argument(
            "--csv-dialect",
            dest="csv_dialect",
            action="store",
            default="excel",
            choices=csv.list_dialects(),
            help="CSV Dialect, excel by default",
        )

    def start_parsing(self, ns: argparse.Namespace) -> PluginInstance:
        return CSVPluginInstance(ns.csv_file, dialect=ns.csv_dialect)
