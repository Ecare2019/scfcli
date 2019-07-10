import unittest
import os
import shutil

from test_common import *
from click.testing import CliRunner
from tcfcli.cmds.configure import cli as configure_cli
from tcfcli.cmds.init import cli as init_cli
from tcfcli.cmds.deploy import cli as deploy_cli


class TestDeploy(unittest.TestCase):
    def setUp(self):
        super(TestDeploy, self).setUp()
        runner = CliRunner()
        result = runner.invoke(configure_cli.set, ['--appid', AppID])
        self.assertEqual(0, result.exit_code)
        result = runner.invoke(configure_cli.set, ['--region', Region])
        self.assertEqual(0, result.exit_code)
        result = runner.invoke(configure_cli.set, ['--secret-id', SecretId])
        self.assertEqual(0, result.exit_code)
        result = runner.invoke(configure_cli.set, ['--secret-key', SecretKey])
        self.assertEqual(0, result.exit_code)

    def tearDown(self):
        super(TestDeploy, self).tearDown()

    def test_deploy_default(self):
        if os.path.exists(PythonDemoProjectPath):
            shutil.rmtree(PythonDemoProjectPath)

        runner = CliRunner()
        result = runner.invoke(init_cli.init, ['-N', '-l', PythonDemoGithub])
        self.assertEqual(
            '[+] Initializing project...\nTemplate: %s\nOutput-Dir: .\n[*] Project initialization is complete\n' % PythonDemoGithub,
            result.output)
        self.assertEqual(0, result.exit_code)

        os.chdir(PythonDemoProjectPath)

        result = runner.invoke(deploy_cli.deploy, ["-f"])
        self.assertIn('Deploy function \'hello_world\' success', result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
