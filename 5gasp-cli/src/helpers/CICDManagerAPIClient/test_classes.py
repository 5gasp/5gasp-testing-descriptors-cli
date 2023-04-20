# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-04-20 13:03:58
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-20 17:21:17

from rich.panel import Panel


class Test:
    def __init__(self, id=None, name=None, description=None,  mandatory=None,
                 test_variables=None):
        self.id = id
        self.name = name
        self.description = description
        self.mandatory = mandatory
        self.test_variables = test_variables

    def load_from_dict(self, test_dict):
        self.id = test_dict["id"]
        self.name = test_dict["name"]
        self.description = test_dict["description"]
        self.mandatory = test_dict["mandatory"]
        self.test_variables = []
        if "test_variables" in test_dict:
            for test_variable in test_dict["test_variables"]:
                self.test_variables.append(
                    TestVariable(
                        name=test_variable["variable_name"],
                        description=test_variable["description"],
                        mandatory=test_variable["mandatory"],
                        possible_options=test_variable["possible_options"],
                        type=test_variable["type"]
                    )
                )

    def to_pannel(self, expand=None, width=None):
        panel_str = f"""
        [b]{self.name.title()} Test[/b]

        [yellow]Test ID:[/yellow] {self.id}
        [yellow]Test Description:[/yellow] {self.description}

        [blue][b]Test Variables: [/b]
        """

        if len(self.test_variables) == 0:
            panel_str += """
            [blue]This test requires no parameters[/blue]
            """

        for tv in self.test_variables:
            panel_str += f"""
            [blue]◉ {tv.name}:
            \t[blue]○ Description:[/blue][white] {tv.description}
            \t[blue]○ Mandatory:[/blue]  {tv.mandatory}
            \t[blue]○ Type:[/blue]  {tv.type}
            """

            if len(tv.possible_options) != 0:
                panel_str += "\t[blue]○ Possible Options:[/blue] "
                panel_str += str(tv.possible_options) + "\n"

        if expand:
            print("dddd")
            return Panel(renderable=panel_str, expand=True)
        if width:
            return Panel(renderable=panel_str, expand=False, width=width)
        if not expand and not width:
            return Panel(renderable=panel_str, expand=False, width=65)


class TestVariable:
    def __init__(self, name, description, mandatory, possible_options, type):
        self.name = name
        self.description = description
        self.mandatory = mandatory
        self.possible_options = possible_options
        self.type = type
