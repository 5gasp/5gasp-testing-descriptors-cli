# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-20 10:43:22
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-20 17:07:48
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.align import Align


class PrintAsTable:
    table = None

    def __init__(self, header, rows):
        self.header = header
        self.rows = rows
        self.__process_table()

    def __process_table(self):
        self.table = Table(*self.header)
        for row in self.rows:
            self.table.add_row(*row)

    def print(self, centered = False):
        console = Console()
        if centered:
            console.print(Align.center(self.table))
            return
        console.print(self.table)


class PrintAsPanelColumns:

    def __init__(self, pannels):
        self.pannels = pannels

    def print(self):
        
        columns = Columns(
            sorted(
                self.pannels,
                key=lambda p: len(p.renderable),
                reverse=True
            )
        )
        console = Console()
        console.print(columns)