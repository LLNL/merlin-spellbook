##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

from abc import ABC, abstractmethod


class CliCommand(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError()
