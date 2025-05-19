# processor/tb/conftest.py
import os
import subprocess
import pytest


def run_cocotb_test(toplevel, verilog_sources, module):
    env = os.environ.copy()
    env['TOPLEVEL'] = toplevel
    env['MODULE'] = module
    env['VERILOG_SOURCES'] = ' '.join([
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", src))
        for src in verilog_sources
    ])
    subprocess.run(
        ['make'],
        cwd=os.path.dirname(__file__),
        env=env,
        check=True
    )


@pytest.fixture
def cocotb_runner():
    return run_cocotb_test
